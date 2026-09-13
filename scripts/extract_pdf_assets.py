#!/usr/bin/env python3
"""Extract embedded PDF Image XObjects, never rasterize a PDF page.

Dependencies: PyMuPDF >= 1.24, Pillow >= 10. Run --help for usage.
Copyright (c) 2026 paper-loom contributors. MIT licensed.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import math
from pathlib import Path
import sys
from typing import Any

try:
    import pymupdf as fitz
    from PIL import Image
except ImportError as exc:
    raise SystemExit(
        "缺少依赖。请运行: python -m pip install 'PyMuPDF>=1.24' 'Pillow>=10'"
    ) from exc


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_pages(spec: str | None, count: int) -> list[int]:
    """Return zero-based page indices; external page numbers are one-based."""
    if not spec:
        return list(range(count))
    selected: set[int] = set()
    try:
        for token in spec.split(","):
            token = token.strip()
            if "-" in token:
                start, end = map(int, token.split("-"))
                if start > end:
                    raise ValueError("页码范围必须递增")
            else:
                start = end = int(token)
            if start < 1 or end > count:
                raise ValueError(f"页码必须在 1–{count} 之间")
            selected.update(range(start - 1, end))
    except (TypeError, ValueError) as exc:
        raise ValueError(f"无效 --pages {spec!r}；示例: 1,3-5。{exc}") from exc
    return sorted(selected)


def numbers(values: Any) -> list[float] | None:
    result = [round(float(value), 5) for value in values]
    return result if all(math.isfinite(value) for value in result) else None


def save_bytes(output: Path, relative: str, data: bytes) -> dict[str, Any]:
    target = output / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    return {"path": relative, "sha256": sha256(data), "bytes": len(data)}


def inspect_pixels(data: bytes) -> dict[str, Any]:
    with Image.open(io.BytesIO(data)) as image:
        image.load()
        info: dict[str, Any] = {
            "width_px": image.width,
            "height_px": image.height,
            "mode": image.mode,
        }
        if "A" in image.getbands():
            low, high = image.getchannel("A").getextrema()
            info["alpha_range"] = [low, high]
        return info


def extract_xobject(doc: Any, xref: int, smask: int, output: Path) -> dict[str, Any]:
    """Decode an existing image resource, optionally reattach its soft mask."""
    raw = doc.extract_image(xref)
    if not raw or not raw.get("image"):
        raise ValueError(f"xref {xref} 不是可提取的 Image XObject")
    extension = raw["ext"].lower()
    if not extension.isalnum():
        raise ValueError(f"不支持的图像扩展名: {extension!r}")
    original = save_bytes(output, f"assets/xref_{xref}.{extension}", raw["image"])
    image_bytes = raw["image"]
    result: dict[str, Any] = {
        "xref": xref,
        "smask_xref": smask,
        "route": "embedded-image-xobject",
        "original": original,
        "source_width_px": int(raw["width"]),
        "source_height_px": int(raw["height"]),
        "source_bits_per_component": raw.get("bpc"),
        "source_colorspace": raw.get("cs-name"),
        "source_mask_dictionary": list(doc.xref_get_key(xref, "Mask")),
    }
    selected_file = original
    if smask > 0:
        mask_raw = doc.extract_image(smask)
        if not mask_raw or not mask_raw.get("image"):
            raise ValueError(f"xref {xref} 的软遮罩 {smask} 无法提取；不输出不透明替代图")
        result["soft_mask"] = save_bytes(
            output, f"assets/mask_{smask}.{mask_raw['ext']}", mask_raw["image"]
        )
        base = fitz.Pixmap(doc, xref)
        mask = fitz.Pixmap(doc, smask)
        if base.alpha:
            base = fitz.Pixmap(base, 0)
        if base.colorspace is None:
            raise ValueError(f"xref {xref} 无颜色空间，需人工检查模板遮罩")
        if base.colorspace.n not in (1, 3):
            base = fitz.Pixmap(fitz.csRGB, base)
        if (base.width, base.height) != (mask.width, mask.height):
            raise ValueError(f"xref {xref} 图像和软遮罩大小不一致，需原生内容复核")
        combined = fitz.Pixmap(base, mask)
        image_bytes = combined.tobytes("png")
        selected_file = save_bytes(output, f"assets/xref_{xref}_alpha.png", image_bytes)
        result["route"] = "embedded-image-xobject-softmask-reconstruction"
    result.update(selected_file)
    try:
        result.update(inspect_pixels(image_bytes))
        result["pixel_decode_verified"] = True
    except Exception as exc:
        # Keep exact extracted bytes even if Pillow lacks the relevant decoder.
        pix = fitz.Pixmap(doc, xref)
        result.update({"width_px": pix.width, "height_px": pix.height})
        result["pixel_decode_verified"] = False
        result["decode_warning"] = f"Pillow 未能验证文件: {exc}"
    return result


def extract_document(
    source: Path, output: Path, pages: str | None = None,
    min_width: int = 0, min_height: int = 0, overwrite: bool = False,
) -> dict[str, Any]:
    source, output = source.resolve(), output.resolve()
    if min_width < 0 or min_height < 0:
        raise ValueError("最小像素尺寸不能为负数")
    if not source.is_file():
        raise FileNotFoundError(source)
    if (output / "manifest.json").exists() and not overwrite:
        raise FileExistsError("输出目录已有 manifest.json；请选择新目录或显式传入 --overwrite")
    with fitz.open(source) as doc:
        if not doc.is_pdf:
            raise ValueError("输入必须是 PDF")
        if doc.needs_pass:
            raise ValueError("PDF 已加密；请先提供可正常读取的解密副本")
        selected = parse_pages(pages, len(doc))
        output.mkdir(parents=True, exist_ok=True)
        manifest: dict[str, Any] = {
            "schema_version": 1,
            "source": {"filename": source.name, "sha256": sha256(source.read_bytes()),
                       "page_count": len(doc)},
            "tool": {"name": "paper-loom/extract_pdf_assets.py",
                     "pymupdf_version": fitz.VersionBind},
            "policy": {"page_rendering_used": False, "clip_screenshots_used": False,
                       "min_width_px": min_width, "min_height_px": min_height,
                       "selected_pages": [i + 1 for i in selected],
                       "coordinates": "PDF points, PyMuPDF unrotated page coordinates; "
                                      "Form candidate bboxes are local Form coordinates"},
            "assets": [], "occurrences": [], "skipped": [],
            "vector_form_candidates": [], "warnings": [], "errors": [],
        }
        asset_by_xref: dict[int, dict[str, Any]] = {}
        skipped_xrefs: set[int] = set()
        failed_xrefs: set[int] = set()
        for index in selected:
            page = doc[index]
            page_no = index + 1
            resources: dict[int, Any] = {}
            for item in page.get_images(full=True):
                resources.setdefault(int(item[0]), item)
            # This reads object metadata, not a rendered page or clipped image.
            image_info = page.get_image_info(xrefs=True)
            locations: dict[int, list[Any]] = {}
            for info in image_info:
                locations.setdefault(info.get("xref", 0), []).append(info)
            for info in locations.get(0, []):
                manifest["warnings"].append({
                    "page": page_no, "kind": "inline-or-unresolved-image",
                    "bbox": numbers(info["bbox"]),
                    "message": "无可定位的 Image XObject xref；请复核原生内容或作者源图，不自动截图。",
                })
            for xref, item in resources.items():
                smask, width, height = int(item[1]), int(item[2]), int(item[3])
                if width < min_width or height < min_height:
                    if xref not in skipped_xrefs:
                        manifest["skipped"].append({
                            "xref": xref, "width_px": width, "height_px": height,
                            "reason": "below-explicit-minimum-size",
                        })
                        skipped_xrefs.add(xref)
                    continue
                if xref not in asset_by_xref and xref not in failed_xrefs:
                    try:
                        asset = extract_xobject(doc, xref, smask, output)
                        asset_by_xref[xref] = asset
                        manifest["assets"].append(asset)
                        if asset["source_mask_dictionary"][0] != "null":
                            manifest["warnings"].append({
                                "page": page_no, "xref": xref, "kind": "explicit-image-mask",
                                "message": "存在 /Mask；请核对最终透明度和页面合成效果。",
                            })
                    except Exception as exc:
                        failed_xrefs.add(xref)
                        manifest["errors"].append({"page": page_no, "xref": xref,
                                                   "error": str(exc)})
                asset = asset_by_xref.get(xref)
                if asset is None:
                    continue
                occurrences = locations.get(xref, [])
                if not occurrences:
                    # Also resolves images invoked through nested Form XObjects.
                    occurrences = [{"bbox": box, "transform": matrix}
                                   for box, matrix in page.get_image_rects(xref, transform=True)]
                if not occurrences:
                    manifest["warnings"].append({
                        "page": page_no, "xref": xref, "kind": "unused-or-unresolved-resource",
                        "message": "资源可提取，但页面显示位置未找到；不能据此认定为可见论文图。",
                    })
                for occurrence in occurrences:
                    manifest["occurrences"].append({
                        "page": page_no, "xref": xref, "path": asset["path"],
                        "sha256": asset["sha256"], "route": asset["route"],
                        "width_px": asset["width_px"], "height_px": asset["height_px"],
                        "bbox": numbers(occurrence["bbox"]),
                        "transform": numbers(occurrence["transform"]),
                    })
            forms = page.get_xobjects()
            for xref, name, invoker, bbox in forms:
                manifest["vector_form_candidates"].append({
                    "page": page_no, "kind": "form-xobject", "xref": xref,
                    "resource_name": name, "invoker_xref": invoker,
                    "bbox_local": numbers(bbox),
                    "action": "inspect-native-content; may contain text, vectors or images",
                })
            drawings = page.get_drawings()
            if drawings:
                rectangles = [fitz.Rect(item["rect"]) for item in drawings if item.get("rect")]
                bounds = fitz.Rect(rectangles[0]) if rectangles else None
                for rectangle in rectangles[1:]:
                    bounds |= rectangle
                manifest["vector_form_candidates"].append({
                    "page": page_no, "kind": "page-vector-paths",
                    "path_count": len(drawings),
                    "bbox_union": numbers(bounds) if bounds is not None else None,
                    "action": "inspect-native-content; paths are not automatically grouped into figures",
                })
        manifest["warnings"].append({
            "kind": "semantic-review-required",
            "message": "Image XObject 可能只是小面板或纹理。按图号和图注核对完整 Figure；"
                       "图内文字、箭头、图例可能来自 PDF 文本或矢量对象，不能靠提取图片自动补齐。",
        })
        manifest["summary"] = {
            "unique_image_xobjects": len(manifest["assets"]),
            "display_occurrences": len(manifest["occurrences"]),
            "softmask_reconstructions": sum(a["smask_xref"] > 0 for a in manifest["assets"]),
            "skipped_by_size": len(manifest["skipped"]),
            "vector_form_candidates": len(manifest["vector_form_candidates"]),
            "errors": len(manifest["errors"]),
        }
        (output / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2, allow_nan=False) + "\n",
            encoding="utf-8",
        )
        return manifest


def main() -> int:
    parser = argparse.ArgumentParser(
        description="直接提取 PDF 内嵌 Image XObject；恢复软遮罩透明度；绝不渲染/截图页面。",
        epilog="示例: python scripts/extract_pdf_assets.py paper.pdf --output work/assets "
               "--pages 1,3-5\n默认不过滤小图。manifest.json 中的 bbox 单位为 PDF point；"
               "图像资源不一定是完整 Figure，使用前必须与图注核对。\n"
               "返回码: 0 成功；1 参数/文件错误；2 部分资源提取失败（仍写出 manifest）。",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("pdf", type=Path, help="输入论文 PDF 的路径")
    parser.add_argument("--output", required=True, type=Path, help="输出目录；资产与 manifest 写入这里")
    parser.add_argument("--pages", help="从 1 开始的页码或范围，如 1,3-5；默认全部页")
    parser.add_argument("--min-width", type=int, default=0, help="可选最小宽度（像素），默认 0")
    parser.add_argument("--min-height", type=int, default=0, help="可选最小高度（像素），默认 0")
    parser.add_argument("--overwrite", action="store_true", help="允许替换此输出目录内已有的提取结果")
    args = parser.parse_args()
    try:
        manifest = extract_document(args.pdf, args.output, args.pages,
                                    args.min_width, args.min_height, args.overwrite)
    except Exception as exc:
        print(f"提取失败: {exc}", file=sys.stderr)
        return 1
    print(json.dumps({"manifest": str((args.output / 'manifest.json').resolve()),
                      **manifest["summary"]}, ensure_ascii=False))
    if manifest["errors"]:
        print("部分资源未能提取。请查看 manifest.errors；未使用截图替代。", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
