"""Regenerate skills/soc2/references/control-index.md from control-catalog.md (stdlib only)."""
import re
import sys
from pathlib import Path

REF = Path(__file__).resolve().parent.parent / "skills" / "soc2" / "references"


def parse(catalog_text):
    rows, cur = [], None
    for line in catalog_text.splitlines():
        m = re.match(r"^### ([A-Z]{2,3}-\d{2}) — (.+)$", line)
        if m:
            cur = {"id": m[1], "title": m[2]}
            rows.append(cur)
        elif cur and line.startswith("- ") and ":" in line:
            k, v = line[2:].split(":", 1)
            cur.setdefault(k.strip(), v.strip())
    return rows


def render(catalog_text):
    rows = parse(catalog_text)
    out = ["# SOC 2 Control Index", "",
           "> This skill prepares for a SOC 2 audit; it is not an attestation. Only a licensed CPA firm can issue a SOC 2 Type 1 or Type 2 report.", "",
           f"One row per control in `control-catalog.md` ({len(rows)} controls). Read this index first to scope and plan. Open a full catalog entry only for a control you evaluate, by searching `control-catalog.md` for `### <ID>`; never load the whole catalog at once. Scope rule: a control is in scope when any criterion in its TSC column belongs to an in-scope category (see the catalog's Scope selection rule). Frequency and Owner are defaults. Cite a control as `<ID> → <TSC>` using the TSC column.", "",
           "| ID | Title | TSC | Category | Frequency | Owner | Scan signals |",
           "|---|---|---|---|---|---|---|"]
    for r in rows:
        tsc, c = (x.strip() for x in r["TSC"].split("| Category:"))
        out.append(f"| {r['id']} | {r['title']} | {tsc} | {c} | {r['Frequency']} | {r['Owner']} | {r['Scan signals']} |")
    return "\n".join(out) + "\n"


def main():
    text = render((REF / "control-catalog.md").read_text(encoding="utf-8"))
    if "--check" in sys.argv:
        cur = (REF / "control-index.md").read_text(encoding="utf-8")
        if cur != text:
            print("control-index.md is stale; run python scripts/build_index.py")
            return 1
        print("control-index.md is up to date")
        return 0
    with open(REF / "control-index.md", "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print(f"wrote control-index.md ({text.count(chr(10)) - 7} controls)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
