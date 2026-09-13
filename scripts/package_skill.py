#!/usr/bin/env python3
"""Build full-use or public-source ZIP; never include caches, Git internals or symlinks."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import argparse
import hashlib
import json

ROOT=Path(__file__).resolve().parents[1]
EXCLUDED={
    '.git','.hg','.svn','node_modules','__pycache__','.venv','venv',
    'dist','build','work','qa','tmp','temp','output','outputs',
    '.cache','.pytest_cache','.mypy_cache','.ruff_cache','.ipynb_checkpoints',
    '.codex','.idea','.vscode',
}
EXCLUDED_FILES={'.ds_store','thumbs.db','desktop.ini'}
DEFAULT_VERSION='1.0.0'  # Standalone skill fixtures may not have package.json.

def package_version(source: Path):
    metadata=source/'package.json'
    if not metadata.is_file():return DEFAULT_VERSION
    version=json.loads(metadata.read_text(encoding='utf-8')).get('version')
    if not isinstance(version,str) or not version.strip():raise ValueError('package.json must contain a non-empty version')
    return version

def package(source: Path, output: Path, variant: str):
    source=source.resolve();output=output.resolve()
    if output.exists():raise ValueError(f'Output exists: {output}')
    if output==source or source in output.parents:raise ValueError('Write the ZIP outside the skill directory')
    if not (source/'SKILL.md').is_file():raise ValueError('Missing SKILL.md')
    if variant not in {'full','github'}:raise ValueError(f'Unknown package variant: {variant}')
    version=package_version(source)
    if variant=='full':
        manifest=json.loads((source/'fonts/manifest.json').read_text(encoding='utf-8'))
        for item in manifest['fonts']:
            if not (source/'fonts'/item['filename']).is_file():raise ValueError(f"Full package requires font: {item['filename']}")
    records=[];files=[]
    for p in sorted(source.rglob('*')):
        rel=p.relative_to(source)
        if any(x.lower() in EXCLUDED for x in rel.parts) or p.is_symlink() or not p.is_file():continue
        if rel.as_posix()=='bundle-manifest.json':continue
        name=p.name.lower()
        if name in EXCLUDED_FILES or name=='.env' or name.startswith('.env.'):continue
        if name.endswith(('.pyc','.tmp','.log','.inspect.ndjson','.draft.pptx')):continue
        if variant=='github' and rel.parts[0]=='fonts' and p.suffix.lower() in {'.ttf','.otf','.ttc'}:continue
        # Hash the same snapshot that is written, even if a source file changes meanwhile.
        data=p.read_bytes();files.append((rel,data))
        records.append({'path':rel.as_posix(),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
    output.parent.mkdir(parents=True,exist_ok=True)
    with ZipFile(output,'w',ZIP_DEFLATED) as z:
        for rel,data in files:z.writestr(f'paper-loom/{rel.as_posix()}',data)
        z.writestr('paper-loom/bundle-manifest.json',json.dumps({'variant':variant,'version':version,'files':records},ensure_ascii=False,indent=2))
    with ZipFile(output) as z:
        if z.testzip():raise RuntimeError('ZIP CRC validation failed')
    return {'path':str(output),'variant':variant,'file_count':len(files)+1,'bytes':output.stat().st_size,'sha256':hashlib.sha256(output.read_bytes()).hexdigest()}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--variant',choices=['full','github'],required=True)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    try:result=package(ROOT,args.output,args.variant)
    except (OSError,ValueError) as e:p.exit(2,f'ERROR: {e}\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))
