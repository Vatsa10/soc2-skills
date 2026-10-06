import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REF = ROOT / "skills" / "soc2" / "references"
KEYS = ["TSC", "Applies when", "Implement", "Scan signals", "Frequency", "Owner",
        "Type 1 test", "Type 2 test", "Evidence", "Type 1 pass", "Type 2 pass"]
FREQUENCIES = {"Continuous/automated", "Per event", "Daily", "Weekly", "Monthly",
               "Quarterly", "Annual"}
ID_RE = re.compile(r"^### ([A-Z]{2,3}-\d{2}) — (.+)$")


def criteria():
    text = (REF / "tsc-criteria.md").read_text(encoding="utf-8")
    return set(re.findall(r"^- \*\*((?:CC|A|PI|C|P)\d+\.\d+)\*\*", text, re.M))


def controls():
    text = (REF / "control-catalog.md").read_text(encoding="utf-8")
    out, cur = {}, None
    for line in text.splitlines():
        m = ID_RE.match(line)
        if m:
            cur = m.group(1)
            out[cur] = {"title": m.group(2), "fields": {}}
        elif cur and line.startswith("- ") and ":" in line:
            k, v = line[2:].split(":", 1)
            out[cur]["fields"][k.strip()] = v.strip()
    return out


class CatalogTest(unittest.TestCase):
    def test_criteria_count(self):
        self.assertGreaterEqual(len(criteria()), 60)

    def test_controls_have_all_keys_in_order(self):
        cs = controls()
        self.assertGreaterEqual(len(cs), 80)
        for cid, c in cs.items():
            self.assertEqual(list(c["fields"]), KEYS, cid)

    def test_tsc_ids_valid(self):
        valid = criteria()
        for cid, c in controls().items():
            tsc = c["fields"]["TSC"].split("|")[0]
            ids = [t.strip() for t in tsc.split(",")]
            for t in ids:
                self.assertIn(t, valid, f"{cid} cites unknown {t}")

    def test_category_matches_tsc_series(self):
        # The Scope selection rule: one Category name per TSC series cited.
        def series(c):
            for pre, name in (("CC", "Security"), ("A1", "Availability"),
                              ("PI", "Processing Integrity"), ("C1", "Confidentiality")):
                if c.startswith(pre):
                    return name
            return "Privacy"
        for cid, c in controls().items():
            tsc, cat = c["fields"]["TSC"].split("| Category:")
            want = {series(x.strip()) for x in tsc.split(",")}
            got = {x.strip() for x in cat.split(",")}
            self.assertEqual(got, want, cid)

    def test_every_criterion_covered(self):
        cited = set()
        for c in controls().values():
            cited.update(t.strip() for t in c["fields"]["TSC"].split("|")[0].split(","))
        self.assertEqual(criteria() - cited, set())

    def test_scan_signals_exist(self):
        import sys
        sys.path.insert(0, str(ROOT / "skills" / "soc2" / "scripts"))
        import scan
        keys = set(scan.flatten_keys(scan.empty_signals()))
        for cid, c in controls().items():
            sig = c["fields"]["Scan signals"]
            if sig == "none":
                continue
            for k in (s.strip() for s in sig.split(",")):
                self.assertIn(k, keys, f"{cid} unknown signal {k}")

    def test_frequency_and_owner_values(self):
        for cid, c in controls().items():
            self.assertIn(c["fields"]["Frequency"], FREQUENCIES, cid)
            self.assertTrue(c["fields"]["Owner"], cid)

    def test_type1_and_type2_pass_are_distinct(self):
        for cid, c in controls().items():
            f = c["fields"]
            self.assertNotEqual(f["Type 1 pass"], f["Type 2 pass"], cid)
            self.assertNotIn("Pass rule", f, cid)

    def test_shared_decision_controls(self):
        cs = controls()
        want = {"GOV-11": {"CC9.2", "CC2.3"}, "GOV-12": {"CC2.3"},
                "GOV-13": {"CC2.2", "CC2.3"}, "PI-06": {"PI1.3"},
                "PI-07": {"PI1.4"}, "PR-17": {"P1.1", "P3.1"},
                "AC-02": {"CC6.1"}, "CHG-04": {"CC8.1"}, "AC-17": {"CC6.1"}}
        for cid, tsc in want.items():
            self.assertIn(cid, cs)
            got = {t.strip() for t in cs[cid]["fields"]["TSC"].split("|")[0].split(",")}
            self.assertEqual(got, tsc, cid)

    def test_no_old_signal_name(self):
        text = (REF / "control-catalog.md").read_text(encoding="utf-8")
        self.assertNotIn("logging.cloudtrail", text)

    def test_index_matches_catalog(self):
        text = (REF / "control-index.md").read_text(encoding="utf-8")
        rows = {}
        for line in text.splitlines():
            cells = [x.strip() for x in line.strip().strip("|").split("|")]
            if len(cells) == 7 and re.fullmatch(r"[A-Z]{2,3}-\d{2}", cells[0]):
                rows[cells[0]] = cells
        cs = controls()
        self.assertEqual(set(rows), set(cs))
        for cid, c in cs.items():
            f = c["fields"]
            tsc, cat = (x.strip() for x in f["TSC"].split("| Category:"))
            self.assertEqual(rows[cid][1:], [c["title"], tsc, cat, f["Frequency"],
                                             f["Owner"], f["Scan signals"]], cid)

    def test_index_is_build_output(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location("build_index", ROOT / "scripts" / "build_index.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        want = mod.render((REF / "control-catalog.md").read_text(encoding="utf-8"))
        got = (REF / "control-index.md").read_text(encoding="utf-8")
        self.assertEqual(got, want, "run python scripts/build_index.py")

    def test_arrow_citations_match_catalog(self):
        cs = controls()
        tsc = {cid: {t.strip() for t in c["fields"]["TSC"].split("|")[0].split(",")}
               for cid, c in cs.items()}
        pat = re.compile(r"\b([A-Z]{2,3}-\d{2})\s*→\s*((?:(?:CC|A|PI|C|P)\d+\.\d+)(?:\s*(?:,|/|and)\s*(?:CC|A|PI|C|P)\d+\.\d+)*)")
        placeholder = re.compile(r"\b([A-Z]{2,3}-\d{2})\s*→\s*<TSC>")
        bad = []
        for md in sorted((ROOT / "skills").rglob("*.md")):
            for n, line in enumerate(md.read_text(encoding="utf-8").splitlines(), 1):
                for m in placeholder.finditer(line):
                    if m.group(1) not in tsc:
                        bad.append(f"unknown id {md.relative_to(ROOT)}:{n} {m.group(0)}")
                for m in pat.finditer(line):
                    cid = m.group(1)
                    where = f"{md.relative_to(ROOT)}:{n} {m.group(0)}"
                    if cid not in tsc:
                        bad.append("unknown id " + where)
                        continue
                    for t in re.findall(r"(?:CC|A|PI|C|P)\d+\.\d+", m.group(2)):
                        if t not in tsc[cid]:
                            bad.append(f"{t} not on {cid} TSC line: {where}")
        self.assertEqual(bad, [], "\n".join(bad))

    def test_cloud_equivalents_exists(self):
        text = (REF / "cloud-equivalents.md").read_text(encoding="utf-8")
        for word in ("AWS", "GCP", "Azure"):
            self.assertIn(word, text)
        self.assertRegex(text, r"\| *AWS *\| *GCP *\| *Azure *\|")


if __name__ == "__main__":
    unittest.main()
