---
name: soc2-type1-readiness
description: Assess SOC 2 Type 1 readiness, i.e. whether in-scope controls are suitably designed and implemented at a point in time, or run a quick implementation check of what is built so far. Use when code/infrastructure exists and the user asks if controls are in place, wants a readiness check or "check what we built", or is preparing for a Type 1 report. On an empty or infrastructure-less repo it returns a build-first roadmap instead of a long matrix.
---

# SOC 2 Type 1 Readiness

This skill prepares for a SOC 2 audit; it is not an attestation. Only a licensed CPA firm can issue a SOC 2 Type 1 or Type 2 report.

A Type 1 report covers whether controls are suitably designed and implemented at a single point in time. This skill checks each in-scope control against the catalog's `Type 1 test` and `Type 1 pass` fields and writes a readiness result. It works the same in Claude Code and Codex.

## Inputs

- Control index: `../soc2/references/control-index.md` (one row per control: ID, Title, TSC, Category, Frequency, Owner, Scan signals). Read this first. It is enough to select controls and to group them.
- Control catalog: `../soc2/references/control-catalog.md`. Never read it whole. For each control you actually evaluate, search for its heading `### <ID>` and read that one entry. Fields: TSC, Applies when, Implement, Scan signals, Frequency, Owner, Type 1 test, Type 2 test, Evidence, Type 1 pass, Type 2 pass. Only `Type 1 test` and `Type 1 pass` apply here.
- Cloud service names for AWS, GCP, and Azure: `../soc2/references/cloud-equivalents.md`. Use the cloud(s) in `system.cloud`.
- Scanner: `../soc2/scripts/scan.py`, which emits repository signals as JSON.
- Project state: `.soc2/state.json` in the user's repo.

Resolve every `../soc2/...` path against the directory containing this SKILL.md, not the shell's cwd. On Windows set `PYTHONIOENCODING=utf-8` and read files as UTF-8 (the catalog contains non-ASCII arrows).

## Procedure

1. **Load state; never re-ask what is there.** Read `.soc2/state.json` and take `tsc_scope` (lowercase keys: `security`, `availability`, `processing_integrity`, `confidentiality`, `privacy`), `report_type`, `system` (name, cloud, workforce, tools), and `decisions`. If the file is missing or `tsc_scope` is empty, ask once for the TSC scope in plain words (Security is the default and is always in scope; one line each for availability, processing integrity, confidentiality, privacy) and write it back. Write only confirmed answers, per the router's First-run rule (`../soc2/SKILL.md`): never pre-fill an unconfirmed default, and leave skipped keys absent. A key present in state is never asked again; when invoked standalone ask only the missing keys.
   - **Report date.** Ask for `type1_report_date` (YYYY-MM-DD) only when `report_type` is `type1` or the user asks for a Type 1 report. Guidance to give: pick an as-of date roughly 4 to 6 weeks after the controls are live and after a CPA firm is engaged, so each control has existing evidence and the firm agrees the date. Store it and reuse it.
   - **If `report_type` is `type2`** (and the user did not ask for a Type 1 report), do not ask for or write `type1_report_date`. Label the output "Implementation check as of <today's date>" instead of "Type 1 readiness", and note that `audit_period` governs the real report. If the Type 2 window has already started or ended and most controls will fail, say so plainly in the summary and offer a later window or a Type 1 report first.
2. **Select controls from the index.** Keep every control in scope by the Scope selection rule (in `../soc2/references/control-catalog.md`): a control is in scope when any criterion on its TSC line belongs to an in-scope category by series (CC → security, A1 → availability, PI1 → processing_integrity, C1 → confidentiality, P → privacy). For each, open its catalog entry (`### <ID>`) only when you evaluate it, and check `Applies when`.
   - **N/A rule.** A control is `n/a` only when its `Applies when` condition is false for this system (for example no personal information, no on-premise office, no customer-facing availability commitment). Record the control as `n/a` with a one-line reason. A control that applies but is not built is `missing`, not `n/a`.
3. **Scan, then confirm in the code.** Run the scanner (resolve `../soc2` against the directory containing this SKILL.md; run `python <that absolute path>/scripts/scan.py <repo root> --if-stale`, use python3 if python is missing; on Windows set PYTHONIOENCODING=utf-8) and parse the JSON. For each control, read its `Scan signals`, then open the relevant code, IaC, CI config, or policy files to confirm. Signals are hints, not proof.
4. **Choose the output branch.**
   - **Empty or no-IaC branch.** If the scan finds no IaC, no CI configuration, and little or no application code (a new or documentation-only repo), do not write a control-by-control matrix. Write a **build-first roadmap** of about 15 controls instead (below).
   - **Otherwise** write the full result below.
5. **Assign a status** by evaluating the control's `Type 1 test` and `Type 1 pass`: the design is adequate AND the control is implemented, shown by one instance as of the report date (or today for an implementation check). Ignore sampling language and the `Type 2 test` and `Type 2 pass` fields, which cover operation over a period. Vocabulary:
   - `designed`: the Type 1 pass holds at single-instance scope and you saw the supporting file, config, or document.
   - `partial`: the control exists but the Type 1 pass is not fully met (for example MFA exists but is optional).
   - `missing`: no implementation found where one should be visible.
   - `needs-evidence`: an organizational control not visible in the repo (for example background checks, `GOV-02`); the user must supply evidence.
   - `n/a`: `Applies when` is false, with a reason.
   Work in this order: first the **code-visible controls** (those with Scan signals other than `none`), confirmed in the repo; then the **org-only controls** (Scan signals `none`: HR, training, policies, vendor reviews, board oversight), which you do not score one by one but group by owner and by artifact to collect as `needs-evidence`.
6. **Write a concrete fix** for every code-visible control that is not `designed`: name the file and the change (for example, "add `.github/CODEOWNERS` covering `infra/`"). For `needs-evidence`, name the artifact to collect and the owner role from the control's `Owner` field.
7. **Cite IDs in arrow form.** Every finding, fix, and matrix row cites `<CONTROL-ID> → <TSC ID>`, for example `AC-02 → CC6.1`. The TSC ID is taken from that control's catalog TSC line; a control with several criteria lists each pair.

## Rules

- Never mark a control `designed` from a scan signal alone. If a signal is present but you have not confirmed it in code or config, read the code first. If the control can live in the repo and the signal is confirmed only in part, mark `partial`; if the control lives outside the repo, mark `needs-evidence`; if there is no signal and no implementation, mark `missing`.
- Use only the catalog's `Type 1 test` and `Type 1 pass`. Do not invent criteria or soften a rule.
- Cite `file:line` where you can; otherwise name the signal key and the file you read.
- Count each control once. The **primary criterion** is the first criterion on its TSC line; its series decides the category row (CC → Security, A1 → Availability, PI1 → Processing integrity, C1 → Confidentiality, P → Privacy). The total of every status column across all rows equals the number of controls evaluated, with no double counting.

## Output

Write `docs/soc2/type1-readiness.md` in the user's repo (title it "Implementation check as of <date>" when `report_type` is `type2` and no Type 1 report was requested).

### Full result (repo has IaC, CI, or application code)

1. Report (as-of) date or check date, scope (from state), and the disclaimer above.
2. **Summary counts by primary criterion category**: one row per in-scope category with columns `designed | partial | missing | needs-evidence | n/a | Total`, plus a final **Total** row. The grand total equals the number of in-scope controls.
3. **Code-visible controls matrix**, one row per control:

   | ID | Title | TSC | Status | Basis (file:line or signal) | Fix |
   |---|---|---|---|---|---|
   | AC-02 | MFA enforced for all workforce access | AC-02 → CC6.1 | partial | ... | ... |

   The TSC column uses the `ID → TSC` arrow form for every criterion on the control's TSC line.
4. **Needs human evidence**: org-only controls grouped by owner role, each with the artifact to collect. Group several controls under one artifact where one document covers them.
5. **N/A controls** with their reasons.

### Build-first roadmap (empty or no-IaC branch)

1. Header with the date, scope, the disclaimer, and one sentence: "No infrastructure or CI was found, so a control-by-control matrix would be all red; this is the order to build in."
2. A numbered list of about 15 controls to build first, chosen from the in-scope index rows: things that cannot be backfilled and that every later control depends on come first (identity with MFA and SSO, cloud audit trail and central logging with retention, branch protection with required review and CI, secrets management, encryption, backups, vulnerability scanning, incident response plan, then the org-only items an auditor asks about first: policies, access reviews, vendor inventory). For each: `<ID> → <TSC>`, one line on what to build (use the cloud names for `system.cloud`), and an owner role.
3. A line stating the number of in-scope controls not on the list and where to find them (`../soc2/references/control-index.md`).
4. Offer the next step: design the system with `soc2-architect` or scaffold the listed items, then re-run this check.

## Finish

Add `soc2-type1-readiness` to `state.completed` in `.soc2/state.json` (keep the existing entries, no duplicates) and give the user the summary counts (or the top five roadmap items) plus the top fixes. Suggest `soc2-type2-operations` once the matrix is mostly `designed`; for a Type 1 report remind the user that the CPA firm confirms the as-of date.
