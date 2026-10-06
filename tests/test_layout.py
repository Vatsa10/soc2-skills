import json
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

POLICIES = ["acceptable-use", "access-control", "asset-management", "business-continuity-dr",
            "change-management", "code-of-conduct", "data-classification",
            "data-retention-disposal", "encryption", "hr-security", "incident-response",
            "information-security", "logging-monitoring", "physical-security", "privacy",
            "risk-assessment", "secure-sdlc", "vendor-management"]
TAG_RE = re.compile(r"\[([A-Z]{2,3}-\d{2}) → ((?:(?:CC|A|PI|C|P)\d+\.\d+(?:, )?)+)\]")
# D2 remaps: tags for these controls may cite only the listed criteria
REMAPS = {"AC-02": {"CC6.1"}, "CHG-04": {"CC8.1"}, "AC-17": {"CC6.1"}}


class PolicyPackagingTest(unittest.TestCase):
    def test_policy_templates_are_the_18(self):
        found = sorted(p.stem for p in (ROOT / "skills/soc2-policies/templates").glob("*.md"))
        self.assertEqual(found, sorted(POLICIES))
        skill = (ROOT / "skills/soc2-policies/SKILL.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        for name in POLICIES:
            self.assertIn(name, skill, name)
        for doc in (skill, readme, agents):
            self.assertIn("18 core polic", doc)
            self.assertNotIn("15 core polic", doc)

    def test_governance_block_and_placeholders(self):
        skill = (ROOT / "skills/soc2-policies/SKILL.md").read_text(encoding="utf-8")
        for name in POLICIES:
            t = (ROOT / "skills/soc2-policies/templates" / f"{name}.md").read_text(encoding="utf-8")
            for field in ("Approver", "Approval date", "Version", "Next review due"):
                self.assertIn(f"| {field} |", t, f"{name}: {field}")
            self.assertIn("## Review and approval", t, name)
            self.assertIn("| Version | Date | Change | Approved by |", t, name)
            self.assertIn("re-acknowledge", t, name)
            self.assertNotIn("recorded in version control history", t, name)
            for ph in set(re.findall(r"\{\{(\w+)\}\}", t)):
                self.assertIn("{{" + ph + "}}", skill, f"{name}: placeholder {ph} undocumented")

    def test_policy_tags_valid(self):
        cat = (ROOT / "skills/soc2/references/control-catalog.md").read_text(encoding="utf-8")
        tsc = {k: {x.strip() for x in v.split(",")} for k, v in
               re.findall(r"^### ([A-Z]{2,3}-\d{2}) .*\n- TSC: (.*?) \|", cat, re.M)}
        for name in POLICIES:
            t = (ROOT / "skills/soc2-policies/templates" / f"{name}.md").read_text(encoding="utf-8")
            tags = TAG_RE.findall(t)
            self.assertGreaterEqual(len(tags), 8, name)
            for cid, cited in tags:
                self.assertIn(cid, tsc, f"{name}: {cid}")
                for c in (x.strip() for x in cited.split(",")):
                    allowed = REMAPS.get(cid, tsc[cid])
                    self.assertIn(c, allowed, f"{name}: {cid} -> {c}")

    def test_policy_content_rules(self):
        d = ROOT / "skills/soc2-policies/templates"
        for p in d.glob("*.md"):
            t = p.read_text(encoding="utf-8")
            self.assertNotRegex(t, r"AWS (KMS|CloudTrail)", p.name)
        ac = (d / "access-control.md").read_text(encoding="utf-8")
        self.assertIn("15 characters", ac)
        self.assertIn("64 characters", ac)
        self.assertIn("{{cloud_secrets}}", ac)
        self.assertIn("{{review_cadence}}", (d / "information-security.md").read_text(encoding="utf-8"))
        self.assertIn("TLS 1.3", (d / "encryption.md").read_text(encoding="utf-8"))
        cm = (d / "change-management.md").read_text(encoding="utf-8")
        self.assertNotIn("within 15 days", cm)  # vulnerability SLAs have a single source
        lm = (d / "logging-monitoring.md").read_text(encoding="utf-8")
        self.assertIn("Known Exploited Vulnerabilities", lm)
        self.assertIn("clock starts", lm)

    def test_plugin_manifests(self):
        plugin = json.loads((ROOT / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
        market = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
        self.assertEqual(plugin["version"], "0.2.0")
        self.assertEqual(market["plugins"][0]["name"], plugin["name"])
        self.assertEqual(market["plugins"][0].get("version", plugin["version"]), plugin["version"])

    def test_readme_packaging_notes(self):
        r = (ROOT / "README.md").read_text(encoding="utf-8")
        for needle in ("/soc2-skills:soc2", ".claude/skills", ".agents/skills",
                       "$soc2", "PYTHONIOENCODING"):
            self.assertIn(needle, r, needle)

    def test_skill_md_is_valid_policies_frontmatter(self):
        t = (ROOT / "skills/soc2-policies/SKILL.md").read_text(encoding="utf-8")
        fm = t.split("---\n")[1]
        self.assertEqual([l.split(":")[0] for l in fm.strip().splitlines()], ["name", "description"])
        self.assertLessEqual(len(re.search(r"^description: (.*)$", fm, re.M).group(1)), 1024)


if __name__ == "__main__":
    unittest.main()
