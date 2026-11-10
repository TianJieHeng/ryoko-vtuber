"""Mutation tests operate in temporary synthetic directories, never the frozen rig."""
import tempfile
import unittest
from pathlib import Path
import source_guards as s
class SourceGuards(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='exp104_source_guard_test_');self.root=Path(self.tmp.name)
        (self.root/'runtime.gd').write_text('unmodified source\n');self.files={'runtime.gd':s.sha(self.root/'runtime.gd')}
    def tearDown(self):self.tmp.cleanup()
    def test_actual_preparation_sources(self):self.assertEqual(s.audit_sources()['status'],'PASS')
    def test_matching_source(self):self.assertEqual(s.verify_manifest(self.root,self.files),[])
    def test_mutated_source(self):
        (self.root/'runtime.gd').write_text('mutated\n');self.assertTrue(s.verify_manifest(self.root,self.files))
    def test_missing_source(self):
        (self.root/'runtime.gd').unlink();self.assertTrue(s.verify_manifest(self.root,self.files))
    def test_wrong_digest(self):self.assertTrue(s.verify_manifest(self.root,{'runtime.gd':'0'*64}))
    def test_parent_escape(self):self.assertTrue(s.verify_manifest(self.root,{'../outside':'0'*64}))
    def test_absolute_path(self):self.assertTrue(s.verify_manifest(self.root,{'/tmp/outside':'0'*64}))
    def test_wrapper_preserves_dimension_gate(self):
        source=(s.W/'check_and_capture.gd').read_text();wrapper=s.expected_wrapper(source,s.W)
        self.assertIn('if im.get_size()!=expected:return',wrapper)
        self.assertIn('Vector2i(568,800)',wrapper);self.assertIn('Vector2i(400,360)',wrapper)
        self.assertEqual((s.W/'native_launcher/static.gd').read_text(),wrapper)
    def test_nonproduction_unique_launcher(self):
        config=(s.W/'native_launcher/project.godot').read_text()
        self.assertIn('Ryoko EXP104 Triumphant Grin PREVIEW ONLY',config)
        self.assertIn('run/main_scene="res://launcher.tscn"',config)
    def test_overwrite_refusal_present(self):
        launch=(s.W/'native_launcher/launcher.gd').read_text()
        self.assertIn('Existing capture must be preserved; refusing overwrite',launch)
        self.assertIn('w+"/capture"',launch);self.assertIn('w+"/motion"',launch)
if __name__=='__main__':unittest.main()
