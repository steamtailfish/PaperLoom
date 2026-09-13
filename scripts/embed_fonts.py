#!/usr/bin/env python3
"""Embed editable/installable TrueType fonts in a PPTX without changing slides.

PPTX uses the Microsoft EOT font payload in ppt/fonts/*.fntdata, referenced
from p:embeddedFontLst.  This program keeps full, unmodified font data (no
subsetting) so the result remains editable, and rejects restricted fonts.

Usage:
  python scripts/embed_fonts.py input.pptx output.pptx [--font path/to/font.ttf ...]
If --font is omitted, embeds FangSong_GB2312 and the four Times New Roman
faces from ../fonts. This checks technical fsType flags, not redistribution
permission. See fonts/README.md before publishing font files.

Format reference: https://www.w3.org/submissions/EOT/ (EOT version 0x10000).
"""
from __future__ import annotations
import argparse
import hashlib
import json
import struct
import sys
import tempfile
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile
from io import BytesIO
from lxml import etree as ET
from fontTools.ttLib import TTFont

P = 'http://schemas.openxmlformats.org/presentationml/2006/main'
R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
PKG = 'http://schemas.openxmlformats.org/package/2006/relationships'
CT = 'http://schemas.openxmlformats.org/package/2006/content-types'
FONT_REL = R + '/font'
PANOSE_KEYS = ('bFamilyType','bSerifStyle','bWeight','bProportion','bContrast',
               'bStrokeVariation','bArmStyle','bLetterForm','bMidline','bXHeight')


def english_name(font: TTFont, number: int, fallback: str = '') -> str:
    records = [n for n in font['name'].names if n.nameID == number]
    records.sort(key=lambda n: (n.platformID != 3 or n.langID != 0x409,
                                n.platformID != 1 or n.langID != 0))
    for n in records:
        try:
            value = n.toUnicode()
            if value: return value
        except (UnicodeError, LookupError):
            continue
    return fallback


def font_eot(path: Path) -> tuple[bytes, dict]:
    raw = path.read_bytes()
    font = TTFont(BytesIO(raw), lazy=False)
    if 'glyf' not in font:
        raise ValueError(f'{path}: this helper accepts TrueType outlines only')
    os2 = font['OS/2']
    fs_type = os2.fsType
    # Editable output: installable (no rights bits) or editable embedding.
    if (fs_type & 0x0200) or (fs_type & 0x000E) not in (0, 8):
        raise ValueError(f'{path}: font does not allow editable outline embedding (fsType={fs_type:#06x})')
    family = english_name(font, 1, path.stem)
    style = english_name(font, 2, 'Regular')
    panose = bytes(getattr(os2.panose, k) for k in PANOSE_KEYS)
    italic = int(bool(os2.fsSelection & 1))
    # This original font supports Chinese GB2312 and declares codepage bit 18.
    cp1 = getattr(os2, 'ulCodePageRange1', 0)
    charset = 134 if cp1 & (1 << 18) else 1
    fixed = struct.pack('<4I10sBBIHH11I', 0, len(raw), 0x00010000, 0,
                        panose, charset, italic, os2.usWeightClass,
                        fs_type, 0x504C,
                        os2.ulUnicodeRange1, os2.ulUnicodeRange2,
                        os2.ulUnicodeRange3, os2.ulUnicodeRange4,
                        cp1, getattr(os2, 'ulCodePageRange2', 0),
                        font['head'].checkSumAdjustment, 0, 0, 0, 0)
    # Every name is UTF-16LE and is preceded by zero padding and byte length.
    names = b''
    for value in (family, style, english_name(font, 5, 'Version 1.0'),
                  english_name(font, 4, family)):
        encoded = value.encode('utf-16le')
        if len(encoded) > 65535:
            raise ValueError('Font name exceeds EOT name length limit')
        names += struct.pack('<HH', 0, len(encoded)) + encoded
    eot = fixed + names + raw
    eot = struct.pack('<I', len(eot)) + eot[4:]
    # Validate the actual payload before putting it in the document.
    assert struct.unpack_from('<I', eot, 0)[0] == len(eot)
    assert struct.unpack_from('<H', eot, 34)[0] == 0x504C
    assert eot[-len(raw):] == raw
    slot = ('boldItalic' if italic and os2.usWeightClass >= 600 else
            'italic' if italic else 'bold' if os2.usWeightClass >= 600 else 'regular')
    return eot, dict(family=family, style=style, slot=slot, fsType=fs_type,
                     charset=charset, panose=panose.hex().upper(),
                     sha256=hashlib.sha256(raw).hexdigest(), font_bytes=len(raw),
                     embedded_bytes=len(eot))


def xml(data: bytes) -> ET._Element:
    return ET.fromstring(data, ET.XMLParser(remove_blank_text=False))


def serialize(root: ET._Element) -> bytes:
    return ET.tostring(root, encoding='UTF-8', xml_declaration=True, standalone=True)


SLOT_ORDER = {'regular': 0, 'bold': 1, 'italic': 2, 'boldItalic': 3}


def embed(src: Path, dest: Path, fonts: list[Path]) -> dict:
    src, dest = Path(src), Path(dest)
    if src.resolve() == dest.resolve():
        raise ValueError('Input and output must be different; the source is never overwritten')
    if dest.exists():
        raise FileExistsError(f'Output already exists; choose a new filename: {dest}')
    if not fonts:
        raise ValueError('At least one font is required')
    prepared = [font_eot(Path(path)) for path in fonts]
    prepared.sort(key=lambda item: (item[1]['family'], SLOT_ORDER[item[1]['slot']]))
    with ZipFile(src) as archive:
        if len(archive.namelist()) != len(set(archive.namelist())):
            raise ValueError('Input ZIP contains duplicate part names')
        payloads = {name: archive.read(name) for name in archive.namelist()}
    presentation = xml(payloads['ppt/presentation.xml'])
    rels = xml(payloads['ppt/_rels/presentation.xml.rels'])
    content_types = xml(payloads['[Content_Types].xml'])
    font_list = presentation.find(f'{{{P}}}embeddedFontLst')
    if font_list is None:
        font_list = ET.Element(f'{{{P}}}embeddedFontLst')
        before = {'custShowLst','photoAlbum','custDataLst','kinsoku',
                  'defaultTextStyle','modifyVerifier','extLst'}
        for index, child in enumerate(presentation):
            if ET.QName(child).localname in before:
                presentation.insert(index, font_list)
                break
        else:
            presentation.append(font_list)
    font_names = set(payloads)
    rel_ids = {rel.get('Id') for rel in rels}
    report = []
    for data, metadata in prepared:
        entry = next((e for e in font_list
                      if e.find(f'{{{P}}}font') is not None and
                      e.find(f'{{{P}}}font').get('typeface') == metadata['family']), None)
        if entry is None:
            entry = ET.SubElement(font_list, f'{{{P}}}embeddedFont')
            ET.SubElement(entry, f'{{{P}}}font', typeface=metadata['family'],
                          panose=metadata['panose'],
                          charset=str(metadata['charset'] if metadata['charset'] < 128
                                      else metadata['charset'] - 256))
        slot = entry.find(f"{{{P}}}{metadata['slot']}")
        if slot is not None:
            raise ValueError(f"{metadata['family']} {metadata['slot']} is already embedded")
        n = 1
        while f'ppt/fonts/font{n}.fntdata' in font_names:
            n += 1
        part = f'ppt/fonts/font{n}.fntdata'
        font_names.add(part)
        payloads[part] = data
        n = 1
        while f'rIdFontEmbedded{n}' in rel_ids:
            n += 1
        rel_id = f'rIdFontEmbedded{n}'
        rel_ids.add(rel_id)
        ET.SubElement(rels, f'{{{PKG}}}Relationship', Id=rel_id,
                      Type=FONT_REL, Target=part.removeprefix('ppt/'))
        ET.SubElement(entry, f"{{{P}}}{metadata['slot']}", {f'{{{R}}}id':rel_id})
        # CT_EmbeddedFont requires p:font, regular, bold, italic, boldItalic.
        # Input --font order is intentionally irrelevant.
        entry[:] = sorted(entry, key=lambda child: -1 if ET.QName(child).localname == 'font'
                          else SLOT_ORDER.get(ET.QName(child).localname, 99))
        metadata['xml_charset'] = metadata['charset'] if metadata['charset'] < 128 else metadata['charset'] - 256
        metadata['part'] = part
        report.append(metadata)
    if not any(child.get('Extension') == 'fntdata' for child in content_types):
        ET.SubElement(content_types, f'{{{CT}}}Default',
                      Extension='fntdata', ContentType='application/x-fontdata')
    presentation.set('embedTrueTypeFonts', '1')
    presentation.set('saveSubsetFonts', '0')
    payloads['ppt/presentation.xml'] = serialize(presentation)
    payloads['ppt/_rels/presentation.xml.rels'] = serialize(rels)
    payloads['[Content_Types].xml'] = serialize(content_types)
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = None
    try:
        with tempfile.NamedTemporaryFile(dir=dest.parent, suffix='.pptx', delete=False) as holder:
            tmp = Path(holder.name)
        with ZipFile(tmp, 'w', ZIP_DEFLATED) as archive:
            for name, value in payloads.items():
                archive.writestr(name, value)
        # Validate before publishing; all slide XML and media stay byte-identical.
        with ZipFile(src) as before, ZipFile(tmp) as after:
            unchanged = [n for n in before.namelist()
                         if n.startswith(('ppt/slides/', 'ppt/media/'))]
            if not all(before.read(n) == after.read(n) for n in unchanged):
                raise RuntimeError('Unexpected slide or media modification')
            if after.testzip() is not None:
                raise RuntimeError('Output ZIP integrity check failed')
        tmp.replace(dest)
    finally:
        if tmp is not None and tmp.exists():
            tmp.unlink()
    return {'input':str(src), 'output':str(dest), 'fonts':report,
            'unchanged_slide_and_media_parts':len(unchanged)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--font', action='append', type=Path)
    args = parser.parse_args()
    if args.input.resolve() == args.output.resolve():
        parser.error('Use a distinct output filename to preserve the original PPTX')
    default_dir = Path(__file__).resolve().parents[1] / 'fonts'
    defaults = [default_dir / name for name in ('仿宋_GB2312.ttf', 'TIMES.TTF', 'TIMESBD.TTF', 'TIMESI.TTF', 'TIMESBI.TTF')]
    print(json.dumps(embed(args.input, args.output, args.font or defaults),
                     ensure_ascii=False, indent=2))

if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, RuntimeError, ET.XMLSyntaxError) as error:
        print(f'ERROR: {error}', file=sys.stderr)
        raise SystemExit(1)
