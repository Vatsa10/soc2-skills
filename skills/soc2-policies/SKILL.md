---
name: soc2-policies
description: Generate a tailored SOC 2 policy set (15 core policies) mapped to Trust Services Criteria and control IDs. Use when the user needs security/privacy policies, the soc2 router reports missing policies, or an auditor asks for policy documents.
---

# SOC 2 policies

This skill prepares for a SOC 2 audit; it is not an attestation. Only a licensed CPA firm can issue a SOC 2 Type 1 or Type 2 report.

Generates the 15 core policy documents an auditor expects, filled in for the user's company and tailored to their scope and cloud. Each policy statement carries a control tag such as `[AC-02 → CC6.1]` (control ID from `../soc2/references/control-catalog.md`, then the Trust Services Criterion it supports).

## Inputs

1. Read `.soc2/state.json` in the user's repo. Fields used: `tsc_scope`, `report_type`, `audit_period`, `system.name`, `system.cloud`, `system.data_classes`, `decisions`, `completed`, and optionally `system.company` and `system.owner`.
2. If the file is missing, tell the user to run the `soc2` router skill first (scope and report type are needed), then stop.
3. Ask only for what is missing, in one message:
   - `company`: legal or trading name (stored as `system.company`).
   - `owner`: name and role of the person accountable for the policies (stored as `system.owner`).
   - Scope: if `tsc_scope` is absent or empty, ask which of the five categories are in scope (security is always included).
   - Optional: `review_cadence` (default `annually`) and `effective_date` (default today's date).
4. Write answers back into `.soc2/state.json` (preserve every other key).

## Procedure

1. Select policies from `templates/` by `tsc_scope`. All 15 are generated, except:
   - `privacy` only when `privacy` is in `tsc_scope`.
   - `business-continuity-dr` is always generated (it also evidences availability when `availability` is in scope).
   - Skip a policy whose file already exists in `docs/policies/` and switch to Review mode for it.
2. Read the one template for each selected policy and replace `{{company}}`, `{{owner}}`, `{{effective_date}}`, `{{review_cadence}}`. Leave no `{{...}}` in the output.
3. Tailor, without removing any tagged statement:
   - Name the real services where the template says "cloud provider" or gives examples: use `system.cloud` (for example AWS KMS and CloudTrail, GCP Cloud KMS and Audit Logs, Azure Key Vault and Activity Log).
   - Apply earlier `decisions` (for example a chosen IdP, ticketing tool or log platform) by naming the tool in the relevant statements.
   - Align retention periods and RTO/RPO with decisions; where the user states a different number, change the number but keep the statement and its tag.
   - Where `system.data_classes` includes personal or health data, keep the Privacy, Retention and Classification statements as written and name those data classes.
   - Statements must stay concrete (who, what, how often); never replace them with generic wording.
4. Do not claim controls the company does not run. If a statement describes something the user says they do not do, keep it, and list it in the output as a gap to close before the audit period starts.
5. Write each policy to `docs/policies/<slug>.md` (create the directory). The slug is the template filename; the scanner detects policies by these stems.
6. Append `"soc2-policies"` to `completed` in `.soc2/state.json` (no duplicates) and record any new choices in `decisions` as `{"control", "choice", "date"}`.

## Review mode

Use when `docs/policies/` (or any `policies/` directory) already holds policies, or when the user asks to review existing documents.

1. Match each existing file to a template by slug stem (`access-control`, `incident-response`, and so on). Note unmatched policies and any of the 15 that are missing.
2. For each matched policy, compare its content against the template's numbered statements. A statement counts as covered only if the policy states the same requirement concretely (the numbers can differ). Vague wording ("appropriate measures", "regularly") is reported as not covered.
3. Report missing statements with their control tags, grouped by policy.
4. Check the policy header for owner, effective date and review cadence, and flag a review date older than the stated cadence.
5. Offer to append the missing statements; edit existing files only after the user agrees.

## Output contract

Finish with:

1. The list of files written or reviewed, as paths under `docs/policies/`.
2. A table `policy | control IDs covered | TSC criteria`, built from the tags in the written files.
3. Open gaps: statements the user said they cannot meet, placeholders still to confirm, and policies skipped because privacy is out of scope.
4. A reminder that policies need leadership approval and employee acknowledgement to count as evidence, and that the disclaimer above applies.
