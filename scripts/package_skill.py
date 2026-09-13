#!/usr/bin/env python3
"""Build full-use or public-source ZIP; never include caches, Git internals or symlinks."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import argparse
import hashlib
import json

ROOT=Path(__file__).resolve().parents[1]
EXCLUDED={'.git','node_modules','__pycache__','.venv','dist','build'}

def package(source: Path, output: Path, variant: str):
    source=source.resolve();output=output.resolve()
    if output.exists():raise ValueError(f'Output exists: {output}')
    if output==source or source in output.parents:raise ValueError('Write the ZIP outside the skill directory')
    if not (source/'SKILL.md').is_file():raise ValueError('Missing SKILL.md')
    if variant=='full':
        manifest=json.loads((source/'fonts/manifest.json').read_text(encoding='utf-8'))
        for item in manifest['fonts']:
            if not (source/'fonts'/item['filename']).is_file():raise ValueError(f"Full package requires font: {item['filename']}")
    records=[];paths=[]
    for p in sorted(source.rglob('*')):
        rel=p.relative_to(source)
        if any(x in EXCLUDED for x in rel.parts) or p.is_symlink() or not p.is_file():continue
        if p.name.endswith(('.pyc','.tmp','.inspect.ndjson','.draft.pptx')):continue
        if variant=='github' and rel.parts[0]=='fonts' and p.suffix.lower() in {'.ttf','.otf','.ttc'}:continue
        data=p.read_bytes();paths.append((p,rel))
        records.append({'path':rel.as_posix(),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
    output.parent.mkdir(parents=True,exist_ok=True)
    with ZipFile(output,'w',ZIP_DEFLATED) as z:
        for p,rel in paths:z.write(p,f'paper-loom/{rel.as_posix()}')
        z.writestr('paper-loom/bundle-manifest.json',json.dumps({'variant':variant,'version':'1.0.0','files':records},ensure_ascii=False,indent=2))
    with ZipFile(output) as z:
        if z.testzip():raise RuntimeError('ZIP CRC validation failed')
    return {'path':str(output),'variant':variant,'file_count':len(paths)+1,'bytes':output.stat().st_size,'sha256':hashlib.sha256(output.read_bytes()).hexdigest()}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--variant',choices=['full','github'],required=True)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    try:result=package(ROOT,args.output,args.variant)
    except (OSError,ValueError) as e:p.exit(2,f'ERROR: {e}\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))
