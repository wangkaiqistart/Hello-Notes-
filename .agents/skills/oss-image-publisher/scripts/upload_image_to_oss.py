#!/usr/bin/env python3
"""上传本地图片到阿里云 OSS，并返回图片链接。

脚本刻意从环境变量读取密钥，避免把 AccessKey 写入仓库文件。
"""

from __future__ import annotations

import argparse
import base64
import datetime as dt
import hashlib
import hmac
import json
import mimetypes
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from email.utils import formatdate
from pathlib import Path
from typing import Any


IMAGE_EXTENSIONS = {
    ".apng",
    ".avif",
    ".gif",
    ".jpeg",
    ".jpg",
    ".png",
    ".svg",
    ".webp",
}


def env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def normalize_endpoint(endpoint: str) -> tuple[str, str]:
    endpoint = endpoint.strip()
    if not endpoint:
        raise ValueError("OSS 访问域名为空")
    parsed = urllib.parse.urlparse(endpoint if "://" in endpoint else f"https://{endpoint}")
    if not parsed.netloc:
        raise ValueError(f"无效的 OSS 访问域名：{endpoint}")
    scheme = parsed.scheme or "https"
    host = parsed.netloc.rstrip("/")
    return scheme, host


def slugify_filename(path: Path) -> str:
    stem = path.stem.lower()
    stem = re.sub(r"[^a-z0-9]+", "-", stem).strip("-")
    return stem or "image"


def detect_content_type(path: Path) -> str:
    guessed, _ = mimetypes.guess_type(path.name)
    if path.suffix.lower() == ".svg" and not guessed:
        return "image/svg+xml"
    return guessed or "application/octet-stream"


def validate_image(path: Path, allow_non_image: bool) -> str:
    if not path.exists():
        raise FileNotFoundError(f"找不到图片文件：{path}")
    if not path.is_file():
        raise ValueError(f"不是文件：{path}")
    content_type = detect_content_type(path)
    if not allow_non_image:
        is_image_type = content_type.startswith("image/")
        is_image_ext = path.suffix.lower() in IMAGE_EXTENSIONS
        if not (is_image_type or is_image_ext):
            raise ValueError(
                f"拒绝上传非图片文件：{path}（{content_type}）。"
                "如确实需要上传，请使用 --allow-non-image。"
            )
    return content_type


def file_digest(path: Path) -> tuple[str, str]:
    md5_hash = hashlib.md5()  # nosec B324 - OSS Content-MD5 需要 MD5。
    sha256_hash = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            md5_hash.update(chunk)
            sha256_hash.update(chunk)
    content_md5 = base64.b64encode(md5_hash.digest()).decode("ascii")
    return content_md5, sha256_hash.hexdigest()


def build_object_key(path: Path, prefix: str, digest: str, explicit_key: str | None) -> str:
    if explicit_key:
        return explicit_key.lstrip("/")

    clean_prefix = prefix.strip("/")
    today = dt.datetime.now(dt.timezone.utc).strftime("%Y/%m/%d")
    extension = path.suffix.lower() or ".bin"
    filename = f"{slugify_filename(path)}-{digest[:12]}{extension}"
    parts = [part for part in [clean_prefix, today, filename] if part]
    return "/".join(parts)


def canonicalized_oss_headers(headers: dict[str, str]) -> str:
    oss_headers: list[tuple[str, str]] = []
    for name, value in headers.items():
        lower_name = name.lower()
        if lower_name.startswith("x-oss-"):
            normalized_value = " ".join(str(value).strip().split())
            oss_headers.append((lower_name, normalized_value))
    oss_headers.sort(key=lambda item: item[0])
    return "".join(f"{name}:{value}\n" for name, value in oss_headers)


def sign_v1(
    *,
    method: str,
    access_key_secret: str,
    content_md5: str,
    content_type: str,
    date_header: str,
    oss_headers: dict[str, str],
    bucket: str,
    object_key: str,
) -> str:
    canonical_resource = f"/{bucket}/{object_key}"
    string_to_sign = (
        f"{method}\n"
        f"{content_md5}\n"
        f"{content_type}\n"
        f"{date_header}\n"
        f"{canonicalized_oss_headers(oss_headers)}"
        f"{canonical_resource}"
    )
    digest = hmac.new(
        access_key_secret.encode("utf-8"),
        string_to_sign.encode("utf-8"),
        hashlib.sha1,
    ).digest()
    return base64.b64encode(digest).decode("ascii")


def build_public_url(public_base_url: str | None, scheme: str, endpoint_host: str, bucket: str, object_key: str) -> str:
    quoted_key = urllib.parse.quote(object_key, safe="/~")
    if public_base_url:
        return f"{public_base_url.rstrip('/')}/{quoted_key}"
    return f"{scheme}://{bucket}.{endpoint_host}/{quoted_key}"


def put_object(
    *,
    path: Path,
    bucket: str,
    endpoint: str,
    access_key_id: str,
    access_key_secret: str,
    object_key: str,
    content_type: str,
    content_md5: str,
    security_token: str | None,
    acl: str | None,
    forbid_overwrite: bool,
) -> None:
    scheme, endpoint_host = normalize_endpoint(endpoint)
    quoted_key = urllib.parse.quote(object_key, safe="/~")
    upload_url = f"{scheme}://{bucket}.{endpoint_host}/{quoted_key}"
    date_header = formatdate(usegmt=True)

    headers = {
        "Content-Type": content_type,
        "Content-MD5": content_md5,
        "Date": date_header,
    }
    if security_token:
        headers["x-oss-security-token"] = security_token
    if acl:
        headers["x-oss-object-acl"] = acl
    if forbid_overwrite:
        headers["x-oss-forbid-overwrite"] = "true"

    signature = sign_v1(
        method="PUT",
        access_key_secret=access_key_secret,
        content_md5=content_md5,
        content_type=content_type,
        date_header=date_header,
        oss_headers=headers,
        bucket=bucket,
        object_key=object_key,
    )
    headers["Authorization"] = f"OSS {access_key_id}:{signature}"

    data = path.read_bytes()
    request = urllib.request.Request(upload_url, data=data, headers=headers, method="PUT")
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            if response.status not in {200, 201}:
                body = response.read().decode("utf-8", errors="replace")
                raise RuntimeError(f"OSS 上传失败，HTTP 状态码 {response.status}：{body}")
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"OSS 上传失败，HTTP 状态码 {error.code}：{body}") from error
    except urllib.error.URLError as error:
        raise RuntimeError(f"OSS 上传失败：{error.reason}") from error


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="上传本地图片到阿里云 OSS，并打印生成的图片链接。",
        add_help=False,
        usage="%(prog)s [选项] 图片路径 [图片路径 ...]",
    )
    parser._positionals.title = "位置参数"
    parser._optionals.title = "选项"
    parser.add_argument("images", nargs="+", help="要上传的本地图片路径。")
    parser.add_argument("-h", "--help", action="help", help="显示帮助信息并退出。")
    parser.add_argument("--bucket", default=os.getenv("ALIYUN_OSS_BUCKET"), help="OSS 存储桶名称。")
    parser.add_argument("--endpoint", default=os.getenv("ALIYUN_OSS_ENDPOINT"), help="OSS 访问域名或完整地址。")
    parser.add_argument("--prefix", default=os.getenv("ALIYUN_OSS_PREFIX", "images"), help="对象路径前缀。")
    parser.add_argument("--public-base-url", default=os.getenv("ALIYUN_OSS_PUBLIC_BASE_URL"), help="公开访问域名、CDN 域名或自定义域名。")
    parser.add_argument("--key", help="明确指定对象路径。仅允许上传一张图片时使用。")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text", help="输出格式：text、json 或 markdown。")
    parser.add_argument("--acl", default=os.getenv("ALIYUN_OSS_OBJECT_ACL"), help="可选的 x-oss-object-acl 值。")
    parser.add_argument(
        "--forbid-overwrite",
        action="store_true",
        default=env_bool("ALIYUN_OSS_FORBID_OVERWRITE"),
        help="发送 x-oss-forbid-overwrite: true，禁止覆盖同名对象。",
    )
    parser.add_argument("--allow-non-image", action="store_true", help="允许上传未被识别为图片的文件。")
    parser.add_argument("--dry-run", action="store_true", help="只生成对象路径和链接，不执行真实上传。")
    return parser.parse_args(argv)


def fail(message: str) -> None:
    print(f"错误：{message}", file=sys.stderr)
    raise SystemExit(2)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv or sys.argv[1:])
    if args.key and len(args.images) != 1:
        fail("--key 只能在上传单张图片时使用")
    if not args.bucket:
        fail("缺少 OSS 存储桶；请设置 ALIYUN_OSS_BUCKET 或传入 --bucket")
    if not args.endpoint:
        fail("缺少 OSS 访问域名；请设置 ALIYUN_OSS_ENDPOINT 或传入 --endpoint")

    access_key_id = os.getenv("ALIYUN_OSS_ACCESS_KEY_ID")
    access_key_secret = os.getenv("ALIYUN_OSS_ACCESS_KEY_SECRET")
    security_token = os.getenv("ALIYUN_OSS_SECURITY_TOKEN")
    if not args.dry_run and (not access_key_id or not access_key_secret):
        fail(
            "缺少 OSS 密钥；请在环境变量中设置 ALIYUN_OSS_ACCESS_KEY_ID 和 "
            "ALIYUN_OSS_ACCESS_KEY_SECRET"
        )

    scheme, endpoint_host = normalize_endpoint(args.endpoint)
    uploads: list[dict[str, Any]] = []
    for image_arg in args.images:
        path = Path(image_arg).expanduser().resolve()
        content_type = validate_image(path, args.allow_non_image)
        content_md5, digest = file_digest(path)
        object_key = build_object_key(path, args.prefix, digest, args.key)
        url = build_public_url(args.public_base_url, scheme, endpoint_host, args.bucket, object_key)

        if not args.dry_run:
            put_object(
                path=path,
                bucket=args.bucket,
                endpoint=args.endpoint,
                access_key_id=access_key_id or "",
                access_key_secret=access_key_secret or "",
                object_key=object_key,
                content_type=content_type,
                content_md5=content_md5,
                security_token=security_token,
                acl=args.acl,
                forbid_overwrite=args.forbid_overwrite,
            )

        uploads.append(
            {
                "源文件": str(path),
                "存储桶": args.bucket,
                "访问域名": endpoint_host,
                "对象路径": object_key,
                "链接": url,
                "内容类型": content_type,
                "大小": path.stat().st_size,
                "是否演练": args.dry_run,
            }
        )

    if args.format == "json":
        print(json.dumps({"成功": True, "上传结果": uploads}, ensure_ascii=False, indent=2))
    elif args.format == "markdown":
        for item in uploads:
            alt = Path(str(item["源文件"])).stem
            print(f"![{alt}]({item['链接']})")
    else:
        for item in uploads:
            print(item["链接"])


if __name__ == "__main__":
    main()
