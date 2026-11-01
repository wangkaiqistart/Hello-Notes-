"""Replace explanatory labels in source diagrams; preserve all other pixels.

Requires Pillow and macOS Heiti SC. Originals stay intact; outputs are lossless PNG.
Run from any directory with: python3 translate/spring-ai-etl-pipeline-zh-CN/localize-images.py
"""

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / "public/images/spring-ai/etl"
FONT = "/System/Library/Fonts/STHeiti Light.ttc"

# Rectangles use reference-view coordinates, scaled to each original's resolution.
# English API identifiers, generic signatures and all diagram edges remain intact.
SPECS = [
    {
        "stem": "document-api",
        "referenceWidth": 1600,
        "labels": [
            ([151, 59, 303, 96], "AGGREGATE", "聚合", 25, "center", [239, 239, 239]),
            ([151, 112, 303, 149], "HAS A", "持有", 25, "center", [239, 239, 239]),
            ([151, 164, 303, 201], "IS A", "继承", 25, "center", [239, 239, 239]),
            ([151, 217, 303, 254], "CLASS", "类", 25, "center", [239, 239, 239]),
            (
                [8, 412, 895, 517],
                "The Content field contains the primary, textual content along with optional Metadata.",
                "Content 字段保存主要文本内容，\n以及可选的元数据（Metadata）。",
                38,
                "left",
                [255, 255, 255],
            ),
            (
                [8, 573, 895, 619],
                "The Media fields contains the multimodal inputs.",
                "Media 字段包含多模态输入。",
                38,
                "left",
                [255, 255, 255],
            ),
            (
                [8, 676, 895, 841],
                "The data of a media attachment in a Document. It consists of a MIME type and either the raw media data or an URI to the data.",
                "文档中的媒体附件数据由 MIME 类型\n和媒体内容组成；内容可以是原始媒体\n数据，也可以是指向该数据的 URI。",
                38,
                "left",
                [255, 255, 255],
            ),
        ],
    },
    {
        "stem": "etl-pipeline",
        "referenceWidth": 2048,
        "labels": [
            ([251, 70, 499, 108], "Document Reader", "文档读取器", 28, "center", [255, 255, 255]),
            ([850, 45, 1172, 86], "Document Transformer", "文档转换器", 28, "center", [255, 255, 255]),
            ([1555, 72, 1832, 111], "Document Writer", "文档写入器", 28, "center", [255, 255, 255]),
            ([53, 162, 168, 198], "Source", "数据源", 25, "center", [255, 255, 255]),
            ([1899, 162, 1998, 198], "Store", "存储", 25, "center", [255, 255, 255]),
        ],
    },
    {
        "stem": "etl-class-diagram",
        "referenceWidth": 2048,
        "labels": [
            ([116, 30, 234, 57], "Interface", "接口", 16, "left", [255, 255, 255]),
            ([116, 84, 234, 109], "Class", "类", 16, "left", [255, 255, 255]),
            ([116, 123, 234, 148], "Extends", "继承", 16, "left", [255, 255, 255]),
            ([116, 157, 234, 183], "Implements", "实现", 16, "left", [255, 255, 255]),
            ([116, 192, 234, 218], "Data flow", "数据流", 16, "left", [255, 255, 255]),
            ([116, 226, 234, 251], "has 0..*", "包含 0..*", 16, "left", [255, 255, 255]),
            ([196, 314, 264, 341], "Source", "数据源", 16, "center", [255, 255, 255]),
            ([1902, 339, 1973, 368], "Store", "存储", 16, "center", [255, 255, 255]),
        ],
    },
]


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def localize(spec):
    source = ASSETS / (spec["stem"] + ".jpg")
    destination = ASSETS / (spec["stem"] + "-zh-CN.png")
    original = Image.open(source).convert("RGB")
    output = original.copy()
    draw = ImageDraw.Draw(output)
    mask = Image.new("L", original.size)
    mask_draw = ImageDraw.Draw(mask)
    scale = original.width / spec["referenceWidth"]
    labels = []
    for rect, english, chinese, size, align, background in spec["labels"]:
        box = tuple(round(value * scale) for value in rect)
        x0, y0, x1, y1 = box
        draw.rectangle(box, fill=tuple(background))
        mask_draw.rectangle(box, fill=255)
        font = ImageFont.truetype(FONT, round(size * scale), index=1)
        spacing = round(size * 0.48 * scale)
        bounds = draw.multiline_textbbox((0, 0), chinese, font=font, spacing=spacing)
        width, height = bounds[2] - bounds[0], bounds[3] - bounds[1]
        assert width <= x1 - x0 and height <= y1 - y0, (spec["stem"], chinese, bounds)
        x = x0 + ((x1 - x0 - width) / 2 if align == "center" else 5 * scale) - bounds[0]
        y = y0 + (y1 - y0 - height) / 2 - bounds[1]
        draw.multiline_text((x, y), chinese, font=font, fill=(30, 30, 30), spacing=spacing)
        labels.append({"source": english, "translation": chinese, "rectangle": box})
    output.save(destination, optimize=True)
    saved = Image.open(destination).convert("RGB")
    delta = ImageChops.difference(original, saved)
    outside = Image.new("RGB", original.size)
    outside.paste(delta, mask=ImageChops.invert(mask))
    assert outside.getbbox() is None, "Pixels outside text rectangles changed"
    preview = saved.copy()
    preview.thumbnail((1600, 1300))
    preview.save("/tmp/" + spec["stem"] + "-zh-CN-preview.png")
    return {
        "source": str(source.relative_to(ROOT)),
        "sourceSha256": sha256(source),
        "output": str(destination.relative_to(ROOT)),
        "outputSha256": sha256(destination),
        "width": saved.width,
        "height": saved.height,
        "outsideTextRectanglesUnchanged": True,
        "labels": labels,
    }


if __name__ == "__main__":
    report = {
        "date": "2026-11-01",
        "method": "Deterministic text replacement on source pixels; lossless PNG output.",
        "font": "Heiti SC Light",
        "preserved": "Original dimensions, layout, colors, shapes, edges and Java API identifiers.",
        "images": [localize(spec) for spec in SPECS],
    }
    path = Path(__file__).with_name("2026-11-01-image-localization.json")
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"images": len(report["images"]), "pixelPreservation": "PASS"}))
