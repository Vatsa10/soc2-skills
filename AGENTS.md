# SOC 2 skill pack (Codex)

This repository is a pack of six skills for SOC 2 Type 1 and Type 2 work across all five Trust Services Criteria. Codex discovers skills from `.agents/skills` (repo) or `~/.agents/skills` (user); `python scripts/install.py --target codex` installs them to the user directory (add `--dest <repo>/.agents/skills` for a repo-local install). In your own project, rely on skill discovery or add one line to its AGENTS.md: use the `soc2` skill (`$soc2`) for SOC 2 work. On Windows set `PYTHONIOENCODING=utf-8` when running scripts.

For any SOC 2 / compliance / architecture work, read `skills/soc2/SKILL.md` first and follow it. It routes to the right phase skill and keeps project state in `.soc2/state.json`.

Skills (all under `skills/`; install all six together, sub-skills reference `../soc2/`):
- `soc2`: router
- `soc2-architect`: design controls in
- `soc2-type1-readiness`: point-in-time design check
- `soc2-type2-operations`: operating evidence over the audit period
- `soc2-audit`: auditor-style gap assessment
- `soc2-policies`: 18 core policy templates (small-team aware)

Tests: `python -m unittest discover tests -v` (stdlib only).
