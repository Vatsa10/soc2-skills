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

## Offer (design intent, no SOC 2 mention)

If no `.soc2/state.json` exists and the user is designing a system without mentioning SOC 2, send ONE line only: "Want me to design this SOC 2-ready? (yes/no)". No intake questions and no route line until they say yes. On no, write `soc2_offer: "declined"` to state and never offer again. Still mention secrets per "Always mention".

## First run

If state is missing keys, ask first and write afterwards, for the missing keys only, in ONE short message (at most 3 questions, plain words):

1. **Report type** (`report_type`: `type1` or `type2`). No default. Type 1 is a snapshot: controls are designed and in place on one date. Type 2 is a movie: they kept working over 3 to 12 months. Ask your customer which they accept; first report or a deal waiting means Type 1 now, Type 2 next. Accept a plain-English answer, echo it back as the stored value.
2. **Cloud(s)** (`system.cloud`): AWS, GCP, Azure, other, or none yet.
3. **Names and size**: the product or system name, company, who owns SOC 2, team size (`system.name`, `system.company`, `system.owner`, `system.workforce`).

Add one line on scope: "Security only is fine for a first report; tell me if customers also expect uptime, accurate processing, confidentiality or privacy." Offer the full category list only when the user asks or the data suggests more (invoices, payments, personal data). Security is always in scope; `tsc_scope` is written only after the user accepts it.

Then, once `report_type` is known, ask the date in the next turn: Type 1 as-of date (`type1_report_date`), or the Type 2 window (`audit_period`). Do the deadline arithmetic in `references/routing.md` and state the dates. Never ask `type1_report_date` for `type2` unless the user wants a Type 1 too.

If `report_type` is still absent when a phase needs it, ask that one question first (two options), then continue. A value the user states in their own words is confirmed: write it and echo it back. A value inferred from the repo is a suggestion, confirmed in one clause ("looks like AWS, right?"). Never pre-fill an unconfirmed default; a skipped key stays absent. Sub-skills never re-ask a key present in state; run alone they ask only missing keys in the same words. `state.system.cloud` always overrides `scan.cloud`.

Schema (router owns; all keys shown for reference):

```json
{
  "tsc_scope": ["security","availability","processing_integrity","confidentiality","privacy"],
  "report_type": "type2",
  "audit_period": {"start": "2027-01-01", "end": "2027-06-30"},
  "audit_period_decision": "keep",
  "type1_report_date": "2026-12-15",
  "system": {"name": "", "company": "", "owner": "", "cloud": [], "type": "", "tenancy": "",
             "workforce": 0, "tools": [], "data_classes": []},
  "decisions": [{"control": "AC-02", "choice": "Okta MFA", "date": "2026-10-06", "adr": "0001"}],
  "excluded": [{"control": "AV-03", "reason": "Availability out of scope", "date": "2026-10-06"}],
  "completed": ["soc2-architect"],
  "next_report": "type2 after type1",
  "soc2_offer": "declined"
}
```

- `type1_report_date` only when `report_type` is `type1` or a Type 1 is requested.
- `system.cloud`: array of `aws`, `gcp`, `azure`, `other` (empty if none yet). "Small team" means `workforce` of 10 or fewer.
- `decisions[].adr` is the 4-digit ADR number string, never a path. `excluded[]` is written by `soc2-architect`; later skills show those controls as n/a with the stored reason and never re-list them.
- `audit_period_decision`: `keep`, `moved` or `type1-first`, set when the window start or end is before today.
- `soc2_offer`: `declined` after a no to the Offer. `next_report` records the plan after this report.
- `.soc2/scan.json` caches signals only, never answers. Write each answer or decision to state immediately.

## Period check (Type 2)

Compare `audit_period` to today and say plainly:

- Start in the future: **pre-period readiness**. Report the dates each control's evidence must be live by. No sampling simulation.
- Start or end before today: ask ONE confirm line (keep the window, move it, or Type 1 first), record `audit_period_decision`. If most controls fail, warn that gaps cannot be backfilled and offer a later window or a Type 1 first.

## Chaining

For "make us SOC 2 ready", "end to end", "do everything": `soc2-architect` → `soc2-policies` → `soc2-type1-readiness` → `soc2-type2-operations`. Carry each output forward. Announce each step with the route line. For `type1`, stop after type1-readiness. Skip skills in `state.completed` unless the user asks to redo them; when skipping, say where the output is and offer regenerate, review or approve (policies). Policies questions run as their own turn, not folded into another step. At the end print what was skipped using the "Not run" template in `references/routing.md` and offer to scaffold. `completed` never blocks a new component or redo request.

## Re-route and overrides

If intent shifts mid-conversation, re-classify, announce, switch. If the user names a skill, that wins: `→ <skill> (user override)`.

## Always mention

If the scan shows `secrets.hardcoded_hits > 0`, mention it briefly on any route, citing `AC-17 → CC6.1`. Never echo the secret. Run `scan.py --secrets` for `path:line kind` per hit. `scan.py --scope <tsc list>` prints the in-scope control IDs, one per line, so skills need not read the whole index.

## Shared files

- `references/routing.md`: routing table, keywords, tie-breakers, chains, deadline arithmetic, templates, examples.
- `references/control-index.md`: one row per control. Read first. `references/control-catalog.md`: full entries (Type 1 pass, Type 2 pass). `references/cloud-equivalents.md`: AWS, GCP, Azure names. `references/tsc-criteria.md`: official criteria.
- `scripts/scan.py`: repo signal scanner.
