import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INSTALL = str(ROOT / "scripts/install.py")


def run(dest):
    return subprocess.run([sys.executable, INSTALL, "--target", "claude", "--dest", dest],
                          capture_output=True, encoding="utf-8")


class InstallTest(unittest.TestCase):
    def test_refuses_repo_skills_dir(self):
        for d in (ROOT / "skills", ROOT / "skills" / "soc2",
                  ROOT / "skills" / "soc2-audit" / ".." / "."):
            r = run(str(d))
            self.assertEqual(r.returncode, 2, r.stdout)
            self.assertIn("error:", r.stderr)
        self.assertTrue((ROOT / "skills/soc2/SKILL.md").exists())

    def test_unrelated_folder_untouched_and_reinstall(self):
        with tempfile.TemporaryDirectory() as d:
            other = Path(d) / "my-other-skill"
            other.mkdir()
            (other / "SKILL.md").write_text("keep me", encoding="utf-8")
            (Path(d) / "soc2").mkdir()
            (Path(d) / "soc2" / "stale.txt").write_text("x", encoding="utf-8")
            for _ in range(2):
                r = run(d)
                self.assertEqual(r.returncode, 0, r.stderr)
            self.assertEqual((other / "SKILL.md").read_text(encoding="utf-8"), "keep me")
            self.assertFalse((Path(d) / "soc2" / "stale.txt").exists())
            self.assertTrue((Path(d) / "soc2" / "SKILL.md").exists())
            leftovers = [p.name for p in Path(d).iterdir() if p.name.startswith(".")]
            self.assertEqual(leftovers, [])


if __name__ == "__main__":
    unittest.main()
