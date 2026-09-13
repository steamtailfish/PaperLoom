from pathlib import Path
from zipfile import ZipFile
import importlib.util
import hashlib
import json
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
def module(name):
    s=importlib.util.spec_from_file_location(name,ROOT/'scripts'/f'{name}.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
pack=module('package_skill');installer=module('install_skill')

class PackagingTest(unittest.TestCase):
    def make_source(self,base):
        source=base/'src';source.mkdir()
        (source/'SKILL.md').write_text('test',encoding='utf-8');(source/'fonts').mkdir()
        (source/'fonts/one.ttf').write_bytes(b'not-a-real-font')
        (source/'fonts/manifest.json').write_text(json.dumps({'fonts':[{'filename':'one.ttf'}]}),encoding='utf-8')
        return source

    def test_two_variants_and_no_cache_or_git(self):
        with tempfile.TemporaryDirectory() as tmp:
            base=Path(tmp);source=self.make_source(base)
            for folder in ['node_modules','.git','build','work','qa','tmp','temp','output','outputs','dist',
                           '.codex','.cache','.pytest_cache','__pycache__','.venv','examples/demo/output']:
                directory=source/folder;directory.mkdir(parents=True,exist_ok=True)
                (directory/'private-paper.pdf').write_bytes(b'private')
                (directory/'work-notes.md').write_text('private',encoding='utf-8')
            for filename in ['work.tmp','session.log','deck.inspect.ndjson','deck.draft.pptx','.env','.env.local','.DS_Store']:
                (source/filename).write_text('exclude',encoding='utf-8')
            # Intended examples remain available; output filtering must not remove all PPTX/PDF assets.
            (source/'examples/demo/reference.pdf').write_bytes(b'reference')
            (source/'examples/demo/layout.pptx').write_bytes(b'example')
            for variant in ['full','github']:
                out=base/f'{variant}.zip';pack.package(source,out,variant)
                with ZipFile(out) as z:
                    expected={'paper-loom/SKILL.md','paper-loom/fonts/manifest.json','paper-loom/bundle-manifest.json',
                              'paper-loom/examples/demo/reference.pdf','paper-loom/examples/demo/layout.pptx'}
                    if variant=='full':expected.add('paper-loom/fonts/one.ttf')
                    self.assertEqual(set(z.namelist()),expected)
                    self.assertIsNone(z.testzip())

    def test_manifest_is_unique_current_and_matches_archive_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            base=Path(tmp);source=self.make_source(base)
            (source/'package.json').write_text(json.dumps({'version':'9.8.7'}),encoding='utf-8')
            (source/'bundle-manifest.json').write_text('{"version":"stale","files":[]}',encoding='utf-8')
            (source/'notes.md').write_text('中文\nResearch evidence',encoding='utf-8')
            for variant in ['full','github']:
                out=base/f'{variant}.zip';result=pack.package(source,out,variant)
                with ZipFile(out) as z:
                    names=z.namelist();manifest_path='paper-loom/bundle-manifest.json'
                    self.assertEqual(len(names),len(set(names)))
                    self.assertEqual(names.count(manifest_path),1)
                    self.assertEqual(result['file_count'],len(names))
                    manifest=json.loads(z.read(manifest_path))
                    self.assertEqual(manifest['version'],'9.8.7')
                    self.assertEqual(manifest['variant'],variant)
                    records=manifest['files']
                    self.assertEqual(len(records),len(names)-1)
                    self.assertEqual({f"paper-loom/{r['path']}" for r in records},set(names)-{manifest_path})
                    for record in records:
                        data=z.read(f"paper-loom/{record['path']}")
                        self.assertEqual(record['bytes'],len(data))
                        self.assertEqual(record['sha256'],hashlib.sha256(data).hexdigest())

    def test_standalone_source_has_explicit_default_version(self):
        with tempfile.TemporaryDirectory() as tmp:
            base=Path(tmp);source=self.make_source(base);out=base/'full.zip'
            pack.package(source,out,'full')
            with ZipFile(out) as z:
                manifest=json.loads(z.read('paper-loom/bundle-manifest.json'))
                self.assertEqual(manifest['version'],pack.DEFAULT_VERSION)

    def test_full_requires_fonts_but_github_does_not(self):
        with tempfile.TemporaryDirectory() as tmp:
            base=Path(tmp);source=self.make_source(base)
            (source/'fonts/one.ttf').unlink()
            with self.assertRaisesRegex(ValueError,'Full package requires font: one.ttf'):
                pack.package(source,base/'full.zip','full')
            pack.package(source,base/'github.zip','github')

    def test_install_does_not_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            source=Path(tmp)/'src';source.mkdir();(source/'SKILL.md').write_text('skill')
            target=Path(tmp)/'installed';installer.install(source,target)
            self.assertEqual((target/'SKILL.md').read_text(),'skill')
            with self.assertRaises(ValueError):installer.install(source,target)
            with self.assertRaises(ValueError):installer.install(source,source/'nested')

    def test_install_excludes_local_test_papers_and_outputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            source=Path(tmp)/'source';source.mkdir()
            (source/'SKILL.md').write_text('skill')
            for name in ['work','output','.codex']:
                (source/name).mkdir();(source/name/'private.pdf').write_bytes(b'private')
            (source/'.env.local').write_text('private')
            (source/'final.draft.pptx').write_bytes(b'draft')
            (source/'examples').mkdir();(source/'examples'/'reference.pdf').write_bytes(b'reference')
            target=Path(tmp)/'client';installer.install(source,target)
            self.assertEqual(sorted(p.relative_to(target).as_posix() for p in target.rglob('*') if p.is_file()),
                             ['SKILL.md','examples/reference.pdf'])

if __name__=='__main__':unittest.main()
