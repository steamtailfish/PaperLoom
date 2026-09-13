"""Preview regressions: real PDF rasterization and conversion failure boundaries."""
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import pymupdf as fitz
from PIL import Image

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "render_preview.py"
SPEC = importlib.util.spec_from_file_location("render_preview", SCRIPT)
preview = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(preview)


class RenderPreviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def make_pdf(self, count=2):
        source = self.root / "slides.pdf"
        with fitz.open() as document:
            for i in range(count):
                page = document.new_page(width=160, height=90)
                color = (1, 0, 0) if i % 2 == 0 else (0, 0, 1)
                page.draw_rect(page.rect, color=color, fill=color)
                page.insert_text((12, 24), str(i + 1), color=(1, 1, 1))
            document.save(source)
        return source

    def test_real_pdf_renders_all_pages_in_numeric_order(self):
        source = self.make_pdf(12)
        original = source.read_bytes()
        output = self.root / "preview"
        result = preview.render_preview(source, output, max_width=320, max_height=180)
        self.assertEqual(result["page_count"], 12)
        names = [f"slide-{i:02d}.png" for i in range(1, 13)]
        self.assertEqual([p["path"] for p in result["pages"]], names)
        self.assertEqual(sorted(p.name for p in output.glob("slide-*.png")), names)
        with Image.open(output / "slide-01.png") as first, Image.open(output / "slide-02.png") as second:
            self.assertEqual(first.size, (320, 180))
            self.assertEqual(first.getpixel((160, 90)), (255, 0, 0))
            self.assertEqual(second.getpixel((160, 90)), (0, 0, 255))
        with Image.open(output / "contact-sheet.png") as sheet:
            # First row follows pages 1, 2, 3 rather than lexical 1, 10, 11.
            self.assertEqual(sheet.getpixel((258, 153)), (255, 0, 0))
            self.assertEqual(sheet.getpixel((756, 153)), (0, 0, 255))
        manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["pages"], result["pages"])
        self.assertEqual(manifest["route"], "pdf-pymupdf")
        self.assertIn("Open every slide", manifest["review_required"])
        self.assertEqual(source.read_bytes(), original)

    def test_existing_output_is_not_changed(self):
        source = self.make_pdf()
        output = self.root / "existing"
        output.mkdir()
        marker = output / "keep.txt"
        marker.write_text("user content", encoding="utf-8")
        with self.assertRaisesRegex(FileExistsError, "choose a new directory"):
            preview.render_preview(source, output)
        self.assertEqual(marker.read_text(encoding="utf-8"), "user content")
        self.assertEqual(list(output.iterdir()), [marker])

    def test_missing_soffice_explains_pdf_fallback_without_output(self):
        source = self.root / "slides.pptx"
        source.write_bytes(b"fixture")
        output = self.root / "preview"
        with patch.object(preview.shutil, "which", return_value=None):
            with self.assertRaisesRegex(FileNotFoundError, "export the PPTX to PDF"):
                preview.render_preview(source, output)
        self.assertFalse(output.exists())

    def test_conversion_failure_or_missing_pdf_never_reports_success(self):
        source = self.root / "slides.pptx"
        source.write_bytes(b"fixture")
        for code in (1, 0):
            with self.subTest(returncode=code):
                output = self.root / f"failed-{code}"
                result = subprocess.CompletedProcess(["soffice"], code, stdout=b"", stderr=b"conversion unavailable")
                with patch.object(preview, "find_soffice", return_value="soffice"), \
                     patch.object(preview.subprocess, "run", return_value=result) as execute:
                    with self.assertRaisesRegex(RuntimeError, "no usable PDF"):
                        preview.render_preview(source, output)
                self.assertFalse(output.exists())
                self.assertEqual(source.read_bytes(), b"fixture")
                command = execute.call_args.args[0]
                profile = next(arg for arg in command if arg.startswith("-env:UserInstallation="))
                self.assertIn("file:", profile)
        self.assertEqual(list(self.root.glob("paperloom-preview-*")), [])


if __name__ == "__main__":
    unittest.main()
