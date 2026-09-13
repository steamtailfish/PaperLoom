from pathlib import Path
from zipfile import ZipFile
import importlib.util
import json
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
def module(name):
    s=importlib.util.spec_from_file_location(name,ROOT/'scripts'/f'{name}.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
pack=module('package_skill');installer=module('install_skill')

class PackagingTest(unittest.TestCase):
    def test_two_variants_and_no_cache_or_git(self):
        with tempfile.TemporaryDirectory() as tmp:
            base=Path(tmp);source=base/'src';source.mkdir()
            (source/'SKILL.md').write_text('test');(source/'fonts').mkdir()
            (source/'fonts/one.ttf').write_bytes(b'not-a-real-font')
            (source/'fonts/manifest.json').write_text(json.dumps({'fonts':[{'filename':'one.ttf'}]}))
            (source/'node_modules').mkdir();(source/'node_modules/private.txt').write_text('exclude')
            (source/'.git').mkdir();(source/'.git/config').write_text('exclude')
            for variant in ['full','github']:
                out=base/f'{variant}.zip';pack.package(source,out,variant)
                with ZipFile(out) as z:
                    names=z.namelist()
                    self.assertEqual('paper-loom/fonts/one.ttf' in names,variant=='full')
                    self.assertTrue(all('node_modules/' not in n and '/.git/' not in n for n in names))
                    self.assertIsNone(z.testzip())
    def test_install_does_not_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            source=Path(tmp)/'src';source.mkdir();(source/'SKILL.md').write_text('skill')
            target=Path(tmp)/'installed';installer.install(source,target)
            self.assertEqual((target/'SKILL.md').read_text(),'skill')
            with self.assertRaises(ValueError):installer.install(source,target)
            with self.assertRaises(ValueError):installer.install(source,source/'nested')

if __name__=='__main__':unittest.main()
