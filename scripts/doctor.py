#!/usr/bin/env python3
"""Inspect portable dependencies and bundled fonts without installing anything."""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

def inspect():
    modules = {n: importlib.util.find_spec(n) is not None for n in ['fitz','pypdf','PIL','lxml','fontTools','yaml']}
    commands = {n: shutil.which(n) for n in ['node','npm','pandoc','soffice']}
    node_package = False
    if commands['node']:
        proc = subprocess.run([commands['node'],'-e',"require.resolve('pptxgenjs')"],cwd=ROOT,capture_output=True)
        node_package = proc.returncode == 0
    manifest = json.loads((ROOT/'fonts/manifest.json').read_text(encoding='utf-8'))
    fonts = []
    for f in manifest['fonts']:
        p=ROOT/'fonts'/f['filename']
        item={'file':f['filename'],'present':p.is_file()}
        if p.is_file():
            item['matches_supplied_version']=hashlib.sha256(p.read_bytes()).hexdigest()==f['sha256']
            if modules['fontTools']:
                from fontTools.ttLib import TTFont
                with TTFont(p) as font:
                    item['family']=sorted({n.toUnicode() for n in font['name'].names if n.nameID==1})
                    item['embedding_fsType']=font['OS/2'].fsType
        fonts.append(item)
    return {'python':sys.version.split()[0], 'python_modules':modules, 'commands':commands,
            'pptxgenjs_resolves':node_package,'fonts':fonts,
            'ready_for_bundled_example':all(modules.values()) and node_package and all(x['present'] for x in fonts),
            'native_equation_conversion_ready':bool(commands['pandoc']) and modules['lxml'],
            'pdf_preview_ready':modules['fitz'] and modules['PIL'],
            'pptx_preview_via_libreoffice_ready':bool(commands['soffice']) and modules['fitz'] and modules['PIL'],
            'notes':['No dependencies or fonts were installed.', 'The default evidence demo has no equations; Pandoc is required only when converting equations.', 'Without soffice, export PDF using an available presentation tool and run render_preview.py on it.', 'Neither dependency checks nor preview rendering are desktop Microsoft PowerPoint validation.', 'Other existing native PPTX builders can replace PptxGenJS.', 'A different licensed font version can have a different hash; review its family and license.']}

if __name__=='__main__':
    if hasattr(sys.stdout,'reconfigure'):sys.stdout.reconfigure(encoding='utf-8')
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--strict',action='store_true',help='Exit 2 unless all bundled-example dependencies and fonts exist')
    args=parser.parse_args();result=inspect()
    print(json.dumps(result,ensure_ascii=False,indent=2))
    raise SystemExit(2 if args.strict and not result['ready_for_bundled_example'] else 0)
