---
name: soc2-audit
description: "Run an auditor-style SOC 2 gap assessment (Type 1 or Type 2) of a repo/system against the in-scope Trust Services Criteria, producing ranked findings, a PBC evidence request list, a remediation plan, and draft system description and management assertion. Use when the user asks for an audit, gap analysis, compliance check, 'are we SOC 2 compliant', 'Type 2 readiness', 'what will the auditor ask us for' (PBC list), or a remediation plan or roadmap (for example a 2-week or 30/60/90 plan)."
---

# SOC 2 Audit (gap assessment)

This skill prepares for a SOC 2 audit; it is not an attestation. Only a licensed CPA firm can issue a SOC 2 Type 1 or Type 2 report.

Never state or imply that the system "is SOC 2 compliant" or "passed". Report readiness against the catalog only. The severity rubric below is for readiness; auditors report deviations and may qualify their opinion, they do not use these tiers.

## Inputs

Resolve `../soc2` against the directory containing this SKILL.md (not the shell's cwd). Call that absolute path `<soc2>`.

- Control index: `<soc2>/references/control-index.md`. Read it FIRST. Open full catalog entries in `<soc2>/references/control-catalog.md` only for controls you evaluate (search for `### <ID>`); never read the whole catalog at once.
- Criteria: `<soc2>/references/tsc-criteria.md`. Cloud equivalents: `<soc2>/references/cloud-equivalents.md`.
- Scanner: `<soc2>/scripts/scan.py`.
- State: `.soc2/state.json` in the user's repo (`tsc_scope`, `report_type`, `audit_period`, `type1_report_date`, `system{... cloud[] ... workforce}`, `decisions`, `completed`). Never re-ask a key present in state. Ask only missing keys, in the router's plain wording (`<soc2>/SKILL.md`), and write only confirmed answers.
- Existing `docs/soc2/*` and `docs/policies/*` in the user's repo.
- Mode details: `references/audit-modes.md`. Templates: `references/report-template.md`, `references/system-description-template.md`, `references/management-assertion-template.md`.

## Modes

Pick one from the request and state, and say which you chose. Full instructions are in `references/audit-modes.md`.

- Full gap (default): every in-scope control, report per the template.
- Type 2 gap: full gap plus evidence continuity and sampling simulation ("Type 2 readiness", gap view).
- Pre-period readiness: forced when `report_type=type2` and `audit_period.start` is after today. Report evidence-live-by dates per control; no sampling simulation.
- PBC-only: "what will the auditor ask for". Build the PBC list from existing `docs/soc2/*` and the index; no full re-evaluation.
- Remediation plan: "plan", "roadmap", "2 week plan". Timeboxed plan (2-week, or 30/60/90) from the latest findings, re-running the gap assessment only if none exist.

Period check (Type 2): if the window has already started or ended and most evaluated controls are `missing`, warn plainly that evidence cannot be backfilled for the elapsed part, and offer a later window or a Type 1.

## Status and severity

Status per control: `designed` | `partial` | `missing` | `needs-evidence` | `n/a` (reason required). A scan signal alone is at most `needs-evidence` unless code or a document proves it.

Severity per finding:
- Blocker: live exposure now: secrets in the repo, publicly exposed data, no logging, no backups of production data.
- High: a control for an in-scope criterion is missing on a live system, or cannot be backfilled for the Type 2 period.
- Medium: partial design, manual-only evidence. A control not yet built on a pre-production repo is at most Medium.
- Low: control works; documentation missing, stale, or unapproved.

Rank: Blockers first, then controls that cannot be backfilled for a Type 2 period (logging, scheduled reviews, backups), then by severity, clustering findings by control family.

## Procedure (full gap)

1. Load state and pick the mode. Confirm `tsc_scope`, `report_type`, and `audit_period` (Type 2) or `type1_report_date` (Type 1).
2. Scan: run `python <soc2>/scripts/scan.py <repo root> --if-stale` (use `python3` if `python` is missing; on Windows set `PYTHONIOENCODING=utf-8`). Signals only, never a verdict.
3. Select controls from the index: in scope when any criterion on its TSC line belongs to an in-scope category (CC → security, A1 → availability, PI1 → processing_integrity, C1 → confidentiality, P → privacy) and its `Applies when` holds. Mark the rest `n/a` with a one-line reason; these feed the system description's "criteria not relevant" section.
4. For each selected control, open its catalog entry. Gather evidence (its scan signals, then code, IaC, CI, documents). Judge Type 1 against `Type 1 test` and `Type 1 pass` (single instance, as of date). Judge Type 2 against `Type 2 test` and `Type 2 pass` (whole period). Do not invent criteria.
5. Every non-`designed` control becomes a finding written as condition / criteria / cause / effect, citing `<ID> → <TSC>` with the TSC taken from that control's catalog TSC line (for example `AC-17 → CC6.1`, `AC-02 → CC6.1`, `CHG-04 → CC8.1`).
6. Tailor every recommendation to `system.cloud`: use the matching column of `cloud-equivalents.md`, never an AWS service for a GCP or Azure system.
7. Type 2 gap mode only: evidence continuity and sampling simulation per `references/audit-modes.md`.
8. PBC list: from each evaluated control's `Evidence` field, grouped by source system (IdP, cloud console, Git host, HR system, ticketing, vendor files) with a merge key so one artifact serves several controls. For each system-generated population record the source system and the query or report parameters so the auditor can re-run it (IPE). Always include the "Report deliverables you own" rows.
9. Remediation roadmap by rank. Add a "Do today" line whenever a Blocker exists (for example: rotate the exposed key; enable backups on the production database).
10. Write `docs/soc2/audit-report.md` from `references/report-template.md`. Also write drafts `docs/soc2/system-description.md` and `docs/soc2/management-assertion.md` from the two templates when they do not exist (if they exist, report gaps against the template; never overwrite). Keep the disclaimer at top and bottom of each.
11. Update `.soc2/state.json`: append `soc2-audit` to `completed`; record scope decisions. Never remove entries.
12. Tell the user: mode, headline counts, the "Do today" line, top three findings, and file paths.

## Report deliverables you own

A SOC 2 report contains documents written by management, not the auditor. Flag each as a PBC row and offer the drafts:
- System description (Section III, AICPA DC 200, DC1-DC9), kept current by GOV-13 → CC2.2. GOV-08 is the inventory it draws on.
- Management's written assertion (Section II, AT-C 205), plus the management representation letter; the CPA firm usually supplies its own wording.
- Subservice organizations and CSOCs, carve-out (default) or inclusive method (GOV-11 → CC9.2). Inclusive requires the subservice organization's own assertion and auditor access; carve-out excludes its controls and lists the CSOCs you rely on.
- Your own CUECs for customers (GOV-12 → CC2.3).
- Your own bridge (gap) letter for customers between your report's period end and the next report: signed by your management, not audited, usually covering 3 months or less.

## Hard rules

- Secrets: `secrets.hardcoded_hits > 0` is a Blocker against `AC-17 → CC6.1`. Get locations only with `python <soc2>/scripts/scan.py <repo root> --secrets` (prints `path:line` and a count, never the value). Never print, quote, or partially reproduce a secret in the chat, report, or state. Recommend: rotate or revoke, remove from code, purge from git history, and move to a secret manager.
- "It's just a test key": still rotate or revoke it, remove it, and purge it from history; a test key in history trains the habit and is often valid somewhere. Downgrade below Blocker only with proof the key is invalid (provider shows it revoked, or it is a documented fake format), recorded with the owner and date. Never echo it to check.
- Every finding and recommendation cites a catalog control ID that exists in the index; look it up, never guess.
- Do not edit the user's code or infrastructure. Offer `soc2-type1-readiness` or `soc2-type2-operations` for fixes and `soc2-policies` for missing policies. The only files this skill writes are the three docs above and state.
- Templates are drafts for management and CPA review, never final report text.
- Phrase uncertainty plainly ("not evidenced in the repository").

## Chaining

Blockers and High code or infrastructure findings → `soc2-type1-readiness`; missing evidence cadence → `soc2-type2-operations`; missing policies → `soc2-policies`.
