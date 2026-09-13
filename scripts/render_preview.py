#!/usr/bin/env python3
"""Render full pages for visual QA, never for extracting paper figures.

python scripts/render_preview.py final.pptx --output work/preview
python scripts/render_preview.py final.pdf --output work/preview

PPTX input requires local LibreOffice/soffice (or --soffice PATH). It exports
a temporary PDF with an isolated user profile, without modifying the PPTX.
An existing PDF from another presentation tool can be rendered directly.
PyMuPDF renders every page; Pillow assembles a contact sheet. No private API,
COM automation, system font installation or desktop window is required.

The output directory must be new. These images are previews, not editable
slides or extracted original figures. Open every slide-*.png with view_image
or another image viewer; successful rendering alone is not visual review.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

try:
    import pymupdf as fitz
    from PIL import Image, ImageDraw
except ImportError as exc:
    raise SystemExit(
        "Preview dependencies are missing. Run: python -m pip install PyMuPDF Pillow"
    ) from exc


REVIEW_NOTICE = (
    "Preview only. Open every slide PNG at full size and inspect labels, text, "
    "tables, formulas and connectors. A contact sheet and successful rendering "
    "do not establish visual quality or desktop PowerPoint compatibility. "
    "Do not use these page images as extracted paper figures."
)


def find_soffice(explicit: str | None = None) -> str:
    """Resolve an explicit executable or an existing LibreOffice on PATH."""
    if explicit:
        candidate = Path(explicit).expanduser()
        found = str(candidate.resolve()) if candidate.is_file() else shutil.which(explicit)
    else:
        found = shutil.which("soffice") or shutil.which("libreoffice")
    if not found:
        raise FileNotFoundError(
            "LibreOffice/soffice was not found. Install LibreOffice or pass "
            "--soffice PATH. Alternatively, export the PPTX to PDF with an "
            "available presentation tool, then run this script on that PDF."
        )
    return found


def convert_pptx(source: Path, workspace: Path, soffice: str) -> Path:
    """Convert to PDF in a private directory, checking output as well as exit code."""
    export_dir = workspace / "pdf"
    export_dir.mkdir()
    profile = workspace / "libreoffice-profile"
    command = [
        soffice, f"-env:UserInstallation={profile.resolve().as_uri()}",
        "--headless", "--nologo", "--nodefault", "--nofirststartwizard",
        "--convert-to", "pdf:impress_pdf_Export", "--outdir", str(export_dir), str(source),
    ]
    try:
        proc = subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
            timeout=120, creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError("LibreOffice PDF conversion timed out after 120 seconds; no preview was published.") from exc
    pdf = export_dir / f"{source.stem}.pdf"
    if proc.returncode or not pdf.is_file() or pdf.stat().st_size == 0:
        details = (proc.stderr + b"\n" + proc.stdout).decode("utf-8", "replace").strip()
        raise RuntimeError(
            f"LibreOffice PDF conversion failed (exit {proc.returncode}); "
            f"no usable PDF was produced. {details[:2000]}"
        )
    return pdf


def contact_sheet(folder: Path, pages: list[dict]) -> str:
    """Assemble labeled thumbnails in numeric page order, with no font dependency."""
    columns = min(3, len(pages))
    thumb_w, thumb_h, gap, label_h = 480, 270, 18, 24
    rows = math.ceil(len(pages) / columns)
    sheet = Image.new("RGB", (
        columns * thumb_w + (columns + 1) * gap,
        rows * (thumb_h + label_h) + (rows + 1) * gap,
    ), "#e7ebef")
    draw = ImageDraw.Draw(sheet)
    for index, record in enumerate(pages):
        x = gap + (index % columns) * (thumb_w + gap)
        y = gap + (index // columns) * (thumb_h + label_h + gap)
        draw.rectangle((x, y, x + thumb_w - 1, y + thumb_h - 1), fill="white")
        with Image.open(folder / record["path"]) as source:
            thumb = source.convert("RGB")
            thumb.thumbnail((thumb_w, thumb_h), Image.Resampling.LANCZOS)
            sheet.paste(thumb, (x + (thumb_w - thumb.width) // 2,
                               y + (thumb_h - thumb.height) // 2))
        draw.text((x, y + thumb_h + 5), f"Slide {record['page']}", fill="#25384b")
    name = "contact-sheet.png"
    sheet.save(folder / name)
    return name


def render_preview(source: Path, output: Path, soffice: str | None = None,
                   max_width: int = 1600, max_height: int = 900) -> dict:
    source = Path(source).expanduser().resolve()
    output = Path(output).expanduser().resolve()
    if output.exists():
        raise FileExistsError(f"Output already exists; choose a new directory: {output}")
    if not source.is_file():
        raise FileNotFoundError(f"Input file was not found: {source}")
    if source.suffix.lower() not in {".pdf", ".pptx"}:
        raise ValueError("Input must be a .pptx presentation or an exported .pdf")
    if max_width <= 0 or max_height <= 0:
        raise ValueError("--max-width and --max-height must be positive integers")
    office = find_soffice(soffice) if source.suffix.lower() == ".pptx" else None
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="paperloom-preview-", dir=output.parent) as temporary:
        workspace = Path(temporary)
        staged = workspace / "preview"
        staged.mkdir()
        pdf = convert_pptx(source, workspace, office) if office else source
        pages = []
        with fitz.open(pdf) as document:
            if document.needs_pass:
                raise ValueError("The PDF requires a password; export an unlocked preview PDF first")
            if document.page_count < 1:
                raise ValueError("The PDF has no pages to render")
            digits = max(2, len(str(document.page_count)))
            for number, page in enumerate(document, start=1):
                width, height = page.rect.width, page.rect.height
                if width <= 0 or height <= 0:
                    raise ValueError(f"Page {number} has invalid dimensions")
                scale = min(max_width / width, max_height / height)
                pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale),
                                      colorspace=fitz.csRGB, alpha=False)
                filename = f"slide-{number:0{digits}d}.png"
                pix.save(staged / filename)
                pages.append({"page": number, "path": filename,
                              "width_px": pix.width, "height_px": pix.height})
        if office:
            shutil.copyfile(pdf, staged / "source-preview.pdf")
        manifest = {
            "purpose": "visual-quality-preview",
            "source": str(source),
            "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            "route": "libreoffice-to-pdf-pymupdf" if office else "pdf-pymupdf",
            "page_count": len(pages), "pages": pages,
            "max_width": max_width, "max_height": max_height,
            "contact_sheet": contact_sheet(staged, pages),
            "preview_pdf": "source-preview.pdf" if office else None,
            "review_required": REVIEW_NOTICE,
        }
        (staged / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        # Reserve exclusively after conversion/rendering succeeds. An existing
        # user directory is never reused, even if another process created it.
        output.mkdir()
        for artifact in staged.iterdir():
            artifact.rename(output / artifact.name)
    return {"output": str(output), **manifest}


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path, required=True, help="New directory for page PNGs, contact sheet and manifest")
    parser.add_argument("--soffice", help="Local LibreOffice/soffice executable, needed only for PPTX input")
    parser.add_argument("--max-width", type=int, default=1600, help="Maximum page width in pixels (default: 1600)")
    parser.add_argument("--max-height", type=int, default=900, help="Maximum page height in pixels (default: 900)")
    args = parser.parse_args()
    try:
        result = render_preview(args.input, args.output, args.soffice, args.max_width, args.max_height)
    except (OSError, ValueError, RuntimeError) as exc:
        parser.exit(2, f"ERROR: {exc}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
