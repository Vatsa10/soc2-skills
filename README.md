# SOC 2 Skills

> This skill prepares for a SOC 2 audit; it is not an attestation. Only a licensed CPA firm can issue a SOC 2 Type 1 or Type 2 report.

A pack of six skills for Claude Code and Codex that helps you design, implement, operate, audit, and document controls for SOC 2 Type 1 and Type 2 across all five Trust Services Criteria (Security, Availability, Processing Integrity, Confidentiality, Privacy).

## Skills

| Skill | Purpose |
| --- | --- |
| `soc2` | Router. Scans the repo, reads project state, picks the right phase skill each turn, chains skills for multi-phase requests. |
| `soc2-architect` | Design systems with controls built in (greenfield, new services, brainstorming). |
| `soc2-type1-readiness` | Point-in-time check that in-scope controls are suitably designed and implemented. |
| `soc2-type2-operations` | Keep controls operating and generating evidence across the audit period. |
| `soc2-audit` | Auditor-style gap assessment: findings, PBC evidence list, remediation plan. |
| `soc2-policies` | 18 core policy templates (small-team aware) mapped to TSC criteria and control IDs. |

All six must be installed together: the phase skills reference the shared control catalog in `../soc2/references/`.

## Install

Clone this repo, then:

```
python scripts/install.py --target claude   # copies to ~/.claude/skills/
python scripts/install.py --target codex    # copies to ~/.agents/skills/
python scripts/install.py --target claude --dest DIR   # custom directory
```

The installer replaces existing copies of these six skills only and leaves other skills untouched. Install all six together; installing a single skill is unsupported because the phase skills read the shared catalog in `../soc2/`.

Repo-local install (skills travel with one project): use `--dest <repo>/.claude/skills` for Claude Code or `--dest <repo>/.agents/skills` for Codex, for example `python scripts/install.py --target codex --dest ../my-app/.agents/skills`.

Claude Code plugin install from GitHub:

```
/plugin marketplace add Vatsa10/soc2-skills
/plugin install soc2-skills@soc2-skills
```

The repo carries `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` (version 0.2.0); `skills/` at the repo root is discovered automatically. Run `claude plugin validate .` before a release. It warns that the repo-level `CLAUDE.md` is not loaded as plugin context; that file is for contributors and the warning is harmless.

### Skill names

A plugin install namespaces the skills: `/soc2-skills:soc2`, `/soc2-skills:soc2-architect`, `/soc2-skills:soc2-type1-readiness`, `/soc2-skills:soc2-type2-operations`, `/soc2-skills:soc2-audit`, `/soc2-skills:soc2-policies`. Copied installs (user or repo-local) expose the bare names `/soc2`, `/soc2-audit`, and so on. In Codex, invoke a skill with `$soc2`. In every case, prompts that mention SOC 2 trigger the skills automatically from their descriptions.

### Codex: pointing your project at the pack

`AGENTS.md` in this repo only applies when you work inside this repo. In your own project, rely on skill discovery (installed under `~/.agents/skills` or `<repo>/.agents/skills`), or add this snippet to your project's `AGENTS.md`:

```
For SOC 2 or compliance work, use the `soc2` skill ($soc2); it routes to the other soc2-* skills.
```

### Windows

Set `PYTHONIOENCODING=utf-8` before running the scanner or installer (the default console encoding is cp1252 and fails on the first non-ASCII character). Use `python`; if it is missing, use `python3`.

## Usage

- "We are starting a SOC 2 Type 2 program, where do we begin?" The router asks the few questions it needs, then chains skills.
- "Design an auth service that will pass SOC 2." Routes to `soc2-architect`.
- "Are we SOC 2 compliant?" Routes to `soc2-audit`.
- "Generate our security policies." Routes to `soc2-policies`.

## How routing works

`soc2` is the entry point. Each turn it reads `.soc2/state.json` in your repo (never re-asking answered questions), scans the repo for control signals with `skills/soc2/scripts/scan.py`, and announces a one-line route to the next phase skill. Skills already in `state.completed` are skipped unless you ask to redo them; for `report_type: type1` the chain stops after readiness. State is written only with your confirmed answers. The scanner also caches its signals in `.soc2/scan.json`, so a `.soc2/` folder can appear in your repo on the first turn, before any state is written; add it to version control or `.gitignore` as you prefer. The schema also has optional `system.company` and `system.owner` keys, used by `soc2-policies` to fill policy headers.

## Tests

```
python -m unittest discover tests -v
```

Stdlib only, no dependencies.

## Credits and license

MIT, see `LICENSE`. Attribution for the projects this pack drew ideas from is in `THIRD_PARTY_NOTICES.md`.
