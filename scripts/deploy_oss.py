"""Publish the site and retire only HTML pages recorded by earlier releases."""

import argparse
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tempfile


MANIFEST_KEY = ".deployment/pages.json"
BOOTSTRAP = Path(__file__).resolve().parent.parent / "deployment/retired-pages.json"


def validate_pages(value):
    if not isinstance(value, dict) or value.get("version") != 1:
        raise ValueError("不支持的发布清单格式")
    pages = value.get("pages")
    if not isinstance(pages, list):
        raise ValueError("发布清单缺少 pages 列表")
    for key in pages:
        if (
            not isinstance(key, str)
            or not key.endswith(".html")
            or key.startswith("/")
            or str(PurePosixPath(key)) != key
            or any(part in (".", "..") for part in key.split("/"))
            or any(char in key for char in "\\*?[]#%\r\n\x00")
        ):
            raise ValueError("发布清单包含非法 HTML 路径")
    return set(pages)


def run_oss(args):
    if args[0] != "cp":
        return subprocess.run(["ossutil", *args], capture_output=True, text=True)
    # ossutil 1.x may put the actual per-object error only in a report file.
    with tempfile.TemporaryDirectory(prefix="oss-report-") as report_dir:
        result = subprocess.run(["ossutil", *args, "--output-dir", report_dir], capture_output=True, text=True)
        if result.returncode:
            for report in Path(report_dir).rglob("*.report"):
                result.stderr += "\n" + report.read_text(errors="replace")
        return result


def safe_error(output):
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    message = next((line for line in lines if re.search(r"error|错误", line, re.I)), lines[-1] if lines else "无错误详情")
    message = re.sub(r"(?:oss|https?)://\S+", "[对象地址]", message)
    message = re.sub(r"LTAI[A-Za-z0-9]+", "[已隐藏]", message)
    message = re.sub(r"(?i)((?:access[-_]?key(?:[-_]?(?:id|secret))?|security[-_]?token|signature)\s*[:=]\s*)[^\s,;]+", r"\1[已隐藏]", message)
    return message[:300]


def checked_oss(runner, args, *, allow_missing=False):
    result = runner(args)
    if result.returncode:
        # Only a missing object is acceptable; authentication/network errors stop deployment.
        detail = result.stdout + result.stderr
        code = re.search(r"ErrorCode\s*[:=]\s*([A-Za-z0-9]+)", detail)
        # A failed HEAD request may have HTTP 404 without an XML error code.
        missing = (code is not None and code[1] == "NoSuchKey") or (
            code is None and re.search(r"(?:StatusCode|status code)\s*[:=]?\s*404\b", detail, re.I)
        )
        if allow_missing and missing:
            return False
        reason = f"，错误码 {code[1]}" if code else f"，{safe_error(detail)}"
        raise RuntimeError(f"OSS {args[0]} 操作失败（退出码 {result.returncode}{reason}），发布已停止")
    return True


def deploy(dist, bucket, *, apply=False, runner=run_oss, bootstrap=BOOTSTRAP):
    dist = Path(dist).resolve()
    if not (dist / "index.html").is_file():
        raise ValueError("缺少 dist/index.html，请先完成构建")
    if not bucket or any(char not in "abcdefghijklmnopqrstuvwxyz0123456789-" for char in bucket):
        raise ValueError("请通过 OSS_BUCKET 设置有效的桶名称")
    current = validate_pages({
        "version": 1,
        "pages": [file.relative_to(dist).as_posix() for file in dist.rglob("*.html")],
    })
    retired = validate_pages(json.loads(Path(bootstrap).read_text()))
    manifest_url = f"oss://{bucket}/{MANIFEST_KEY}"
    with tempfile.TemporaryDirectory(prefix="site-publish-") as tmp:
        previous_file = Path(tmp) / "previous.json"
        exists = checked_oss(runner, ["cp", manifest_url, str(previous_file), "--force"], allow_missing=True)
        previous = validate_pages(json.loads(previous_file.read_text())) if exists else set()
        stale = sorted((previous | retired) - current)
        plan = {"pages": len(current), "remove": stale, "apply": apply}
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        if not apply:
            return plan

        # Never delete before a complete upload, and record the release only after cleanup succeeds.
        checked_oss(runner, ["cp", "-r", str(dist), f"oss://{bucket}/", "--force"])
        for key in stale:
            checked_oss(runner, ["rm", f"oss://{bucket}/{key}", "--force"], allow_missing=True)
        current_file = Path(tmp) / "current.json"
        current_file.write_text(json.dumps({"version": 1, "pages": sorted(current)}, indent=2) + "\n")
        checked_oss(runner, ["cp", str(current_file), manifest_url, "--force"])
        return plan


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dist", default="dist")
    parser.add_argument("--apply", action="store_true", help="上传并清理；默认仅预览")
    args = parser.parse_args()
    try:
        deploy(args.dist, os.environ.get("OSS_BUCKET", ""), apply=args.apply)
    except (ValueError, RuntimeError, OSError) as error:
        # Surface safe diagnostics in Actions annotations without printing credentials or CLI output.
        message = str(error).replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
        print(f"::error::{message}", file=sys.stderr)
        sys.exit(1)
