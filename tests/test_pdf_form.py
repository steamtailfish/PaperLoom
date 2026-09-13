import importlib.util
from pathlib import Path
import tempfile
import unittest
import fitz
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, ArrayObject, FloatObject

spec = importlib.util.spec_from_file_location('export_form', Path(__file__).resolve().parents[1] / 'scripts/export_pdf_form.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class FormExportTest(unittest.TestCase):
    def fixture(self, folder, matrix=False):
        figure = fitz.open()
        p = figure.new_page(width=200, height=100)
        p.insert_text((15, 40), 'INSIDE FIGURE')
        p.draw_line((10, 60), (180, 60), color=(1, 0, 0), width=2)
        page = fitz.open()
        p = page.new_page()
        p.insert_text((20, 20), 'OUTSIDE PAPER TEXT')
        p.show_pdf_page(fitz.Rect(20, 100, 220, 200), figure, 0)
        source = folder / 'source.pdf'
        page.save(source)
        xref = next(x[0] for x in p.get_xobjects() if x[1] == 'fullpage')
        page.close()
        if matrix:
            reader = PdfReader(source)
            writer = PdfWriter(clone_from=reader)
            # Locate the cloned inner form independently of its renumbered xref.
            outer = next(iter(writer.pages[0]['/Resources']['/XObject'].values())).get_object()
            inner = outer['/Resources']['/XObject']['/fullpage']
            inner[NameObject('/Matrix')] = ArrayObject([FloatObject(v) for v in [0, 1, -1, 0, 23, -12]])
            writer.write(folder / 'matrix.pdf')
            source = folder / 'matrix.pdf'
            with fitz.open(source) as doc:
                xref = next(x[0] for x in doc[0].get_xobjects() if x[1] == 'fullpage')
        return source, xref

    def test_exports_only_selected_form_with_vector_and_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, xref = self.fixture(root)
            result = module.export_form(source, xref, root / 'out', 1)
            with fitz.open(root / 'out/figure.pdf') as d:
                self.assertIn('INSIDE FIGURE', d[0].get_text())
                self.assertNotIn('OUTSIDE', d[0].get_text())
                self.assertTrue(d[0].get_drawings())
                self.assertEqual(tuple(d[0].rect)[2:], (200, 100))
            self.assertFalse(result['completeness_verified'])
            self.assertTrue((root / 'out/figure.svg').stat().st_size)
            with self.assertRaises(ValueError):
                module.export_form(source, xref, root / 'out')

    def test_matrix_rotation_translation_and_wrong_page(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, xref = self.fixture(root, matrix=True)
            result = module.export_form(source, xref, root / 'out')
            self.assertEqual(result['size_pt'], [100, 200])
            with fitz.open(root / 'out/figure.pdf') as d:
                self.assertIn('INSIDE FIGURE', d[0].get_text())
            with self.assertRaises(ValueError):
                module.export_form(source, xref, root / 'bad', 2)
