#!/usr/bin/env python3
"""Copy this complete skill to a client directory without overwriting an existing skill."""
from pathlib import Path
import argparse
import shutil

ROOT=Path(__file__).resolve().parents[1]
EXCLUDED={'.git','node_modules','__pycache__','.venv','dist','build'}

def install(source: Path,dest: Path,dry_run=False):
    source=source.resolve();dest=dest.expanduser().resolve()
    if not (source/'SKILL.md').is_file():raise ValueError('Source must contain SKILL.md')
    if dest.exists():raise ValueError(f'Destination already exists; choose a new destination: {dest}')
    if dest==source or source in dest.parents:raise ValueError('Destination cannot be inside the source skill')
    if dry_run:return dest
    def ignore(folder,names):
        return [n for n in names if n in EXCLUDED or n.endswith(('.pyc','.tmp','.inspect.ndjson')) or (Path(folder)/n).is_symlink()]
    dest.parent.mkdir(parents=True,exist_ok=True)
    shutil.copytree(source,dest,ignore=ignore)
    return dest

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--dest',type=Path,default=Path.home()/'.agents/skills/paper-loom',help='Exact destination skill folder')
    p.add_argument('--dry-run',action='store_true')
    args=p.parse_args()
    try:
        target=install(ROOT,args.dest,args.dry_run)
    except (ValueError,OSError) as e:p.exit(2,f'ERROR: {e}\n')
    print(('Would copy skill to: ' if args.dry_run else 'Copied complete skill to: ')+str(target))
    print('Confirm PaperLoom in the client skill list. This script does not install Python/Node/Pandoc dependencies or register OS fonts.')
