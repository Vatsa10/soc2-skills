"""Install the SOC 2 skill pack for Claude Code or Codex. Stdlib only."""
import argparse
import os
import shutil
import sys
from pathlib import Path

SKILLS = ["soc2", "soc2-architect", "soc2-type1-readiness",
          "soc2-type2-operations", "soc2-audit", "soc2-policies"]
ROOT = Path(__file__).resolve().parent.parent
# Codex reads user-level skills from ~/.agents/skills (not ~/.codex/skills).
DEFAULTS = {"claude": Path.home() / ".claude" / "skills",
            "codex": Path.home() / ".agents" / "skills"}


def _inside(a, b):
    """True when path a equals b or lies inside b."""
    try:
        a.relative_to(b)
        return True
    except ValueError:
        return False


def _remove(p):
    if p.is_symlink() or p.is_file():
        p.unlink()
    elif p.exists():
        shutil.rmtree(p)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--target", choices=sorted(DEFAULTS), required=True)
    ap.add_argument("--dest", help="override install directory")
    a = ap.parse_args(argv)
    dest = (Path(a.dest) if a.dest else DEFAULTS[a.target]).expanduser().resolve()
    src_root = (ROOT / "skills").resolve()
    # dest equal to skills/ (or inside it or a source skill) would overwrite
    # or nest into the sources being copied.
    for src in [src_root] + [(src_root / s).resolve() for s in SKILLS]:
        if _inside(dest, src):
            print(f"error: --dest {dest} overlaps the pack's own source {src}; "
                  "choose a directory outside the repository's skills/",
                  file=sys.stderr)
            return 2
    dest.mkdir(parents=True, exist_ok=True)
    # Stage every skill first, so a failed copy never removes an installed one.
    staged = []
    try:
        for s in SKILLS:
            tmp = dest / f".{s}.tmp"
            _remove(tmp)
            shutil.copytree(ROOT / "skills" / s, tmp,
                            ignore=shutil.ignore_patterns("__pycache__"))
            staged.append((s, tmp))
    except OSError as e:
        for _, tmp in staged:
            _remove(tmp)
        _remove(dest / f".{SKILLS[len(staged)]}.tmp")
        print(f"error: copy failed, nothing was replaced: {e}", file=sys.stderr)
        return 1
    # all six together: sub-skills reference ../soc2/
    for s, tmp in staged:
        out = dest / s
        old = dest / f".{s}.old"
        _remove(old)
        if out.exists() or out.is_symlink():
            os.replace(out, old)
        os.replace(tmp, out)
        _remove(old)
        print(f"installed {s} -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
