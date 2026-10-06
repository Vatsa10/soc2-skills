---
name: soc2
description: SOC 2 router for Type 1 and Type 2 across the Trust Services Criteria (Security, Availability, Processing Integrity, Confidentiality, Privacy). Use when the user mentions SOC 2, compliance, an auditor, a customer asking for SOC 2, an enterprise security review or security questionnaire, or designs a system that handles invoices, billing, payments or a data pipeline. Also use when .soc2/state.json exists. Scans the repo, picks the right phase skill each turn, and chains skills for multi-phase requests. When no .soc2/state.json exists and the user is designing a system, offer once to design it SOC 2-ready.
---

# SOC 2 Router

This skill prepares for a SOC 2 audit; it is not an attestation. Only a licensed CPA firm can issue a SOC 2 Type 1 or Type 2 report.

This skill does not do the compliance work itself. It decides which phase skill should handle the current turn, announces that choice, and hands off.

## Every turn

Do all five steps on every user turn, not only the first.

1. **Read state.** If `.soc2/state.json` exists in the user's repo, read it. Anything already answered there is never asked again.
2. **Scan.** Resolve `../soc2` against the directory containing this SKILL.md (not the shell's cwd). Run `python <that absolute path>/scripts/scan.py <repo root> --if-stale` and read the JSON it prints. Use `python3` if `python` is missing. On Windows set `PYTHONIOENCODING=utf-8`. The scanner caches to `.soc2/scan.json` and re-scans only when files are newer than the cache; pass `--write` to force a refresh when the user asks for a re-scan. Exit code 2 means a bad path: fix the path and retry.
3. **Classify.** Pick the phase using `references/routing.md` (intent first, scan signals second).
4. **Announce.** Print one line: `→ <skill> (<reason>)`, for example `→ soc2-architect (empty repo, design intent)`. The user can override it.
5. **Hand off.** Read the target skill's file at `../<skill>/SKILL.md` and follow it for the rest of the turn.

Route targets: `soc2-architect`, `soc2-type1-readiness`, `soc2-type2-operations`, `soc2-audit`, `soc2-policies`.

Skills read `references/control-index.md` first and open full entries in `references/control-catalog.md` only for the controls they evaluate (search `### <ID>`). For GCP or Azure, use `references/cloud-equivalents.md`.

## First run

If `.soc2/state.json` does not exist, or lacks any of the keys below, ask first and write afterwards. Ask only for the missing keys, in ONE message with at most 4 plain-language questions:

1. **Report type** (`report_type`: `type1` or `type2`). No default. Explain in three lines:
   - Type 1: a snapshot. Are the controls designed and in place on one date?
   - Type 2: a movie. Did the controls keep working over a period, usually 3 to 12 months?
   - Ask your customer which one they accept. Rule of thumb: first report, or a deal is waiting, take Type 1 now and Type 2 next; if the customer demands Type 2, go straight to it.
2. **Date.** Type 1: the as-of date (`type1_report_date`). Type 2: the start and end of the observation window (`audit_period`). Do not ask for `type1_report_date` when `report_type` is `type2`, unless the user asks for a Type 1 report too.
3. **Cloud(s)** (`system.cloud`): AWS, GCP, Azure, other, or none yet.
4. **Company name, owner, team size** (`system.company`, `system.owner`, `system.workforce`).

Offer the TSC scope inside question 1's message, not as a fifth question: Security is the default and always in scope. Add one line each for the others: Availability (uptime and recovery promises), Processing Integrity (data processed completely and accurately, such as invoices and payments), Confidentiality (protecting data marked confidential), Privacy (personal information handled per your notice). Anything the user does not narrow stays at the Security default only after they accept it.

Write `.soc2/state.json` (creating the `.soc2/` folder) only with the user's confirmed answers or their explicit acceptance of a default. Never pre-fill a key with an unconfirmed default. A key the user skipped stays absent, so it is asked again next time. Sub-skills never re-ask a key present in state; invoked on their own they ask only the missing keys, in the same plain wording. Schema, all keys shown for reference:

```json
{
  "tsc_scope": ["security","availability","processing_integrity","confidentiality","privacy"],
  "report_type": "type2",
  "audit_period": {"start": "2027-01-01", "end": "2027-06-30"},
  "type1_report_date": "2026-12-15",
  "system": {
    "name": "", "company": "", "owner": "",
    "cloud": [], "type": "", "tenancy": "",
    "workforce": 0, "tools": [], "data_classes": []
  },
  "decisions": [{"control": "AC-02", "choice": "Okta MFA", "date": "2026-10-06", "adr": "docs/adr/0001-mfa.md"}],
  "completed": ["soc2-architect"],
  "next_report": "type2 after type1"
}
```

Notes on keys:
- `type1_report_date` appears only when `report_type` is `type1` or the user asks for a Type 1 report.
- `system.cloud` is an array of `aws`, `gcp`, `azure`, `other` (empty when none yet).
- `system.workforce` is the head count. "Small team" means `workforce` of 10 or fewer.
- `decisions[].adr` points to the decision record written by `soc2-architect`.
- `next_report` records the plan after this report, for example `type2 after type1`.
- The scanner caches signals in `.soc2/scan.json`, so `.soc2/` can appear before state.json is written. That cache holds signals only, never answers.

Write each later answer or decision back to state.json immediately, not at the end of the session. Never re-ask a key that is present; absent keys are unanswered.

## Period check (Type 2)

When `audit_period` is set, compare it to today and tell the user plainly:

- Window start is in the future: **pre-period readiness**. Report the dates each control's evidence must be live by. Do not simulate sampling.
- Window has started or ended and most controls fail: warn that the gaps cannot be backfilled, and offer a later window or a Type 1 first.

## Chaining

For multi-phase requests ("make us SOC 2 ready", "end to end", "do everything"), run the skills in this order, carrying each output into the next:

`soc2-architect` → `soc2-policies` → `soc2-type1-readiness` → `soc2-type2-operations`

Skip any skill already listed in `state.completed`, unless the user asks to redo it. Announce each step with the one-line route format as it starts. For `report_type: type1`, stop after `soc2-type1-readiness`. When a step is skipped (completed, or out of scope for the report type), print what was skipped and why, then offer to scaffold the work that remains (policies, IaC, CI evidence jobs). See `references/routing.md` for chain definitions.

`completed` never blocks a new request: if the user asks to add a component or redo a phase, run it, even when that skill is listed.

## Re-route

If the user's intent shifts mid-conversation (for example from design questions to "are we compliant?"), re-classify, announce the new route, and switch to that skill.

## Overrides

If the user names a skill (for example "use soc2-audit"), that wins over routing. Announce it as `→ <skill> (user override)`.

## Always mention

If the scan shows `secrets.hardcoded_hits > 0`, mention it briefly in whatever route you take, citing `AC-17 → CC6.1` (secrets management and no hardcoded credentials, per `references/control-catalog.md`). Never echo the secret value itself; give only file path and line (`scan.py --secrets` prints exactly that).

## Shared files

- `references/routing.md`: routing table, keywords, tie-breakers, chains, examples.
- `references/control-index.md`: one row per control (ID, title, TSC, frequency, owner, scan signals). Read this first.
- `references/control-catalog.md`: full control entries, including Type 1 pass and Type 2 pass.
- `references/cloud-equivalents.md`: AWS, GCP and Azure service names per control family.
- `references/tsc-criteria.md`: official criteria and points of focus.
- `scripts/scan.py`: repo signal scanner.
