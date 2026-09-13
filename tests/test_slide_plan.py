from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('audit_slide_plan', ROOT / 'scripts/audit_slide_plan.py')
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class SlidePlanTest(unittest.TestCase):
    def setUp(self):
        self.plan = json.loads((ROOT / 'examples/panel-plan.example.json').read_text(encoding='utf-8'))

    def codes(self, plan=None):
        return {e['code'] for e in checker.audit(self.plan if plan is None else plan)['errors']}

    def test_complete_example(self):
        report = checker.audit(self.plan)
        self.assertEqual(report['errors'], [])
        self.assertEqual(len(report['visible_content_ids']), 9)
        self.assertEqual(report['warnings'], [])

    def test_required_content_in_notes_only_is_missing(self):
        self.plan['slides'][0]['panels'][0]['content_ids'] = ['M02']
        self.plan['slides'][0]['speaker_notes'] = 'M01: detailed state maintenance explanation'
        self.assertIn('missing_visible_content', self.codes())

    def test_new_content_requires_new_visible_allocation(self):
        self.plan['content_inventory'].append({'id': 'E04', 'topic': 'Sensitivity',
            'source': 'Table 4', 'required_on_slide': True})
        self.assertIn('missing_visible_content', self.codes())
        self.plan['slides'][2]['panels'].append({'label': 'D', 'title': 'Sensitivity',
            'content_ids': ['E04'], 'key_points': ['Compare all tested settings'], 'visual': 'Parameter table'})
        self.assertFalse(self.codes())

    def test_large_deck_has_no_implicit_cap_but_honors_user_count(self):
        self.plan['slides'] *= 4
        self.plan['slides'] = [deepcopy(s) for s in self.plan['slides']]
        for i, slide in enumerate(self.plan['slides'], 1):
            slide['slide'] = i
        self.plan['deck']['planned_slide_count'] = 12
        self.assertFalse(self.codes())
        self.plan['deck']['requested_slide_count'] = 8
        self.assertIn('requested_count_mismatch', self.codes())

    def test_duplicate_and_unknown_ids(self):
        self.plan['content_inventory'].append(deepcopy(self.plan['content_inventory'][0]))
        self.plan['slides'][0]['panels'][0]['content_ids'].append('unknown')
        self.assertTrue({'duplicate_content', 'unknown_content'} <= self.codes())

    def test_single_dense_panel_can_be_justified(self):
        slide = self.plan['slides'][0]
        slide['panels'] = [dict(slide['panels'][0], content_ids=['M01', 'M02', 'M03'])]
        self.assertFalse(self.codes())
        self.assertTrue(checker.audit(self.plan)['warnings'])
        slide['panel_count_reason'] = 'The full comparison matrix requires the readable canvas.'
        self.assertEqual(checker.audit(self.plan)['warnings'], [])

    def test_blank_letter_panels_do_not_satisfy_plan(self):
        self.plan['slides'][0]['panels'][0]['key_points'] = []
        self.assertIn('empty_panel', self.codes())

    def test_excluded_supplement_needs_reason(self):
        self.plan['content_inventory'].append({'id': 'S01', 'topic': 'Duplicate derivation',
            'source': 'Appendix A', 'required_on_slide': False})
        self.assertIn('unexplained_exclusion', self.codes())
        self.plan['content_inventory'][-1]['exclusion_reason'] = 'Algebraic expansion in notes; mechanism remains visible.'
        self.assertFalse(self.codes())

    def test_invalid_shapes_fail_without_traceback(self):
        for value in [None, [], {}, {'slides': [None], 'content_inventory': [None]},
                      dict(self.plan, deck={'planned_slide_count': True})]:
            self.assertTrue(checker.audit(value)['errors'])

    def test_cli_writes_failed_report_and_refuses_input_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'plan.json'
            output = Path(tmp) / 'reports/audit.json'
            self.plan['slides'][0]['panels'][0]['content_ids'] = ['M02']
            path.write_text(json.dumps(self.plan), encoding='utf-8')
            before = path.read_bytes()
            cmd = [sys.executable, str(ROOT / 'scripts/audit_slide_plan.py'), str(path), '--report']
            result = subprocess.run(cmd + [str(output)], capture_output=True)
            self.assertEqual(result.returncode, 1)
            self.assertTrue(json.loads(output.read_text(encoding='utf-8'))['errors'])
            result = subprocess.run(cmd + [str(path)], capture_output=True)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(path.read_bytes(), before)


if __name__ == '__main__':
    unittest.main()
