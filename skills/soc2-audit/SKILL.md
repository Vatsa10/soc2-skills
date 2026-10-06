---
name: soc2-audit
description: Run an auditor-style SOC 2 gap assessment (Type 1 or Type 2) of a repo/system against all in-scope Trust Services Criteria, producing findings, a PBC evidence request list, and a remediation plan. Use when the user asks for an audit, gap analysis, compliance check, or 'are we SOC 2 compliant'.
---

# SOC 2 Audit (gap assessment)

This skill prepares for a SOC 2 audit; it is not an attestation. Only a licensed CPA firm can issue a SOC 2 Type 1 or Type 2 report.

Never state or imply that the system "is SOC 2 compliant" or "passed". Report readiness against the catalog only.

## Inputs

Paths are relative to this skill folder; the shared files live in the sibling `soc2` skill.

- Catalog: `../soc2/references/control-catalog.md` (every control, Pass rule, Type 1 test, Type 2 test, Evidence, sampling guide)
- Criteria: `../soc2/references/tsc-criteria.md`
- Scanner: `../soc2/scripts/scan.py`
- State: `.soc2/state.json` in the user's repo (`tsc_scope`, `report_type`, `audit_period`, `system`, `decisions`, `completed`). Read it first; do not re-ask anything already answered. Ask only for missing scope items.
- Existing `docs/soc2/*` and `docs/policies/*` in the user's repo.

## Severity rubric

- High: no control exists for a criterion in scope; hardcoded secrets; no logging (no security event logging or audit trail).
- Medium: control partly designed or implemented; evidence is manual-only or not repeatable.
- Low: control works but documentation is missing, stale, or unapproved.

## Procedure

1. Load state. Confirm `tsc_scope`, `report_type`, and (Type 2) `audit_period`. If absent, ask briefly and write them to state. Write only confirmed answers, per the router's First-run rule (`../soc2/SKILL.md`): never pre-fill an unconfirmed default, and leave skipped keys absent.
2. Scan: run `python ../soc2/scripts/scan.py <repo_path> --if-stale` (path relative to this skill folder). It always prints JSON, reuses the `.soc2/scan.json` cache unless tracked files changed, and rewrites it when they did. Scan output is signals only, never a verdict.
3. Select every catalog control in scope under the catalog's Scope selection rule (`../soc2/references/control-catalog.md`): a control is in scope when any criterion on its `TSC:` line belongs to an in-scope category by series (CC → security, A1 → availability, PI1 → processing_integrity, C1 → confidentiality, P → privacy), and whose `Applies when` is true. Mark the rest N/A with a one-line reason.
4. For each selected control, in catalog order:
   - Gather evidence: the scan signals listed on the control, then read the code, IaC, CI config, and documents that confirm or contradict them.
   - Apply the control's `Pass rule` exactly. For Type 1, use the Type 1 test column at single-instance, as-of-date scope and ignore the Pass rule's sampling language. For Type 2, use the Type 2 test column with period-wide evidence and sampling. Do not invent criteria.
   - Rate PASS, PARTIAL, FAIL, or N/A. A signal alone is at most "likely implemented": mark PARTIAL and request evidence in the PBC list unless the code or a document proves it.
   - Every non-PASS control becomes a finding with severity from the rubric. Cite `control ID → TSC criterion` (for example `AC-17 → CC6.1`, taking the criterion from that control's `TSC` field).
5. Type 2 additions, per control:
   - Evidence continuity: confirm evidence would exist for the whole period, not just now. Check for a control that has not yet fired in the period, a missed cycle (quarterly, monthly), a gap in continuous logging, or a mid-period change.
   - Sampling simulation: take the control's frequency, use the catalog sampling table to pick a sample size, choose samples spread across the period (first month included, not only the latest), and test each against the Pass rule. Any sample that would fail goes in "Exceptions likely".
6. Build the PBC list from each evaluated control's `Evidence` field: request, control IDs, owner, due date. Merge duplicates so one artifact serves several controls.
7. Build the 30/60/90 day roadmap: High first, then Medium, then Low.
8. Fill `references/report-template.md` and write the result to `docs/soc2/audit-report.md` in the user's repo (create the folder if needed). Keep the disclaimer at the top and bottom. Omit the Exceptions-likely section for Type 1.
9. Update `.soc2/state.json`: add `soc2-audit` to `completed` and record any scope decisions made. Do not remove existing entries.
10. Tell the user the headline counts, the top three findings, and where the report is.

## Hard rules

- `secrets.hardcoded_hits > 0` is always a High finding against `AC-17 → CC6.1`. Locate the hits without printing them: use a file-and-line-only search (for example `grep -rlE <pattern> .` for files, or `grep -rnE <pattern> . | cut -d: -f1,2`, never the full matching line), and redact any matched text before it enters the transcript or report. Report file path and line number only. The report, chat reply, and state file must never reproduce a secret value, not even partially. Recommend rotating every exposed credential and removing it from git history.
- Every finding and recommendation cites a catalog control ID and a TSC criterion. Every ID must exist in the catalog; look it up, never guess.
- Pass/fail comes only from the catalog `Pass rule`.
- Do not edit the user's code or infrastructure during an audit. Findings and recommendations only; offer `soc2-type1-readiness` or `soc2-type2-operations` for fixes and `soc2-policies` for missing policy documents.
- Write findings as condition / criteria / cause / effect: what was observed, which control and criterion it falls short of, why, and the consequence.
- Phrase uncertainty plainly ("not evidenced in the repository") rather than asserting a failure the repository cannot show.

## Chaining

After the report, suggest the next skill: High findings in code or infrastructure go to `soc2-type1-readiness`; missing evidence cadence goes to `soc2-type2-operations`; missing policies go to `soc2-policies`.
