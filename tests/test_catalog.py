import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REF = ROOT / "skills" / "soc2" / "references"
KEYS = ["TSC", "Applies when", "Implement", "Scan signals",
        "Type 1 test", "Type 2 test", "Evidence", "Pass rule"]
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


if __name__ == "__main__":
    unittest.main()
