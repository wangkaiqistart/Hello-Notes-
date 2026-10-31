import contextlib
import io
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

from deploy_oss import MANIFEST_KEY, deploy


class PublishTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.dist = self.root / "dist"
        self.dist.mkdir()
        (self.dist / "index.html").write_text("home")
        self.bootstrap = self.root / "retired.json"
        self.bootstrap.write_text(json.dumps({"version": 1, "pages": ["old/index.html"]}))
        self.calls = []
        self.previous = {"version": 1, "pages": ["index.html", "gone/index.html"]}
        self.fail = None
        self.manifest = None

    def runner(self, args):
        self.calls.append(args)
        if self.fail and self.fail(args):
            return subprocess.CompletedProcess(args, 1, "", "AccessDenied")
        if args[:2] == ["cp", f"oss://example/{MANIFEST_KEY}"]:
            if self.previous is None:
                return subprocess.CompletedProcess(args, 1, "", "ErrorCode=NoSuchKey")
            Path(args[2]).write_text(json.dumps(self.previous))
        if args[0] == "cp" and args[2] == f"oss://example/{MANIFEST_KEY}":
            self.manifest = json.loads(Path(args[1]).read_text())
        return subprocess.CompletedProcess(args, 0, "", "")

    def publish(self, apply=True):
        with contextlib.redirect_stdout(io.StringIO()):
            return deploy(self.dist, "example", apply=apply, runner=self.runner, bootstrap=self.bootstrap)

    def test_first_publish_cleans_only_bootstrap_html(self):
        self.previous = None
        plan = self.publish()
        self.assertEqual(plan["remove"], ["old/index.html"])
        self.assertEqual([args for args in self.calls if args[0] == "rm"], [["rm", "oss://example/old/index.html", "--force"]])
        self.assertEqual(self.manifest, {"version": 1, "pages": ["index.html"]})

    def test_future_publish_preserves_current_or_reintroduced_pages(self):
        (self.dist / "old").mkdir()
        (self.dist / "old/index.html").write_text("restored")
        self.assertEqual(self.publish()["remove"], ["gone/index.html"])
        self.assertIn("old/index.html", self.manifest["pages"])

    def test_preview_does_not_write_remote_objects(self):
        self.publish(apply=False)
        self.assertEqual(len(self.calls), 1)
        self.assertIsNone(self.manifest)

    def test_manifest_authentication_error_stops_all_writes(self):
        self.fail = lambda args: True
        with self.assertRaises(RuntimeError):
            self.publish()
        self.assertEqual(len(self.calls), 1)

    def test_failed_upload_never_deletes_or_updates_manifest(self):
        self.fail = lambda args: args[:2] == ["cp", "-r"]
        with self.assertRaises(RuntimeError):
            self.publish()
        self.assertFalse(any(args[0] == "rm" for args in self.calls))
        self.assertIsNone(self.manifest)

    def test_failed_cleanup_keeps_old_manifest_for_retry(self):
        self.fail = lambda args: args[0] == "rm"
        with self.assertRaises(RuntimeError):
            self.publish()
        self.assertIsNone(self.manifest)

    def test_unsafe_or_non_html_manifest_cannot_delete(self):
        for key in ["../other.html", "/index.html", "images/logo.png", "foo/*.html", "foo//bar.html"]:
            with self.subTest(key=key):
                self.previous = {"version": 1, "pages": [key]}
                self.calls = []
                with self.assertRaises(ValueError):
                    self.publish()
                self.assertEqual(len(self.calls), 1)


if __name__ == "__main__":
    unittest.main()
