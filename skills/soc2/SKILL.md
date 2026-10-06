---
name: soc2
description: SOC 2 router for Type 1 and Type 2 across all five Trust Services Criteria (Security, Availability, Processing Integrity, Confidentiality, Privacy). Use whenever the user mentions SOC 2, trust services criteria, compliance audits, auditors, compliant architecture, or brainstorms/designs a system in a repo containing a .soc2/ directory. Scans the repo, picks the right SOC 2 phase skill each turn, and chains skills for multi-phase requests.
---

# SOC 2 Router

This skill prepares for a SOC 2 audit; it is not an attestation. Only a licensed CPA firm can issue a SOC 2 Type 1 or Type 2 report.

This skill does not do the compliance work itself. It decides which phase skill should handle the current turn, announces that choice, and hands off.

## Every turn

Do all five steps on every user turn, not only the first.

1. **Read state.** If `.soc2/state.json` exists in the user's repo, read it. Anything already answered there is never asked again.
2. **Scan.** Run this shell command and read the JSON it prints:
   `python <this skill dir>/scripts/scan.py <repo> --if-stale`
   `<this skill dir>` is the folder containing this SKILL.md. `<repo>` is the user's project root. The scanner caches to `.soc2/scan.json` and re-scans only when files are newer than the cache; pass `--write` to force a refresh when the user asks for a re-scan. Exit code 2 means a bad path: fix the path and retry.
3. **Classify.** Pick the phase using `references/routing.md` (intent first, scan signals second).
4. **Announce.** Print one line: `→ <skill> (<reason>)`, for example `→ soc2-architect (empty repo, design intent)`. The user can override it.
5. **Hand off.** Read the target skill's file at `../<skill>/SKILL.md` and follow it for the rest of the turn.

Route targets: `soc2-architect`, `soc2-type1-readiness`, `soc2-type2-operations`, `soc2-audit`, `soc2-policies`.

## First run

If `.soc2/state.json` does not exist, create it (and the `.soc2/` folder) with this schema:

```json
{
  "tsc_scope": ["security","availability","processing_integrity","confidentiality","privacy"],
  "report_type": "type2",
  "audit_period": {"start": "", "end": ""},
  "system": {"name": "", "cloud": [], "data_classes": []},
  "decisions": [],
  "completed": []
}
```

Ask the user only these three things, in one message:

- `tsc_scope`: which Trust Services Criteria are in scope (default: all five).
- `report_type`: `type1` or `type2`.
- `audit_period`: start and end dates, asked only when `report_type` is `type2`. For `type1`, leave it empty.

Never re-ask a key that is already present and filled in. The phase skills fill in `system`, `decisions`, and `completed` as they work.

## Chaining

For multi-phase requests ("make us SOC 2 ready", "end to end", "do everything"), run the skills in this order, carrying each output into the next:

`soc2-architect` → `soc2-policies` → `soc2-type1-readiness` → `soc2-type2-operations`

Skip any skill already listed in `state.completed`, unless the user asks to redo it. Announce each step with the one-line route format as it starts. For `report_type: type1`, stop after `soc2-type1-readiness`. See `references/routing.md` for chain definitions.

## Re-route

If the user's intent shifts mid-conversation (for example from design questions to "are we compliant?"), re-classify, announce the new route, and switch to that skill.

## Overrides

If the user names a skill (for example "use soc2-audit"), that wins over routing. Announce it as `→ <skill> (user override)`.

## Always mention

If the scan shows `secrets.hardcoded_hits > 0`, mention it briefly in whatever route you take, citing the relevant control ID from `references/control-catalog.md`.

## Shared files

- `references/routing.md`: routing table, keywords, tie-breakers, chains, examples.
- `references/control-catalog.md`: single source of truth for controls and pass rules.
- `references/tsc-criteria.md`: official criteria and points of focus.
- `scripts/scan.py`: repo signal scanner.
