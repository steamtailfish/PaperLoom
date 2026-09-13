"""Small format regressions plus optional real-deck integration.

Run: python -m unittest discover -s tests -v
Set PAPER_DECK_REAL_PPTX to validate a real eight-slide/three-formula deck.
Font regressions skip explicitly in the font-free GitHub source distribution.
"""
from __future__ import annotations
import importlib.util
import json
import os
from pathlib import Path
import shutil
import struct
import tempfile
import unittest
from zipfile import ZipFile, ZIP_DEFLATED
from lxml import etree as ET

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / f'{name}.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


embed_fonts = load('embed_fonts')
inject = load('inject_equations')
validator = load('validate_pptx')
NS = validator.NS


def minimal_pptx(path, text='[[EQ_1]]', absolute_target=False):
    """Small package fixture for targeted structural unit tests, not visual QA."""
    p, a, r, rel, ct = (NS[k] for k in ('p', 'a', 'r', 'rel', 'ct'))
    target = '/ppt/slides/slide1.xml' if absolute_target else 'slides/slide1.xml'
    parts = {
        '[Content_Types].xml': f'<Types xmlns="{ct}"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/><Override PartName="/ppt/slides/slide1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/></Types>',
        '_rels/.rels': f'<Relationships xmlns="{rel}"><Relationship Id="rId1" Type="{r}/officeDocument" Target="ppt/presentation.xml"/></Relationships>',
        'ppt/presentation.xml': f'<p:presentation xmlns:p="{p}" xmlns:r="{r}"><p:sldIdLst><p:sldId id="256" r:id="rId1"/></p:sldIdLst><p:sldSz cx="12192000" cy="6858000"/><p:notesSz cx="6858000" cy="9144000"/></p:presentation>',
        'ppt/_rels/presentation.xml.rels': f'<Relationships xmlns="{rel}"><Relationship Id="rId1" Type="{r}/slide" Target="{target}"/></Relationships>',
        'ppt/slides/slide1.xml': f'<p:sld xmlns:p="{p}" xmlns:a="{a}"><p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/><p:sp><p:nvSpPr><p:cNvPr id="2" name="Equation"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr><p:spPr/><p:txBody><a:bodyPr/><a:lstStyle/><a:p><a:r><a:rPr sz="2000"/><a:t>{text}</a:t></a:r></a:p></p:txBody></p:sp></p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>',
    }
    with ZipFile(path, 'w', ZIP_DEFLATED) as z:
        for name, data in parts.items():
            z.writestr(name, data.encode())
    return path


def rewrite(src, dest, callback):
    with ZipFile(src) as zin, ZipFile(dest, 'w', ZIP_DEFLATED) as zout:
        for name in zin.namelist():
            zout.writestr(name, callback(name, zin.read(name)))


class OfficeRegressionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.dir = Path(self.temp.name)

    def test_absolute_relationship_target(self):
        file = minimal_pptx(self.dir / 'absolute.pptx', text='Ready', absolute_target=True)
        report = validator.validate(file, expected_slides=1, expected_math=0)
        self.assertTrue(report['ok'], report['errors'])
        self.assertEqual(validator.resolve_target('ppt/slides/slide1.xml', '../media/image1.png'), 'ppt/media/image1.png')

    def test_unresolved_equation_is_error(self):
        file = minimal_pptx(self.dir / 'tokens.pptx')
        self.assertTrue(any('Unconverted equation' in e for e in validator.validate(file)['errors']))

    def test_bad_charset_rejected(self):
        file = minimal_pptx(self.dir / 'source.pptx', 'Ready')
        bad = self.dir / 'bad.pptx'
        def mutate(name, data):
            if name == 'ppt/presentation.xml':
                root = ET.fromstring(data)
                entries = ET.SubElement(root, f'{{{NS["p"]}}}embeddedFontLst')
                entry = ET.SubElement(entries, f'{{{NS["p"]}}}embeddedFont')
                ET.SubElement(entry, f'{{{NS["p"]}}}font', typeface='FangSong_GB2312', charset='134')
                return ET.tostring(root)
            return data
        rewrite(file, bad, mutate)
        report = validator.validate(bad)
        self.assertFalse(report['ok'])
        self.assertTrue(any('signed-byte' in e for e in report['errors']))

    def test_presentation_notes_master_order(self):
        source = minimal_pptx(self.dir / 'source.pptx', 'Ready')
        for valid_order in (False, True):
            with self.subTest(valid_order=valid_order):
                dest = self.dir / f'notes-order-{valid_order}.pptx'
                def mutate(name, data):
                    if name != 'ppt/presentation.xml':
                        return data
                    root = ET.fromstring(data)
                    master_list = ET.Element(f'{{{NS["p"]}}}notesMasterIdLst')
                    # Before sldIdLst is legal; after sldIdLst caused Office's
                    # CT_Presentation schema failure in the public demo.
                    root.insert(0 if valid_order else 1, master_list)
                    return ET.tostring(root)
                rewrite(source, dest, mutate)
                report = validator.validate(dest)
                self.assertEqual(report['ok'], valid_order, report['errors'])
                if not valid_order:
                    self.assertTrue(any('presentation child order' in e for e in report['errors']))

    def test_paragraph_properties_unique_and_before_runs(self):
        source = minimal_pptx(self.dir / 'source.pptx', 'Ready')
        for variant in ('duplicate', 'late', 'valid'):
            with self.subTest(variant=variant):
                dest = self.dir / f'paragraph-{variant}.pptx'
                def mutate(name, data):
                    if name != 'ppt/slides/slide1.xml':
                        return data
                    root = ET.fromstring(data)
                    paragraph = root.find('.//a:p', NS)
                    if variant in ('duplicate', 'valid'):
                        paragraph.insert(0, ET.Element(f'{{{NS["a"]}}}pPr'))
                    if variant in ('duplicate', 'late'):
                        ET.SubElement(paragraph, f'{{{NS["a"]}}}pPr')
                    return ET.tostring(root)
                rewrite(source, dest, mutate)
                report = validator.validate(dest)
                self.assertEqual(report['ok'], variant == 'valid', report['errors'])
                if variant != 'valid':
                    self.assertTrue(any('a:pPr' in e for e in report['errors']))

    def test_non_target_slide_comparison(self):
        source = minimal_pptx(self.dir / 'before.pptx', 'Before')
        after = self.dir / 'after.pptx'
        rewrite(source, after, lambda name, data: data.replace(b'Before', b'After') if name.endswith('slide1.xml') else data)
        self.assertFalse(validator.validate(after, compare=source)['ok'])
        self.assertTrue(validator.validate(after, compare=source, allowed_slides=[1])['ok'])

    def test_source_overwrite_is_rejected(self):
        source = minimal_pptx(self.dir / 'source.pptx')
        original = source.read_bytes()
        with self.assertRaises(ValueError):
            inject.inject_equations(source, source, {'[[EQ_1]]': {'latex': 'x'}})
        with self.assertRaises(ValueError):
            embed_fonts.embed(source, source, [])
        self.assertEqual(source.read_bytes(), original)

    @unittest.skipUnless(shutil.which('pandoc'), 'Pandoc is not installed; native LaTeX-to-OMML test requires pandoc on PATH')
    def test_native_formula_replaces_token_and_preserves_parts(self):
        source = minimal_pptx(self.dir / 'source.pptx')
        dest = self.dir / 'math.pptx'
        report = inject.inject_equations(source, dest, {'[[EQ_1]]': {'latex': r'P=\frac{x}{1+x}'}})
        self.assertEqual(report['math_expressions'], 1)
        self.assertTrue(validator.validate(dest, expected_math=1)['ok'])
        with ZipFile(source) as before, ZipFile(dest) as after:
            for name in before.namelist():
                if name != 'ppt/slides/slide1.xml':
                    self.assertEqual(before.read(name), after.read(name))
            root = ET.fromstring(after.read('ppt/slides/slide1.xml'))
            self.assertTrue(root.findall('.//a14:m//m:f', NS))
            self.assertEqual(set(root.xpath('//a14:m//a:latin/@typeface', namespaces=NS)), {'Times New Roman'})
        with self.assertRaises(FileExistsError):
            inject.inject_equations(source, dest, {'[[EQ_1]]': {'latex': 'x'}})

    @unittest.skipUnless(shutil.which('pandoc'), 'Pandoc is not installed')
    def test_partial_paragraph_token_rejected_without_output(self):
        source = minimal_pptx(self.dir / 'source.pptx', 'Inline [[EQ_1]] text')
        dest = self.dir / 'bad.pptx'
        with self.assertRaises(ValueError):
            inject.inject_equations(source, dest, {'[[EQ_1]]': {'latex': 'x'}})
        self.assertFalse(dest.exists())

    def test_font_order_and_signed_charset(self):
        font_names = ['TIMESBI.TTF', 'TIMESI.TTF', 'TIMES.TTF', 'TIMESBD.TTF', '仿宋_GB2312.ttf']
        paths = [ROOT / 'fonts' / name for name in font_names]
        if not all(p.is_file() for p in paths):
            self.skipTest('Font files intentionally absent in source-only distribution; supply licensed files in fonts/ to test embedding')
        source = minimal_pptx(self.dir / 'source.pptx', 'Ready')
        dest = self.dir / 'fonts.pptx'
        embed_fonts.embed(source, dest, paths)
        self.assertTrue(validator.validate(dest)['ok'])
        with ZipFile(dest) as z:
            root = ET.fromstring(z.read('ppt/presentation.xml'))
            for entry in root.findall('p:embeddedFontLst/p:embeddedFont', NS):
                font = entry.find('p:font', NS)
                if font.get('typeface') == 'Times New Roman':
                    self.assertEqual([ET.QName(c).localname for c in entry], ['font', 'regular', 'bold', 'italic', 'boldItalic'])
                if font.get('typeface') == 'FangSong_GB2312':
                    self.assertEqual(font.get('charset'), '-122')
        eot, meta = embed_fonts.font_eot(paths[-1])
        self.assertEqual(eot[26], 134)  # EOT charset remains an unsigned BYTE.
        self.assertEqual(meta['charset'], 134)
        self.assertEqual(struct.unpack_from('<I', eot)[0], len(eot))
        with self.assertRaises(ValueError):
            embed_fonts.embed(dest, self.dir / 'duplicate.pptx', paths)
        self.assertFalse((self.dir / 'duplicate.pptx').exists())

    def test_real_example_if_available(self):
        configured = os.environ.get('PAPER_DECK_REAL_PPTX')
        path = Path(configured) if configured else ROOT / 'examples/layout-demo/layout-demo.pptx'
        if not path.is_file():
            self.skipTest('Set PAPER_DECK_REAL_PPTX or provide the bundled layout-demo.pptx')
        # The optional GeoNav fixture has 8 slides/3 formulas; the public
        # component demonstration deliberately has 3 slides/1 formula.
        report = validator.validate(path, expected_slides=8 if configured else 3,
                                     expected_math=3 if configured else 1)
        self.assertTrue(report['ok'], report['errors'])


if __name__ == '__main__':
    unittest.main()
