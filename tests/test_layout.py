import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ["soc2", "soc2-architect", "soc2-type1-readiness",
          "soc2-type2-operations", "soc2-audit", "soc2-policies"]
DISCLAIMER = ("This skill prepares for a SOC 2 audit; it is not an attestation. "
              "Only a licensed CPA firm can issue a SOC 2 Type 1 or Type 2 report.")
REF_RE = re.compile(r"(?:\.\./)+soc2/[\w./-]+")
ID_RE = re.compile(r"\b(?:GOV|RSK|MON|CTL|AC|OPS|CHG|VND|AV|PI|CF|PR)-\d{2}\b")


def catalog_ids():
    t = (ROOT / "skills/soc2/references/control-catalog.md").read_text(encoding="utf-8")
    return set(re.findall(r"^### ([A-Z]{2,3}-\d{2})", t, re.M))


class LayoutTest(unittest.TestCase):
    def test_frontmatter_and_disclaimer(self):
        for s in SKILLS:
            t = (ROOT / "skills" / s / "SKILL.md").read_text(encoding="utf-8")
            self.assertTrue(t.startswith("---\n"), s)
            self.assertIn(f"\nname: {s}\n", t, s)
            self.assertIn("\ndescription: ", t, s)
            self.assertIn(DISCLAIMER, t, s)
            # an unquoted ": " in a plain YAML scalar breaks frontmatter parsing
            desc = re.search(r"^description: (.*)$", t, re.M).group(1)
            if not desc.startswith(("'", '"')):
                self.assertNotIn(": ", desc, s)

    def test_cited_ids_exist(self):
        ids = catalog_ids()
        for s in SKILLS:
            for p in (ROOT / "skills" / s).rglob("*.md"):
                if p.name == "control-catalog.md":
                    continue
                for cid in ID_RE.findall(p.read_text(encoding="utf-8")):
                    self.assertIn(cid, ids, f"{p}: {cid}")

    def test_install_resolves_sibling_refs(self):
        with tempfile.TemporaryDirectory() as d:
            r = subprocess.run([sys.executable, str(ROOT / "scripts/install.py"),
                                "--target", "claude", "--dest", d],
                               capture_output=True, encoding="utf-8")
            self.assertEqual(r.returncode, 0, r.stderr)
            checked = 0
            for s in SKILLS:
                for p in (Path(d) / s).rglob("*.md"):
                    for ref in REF_RE.findall(p.read_text(encoding="utf-8")):
                        # resolve relative to the file's own directory
                        self.assertTrue((p.parent / ref).exists(), f"{p}: {ref}")
                        checked += 1
            self.assertGreater(checked, 0)

    def test_doc_ids_exist_and_arrows_match(self):
        ids = catalog_ids()
        cat = (ROOT / "skills/soc2/references/control-catalog.md").read_text(encoding="utf-8")
        tsc = dict(re.findall(r"^### ([A-Z]{2,3}-\d{2}) .*\n- TSC: (.*?) \|", cat, re.M))
        shaped = re.compile(r"\b[A-Z]{2,3}-\d{2}\b")
        arrow = re.compile(r"\b([A-Z]{2,3}-\d{2}) → ((?:(?:CC|A|PI|C|P)\d+\.\d+(?:, )?)+)")
        for name in ("tests/router-evals.md", "README.md", "AGENTS.md", "CLAUDE.md"):
            p = ROOT / name
            if not p.exists():
                continue
            text = p.read_text(encoding="utf-8")
            for cid in shaped.findall(text):
                self.assertIn(cid, ids, f"{name}: {cid}")
            for cid, cited in arrow.findall(text):
                self.assertEqual(cited.rstrip(", "), tsc[cid], f"{name}: {cid}")

    def test_readme_disclaimer(self):
        self.assertIn(DISCLAIMER, (ROOT / "README.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
