"""Run unchanged unit assertions against isolated relocated synthetic fixtures.

Only the fixture builder differs from the historical test module. A fixture has
its own input-freeze hash, checked by the original validator; its negative test
still changes that freeze and must fail. No actual capture evidence, historical
validator, approval, candidate, or frozen review input is modified.
"""
import argparse
import contextlib
import io
from pathlib import Path
import tempfile
import unittest
import test_review_validation as historical
import test_encode_preview as encoder

W=Path(__file__).resolve().parent
review=historical.review

def run_isolated_fixture(self, transform=None):
    with tempfile.TemporaryDirectory(prefix='exp123-portable-synthetic-') as tmp:
        root=Path(tmp); work=root/'puzzled_work'; work.mkdir()
        skip={'capture','motion','motion_checks.json','review_evidence',
              'Puzzled_review_v1.mp4','__pycache__','review_input_freeze.json'}
        for path in W.iterdir():
            if path.name not in skip:
                (work/path.name).symlink_to(path,target_is_directory=path.is_dir())
        for name,id in [('mental_arithmetic_work','129'),('controlled_anger_work','041'),('broad_surprise_work','061')]:
            (root/name).mkdir()
            (root/name/f'EXP-{id}.json').symlink_to(W/f'comparison_profiles/EXP-{id}.json')
        fixture=review.load(W/'review_input_freeze.json')
        before={n:review.sha(W/n) for n in fixture['files']}
        fixture['status']='SYNTHETIC RELOCATED UNIT FIXTURE ONLY; no native capture or approval'
        fixture['files']=before
        review.write(work/'review_input_freeze.json',fixture)
        expected=review.sha(work/'review_input_freeze.json')
        if transform:transform(work)
        previous=review.EXPECTED_INPUT_FREEZE_SHA256
        try:
            review.EXPECTED_INPUT_FREEZE_SHA256=expected
            with contextlib.redirect_stdout(io.StringIO()):
                code=review.run(argparse.Namespace(work=work,output=root/'reports',video=None))
        finally:
            review.EXPECTED_INPUT_FREEZE_SHA256=previous
        result=review.load(root/'reports/review_checks.json')
        self.assertEqual(before,{n:review.sha(W/n) for n in before})
        return code,result

if __name__=='__main__':
    historical.ReviewValidationTests.run_isolated_fixture=run_isolated_fixture
    suite=unittest.TestSuite([unittest.defaultTestLoader.loadTestsFromModule(m) for m in [historical,encoder]])
    raise SystemExit(not unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful())
