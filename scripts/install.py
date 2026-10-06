"""Install the SOC 2 skill pack for Claude Code or Codex. Stdlib only."""
import argparse
import shutil
import sys
from pathlib import Path

SKILLS = ["soc2", "soc2-architect", "soc2-type1-readiness",
          "soc2-type2-operations", "soc2-audit", "soc2-policies"]
ROOT = Path(__file__).resolve().parent.parent
# Codex reads user-level skills from ~/.agents/skills (not ~/.codex/skills).
DEFAULTS = {"claude": Path.home() / ".claude" / "skills",
            "codex": Path.home() / ".agents" / "skills"}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--target", choices=sorted(DEFAULTS), required=True)
    ap.add_argument("--dest", help="override install directory")
    a = ap.parse_args(argv)
    dest = Path(a.dest) if a.dest else DEFAULTS[a.target]
    dest.mkdir(parents=True, exist_ok=True)
    for s in SKILLS:  # all six together: sub-skills reference ../soc2/
        out = dest / s
        if out.exists():
            shutil.rmtree(out)
        shutil.copytree(ROOT / "skills" / s, out,
                        ignore=shutil.ignore_patterns("__pycache__"))
        print(f"installed {s} -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
