import argparse
import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from init_site import create, origin


class InitSiteTests(unittest.TestCase):
    def args(self, target, **kwargs):
        data = dict(target=str(target), profile='java', title=None, description=None,
                    name=None, site='https://java.example.com', dry_run=False)
        data.update(kwargs)
        return argparse.Namespace(**data)

    def generate(self, args):
        with contextlib.redirect_stdout(io.StringIO()):
            return create(args)

    def test_nonempty_target_keeps_original_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            original = target / 'notes.md'
            original.write_bytes(b'existing user material\x00')
            with self.assertRaises(ValueError):
                self.generate(self.args(target))
            self.assertEqual(original.read_bytes(), b'existing user material\x00')
            self.assertEqual(list(target.iterdir()), [original])

    def test_profiles_have_actual_routes_and_independent_config(self):
        for profile, tracks in [('java', ['java']), ('frontend', ['frontend']), ('mixed', ['java', 'frontend'])]:
            with self.subTest(profile=profile), tempfile.TemporaryDirectory() as directory:
                target = Path(directory) / 'new-site'
                self.generate(self.args(target, profile=profile, title='研发 "笔记" <测试>'))
                config = json.loads((target / 'site.config.json').read_text())
                self.assertEqual(config['title'], '研发 "笔记" <测试>')
                self.assertEqual(config['site'], 'https://java.example.com')
                self.assertEqual([t['id'] for t in config['topics']], tracks)
                for topic in config['topics']:
                    self.assertTrue((target / 'src/content/docs' / topic['id'] / 'index.md').is_file())
                self.assertFalse((target / 'src/content/docs/index.md').exists())
                self.assertTrue((target / 'CLAUDE.md').samefile(target / 'AGENTS.md'))
                self.assertFalse((target / 'node_modules').exists())
                self.assertFalse((target / '.git').exists())

    def test_dry_run_does_not_create_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'dry-run'
            self.generate(self.args(target, dry_run=True))
            self.assertFalse(target.exists())

    def test_existing_git_metadata_preserved_and_rerun_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            (target / '.git').mkdir()
            (target / '.git/HEAD').write_text('user-branch')
            self.generate(self.args(target))
            self.assertEqual((target / '.git/HEAD').read_text(), 'user-branch')
            with self.assertRaises(ValueError):
                self.generate(self.args(target))

    def test_reject_symlink_and_invalid_package_name(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            linked = target / 'link'
            linked.symlink_to(target, target_is_directory=True)
            with self.assertRaises(ValueError):
                self.generate(self.args(linked))
            with self.assertRaises(ValueError):
                self.generate(self.args(target / 'empty', name='../bad'))
            self.assertFalse((target / 'empty').exists())

    def test_domain_accepts_only_https_origin(self):
        self.assertEqual(origin('https://java.example.com/'), 'https://java.example.com')
        for value in ['http://example.com', 'https://user:secret@example.com',
                      'https://example.com/docs', 'https://example.com?x=1',
                      'https://example.com#x', 'https://example.com:bad']:
            with self.subTest(value=value), self.assertRaises(argparse.ArgumentTypeError):
                origin(value)


if __name__ == '__main__':
    unittest.main()
