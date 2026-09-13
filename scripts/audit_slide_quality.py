#!/usr/bin/env python3
"""Inspect PPTX slide-content risks; this is not an aesthetic score or visual QA.

python scripts/audit_slide_quality.py final.pptx --report qa/slide-quality.json

Warnings never change the exit status. Total characters have no default ceiling:
a useful scientific table can contain more text than an uninformative slide.
Calibrate optional thresholds against the user's reference and inspect renders.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import posixpath
import re
import sys
from urllib.parse import unquote, urlsplit
from zipfile import BadZipFile, ZipFile

from lxml import etree as ET

NS = {
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'c': 'http://schemas.openxmlformats.org/drawingml/2006/chart',
    'm': 'http://schemas.openxmlformats.org/officeDocument/2006/math',
    'mc': 'http://schemas.openxmlformats.org/markup-compatibility/2006',
}
SLIDE_RE = re.compile(r'ppt/slides/slide(\d+)\.xml')
BOUNDARY = '风险提示，不是审美评分；审计完成或零告警均不代表高质量。必须另行渲染并逐页检查。'
LIMITATIONS = [
    '字符数为 slide XML 内 a:t/m:t 的非空白 Unicode 字符数，不是信息密度或认知负担；不含图片内文字、嵌入图表的标签、母版/版式文字。',
    '表格文字单独统计；正文标签、公式和术语仍可能计入非表格正文。公式仅计文本结点；原生公式预览不保留分式、上下标、根号或结构化括号，不能作为可还原的公式。长段落不能自动认定为散文或删减对象。',
    '标题/页脚先按本页占位符识别；无占位符时仅把顶部宽且显式字号至少 20 pt 的唯一候选当标题，底部页码或来源前缀当页脚。未解析版式/母版角色。每个文本对象报告分类依据和文字预览，其余保留正文。',
    '面积为显式位置对象的轴对齐边界框并集/整页面积，裁剪到画布；重叠去重。不是实际墨迹、证据面积、可读性或有效信息密度。',
    '支持群组的平移和缩放；缺少显式变换、旋转或翻转的对象不估面积。未解析母版/版式继承几何、自由形状轮廓、遮挡、透明度、隐藏状态、动画和图片内部留白。',
    '原生形状/连接线仅是流程图候选，装饰也可能被计入；显式无填充且无显式描边的文本框不算形状候选，线几何也计作连接线候选。缺少图片/图表不等于缺少视觉表达。各类别面积不能相加。',
    '字号只读取本页显式运行/段落默认字号；未解析主题、母版、版式、列表样式继承及自动缩放。未知字号不会猜测。',
    '未选择 AlternateContent 兼容分支；此类页面另行提示，文字可能含替代分支、嵌套对象可能漏计。',
    'notes 仅检查是否存在非页码/页眉页脚的文字；不评估讲稿的正确性、充分性或是否重复正文。此脚本也不代替 validate_pptx.py 的结构检查。',
]


def char_count(value):
    return len(re.sub(r'\s', '', value))


def paragraphs(element):
    return [''.join(p.xpath('.//a:t/text() | .//m:t/text()', namespaces=NS))
            for p in element.findall('.//a:p', NS)]


def resolve_target(source, target):
    parsed = urlsplit(target)
    if parsed.scheme or parsed.netloc:
        raise ValueError('External URI in an internal relationship')
    path = unquote(parsed.path)
    result = posixpath.normpath(path.lstrip('/') if path.startswith('/') else
                               posixpath.join(posixpath.dirname(source), path))
    if result == '..' or result.startswith('../'):
        raise ValueError('Relationship target escapes package root')
    return result


def relationships(archive, source):
    directory, filename = posixpath.split(source)
    name = posixpath.join(directory, '_rels', filename + '.rels')
    if name not in archive.namelist():
        return {}
    root = parse(archive.read(name))
    return {rel.get('Id'): (rel.get('Type', '').rsplit('/', 1)[-1],
                            resolve_target(source, rel.get('Target', '')))
            for rel in root if rel.get('TargetMode') != 'External'}


def parse(data):
    return ET.fromstring(data, ET.XMLParser(resolve_entities=False, no_network=True))


def union_area(rectangles):
    """Exact union of axis-aligned (left, top, right, bottom) rectangles."""
    xs = sorted({r[i] for r in rectangles for i in (0, 2)})
    total = 0.0
    for left, right in zip(xs, xs[1:]):
        intervals = sorted((r[1], r[3]) for r in rectangles
                           if r[0] < right and r[2] > left)
        length, end = 0.0, float('-inf')
        for top, bottom in intervals:
            length += max(0, bottom - max(top, end))
            end = max(end, bottom)
        total += (right - left) * length
    return total


def unsafe_transform(xfrm):
    return (xfrm.get('rot', '0') != '0' or
            any(xfrm.get(key, '0').lower() in ('1', 'true') for key in ('flipH', 'flipV')))


def pair(xfrm, child, keys):
    element = xfrm.find('a:' + child, NS)
    if element is None:
        raise ValueError('missing ' + child)
    return tuple(float(element.attrib[key]) for key in keys)


def group_transform(group, parent):
    """Return scale/translation in slide space, or None for unsupported geometry."""
    xfrm = group.find('p:grpSpPr/a:xfrm', NS)
    if parent is None or xfrm is None or unsafe_transform(xfrm):
        return None
    try:
        x, y = pair(xfrm, 'off', ('x', 'y'))
        w, h = pair(xfrm, 'ext', ('cx', 'cy'))
        child_x, child_y = pair(xfrm, 'chOff', ('x', 'y'))
        child_w, child_h = pair(xfrm, 'chExt', ('cx', 'cy'))
        if min(w, h, child_w, child_h) <= 0:
            return None
        sx, sy, tx, ty = parent
        return (sx * w / child_w, sy * h / child_h,
                tx + sx * (x - child_x * w / child_w),
                ty + sy * (y - child_y * h / child_h))
    except (ValueError, KeyError):
        return None


def bounds(shape, transform, slide_size):
    xfrm = shape.find('p:spPr/a:xfrm', NS)
    if xfrm is None:
        xfrm = shape.find('p:xfrm', NS)
    if transform is None or xfrm is None or unsafe_transform(xfrm):
        return None
    try:
        x, y = pair(xfrm, 'off', ('x', 'y'))
        w, h = pair(xfrm, 'ext', ('cx', 'cy'))
        if w < 0 or h < 0:
            return None
        sx, sy, tx, ty = transform
        left, top = tx + sx * x, ty + sy * y
        right, bottom = left + sx * w, top + sy * h
        sw, sh = slide_size
        return (max(0, min(sw, left)), max(0, min(sh, top)),
                max(0, min(sw, right)), max(0, min(sh, bottom)))
    except (ValueError, KeyError):
        return None


def shapes(tree, transform=(1, 1, 0, 0)):
    for child in tree:
        if not isinstance(child.tag, str):
            continue
        name = ET.QName(child).localname
        if name == 'grpSp':
            yield from shapes(child, group_transform(child, transform))
        elif name in ('sp', 'pic', 'graphicFrame', 'cxnSp'):
            yield child, transform


def inferred_title(tree, slide_size):
    """Select one prominent header, never every text box near the top edge."""
    candidates = []
    sw, sh = slide_size
    for shape, transform in shapes(tree):
        ph = shape.find('.//p:ph', NS)
        if ph is not None:
            if ph.get('type') in ('title', 'ctrTitle'):
                return None  # An explicit title makes geometric guessing unnecessary.
            continue
        if ET.QName(shape).localname != 'sp':
            continue
        box = bounds(shape, transform, slide_size)
        count = sum(char_count(p) for p in paragraphs(shape))
        if box is None or not 1 <= count <= 80:
            continue
        left, top, right, bottom = box
        fonts, unknown = font_samples(shape)
        if (top <= sh * .08 and bottom <= sh * .18 and right - left >= sw * .35
                and fonts and not unknown and min(pt for pt, _ in fonts) >= 20):
            candidates.append((min(pt for pt, _ in fonts), right - left, -top, shape))
    return max(candidates, key=lambda entry: entry[:3])[-1] if candidates else None


def text_role(shape, box, slide_size, title_candidate=None):
    ph = shape.find('.//p:ph', NS)
    if ph is not None:
        kind = ph.get('type', 'obj')
        if kind in ('title', 'ctrTitle'):
            return 'title', 'local_placeholder:' + kind
        if kind in ('ftr', 'hdr', 'sldNum', 'dt'):
            return 'footer', 'local_placeholder:' + kind
        return 'body', 'local_placeholder:' + kind
    text = ' '.join(paragraphs(shape)).strip()
    count = char_count(text)
    if box is not None:
        _, top, _, bottom = box
        height = bottom - top
        sh = slide_size[1]
        footer_text = (re.fullmatch(r'\d+(?:\s*[/／-]\s*\d+)?', text) is not None or
                       re.match(r'(?:来源|引用|参考|source\b|doi\b|https?://)', text, re.I) is not None)
        if top >= sh * .92 and height <= sh * .08 and count <= 80 and footer_text:
            return 'footer', 'position_and_footer_text_heuristic'
        if shape is title_candidate:
            return 'title', 'single_prominent_header_heuristic'
    return 'body', 'default_body'


def font_samples(shape):
    known, unknown = [], 0
    for paragraph in shape.findall('.//a:p', NS):
        default = paragraph.find('a:pPr/a:defRPr', NS)
        for run in paragraph:
            values = run.xpath('.//a:t/text() | .//m:t/text()', namespaces=NS)
            count = sum(char_count(value) for value in values)
            if not count:
                continue
            properties = run.find('a:rPr', NS)
            size = properties.get('sz') if properties is not None else None
            if size is None and default is not None:
                size = default.get('sz')
            try:
                points = float(size) / 100
                if points <= 0:
                    raise ValueError('nonpositive font')
                known.append((points, count))
            except (TypeError, ValueError):
                unknown += count
    return known, unknown


def area_metric(items, slide_area):
    known = [box for box in items if box is not None]
    return {'object_count': len(items), 'measured_object_count': len(known),
            'unmeasured_object_count': len(items) - len(known),
            'known_bounds_union_ratio': round(union_area(known) / slide_area, 6) if known else None,
            'all_objects_measured': len(known) == len(items)}


def notes_characters(archive, slide_part):
    note_parts = [target for kind, target in relationships(archive, slide_part).values()
                  if kind == 'notesSlide']
    total = 0
    for part in note_parts:
        root = parse(archive.read(part))
        for shape in root.findall('.//p:sp', NS):
            ph = shape.find('.//p:ph', NS)
            if ph is not None and ph.get('type') in ('sldNum', 'ftr', 'hdr', 'dt', 'sldImg'):
                continue
            total += sum(char_count(p) for p in paragraphs(shape))
    return total


def inspect_slide(archive, part, number, slide_size, config):
    root = parse(archive.read(part))
    tree = root.find('p:cSld/p:spTree', NS)
    if tree is None:
        raise ValueError(f'Missing shape tree: {part}')
    counts = Counter(pictures=0, native_charts=0, tables=0, smartart=0,
                     native_shape_candidates=0, connectors=0)
    boxes = {key: [] for key in counts}
    objects, signature = [], []
    role_characters = Counter(body=0, title=0, footer=0, table=0)
    body_paragraphs, body_fonts, unknown_font_chars = [], [], 0
    sw, sh = slide_size
    title_candidate = inferred_title(tree, slide_size)
    for shape, transform in shapes(tree):
        kind = ET.QName(shape).localname
        box = bounds(shape, transform, slide_size)
        category = None
        if kind == 'pic':
            category = 'pictures'
        elif kind == 'cxnSp':
            category = 'connectors'
        elif kind == 'graphicFrame':
            if shape.find('.//c:chart', NS) is not None:
                category = 'native_charts'
            elif shape.find('.//a:tbl', NS) is not None:
                category = 'tables'
            else:
                data = shape.find('.//a:graphicData', NS)
                if data is not None and 'diagram' in data.get('uri', ''):
                    category = 'smartart'
        elif kind == 'sp':
            properties = shape.find('p:nvSpPr/p:cNvSpPr', NS)
            geometry = shape.find('p:spPr/a:prstGeom', NS)
            has_geometry = (geometry is not None or
                            shape.find('p:spPr/a:custGeom', NS) is not None)
            line = shape.find('p:spPr/a:ln', NS)
            no_explicit_line = (line is None or len(line) == 0 or line.find('a:noFill', NS) is not None)
            plain_text_box = (shape.find('p:txBody', NS) is not None and
                              shape.find('p:spPr/a:noFill', NS) is not None and no_explicit_line)
            if geometry is not None and geometry.get('prst') in ('line', 'straightConnector1'):
                category = 'connectors'
            elif has_geometry and not plain_text_box and (properties is None or properties.get('txBox') not in ('1', 'true')):
                category = 'native_shape_candidates'
        if category:
            counts[category] += 1
            boxes[category].append(box)
        texts = paragraphs(shape)
        role, basis = ('table', 'native_table') if category == 'tables' else text_role(shape, box, slide_size, title_candidate)
        characters = sum(char_count(p) for p in texts)
        if characters:
            role_characters[role] += characters
            known_fonts, unknown_fonts = font_samples(shape)
            identity = shape.find('.//p:cNvPr', NS)
            objects.append({'name': identity.get('name', '') if identity is not None else '',
                            'role': role, 'classification_basis': basis,
                            'text_preview': ' | '.join(texts)[:160],
                            'native_math_expressions': len(shape.findall('.//m:oMath', NS)),
                            'characters': characters,
                            'longest_paragraph_characters': max(map(char_count, texts), default=0),
                            'minimum_known_font_pt': min((pt for pt, _ in known_fonts), default=None),
                            'unknown_font_characters': unknown_fonts,
                            'bounds_emu': list(box) if box is not None else None})
            if role == 'body':
                body_paragraphs.extend(char_count(p) for p in texts if char_count(p))
                body_fonts.extend(known_fonts)
                unknown_font_chars += unknown_fonts
        # Coarse geometry only; a warning asks whether the repeated organization
        # expresses the argument. It cannot tell whether repetition is useful.
        if box is not None and (category or (characters and role == 'body')):
            signature.append((category or 'body_text', *(round(v / dim * 20)
                              for v, dim in zip(box, (sw, sh, sw, sh)))))
    notes = notes_characters(archive, part)
    media_boxes = sum((boxes[k] for k in ('pictures', 'native_charts', 'tables', 'smartart')), [])
    result = {'slide_number': number, 'slide_part': part,
              'text_characters': dict(role_characters),
              'total_slide_xml_text_characters': sum(role_characters.values()),
              'body_paragraph_count': len(body_paragraphs),
              'longest_body_paragraph_characters': max(body_paragraphs, default=0),
              'body_paragraphs_above_threshold': sum(n > config['max_paragraph_chars'] for n in body_paragraphs),
              'body_characters_in_long_paragraphs': sum(n for n in body_paragraphs if n > config['max_paragraph_chars']),
              'body_minimum_known_font_pt': min((pt for pt, _ in body_fonts), default=None),
              'body_characters_below_font_threshold': sum(n for pt, n in body_fonts if pt < config['min_body_font_pt']),
              'body_unknown_font_characters': unknown_font_chars,
              'notes_characters': notes, 'object_counts': dict(counts),
              'geometry': {k: area_metric(v, sw * sh) for k, v in boxes.items()},
              'media_and_tables_geometry': area_metric(media_boxes, sw * sh),
              'text_objects': objects, 'warnings': [], '_layout_signature': sorted(signature)}
    warnings = result['warnings']
    def warn(code, message):
        warnings.append({'code': code, 'message': message})
    if root.find('.//mc:AlternateContent', NS) is not None:
        warn('alternate_content_review', '页面含未解析的兼容分支；文字和对象统计可能不完整或重复，请以渲染结果核对。')
    if result['body_paragraphs_above_threshold']:
        warn('long_body_paragraph', f"非表格正文有 {result['body_paragraphs_above_threshold']} 段超过 {config['max_paragraph_chars']} 字符；复核是否为长解释，需保留的数据、公式、标签不能机械删减。")
    ceiling = config['max_body_chars']
    if ceiling is not None and role_characters['body'] > ceiling:
        warn('body_text_budget_review', f'非表格正文 {role_characters["body"]} 字符，超过用户配置的 {ceiling}；与参考样本比较后判断，字符数不等于信息密度。')
    if result['body_characters_below_font_threshold']:
        warn('small_body_font', f"已知显式非表格正文中 {result['body_characters_below_font_threshold']} 字符小于 {config['min_body_font_pt']:g} pt，可能是变量、图注或来源；定位文字预览并渲染检查，不能仅凭此提示删字或统一放大。")
    media = result['media_and_tables_geometry']
    if not media['object_count']:
        warn('native_visual_review', f'未发现图片/原生图表/表格/SmartArt；有 {counts["native_shape_candidates"]} 个原生形状候选及 {counts["connectors"]} 条连接线候选，请人工检查是否已形成有效的流程、比较或推导。')
    elif media['all_objects_measured'] and media['known_bounds_union_ratio'] < config['min_media_area_ratio']:
        warn('small_media_bounds_review', '图片/图表/表格/SmartArt 的边界框并集较小；检查核心证据是否足够大。装饰图、流程图页和章节页可合理例外。')
    if any(metric['unmeasured_object_count'] for metric in result['geometry'].values()):
        warn('partial_geometry', '部分对象几何未知；已测边界框面积不代表整页视觉面积，请看渲染。')
    if not notes:
        warn('missing_notes_text', '未找到有效 notes 文字；检查讲解、条件和局限是否已有讲稿承接。封面等页面可合理例外。')
    return result


def audit(path, *, max_paragraph_chars=100, max_body_chars=None,
          min_body_font_pt=16, min_media_area_ratio=.12, repeat_layout_run=3):
    config = dict(max_paragraph_chars=max_paragraph_chars, max_body_chars=max_body_chars,
                  min_body_font_pt=min_body_font_pt, min_media_area_ratio=min_media_area_ratio,
                  repeat_layout_run=repeat_layout_run)
    report = {'file': str(path), 'audit_complete': False, 'boundary': BOUNDARY,
              'limitations': LIMITATIONS, 'thresholds': config, 'errors': [],
              'warnings': [], 'slides': []}
    try:
        with ZipFile(path) as archive:
            presentation = parse(archive.read('ppt/presentation.xml'))
            size = presentation.find('p:sldSz', NS)
            if size is None:
                raise ValueError('Missing explicit presentation slide size')
            slide_size = (float(size.attrib['cx']), float(size.attrib['cy']))
            if min(slide_size) <= 0:
                raise ValueError('Slide dimensions must be positive')
            rels = relationships(archive, 'ppt/presentation.xml')
            listed = presentation.findall('p:sldIdLst/p:sldId', NS)
            parts = []
            if listed:
                for entry in listed:
                    kind, part = rels[entry.get(f'{{{NS["r"]}}}id')]
                    if kind != 'slide':
                        raise ValueError('Presentation slide list references a non-slide part')
                    parts.append(part)
            else:
                parts = sorted((n for n in archive.namelist() if SLIDE_RE.fullmatch(n)),
                               key=lambda n: int(SLIDE_RE.fullmatch(n).group(1)))
                report['warnings'].append({'code': 'numeric_part_order_fallback',
                                           'message': '缺少放映页序，暂按 slide 文件名数字排序；先修复 PPTX 结构。'})
            if not parts:
                raise ValueError('No slides found')
            report['slide_size_emu'] = list(slide_size)
            report['slides'] = [inspect_slide(archive, part, i, slide_size, config)
                                for i, part in enumerate(parts, 1)]
        previous, start = None, 0
        for index, slide in enumerate(report['slides']):
            signature = slide.pop('_layout_signature')
            if not signature or signature != previous:
                start = index
            if signature and index - start + 1 == repeat_layout_run:
                report['warnings'].append({'code': 'repeated_layout_review',
                    'slides': list(range(start + 1, index + 2)),
                    'message': '这些连续页面的粗粒度对象位置相同；核对是否需要比较、流程、图表等不同信息结构。统一版式或连续实验页可能合理。'})
            previous = signature
        report['warning_count'] = len(report['warnings']) + sum(len(s['warnings']) for s in report['slides'])
        report['audit_complete'] = True
    except (OSError, BadZipFile, KeyError, ValueError, ET.XMLSyntaxError, RuntimeError) as exc:
        report['errors'].append(f'Cannot audit PPTX: {exc}')
    return report


def main():
    # Keep reports legible when Windows defaults to a legacy code page, including
    # math symbols and Chinese text. The report file is also always UTF-8.
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('--report', type=Path, help='Write the same JSON report to this path')
    parser.add_argument('--max-paragraph-chars', type=int, default=100,
                        help='Non-table body paragraph review threshold (default: 100)')
    parser.add_argument('--max-body-chars', type=int, default=None,
                        help='Optional non-table body character budget; DISABLED by default')
    parser.add_argument('--min-body-font-pt', type=float, default=16,
                        help='Explicit body font review threshold (default: 16)')
    parser.add_argument('--min-media-area-ratio', type=float, default=.12,
                        help='Known media/table bounding-box union review threshold (default: .12)')
    parser.add_argument('--repeat-layout-run', type=int, default=3,
                        help='Consecutive similar geometry count for review (default: 3)')
    args = parser.parse_args()
    if args.report and args.report.resolve() == args.input.resolve():
        parser.error('--report must not overwrite the PPTX being inspected')
    if (args.max_paragraph_chars <= 0 or args.min_body_font_pt <= 0 or
            args.repeat_layout_run < 2 or not 0 <= args.min_media_area_ratio <= 1 or
            (args.max_body_chars is not None and args.max_body_chars <= 0)):
        parser.error('Thresholds must be positive; area ratio must be 0..1; repeat count must be >=2')
    options = vars(args).copy()
    options.pop('input')
    options.pop('report')
    report = audit(args.input, **options)
    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(rendered + '\n', encoding='utf-8')
    print(rendered)
    raise SystemExit(0 if report['audit_complete'] else 1)


if __name__ == '__main__':
    main()
