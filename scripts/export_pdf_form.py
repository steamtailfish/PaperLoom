#!/usr/bin/env python3
"""Export one native PDF Form XObject with its resources, never a page crop."""
import argparse
import hashlib
import json
from pathlib import Path

import fitz
from pypdf import PdfReader, PdfWriter
from pypdf.generic import DictionaryObject, NameObject, DecodedStreamObject, IndirectObject


def export_form(source, xref, output, page=None, dpi=180):
    source, output = Path(source), Path(output)
    if output.exists():
        raise ValueError('Output directory already exists; choose a new directory')
    if dpi < 36 or dpi > 600:
        raise ValueError('dpi must be between 36 and 600')
    reader = PdfReader(source)
    form = IndirectObject(xref, 0, reader).get_object()
    if form.get('/Subtype') != '/Form':
        raise ValueError('Selected object is not a Form XObject')
    with fitz.open(source) as original:
        occurrences = [i + 1 for i, p in enumerate(original)
                       if any(item[0] == xref for item in p.get_xobjects())]
    if page is not None and page not in occurrences:
        raise ValueError('Form is not referenced by the requested page')
    if not occurrences:
        raise ValueError('Form has no page occurrence')
    x0, y0, x1, y1 = map(float, form['/BBox'])
    a, b, c, d, e, f = map(float, form.get('/Matrix', [1, 0, 0, 1, 0, 0]))
    corners = [(a*x+c*y+e, b*x+d*y+f) for x, y in
               [(x0,y0), (x1,y0), (x0,y1), (x1,y1)]]
    left, bottom = min(p[0] for p in corners), min(p[1] for p in corners)
    width = max(p[0] for p in corners) - left
    height = max(p[1] for p in corners) - bottom
    if width <= 0 or height <= 0 or width * height * (dpi / 72)**2 > 80_000_000:
        raise ValueError('Invalid or excessive figure dimensions')
    writer = PdfWriter()
    canvas = writer.add_blank_page(width=width, height=height)
    cloned = form.clone(writer)
    canvas[NameObject('/Resources')] = DictionaryObject({NameObject('/XObject'):
        DictionaryObject({NameObject('/Figure'): cloned.indirect_reference})})
    content = DecodedStreamObject()
    content.set_data(f'q 1 0 0 1 {-left:.8f} {-bottom:.8f} cm /Figure Do Q'.encode())
    canvas[NameObject('/Contents')] = writer._add_object(content)
    output.mkdir(parents=True)
    writer.write(output / 'figure.pdf')
    with fitz.open(output / 'figure.pdf') as isolated:
        isolated[0].get_pixmap(dpi=dpi, alpha=False).save(output / 'figure.png')
        (output / 'figure.svg').write_text(isolated[0].get_svg_image(text_as_path=True), encoding='utf-8')
    manifest = {'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
        'xref': xref, 'pages': occurrences, 'form_bbox': [x0,y0,x1,y1],
        'form_matrix': [a,b,c,d,e,f], 'size_pt': [width,height],
        'route': 'native Form clone with dependent resources; PNG renders isolated Form PDF',
        'completeness_verified': False,
        'files': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in output.iterdir()}}
    (output / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('--xref', type=int, required=True)
    parser.add_argument('--page', type=int)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--dpi', type=int, default=180)
    args = parser.parse_args()
    try:
        print(json.dumps(export_form(args.input, args.xref, args.output, args.page, args.dpi), indent=2))
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(1, f'{exc}\n')


if __name__ == '__main__':
    main()
