"""Regression tests for measurable PPTX risks; fixtures do not test rendering."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from xml.sax.saxutils import escape
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('audit_slide_quality', ROOT / 'scripts/audit_slide_quality.py')
quality = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(quality)
NS = quality.NS
REL_NS = 'http://schemas.openxmlformats.org/package/2006/relationships'


def transform(x, y, width, height, *, rotation=None):
    attrs = f' rot="{rotation}"' if rotation is not None else ''
    return f'<a:xfrm{attrs}><a:off x="{x}" y="{y}"/><a:ext cx="{width}" cy="{height}"/></a:xfrm>'


def text_shape(text, *, x=100, y=200, width=800, height=300, role=None, size=2200, rotation=None):
    ph = f'<p:ph type="{role}"/>' if role else ''
    rpr = f'<a:rPr sz="{size}"/>' if size is not None else ''
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="2" name="Text"/><p:cNvSpPr txBox="1"/>'
            f'<p:nvPr>{ph}</p:nvPr></p:nvSpPr><p:spPr>'
            f'{transform(x, y, width, height, rotation=rotation)}</p:spPr><p:txBody><a:bodyPr/><a:lstStyle/>'
            f'<a:p><a:r>{rpr}<a:t>{escape(text)}</a:t></a:r></a:p></p:txBody></p:sp>')


def picture(x=100, y=200, width=500, height=500, rotation=None):
    return (f'<p:pic><p:nvPicPr><p:cNvPr id="3" name="Evidence image"/><p:cNvPicPr/><p:nvPr/>'
            f'</p:nvPicPr><p:blipFill><a:blip r:embed="img1"/></p:blipFill><p:spPr>'
            f'{transform(x, y, width, height, rotation=rotation)}</p:spPr></p:pic>')


def graphic(category, text=''):
    if category == 'chart':
        content = '<c:chart r:id="chart1"/>'
        uri = NS['c']
    else:
        content = ('<a:tbl><a:tr h="500"><a:tc><a:txBody><a:bodyPr/><a:lstStyle/>'
                   f'<a:p><a:r><a:rPr sz="1200"/><a:t>{escape(text)}</a:t></a:r></a:p>'
                   '</a:txBody><a:tcPr/></a:tc></a:tr></a:tbl>')
        uri = NS['a'] + '/table'
    return ('<p:graphicFrame><p:nvGraphicFramePr><p:cNvPr id="4" name="Data"/>'
            '<p:cNvGraphicFramePr/><p:nvPr/></p:nvGraphicFramePr>'
            '<p:xfrm><a:off x="100" y="200"/><a:ext cx="500" cy="500"/></p:xfrm>'
            f'<a:graphic><a:graphicData uri="{uri}">{content}</a:graphicData></a:graphic></p:graphicFrame>')


def group(content):
    return ('<p:grpSp><p:nvGrpSpPr><p:cNvPr id="8" name="Flow"/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
            '<p:grpSpPr><a:xfrm><a:off x="100" y="200"/><a:ext cx="600" cy="400"/>'
            '<a:chOff x="10" y="20"/><a:chExt cx="300" cy="200"/></a:xfrm></p:grpSpPr>'
            f'{content}</p:grpSp>')


def package(path, slide_contents, *, order=None, notes=None, slide_list=True):
    """Purpose-built OOXML fixtures: audit content/geometry, not OPC conformance."""
    order = list(slide_contents) if order is None else order
    namespaces = ' '.join(f'xmlns:{prefix}="{uri}"' for prefix, uri in NS.items())
    ids = ''.join(f'<p:sldId id="{256 + index}" r:id="rId{number}"/>' for index, number in enumerate(order))
    presentation = f'<p:presentation {namespaces}>'
    if slide_list:
        presentation += f'<p:sldIdLst>{ids}</p:sldIdLst>'
    presentation += '<p:sldSz cx="1000" cy="1000"/></p:presentation>'
    slide_rels = ''.join(f'<Relationship Id="rId{number}" Type="{NS["r"]}/slide" Target="slides/slide{number}.xml"/>' for number in order)
    parts = {'ppt/presentation.xml': presentation,
             'ppt/_rels/presentation.xml.rels': f'<Relationships xmlns="{REL_NS}">{slide_rels}</Relationships>'}
    for number, content in slide_contents.items():
        parts[f'ppt/slides/slide{number}.xml'] = f'<p:sld {namespaces}><p:cSld><p:spTree>{content}</p:spTree></p:cSld></p:sld>'
        rels = ''
        if notes is not None and number in notes:
            note = text_shape(notes[number], role='body') + text_shape(str(number), role='sldNum')
            parts[f'ppt/notesSlides/notesSlide{number}.xml'] = f'<p:notes {namespaces}><p:cSld><p:spTree>{note}</p:spTree></p:cSld></p:notes>'
            rels += f'<Relationship Id="notes1" Type="{NS["r"]}/notesSlide" Target="../notesSlides/notesSlide{number}.xml"/>'
        parts[f'ppt/slides/_rels/slide{number}.xml.rels'] = f'<Relationships xmlns="{REL_NS}">{rels}</Relationships>'
    with ZipFile(path, 'w', ZIP_DEFLATED) as archive:
        for name, content in parts.items():
            archive.writestr(name, content.encode('utf-8'))
    return path


class SlideQualityTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.directory = Path(temp.name)

    def inspect(self, content, **options):
        file = package(self.directory / 'deck.pptx', {1: content})
        report = quality.audit(file, **options)
        self.assertTrue(report['audit_complete'], report['errors'])
        return report['slides'][0]

    def codes(self, slide):
        return {warning['code'] for warning in slide['warnings']}

    def test_long_explanatory_text_warns_but_no_default_total_ceiling(self):
        slide = self.inspect(text_shape('解释' * 200))
        self.assertEqual(slide['text_characters']['body'], 400)
        self.assertEqual(slide['longest_body_paragraph_characters'], 400)
        self.assertIn('long_body_paragraph', self.codes(slide))
        self.assertNotIn('body_text_budget_review', self.codes(slide))
        configured = self.inspect(text_shape('解释' * 200), max_body_chars=300)
        self.assertIn('body_text_budget_review', self.codes(configured))

    def test_table_data_separate_from_non_table_body_and_small_font(self):
        slide = self.inspect(graphic('table', '1234567890' * 100) + text_shape('结论成立'))
        self.assertEqual(slide['text_characters']['table'], 1000)
        self.assertEqual(slide['text_characters']['body'], 4)
        self.assertEqual(slide['object_counts']['tables'], 1)
        self.assertNotIn('long_body_paragraph', self.codes(slide))
        self.assertNotIn('small_body_font', self.codes(slide))

    def test_title_footer_and_notes_do_not_inflate_body(self):
        content = (text_shape('报告标题', role='title') + text_shape('来源与页码', role='ftr') +
                   text_shape('核心结论'))
        path = package(self.directory / 'notes.pptx', {1: content}, notes={1: '解释' * 300})
        slide = quality.audit(path)['slides'][0]
        self.assertEqual(slide['text_characters'], {'body': 4, 'title': 4, 'footer': 5, 'table': 0})
        self.assertEqual(slide['notes_characters'], 600)
        self.assertNotIn('long_body_paragraph', self.codes(slide))
        self.assertNotIn('missing_notes_text', self.codes(slide))

    def test_notes_page_number_alone_does_not_count_as_script(self):
        path = package(self.directory / 'empty-notes.pptx', {1: text_shape('结论')}, notes={1: ''})
        slide = quality.audit(path)['slides'][0]
        self.assertEqual(slide['notes_characters'], 0)
        self.assertIn('missing_notes_text', self.codes(slide))

    def test_chart_and_picture_overlap_is_counted_once(self):
        slide = self.inspect(picture() + graphic('chart'))
        self.assertEqual(slide['object_counts']['pictures'], 1)
        self.assertEqual(slide['object_counts']['native_charts'], 1)
        self.assertEqual(slide['media_and_tables_geometry']['object_count'], 2)
        self.assertEqual(slide['media_and_tables_geometry']['known_bounds_union_ratio'], .25)
        self.assertTrue(slide['media_and_tables_geometry']['all_objects_measured'])
        self.assertNotIn('small_media_bounds_review', self.codes(slide))

    def test_partial_overlap_and_off_canvas_clipping(self):
        slide = self.inspect(picture(0, 0, 600, 500) + picture(400, 0, 800, 500))
        self.assertEqual(slide['geometry']['pictures']['known_bounds_union_ratio'], .5)
        self.assertAlmostEqual(quality.union_area([(0, 0, 5, 5), (2, 2, 7, 7)]), 41)

    def test_group_translation_and_scale_are_applied(self):
        slide = self.inspect(group(picture(10, 20, 100, 50)))
        self.assertEqual(slide['geometry']['pictures']['known_bounds_union_ratio'], .02)

    def test_unmeasurable_rotated_media_does_not_create_fake_total_area(self):
        slide = self.inspect(picture(width=100, height=100) + picture(rotation=600000))
        geometry = slide['media_and_tables_geometry']
        self.assertEqual(geometry['known_bounds_union_ratio'], .01)
        self.assertEqual(geometry['unmeasured_object_count'], 1)
        self.assertFalse(geometry['all_objects_measured'])
        self.assertIn('partial_geometry', self.codes(slide))
        self.assertNotIn('small_media_bounds_review', self.codes(slide))

    def test_inherited_geometry_remains_unknown(self):
        content = picture().replace(transform(100, 200, 500, 500), '')
        slide = self.inspect(content)
        self.assertIsNone(slide['geometry']['pictures']['known_bounds_union_ratio'])
        self.assertEqual(slide['geometry']['pictures']['unmeasured_object_count'], 1)

    def test_presentation_order_is_authoritative(self):
        path = package(self.directory / 'order.pptx', {1: text_shape('一'), 10: text_shape('十'), 2: text_shape('二')}, order=[10, 2, 1])
        report = quality.audit(path)
        self.assertEqual([s['slide_part'] for s in report['slides']],
                         ['ppt/slides/slide10.xml', 'ppt/slides/slide2.xml', 'ppt/slides/slide1.xml'])
        self.assertEqual([s['slide_number'] for s in report['slides']], [1, 2, 3])

    def test_missing_slide_list_falls_back_to_numeric_not_lexical_order(self):
        path = package(self.directory / 'fallback.pptx', {10: text_shape('十'), 2: text_shape('二'), 1: text_shape('一')}, slide_list=False)
        report = quality.audit(path)
        self.assertEqual([s['slide_part'] for s in report['slides']],
                         ['ppt/slides/slide1.xml', 'ppt/slides/slide2.xml', 'ppt/slides/slide10.xml'])
        self.assertIn('numeric_part_order_fallback', self.codes(report))

    def test_flow_shapes_are_reported_as_candidates_without_semantic_claims(self):
        content = text_shape('判断条件').replace('txBox="1"', '').replace('</p:spPr>', '<a:prstGeom prst="diamond"/></p:spPr>')
        slide = self.inspect(content)
        self.assertEqual(slide['object_counts']['native_shape_candidates'], 1)
        warning = next(w for w in slide['warnings'] if w['code'] == 'native_visual_review')
        self.assertIn('1 个原生形状候选', warning['message'])

    def test_unknown_fonts_not_guessed_and_explicit_small_font_warns(self):
        unknown = self.inspect(text_shape('字号继承', size=None))
        self.assertIsNone(unknown['body_minimum_known_font_pt'])
        self.assertEqual(unknown['body_unknown_font_characters'], 4)
        self.assertNotIn('small_body_font', self.codes(unknown))
        small = self.inspect(text_shape('小字正文', size=1200))
        self.assertEqual(small['body_characters_below_font_threshold'], 4)
        self.assertIn('small_body_font', self.codes(small))

    def test_header_heuristic_preserves_subtitle_variables_and_bottom_conclusion(self):
        content = (text_shape('机制标题', y=20, height=60, size=2800) +
                   text_shape('需要保留的图注', y=100, height=50, size=1550) +
                   text_shape('I_t + g', x=850, y=30, width=100, height=40, size=1600) +
                   text_shape('末行结论不能归页脚', y=930, height=50, size=1800) +
                   text_shape('01 / 03', x=850, y=950, width=100, height=20, size=1000))
        slide = self.inspect(content)
        self.assertEqual(slide['text_characters']['title'], 4)
        self.assertEqual(slide['text_characters']['footer'], 5)
        objects = {o['text_preview']: o for o in slide['text_objects']}
        self.assertEqual(objects['需要保留的图注']['role'], 'body')
        self.assertEqual(objects['I_t + g']['role'], 'body')
        self.assertEqual(objects['末行结论不能归页脚']['role'], 'body')
        self.assertIn('不能仅凭此提示删字', next(w['message'] for w in slide['warnings'] if w['code'] == 'small_body_font'))

    def test_pptxgenjs_plain_text_rectangle_not_counted_as_flow_shape(self):
        content = text_shape('标签').replace('txBox="1"', '').replace('</p:spPr>',
                  '<a:prstGeom prst="rect"/><a:noFill/><a:ln/></p:spPr>')
        slide = self.inspect(content)
        self.assertEqual(slide['object_counts']['native_shape_candidates'], 0)
        self.assertEqual(slide['text_characters']['body'], 2)

    def test_line_geometry_is_a_connector_candidate(self):
        content = text_shape('').replace('txBox="1"', '').replace('</p:spPr>',
                  '<a:prstGeom prst="line"/><a:noFill/><a:ln><a:solidFill><a:srgbClr val="111111"/></a:solidFill></a:ln></p:spPr>')
        slide = self.inspect(content)
        self.assertEqual(slide['object_counts']['connectors'], 1)
        self.assertEqual(slide['object_counts']['native_shape_candidates'], 0)

    def test_native_equation_glyphs_remain_in_body_text_with_unknown_font(self):
        content = text_shape('placeholder').replace('<a:r><a:rPr sz="2200"/><a:t>placeholder</a:t></a:r>',
                  '<m:oMath><m:r><m:t>S=</m:t></m:r><m:sSub><m:e><m:r><m:t>αS</m:t></m:r></m:e>'
                  '<m:sub><m:r><m:t>global</m:t></m:r></m:sub></m:sSub></m:oMath>')
        slide = self.inspect(content)
        self.assertEqual(slide['text_characters']['body'], 10)
        self.assertEqual(slide['body_unknown_font_characters'], 10)
        self.assertEqual(slide['text_objects'][0]['text_preview'], 'S=αSglobal')
        self.assertEqual(slide['text_objects'][0]['native_math_expressions'], 1)
        self.assertNotIn('small_body_font', self.codes(slide))

    def test_consecutive_layout_risk_respects_display_order(self):
        path = package(self.directory / 'repeat.pptx', {1: text_shape('方法'), 2: text_shape('结果'), 3: text_shape('结论')})
        report = quality.audit(path)
        warnings = [w for w in report['warnings'] if w['code'] == 'repeated_layout_review']
        self.assertEqual(len(warnings), 1)
        self.assertEqual(warnings[0]['slides'], [1, 2, 3])
        self.assertNotIn('_layout_signature', report['slides'][0])

    def test_cli_warnings_do_not_block_and_json_is_written(self):
        path = package(self.directory / 'cli.pptx', {1: text_shape('解释' * 150)})
        output = self.directory / 'qa' / 'quality.json'
        completed = subprocess.run([sys.executable, str(ROOT / 'scripts/audit_slide_quality.py'),
                                    str(path), '--report', str(output)], capture_output=True)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        report = json.loads(output.read_text(encoding='utf-8'))
        self.assertTrue(report['audit_complete'])
        self.assertGreater(report['warning_count'], 0)
        self.assertEqual(json.loads(completed.stdout.decode('utf-8')), report)

    def test_unreadable_input_is_not_reported_as_success(self):
        report = quality.audit(self.directory / 'absent.pptx')
        self.assertFalse(report['audit_complete'])
        self.assertTrue(report['errors'])


if __name__ == '__main__':
    unittest.main()
