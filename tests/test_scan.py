import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "skills" / "soc2" / "scripts" / "scan.py"
FIX = ROOT / "tests" / "fixtures"
sys.path.insert(0, str(SCRIPT.parent))
import scan  # noqa: E402


class ScanTest(unittest.TestCase):
    def test_empty_repo_matches_defaults(self):
        self.assertEqual(scan.scan(FIX / "empty"), scan.empty_signals())

    def test_tf_aws(self):
        s = scan.scan(FIX / "tf_aws")
        self.assertEqual(s["iac"], ["terraform"])
        self.assertEqual(s["ci"], ["github-actions"])
        self.assertEqual(s["cloud"], ["aws"])
        self.assertTrue(s["encryption"]["kms"])
        self.assertTrue(s["encryption"]["at_rest_hint"])
        self.assertTrue(s["logging"]["cloudtrail"])
        self.assertEqual(s["logging"]["retention_days"], 400)
        self.assertTrue(s["backups"]["configured"])
        self.assertTrue(s["change_mgmt"]["codeowners"])
        self.assertTrue(s["secrets"]["scanning"])
        self.assertTrue(s["deps"]["sast"])

    def test_bare_app(self):
        s = scan.scan(FIX / "bare_app")
        self.assertEqual(s["secrets"]["hardcoded_hits"], 1)
        self.assertTrue(s["privacy"]["pii_fields"])
        self.assertFalse(s["auth"]["sso"])

    def test_schema_keys_stable(self):
        self.assertIn("auth.sso", scan.flatten_keys(scan.empty_signals()))
        self.assertEqual(len(scan.flatten_keys(scan.empty_signals())), 28)

    def test_non_utf8_and_big_and_vendored_skipped(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            (p / "bad.py").write_bytes(b"\xff\xfe\x81 okta \x9d")
            (p / "big.tf").write_bytes(b'provider "aws" {}\n' + b"#" * 1_100_000)
            (p / "node_modules").mkdir()
            (p / "node_modules" / "x.tf").write_text('provider "google" {}', encoding="utf-8")
            s = scan.scan(p)
            self.assertEqual(s["auth"]["idp"], ["okta"])
            self.assertEqual(s["cloud"], [])
            self.assertEqual(s["iac"], [])

    def test_cli_bad_path_exit_2(self):
        r = subprocess.run([sys.executable, str(SCRIPT), str(FIX / "nope")],
                           capture_output=True, encoding="utf-8")
        self.assertEqual(r.returncode, 2)
        self.assertIn("error:", r.stderr)
        self.assertNotIn("Traceback", r.stderr)

    def test_cli_write_and_if_stale(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "main.tf").write_text('provider "aws" {}', encoding="utf-8")
            r = subprocess.run([sys.executable, str(SCRIPT), d, "--write"],
                               capture_output=True, encoding="utf-8")
            self.assertEqual(r.returncode, 0, r.stderr)
            cached = json.loads((Path(d) / ".soc2" / "scan.json").read_text(encoding="utf-8"))
            self.assertEqual(cached["cloud"], ["aws"])
            r2 = subprocess.run([sys.executable, str(SCRIPT), d, "--if-stale"],
                                capture_output=True, encoding="utf-8")
            self.assertEqual(json.loads(r2.stdout), cached)


if __name__ == "__main__":
    unittest.main()
