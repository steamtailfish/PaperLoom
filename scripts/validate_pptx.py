#!/usr/bin/env python3
"""Check targeted PPTX packaging, font and native-equation invariants.

This is NOT full OOXML XSD validation and NOT a desktop PowerPoint opening test.
It deliberately works without Microsoft Office or internal presentation tools.

python scripts/validate_pptx.py final.pptx --expected-slides 8 --expected-math 3
python scripts/validate_pptx.py revised.pptx --compare previous.pptx --allow-changed-slides 2
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
from zipfile import ZipFile, BadZipFile
from lxml import etree as ET

NS = {
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'rel': 'http://schemas.openxmlformats.org/package/2006/relationships',
    'ct': 'http://schemas.openxmlformats.org/package/2006/content-types',
    'm': 'http://schemas.openxmlformats.org/officeDocument/2006/math',
    'a14': 'http://schemas.microsoft.com/office/drawing/2010/main',
    'mc': 'http://schemas.openxmlformats.org/markup-compatibility/2006',
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
}
SLIDE_RE = re.compile(r'ppt/slides/slide(\d+)\.xml')
SLIDE_PART_RE = re.compile(r'ppt/slides/(?:_rels/)?slide(\d+)\.xml(?:\.rels)?')
BOUNDARY = '不是桌面 Office 打开验证；不是全 XSD 验证。Checks are targeted structural checks only.'


def relationship_source(name: str) -> str:
    if name == '_rels/.rels':
        return ''
    directory, basename = posixpath.split(name)
    if posixpath.basename(directory) != '_rels' or not basename.endswith('.rels'):
        raise ValueError(f'Invalid relationship part path: {name}')
    return posixpath.join(posixpath.dirname(directory), basename[:-5])


def resolve_target(source: str, target: str) -> str:
    """Resolve OPC relative or package-absolute Target URIs, preserving fragments."""
    parsed = urlsplit(target)
    if parsed.scheme or parsed.netloc:
        raise ValueError(f'Internal Target is an external URI: {target}')
    path = unquote(parsed.path)
    if not path:
        return source
    resolved = posixpath.normpath(path.lstrip('/') if path.startswith('/') else
                                 posixpath.join(posixpath.dirname(source), path))
    if resolved == '..' or resolved.startswith('../'):
        raise ValueError(f'Target escapes package root: {target}')
    return resolved


def validate(path: Path, expected_slides=None, expected_math=None,
             compare: Path | None = None, allowed_slides=()) -> dict:
    path = Path(path)
    errors, warnings = [], []
    report = {'file': str(path), 'ok': False, 'validation_boundary': BOUNDARY,
              'errors': errors, 'warnings': warnings}
    try:
        with ZipFile(path) as archive:
            names = archive.namelist()
            duplicates = [n for n, count in Counter(names).items() if count > 1]
            if duplicates:
                errors.append(f'Duplicate ZIP entries: {duplicates}')
            bad = archive.testzip()
            if bad:
                errors.append(f'ZIP CRC failure: {bad}')
            payloads = {n: archive.read(n) for n in names if not n.endswith('/')}
    except (OSError, BadZipFile, RuntimeError) as exc:
        errors.append(f'Cannot read PPTX ZIP: {exc}')
        return report
    for required in ('[Content_Types].xml', '_rels/.rels', 'ppt/presentation.xml',
                     'ppt/_rels/presentation.xml.rels'):
        if required not in payloads:
            errors.append(f'Missing required part: {required}')
    roots = {}
    parser = ET.XMLParser(resolve_entities=False, no_network=True)
    for name, data in payloads.items():
        if name.endswith(('.xml', '.rels')):
            try:
                roots[name] = ET.fromstring(data, parser)
            except ET.XMLSyntaxError as exc:
                errors.append(f'Malformed XML {name}: {exc}')
    relationships = {}
    relationship_count = 0
    for name, root in roots.items():
        if not name.endswith('.rels'):
            continue
        try:
            source = relationship_source(name)
        except ValueError as exc:
            errors.append(str(exc)); continue
        if source and source not in payloads:
            errors.append(f'Relationship owner does not exist: {name} -> {source}')
        ids = {}
        for rel in root:
            rid, target = rel.get('Id'), rel.get('Target')
            relationship_count += 1
            if not rid or rid in ids:
                errors.append(f'Missing/duplicate relationship ID in {name}: {rid}')
            ids[rid] = rel
            if not target:
                errors.append(f'Missing relationship Target in {name}: {rid}')
                continue
            if rel.get('TargetMode') == 'External':
                continue
            try:
                resolved = resolve_target(source, target)
                if resolved not in payloads:
                    errors.append(f'Broken relationship {name} {rid}: {target} -> {resolved}')
            except ValueError as exc:
                errors.append(f'{name} {rid}: {exc}')
        relationships[source] = ids
    # Empirical desktop compatibility warning, not an OOXML XSD constraint:
    # PowerPoint 16.0 rejected the PptxGenJS 4.0.1 demo with 0x80070570 when a
    # correctly ordered notesMaster and the slide master shared a theme. A
    # byte-identical dedicated theme fixed loading and preserved all notes.
    themes_by_owner = {'sldMaster': set(), 'notesMaster': set()}
    for source, rels in relationships.items():
        owner = roots.get(source)
        if owner is None or not isinstance(owner.tag, str):
            continue
        kind = ET.QName(owner).localname
        if kind not in themes_by_owner or ET.QName(owner).namespace != NS['p']:
            continue
        for rel in rels.values():
            if (rel.get('Type', '').rsplit('/', 1)[-1] == 'theme' and
                    rel.get('TargetMode') != 'External' and rel.get('Target')):
                try:
                    themes_by_owner[kind].add(resolve_target(source, rel.get('Target')))
                except ValueError:
                    pass  # Already reported during relationship validation.
    shared_themes = sorted(themes_by_owner['sldMaster'] & themes_by_owner['notesMaster'])
    report['shared_notes_slide_theme_parts'] = shared_themes
    if shared_themes:
        warnings.append(f'Desktop compatibility risk: notes master and slide master share theme parts {shared_themes}. '
                        'PowerPoint 16.0 rejected this arrangement in the PptxGenJS 4.0.1 demo; '
                        'use a dedicated notes theme and verify desktop opening. This is not an XSD error.')
    for name, root in roots.items():
        if name.endswith('.rels'):
            continue
        ids = relationships.get(name, {})
        for element in root.iter():
            for attr, value in element.attrib.items():
                if attr in {f'{{{NS["r"]}}}id', f'{{{NS["r"]}}}embed', f'{{{NS["r"]}}}link'} and value not in ids:
                    errors.append(f'Unresolved relationship attribute in {name}: {value}')
            ignorable = element.get(f'{{{NS["mc"]}}}Ignorable', '').split()
            for prefix in ignorable:
                if prefix not in element.nsmap:
                    errors.append(f'Unbound mc:Ignorable prefix in {name}: {prefix}')
        # Targeted CT_TextParagraph check: pPr is optional, unique, and first.
        # This catches generators that append a second pPr after the text runs.
        for paragraph in root.findall('.//a:p', NS):
            pprs = paragraph.findall('a:pPr', NS)
            location = root.getroottree().getpath(paragraph)
            if len(pprs) > 1:
                errors.append(f'Duplicate a:pPr in DrawingML paragraph {name}:{location}; at most one is allowed')
            if pprs and list(paragraph).index(pprs[0]) != 0:
                errors.append(f'a:pPr must precede runs and be the first paragraph child: {name}:{location}')
        shape_ids = root.xpath('//p:cNvPr/@id', namespaces=NS)
        repeated = [sid for sid, count in Counter(shape_ids).items() if count > 1]
        if repeated:
            errors.append(f'Duplicate cNvPr shape IDs in {name}: {repeated}')
        font_tags = {f'{{{NS["a"]}}}{local}' for local in ('latin', 'ea', 'cs', 'sym')}
        font_tags.add(f'{{{NS["p"]}}}font')
        for element in root.iter():
            if element.tag not in font_tags or element.get('charset') is None:
                continue
            charset = element.get('charset')
            try:
                valid = re.fullmatch(r'[+-]?\d+', charset) is not None and -128 <= int(charset) <= 127
            except (ValueError, TypeError):
                valid = False
            if not valid:
                errors.append(f'Invalid signed-byte font charset in {name}: {charset}; expected -128..127')
    ct = roots.get('[Content_Types].xml')
    if ct is not None:
        defaults = {e.get('Extension'): e.get('ContentType') for e in ct if ET.QName(e).localname == 'Default'}
        overrides = {unquote(e.get('PartName', '')).lstrip('/'): e.get('ContentType')
                     for e in ct if ET.QName(e).localname == 'Override'}
        for name in payloads:
            if name == '[Content_Types].xml':
                continue
            if name not in overrides and name.rsplit('.', 1)[-1] not in defaults:
                errors.append(f'No ContentType for package part: {name}')
        for name in overrides:
            if name not in payloads:
                errors.append(f'ContentType Override points to missing part: {name}')
    slides = sorted(n for n in roots if SLIDE_RE.fullmatch(n))
    presentation = roots.get('ppt/presentation.xml')
    slide_count = len(slides)
    if presentation is not None:
        # ECMA-376 CT_Presentation uses this ordered sequence. Only known core
        # children are checked here; this is not a replacement for full XSD/MC.
        presentation_order = [
            'sldMasterIdLst', 'notesMasterIdLst', 'handoutMasterIdLst',
            'sldIdLst', 'sldSz', 'notesSz', 'smartTags', 'embeddedFontLst',
            'custShowLst', 'photoAlbum', 'custDataLst', 'kinsoku',
            'defaultTextStyle', 'modifyVerifier', 'extLst',
        ]
        core_children = [ET.QName(child).localname for child in presentation
                         if isinstance(child.tag, str) and
                         ET.QName(child).namespace == NS['p'] and
                         ET.QName(child).localname in presentation_order]
        if core_children != sorted(core_children, key=presentation_order.index):
            errors.append(f'Invalid presentation child order in ppt/presentation.xml: {core_children}; '
                          'notesMasterIdLst must precede sldIdLst, and core children must follow CT_Presentation sequence')
        repeated_core = [tag for tag, count in Counter(core_children).items() if count > 1]
        if repeated_core:
            errors.append(f'Duplicate presentation core children: {repeated_core}')
        listed = presentation.findall('p:sldIdLst/p:sldId', NS)
        slide_count = len(listed)
        sids = [e.get('id') for e in listed]
        if len(sids) != len(set(sids)):
            errors.append('Duplicate presentation slide IDs')
        if slide_count != len(slides):
            errors.append(f'Presentation lists {slide_count} slides but package has {len(slides)} slide parts')
        slot_order = ['font', 'regular', 'bold', 'italic', 'boldItalic']
        for entry in presentation.findall('p:embeddedFontLst/p:embeddedFont', NS):
            tags = [ET.QName(child).localname for child in entry]
            if not tags or tags[0] != 'font' or any(tag not in slot_order for tag in tags):
                errors.append(f'Invalid embedded-font children: {tags}')
            elif len(tags) != len(set(tags)) or tags != sorted(tags, key=slot_order.index):
                errors.append(f'Embedded-font slot order must be font, regular, bold, italic, boldItalic: {tags}')
    maths = 0
    objects = 0
    math_slides = []
    for name in slides:
        root = roots[name]
        wrappers = root.findall('.//a14:m', NS)
        expressions = root.findall('.//m:oMath', NS)
        objects += len(wrappers)
        maths += len(expressions)
        if wrappers:
            math_slides.append(name)
        for wrapper in wrappers:
            if wrapper.getparent().tag != f'{{{NS["a"]}}}p':
                errors.append(f'a14:m must be inside a:p: {name}')
            if not wrapper.findall('.//m:oMath', NS):
                errors.append(f'Empty native math object: {name}')
            if wrapper.findall('.//w:rPr', NS):
                errors.append(f'Word run properties remain inside PowerPoint math: {name}')
            ignorable = set()
            for ancestor in [wrapper, *wrapper.iterancestors()]:
                for prefix in ancestor.get(f'{{{NS["mc"]}}}Ignorable', '').split():
                    ignorable.add(ancestor.nsmap.get(prefix))
            if NS['a14'] not in ignorable:
                errors.append(f'Native math extension is missing inherited mc:Ignorable a14: {name}')
        for expression in expressions:
            if not any(a.tag == f'{{{NS["a14"]}}}m' for a in expression.iterancestors()):
                errors.append(f'OMML expression is not inside a14:m: {name}')
        for paragraph in root.findall('.//a:p', NS):
            text = ''.join(paragraph.xpath('.//a:t/text()', namespaces=NS))
            tokens = re.findall(r'\[\[EQ_[^\]]+\]\]', text)
            if tokens:
                errors.append(f'Unconverted equation placeholders in {name}: {tokens}')
    if expected_slides is not None and slide_count != expected_slides:
        errors.append(f'Expected {expected_slides} slides, found {slide_count}')
    if expected_math is not None and maths != expected_math:
        errors.append(f'Expected {expected_math} OMML expressions, found {maths}')
    if compare:
        allowed = set(allowed_slides)
        with ZipFile(compare) as archive:
            old = {n: archive.read(n) for n in archive.namelist() if not n.endswith('/')}
        changed = sorted(n for n in set(old) | set(payloads) if old.get(n) != payloads.get(n))
        report['changed_parts'] = changed
        report['allowed_changed_slide_numbers'] = sorted(allowed)
        for name in changed:
            match = SLIDE_PART_RE.fullmatch(name)
            if match and int(match.group(1)) not in allowed:
                errors.append(f'Non-target slide part changed: {name}')
    report.update(slides=slide_count, native_math_objects=objects, native_math_expressions=maths,
                  slides_with_math=math_slides, xml_parts=len(roots), relationships=relationship_count)
    report['ok'] = not errors
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('--expected-slides', type=int)
    parser.add_argument('--expected-math', type=int, help='Expected count of m:oMath expressions')
    parser.add_argument('--report', type=Path)
    parser.add_argument('--compare', type=Path, help='Previous file; check all non-target slide XML/relations remain identical')
    parser.add_argument('--allow-changed-slides', type=int, nargs='*', default=[], metavar='N')
    args = parser.parse_args()
    if args.report and args.report.resolve() in {args.input.resolve(), args.compare.resolve() if args.compare else args.input.resolve()}:
        parser.error('--report must not overwrite a PPTX being inspected')
    if args.allow_changed_slides and args.compare is None:
        parser.error('--allow-changed-slides requires --compare')
    try:
        report = validate(args.input, args.expected_slides, args.expected_math, args.compare, args.allow_changed_slides)
    except (OSError, BadZipFile, ValueError) as error:
        print(f'ERROR: {error}', file=sys.stderr)
        raise SystemExit(1)
    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(rendered + '\n', encoding='utf-8')
    print(rendered)
    raise SystemExit(0 if report['ok'] else 1)


if __name__ == '__main__':
    main()
