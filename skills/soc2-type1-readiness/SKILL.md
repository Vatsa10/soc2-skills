---
name: soc2-type1-readiness
description: Assess SOC 2 Type 1 readiness, i.e. whether in-scope controls are suitably designed and implemented at a point in time. Use when code/infrastructure exists and the user asks if controls are in place, wants a readiness check, or is preparing for a Type 1 report.
---

# SOC 2 Type 1 Readiness

This skill prepares for a SOC 2 audit; it is not an attestation. Only a licensed CPA firm can issue a SOC 2 Type 1 or Type 2 report.

A Type 1 report covers whether controls are suitably designed and implemented at a single point in time. This skill checks each in-scope control against the catalog's `Type 1 test` and `Pass rule` and writes a readiness matrix. It works the same in Claude Code and Codex.

## Inputs

- Control catalog: `../soc2/references/control-catalog.md` (fields: TSC, Applies when, Implement, Scan signals, Type 1 test, Type 2 test, Evidence, Pass rule). Only the `Type 1 test` column applies here.
- Scanner: `../soc2/scripts/scan.py`, which emits repository signals as JSON.
- Project state: `.soc2/state.json` in the user's repo.

## Procedure

1. **Load scope and report date from state.** Read `.soc2/state.json` and take `tsc_scope` (lowercase keys: `security`, `availability`, `processing_integrity`, `confidentiality`, `privacy`). Never re-ask anything already in state. If the file is missing or `tsc_scope` is empty, ask for the TSC scope once (Security is always in scope) and write it back. Type 1 is as of a single date: ask once for the report (as-of) date, store it in state as `type1_report_date` (YYYY-MM-DD), and reuse it afterward. `audit_period` is a Type 2 field and is ignored here.
2. **Select controls.** Read the catalog and keep every control whose category is in scope. The category is the `Category:` value after `|` in the TSC field (Security, Availability, Processing Integrity, Confidentiality, Privacy), matched to the lowercase state keys. Check each control's `Applies when`; if it does not apply, record it as N/A with a reason instead of scoring it.
3. **Scan, then confirm in the code.** Run `python ../soc2/scripts/scan.py <repo> --if-stale` (the path assumes the working directory is this skill's folder; otherwise resolve `../soc2/scripts/scan.py` against this SKILL.md's directory, since skills install as sibling folders) and parse the JSON. For each control, read its `Scan signals`, then open the relevant code, IaC, CI config, or policy files to confirm. Signals are hints, not proof.
4. **Assign a status** by evaluating the catalog `Type 1 test`: the design is adequate AND the control is implemented, shown by at least one instance as of the report date. Apply the `Pass rule` at that single-instance, as-of-date scope; ignore sampling language (such as "every sampled hire") and the `Type 2 test` column, which cover operation over a period.
   - `designed`: the Type 1 test is satisfied, the Pass rule holds at single-instance scope, and you saw the supporting file, config, or document.
   - `partial`: the control exists but the Pass rule is not fully met (for example MFA exists but is optional).
   - `missing`: no implementation found where one should be visible.
   - `needs-evidence`: an organizational control not visible in the repo (for example background checks, `GOV-02`); the user must supply evidence.
5. **Write a concrete fix** for every control that is not `designed`: name the file and the change (for example, "add `.github/CODEOWNERS` covering `infra/`"). For `needs-evidence`, name the artifact to collect.
6. **Cite IDs in arrow form.** Every finding, fix, and matrix row cites `<CONTROL-ID> → <TSC ID>`, for example `AC-02 → CC6.1`. A control with several criteria lists each pair (`AC-02 → CC6.1`, `AC-02 → CC6.2`), taken from the catalog.

## Rules

- Never mark a control `designed` from a scan signal alone. If a signal is present but you have not yet confirmed it in code or config, read the code first. If the control can live in the repo and the signal is confirmed only in part, mark `partial`; if the control lives outside the repo, mark `needs-evidence`; if there is no signal and no implementation, mark `missing`.
- Use only the catalog's Type 1 test and Pass rule. Do not invent criteria or soften a rule.
- Cite `file:line` where you can; otherwise name the signal key and the file you read.

## Output

Write `docs/soc2/type1-readiness.md` in the user's repo with:

1. Report (as-of) date, scope (from state), and the disclaimer above.
2. **Summary counts per TSC category**: a table with one row per in-scope category and columns `designed | partial | missing | needs-evidence | N/A`.
3. **Control matrix**, one row per in-scope control:

   | ID | Title | TSC | Status | Basis (file:line or signal) | Fix |
   |---|---|---|---|---|---|
   | AC-02 | MFA enforced for all workforce access | AC-02 → CC6.1, AC-02 → CC6.2 | partial | ... | ... |

   The TSC column must use the `ID → TSC` arrow form for every criterion.

4. **Needs human evidence**: a list of every `needs-evidence` control with the artifact to collect and a suggested owner.

## Finish

Add `soc2-type1-readiness` to `state.completed` in `.soc2/state.json` (keep the existing entries, no duplicates) and give the user the summary counts plus the top fixes. Suggest `soc2-type2-operations` once the matrix is mostly `designed`.
