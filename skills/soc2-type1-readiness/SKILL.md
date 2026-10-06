---
name: soc2-type1-readiness
description: Assess SOC 2 Type 1 readiness: whether in-scope controls are suitably designed and implemented at a point in time. Use when code/infrastructure exists and the user asks if controls are in place, wants a readiness check, or is preparing for a Type 1 report.
---

# SOC 2 Type 1 Readiness

This skill prepares for a SOC 2 audit; it is not an attestation. Only a licensed CPA firm can issue a SOC 2 Type 1 or Type 2 report.

A Type 1 report covers whether controls are suitably designed and implemented at a single point in time. This skill checks each in-scope control against the catalog's `Type 1 test` and `Pass rule` and writes a readiness matrix. It works the same in Claude Code and Codex.

## Inputs

- Control catalog: `../soc2/references/control-catalog.md` (fields: TSC, Applies when, Implement, Scan signals, Type 1 test, Type 2 test, Evidence, Pass rule). Only the `Type 1 test` column applies here.
- Scanner: `../soc2/scripts/scan.py`, which emits repository signals as JSON.
- Project state: `.soc2/state.json` in the user's repo.

## Procedure

1. **Load scope from state.** Read `.soc2/state.json` and take `tsc_scope`. Never re-ask anything already in state. If the file is missing or `tsc_scope` is empty, ask for the TSC scope once (Security is always in scope) and write it back.
2. **Select controls.** Read the catalog and keep every control whose `Category` is in scope (Security, Availability, Processing Integrity, Confidentiality, Privacy). Check each control's `Applies when`; if it does not apply, record it as N/A with a reason instead of scoring it.
3. **Scan, then confirm in the code.** Run `python ../soc2/scripts/scan.py <repo> --if-stale` (path relative to this skill folder; use the installed location of the `soc2` skill if different) and parse the JSON. For each control, read its `Scan signals`, then open the relevant code, IaC, CI config, or policy files to confirm. Signals are hints, not proof.
4. **Assign a status** by applying the catalog `Pass rule` and `Type 1 test`:
   - `designed`: the Pass rule is met and you saw the supporting file, config, or document.
   - `partial`: the control exists but the Pass rule is not fully met (for example MFA exists but is optional).
   - `missing`: no implementation found where one should be visible.
   - `needs-evidence`: an organizational control not visible in the repo (for example background checks, `GOV-02`); the user must supply evidence.
5. **Write a concrete fix** for every control that is not `designed`: name the file and the change (for example, "add `.github/CODEOWNERS` covering `infra/`"). For `needs-evidence`, name the artifact to collect.
6. **Cite IDs.** Every row and finding cites the control ID and its TSC criteria (for example `AC-02` with its CC criteria), taken from the catalog.

## Rules

- Never mark a control `designed` from a scan signal alone. A signal with no confirming read of the code or config is at most `partial`, or `needs-evidence` when the control lives outside the repo.
- Use only the catalog's Pass rule. Do not invent criteria or soften a rule.
- Cite `file:line` where you can; otherwise name the signal key and the file you read.

## Output

Write `docs/soc2/type1-readiness.md` in the user's repo with:

1. Report date, scope (from state), and the disclaimer above.
2. **Summary counts per TSC category**: a table with one row per in-scope category and columns `designed | partial | missing | needs-evidence | N/A`.
3. **Control matrix**, one row per in-scope control:

   | ID | Title | TSC | Status | Basis (file:line or signal) | Fix |
   |---|---|---|---|---|---|

4. **Needs human evidence**: a list of every `needs-evidence` control with the artifact to collect and a suggested owner.

## Finish

Add `soc2-type1-readiness` to `state.completed` in `.soc2/state.json` (keep the existing entries, no duplicates) and give the user the summary counts plus the top fixes. Suggest `soc2-type2-operations` once the matrix is mostly `designed`.
