"""Meaningful extraction regressions: masks, repeated images, nested Forms, no render."""

import importlib.util
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import pymupdf as fitz
from PIL import Image

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "extract_pdf_assets.py"
SPEC = importlib.util.spec_from_file_location("extract_pdf_assets", SCRIPT)
extractor = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(extractor)


def png_bytes(size=(40, 20), rgba=False):
    image = Image.new("RGBA" if rgba else "RGB", size, (30, 90, 150, 255) if rgba else (30, 90, 150))
    if rgba:
        image.putpixel((0, 0), (30, 90, 150, 0))
        image.putpixel((1, 0), (30, 90, 150, 128))
    stream = io.BytesIO()
    image.save(stream, format="PNG")
    return stream.getvalue()


class ExtractionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def build_pdf(self):
        source = self.root / "synthetic.pdf"
        with fitz.open() as doc:
            page = doc.new_page()
            xref = page.insert_image(fitz.Rect(10, 10, 90, 50), stream=png_bytes(rgba=True))
            page.insert_image(fitz.Rect(100, 10, 180, 50), xref=xref)
            page.draw_rect(fitz.Rect(20, 100, 160, 200), color=(1, 0, 0))
            page = doc.new_page()
            page.insert_image(fitz.Rect(10, 10, 90, 50), xref=xref)
            page.insert_image(fitz.Rect(10, 60, 18, 68), stream=png_bytes(size=(2, 2)))
            doc.save(source)
        return source, xref

    def test_softmask_dedup_all_positions_and_no_page_render(self):
        source, xref = self.build_pdf()
        output = self.root / "assets"
        with patch.object(fitz.Page, "get_pixmap", side_effect=AssertionError("Page rasterization forbidden")):
            manifest = extractor.extract_document(source, output)
        self.assertEqual(manifest["summary"]["unique_image_xobjects"], 2)
        self.assertEqual(manifest["summary"]["errors"], 0)
        self.assertEqual(manifest["summary"]["softmask_reconstructions"], 1)
        occurrences = [o for o in manifest["occurrences"] if o["xref"] == xref]
        self.assertEqual([o["page"] for o in occurrences], [1, 1, 2])
        asset = next(a for a in manifest["assets"] if a["xref"] == xref)
        self.assertEqual(asset["route"], "embedded-image-xobject-softmask-reconstruction")
        with Image.open(output / asset["path"]) as image:
            self.assertEqual(image.mode, "RGBA")
            self.assertEqual(image.getpixel((0, 0))[3], 0)
            self.assertEqual(image.getpixel((1, 0))[3], 128)
            self.assertEqual(image.getpixel((2, 0))[3], 255)
        self.assertEqual(extractor.sha256((output / asset["path"]).read_bytes()), asset["sha256"])
        self.assertTrue(any(c["kind"] == "page-vector-paths" for c in manifest["vector_form_candidates"]))
        self.assertFalse(manifest["policy"]["page_rendering_used"])

    def test_nested_form_image_is_extracted(self):
        source = self.root / "form.pdf"
        with fitz.open() as inner, fitz.open() as outer:
            inner.new_page(width=100, height=100).insert_image(
                fitz.Rect(10, 10, 90, 50), stream=png_bytes()
            )
            outer.new_page(width=300, height=300).show_pdf_page(fitz.Rect(20, 20, 220, 220), inner, 0)
            outer.save(source)
        manifest = extractor.extract_document(source, self.root / "form-assets")
        self.assertEqual(len(manifest["assets"]), 1)
        self.assertEqual(len(manifest["occurrences"]), 1)
        self.assertTrue(any(c["kind"] == "form-xobject" for c in manifest["vector_form_candidates"]))
        self.assertEqual(manifest["occurrences"][0]["bbox"], [40.0, 40.0, 200.0, 120.0])

    def test_page_selection_small_panels_and_explicit_filter(self):
        source, _ = self.build_pdf()
        page_two = extractor.extract_document(source, self.root / "page-two", pages="2")
        self.assertEqual(len(page_two["assets"]), 2)
        self.assertTrue(all(o["page"] == 2 for o in page_two["occurrences"]))
        filtered = extractor.extract_document(source, self.root / "filtered", min_width=3)
        self.assertEqual(len(filtered["assets"]), 1)
        self.assertEqual(filtered["summary"]["skipped_by_size"], 1)

    def test_bad_page_ranges_and_existing_output_are_rejected(self):
        self.assertEqual(extractor.parse_pages("1,3-5,3", 5), [0, 2, 3, 4])
        for value in ["0", "6", "3-1", "1,", "a"]:
            with self.assertRaises(ValueError):
                extractor.parse_pages(value, 5)
        source, _ = self.build_pdf()
        output = self.root / "existing"
        extractor.extract_document(source, output)
        with self.assertRaises(FileExistsError):
            extractor.extract_document(source, output)


if __name__ == "__main__":
    unittest.main()
