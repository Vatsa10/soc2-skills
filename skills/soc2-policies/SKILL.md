---
name: soc2-policies
description: Generate a tailored SOC 2 policy set (18 core policies, small-team aware) mapped to Trust Services Criteria and control IDs, or review existing policies. Use for information security policy, acceptable use, access control, incident response plan, code of conduct, physical security, secure SDLC, policy templates, policy review, or when an auditor or customer asks for policy documents.
---

# SOC 2 policies

This skill prepares for a SOC 2 audit; it is not an attestation. Only a licensed CPA firm can issue a SOC 2 Type 1 or Type 2 report.

Generates the 18 core policy documents an auditor expects, filled in for the user's company and tailored to their scope, cloud and team size. Each policy statement carries a control tag such as `[AC-02 → CC6.1]` (control ID from `../soc2/references/control-catalog.md`, then the Trust Services Criterion it supports; the TSC in a tag always comes from that control's catalog TSC line). Read `../soc2/references/control-index.md` first when you need to look up a control, and open a full catalog entry (search `### <ID>`) only for a control you must evaluate; never read the whole catalog.

## Inputs

1. Read `.soc2/state.json` in the user's repo. Fields used: `tsc_scope`, `report_type`, `audit_period`, `system.name`, `system.cloud`, `system.workforce`, `system.tools`, `system.data_classes`, `decisions`, `completed`, and optionally `system.company` and `system.owner`. Never re-ask a key that is present.
2. If the file is missing, do not stop: ask for the missing keys with the router's plain wording (see First run in `../soc2/SKILL.md`: report type with the same three-line Type 1 vs Type 2 explanation and rule of thumb, the Type 1 date or Type 2 window, cloud, company, owner, team size; scope with Security as default) and create `.soc2/state.json`.
3. Ask for what is missing in ONE merged inputs message, run as its own turn (when chained from the router, do not bundle it with another skill's questions). Put these together: the missing keys below, the top-10 commitments to confirm (see Confirming commitments), `reporting_channel`, `gift_limit`, and the approver. Approver shortcut: the user can reply "approver: <name>, <role>" (sets `{{approver}}` only; approval date stays `Pending approval` and version `0.1 draft`) or "approved by <name> on <date>" (sets approver, approval date and version `1.0`). Never invent an approval date.
   - `company`: legal or trading name (stored as `system.company`).
   - `owner`: name and role of the person accountable for the policies (stored as `system.owner`).
   - `approver`: name and role of the person who will approve the policies (often the most senior executive; default is to leave it for the user to supply).
   - Scope: if `tsc_scope` is absent or empty, ask which categories are in scope (security is always included).
   - On-call coverage, at any team size (`24x7`, `business hours` plus the hours and timezone, or `none`). Record the confirmed answer in `decisions` (control `OPS-14`) so later runs do not re-ask.
   - Small-team profile (see below) when `system.workforce` is 10 or fewer: ask once for team size if absent and who handles Legal and HR (a named person, an outside firm or PEO, or nobody yet).
   - `data_classes`, only when absent and `privacy` is in scope: ask once in this turn, using the scanner's `pii` hint from `.soc2/scan.json` as the suggestion ("your code looks like it handles email and address; anything else, such as health, payment or government IDs?"), and write the confirmed answer to `system.data_classes`.
   - Optional: `review_cadence` (default `annually`; any value must be 12 months or shorter) and `effective_date` (default today's date).
4. Write answers back into `.soc2/state.json` (preserve every other key). Write only confirmed answers, per the router's First-run rule (`../soc2/SKILL.md`): never pre-fill an unconfirmed default, and leave skipped keys absent. `effective_date` and `review_cadence` are written to state only after the user accepts them.

## Procedure

1. Select policies from `templates/` by `tsc_scope`. All 18 are generated: acceptable-use, access-control, asset-management, business-continuity-dr, change-management, code-of-conduct, data-classification, data-retention-disposal, encryption, hr-security, incident-response, information-security, logging-monitoring, physical-security, privacy, risk-assessment, secure-sdlc, vendor-management. Exceptions:
   - `privacy` only when `privacy` is in `tsc_scope`.
   - `business-continuity-dr` is always generated (it also evidences availability when `availability` is in scope).
   - Category-specific statements start with `(if privacy in scope)`, `(if processing_integrity in scope)` or `(if availability in scope)`. Keep such a statement (and drop the prefix) only when that category is in `tsc_scope`; otherwise remove the statement entirely. Unprefixed statements are always kept.
   - Skip a policy whose file already exists in `docs/policies/` and switch to Review mode for it.
2. Read the one template for each selected policy and replace every placeholder; leave no `{{...}}` in the output:
   - `{{company}}`, `{{owner}}`, `{{effective_date}}`, `{{review_cadence}}` as above.
   - `{{approver}}` with the approver's name and role (or `Pending: approver to be named` if the user has not supplied one), `{{approval_date}}` with `Pending approval` until the user gives the real date, `{{version}}` with `0.1 draft` until approved and `1.0` once approved, `{{next_review}}` with the effective date plus the review cadence (a date).
   - Cloud placeholders, filled from `system.cloud` using `../soc2/references/cloud-equivalents.md` for current service names (name every cloud when there are several): `{{cloud_kms}}` (key service, for example AWS KMS, Google Cloud KMS, Azure Key Vault), `{{cloud_audit_trail}}` (for example AWS CloudTrail, Google Cloud Audit Logs, Azure Activity Log), `{{cloud_secrets}}` (for example AWS Secrets Manager, Google Secret Manager, Azure Key Vault secrets), `{{cloud_backup}}` (for example AWS Backup, Google Cloud Backup and DR or managed-database backups, Azure Backup). If `system.cloud` is empty, ask once; do not guess.
   - `{{oncall_hours}}`: `24x7` only when on-call really is 24x7; otherwise `during business hours (<hours> <timezone>)` or `none (alerts are reviewed on the next business day)`. See Tailoring step on on-call.
   - Policy-specific placeholders, each a default the user confirms: `{{gift_limit}}` (default 100 USD), `{{reporting_channel}}` (anonymous form or mailbox the company really runs), `{{sast_block_severity}}` (default `high or critical`), `{{dast_cadence}}` (default quarterly).
3. Tailor, without removing any unconditional tagged statement:
   - Name the real services in cloud placeholders and wherever a statement gives examples. Apply earlier `decisions` (a chosen IdP, ticketing tool, log platform) by naming the tool.
   - Every number, cadence and timeframe in a statement is a default the company must actually be able to meet, because an auditor tests against the policy as written. Defaults follow the control catalog's Implement values. Where the company runs a different number, change the number but keep the statement and its tag. Never set a number the company does not run.
   - Vulnerability deadlines live in one place only (Logging and Monitoring Policy statement 9); other policies reference it. If the company changes a number, change it there only. The 7-day window for known-exploited vulnerabilities is a stated company commitment based on common practice, not a standard; say so when asking for confirmation.
   - Password rules follow NIST SP 800-63B-4 (15 characters when a password is the only authenticator, 8 minimum with MFA, accept at least 64 characters, no composition rules, no scheduled rotation, blocklist check, rate limiting). The template sets 12 with MFA; do not weaken it below 8 or drop the 15-character password-only rule.
   - Align retention periods and RTO/RPO with decisions. Where `system.data_classes` includes personal or health data, keep the Privacy, Retention and Classification statements as written and name those data classes.
   - Flag any statement that contradicts the scan signals in `.soc2/scan.json` (when present) (for example MFA required everywhere while `auth.mfa_hint` is false, or 12-month log retention while `logging.retention_days` is lower) as a gap, not as a claim.
   - Statements must stay concrete (who, what, how often); never replace them with generic wording.
4. On-call, at any team size. Whenever on-call is not 24x7, set `{{oncall_hours}}` accordingly and also rewrite the fixed windows: replace "at any hour" and "24x7" with "during business hours (<hours> <timezone>); alerts outside those hours are reviewed by the next business day", and replace the 1-hour triage and 15-minute acknowledgement windows with "1 business hour" (Incident Response statements 1, 2, 9, 11; Logging and Monitoring statements 6, 7 and the On-call engineer roles row). Keep every tag. Ask which hours.
5. Small-team profile (`system.workforce` of 10 or fewer). Do not leave statements the company cannot run; rewrite them concretely, keep the tag, and list each rewrite under Open gaps:
   - No Legal: replace "Legal" and "Communications lead" with {{owner}} plus a named outside counsel or "outside counsel engaged when needed", in statements and in every roles-table row (legal holds, customer and regulator notices, enforcement). No HR: replace "People Operations" and "People operations" with the most senior executive or {{owner}} and name that person, in statements and roles-table rows (Access Control, HR Security, Acceptable Use and the enforcement paragraphs).
   - No board: "leadership" and "board oversight" mean the founders or leadership team; the quarterly metrics and risk-register reviews are recorded in short meeting notes with attendees and date.
   - One engineer: peer review by "someone other than the author" cannot be met; rewrite as review by another engineer, a contractor or the {{owner}}, and where nobody else can review, a post-merge review within 2 business days with a recorded exception. Tabletop exercises become a 1-hour desk exercise.
   - Do not drop a control that auditors test (access review, backup restore test, vendor review, risk assessment, incident log) just because the team is small; reduce the scale, not the evidence.
6. After writing, grep every written policy for `24x7|at any hour|Legal|Communications lead|People operations|People Operations`. Each hit must be either justified (the company really has that function or coverage) or rewritten; list unresolved hits under Open gaps. Also confirm no `{{` remains.
7. Do not claim controls the company does not run. If a statement describes something the user says they do not do, keep it, and list it in the output as a gap to close before the audit period starts.
8. Write each policy to `docs/policies/<slug>.md` (create the directory). The slug is the template filename; the scanner detects policies by these stems.
9. Append `"soc2-policies"` to `completed` in `.soc2/state.json` (no duplicates) and record any new choices in `decisions` as `{"control", "choice", "date"}`.

## Already generated

If `completed` contains `"soc2-policies"` or `docs/policies/` already holds the policies, do not drop silently into Review mode. Say where they are (`docs/policies/`, with the version and approval status read from the headers) and offer three choices: regenerate (with the backup rule below), review against the templates, or record approval (approver, date, version `1.0`). Proceed on the user's answer. A request for a new or changed policy statement is treated as regenerate or review of that one file.

## Confirming commitments

A blanket answer such as "sure whatever", "defaults are fine" or "looks good" is not confirmation of any number. Do not ask the user to confirm 80 numbers.

1. Pick the roughly 10 commitments an auditor tests most, and ask for an explicit yes or a changed value for each, one line each with the default shown: quarterly access reviews (AC-05); access removed within 24 hours of termination (AC-04); vulnerability deadlines including the 7-day known-exploited window (OPS-01); log retention of 12 months with 90 days searchable (OPS-07); RTO and RPO plus backup retention (RSK-05, AV-03); annual restore test (AV-04); incident triage and on-call hours (OPS-09, OPS-14); customer notification within 72 hours of confirmation (OPS-13); annual penetration test (MON-02); training within 30 days of hire (GOV-05); service key rotation every 90 days (AC-17); background checks before access (GOV-02).
2. All other numbers are listed in one table as "applies as written unless you tell me you cannot meet it".
3. If the answer to the top-10 list is vague or blanket, ask once more for the specific items. If it is still vague, write the policies marked `0.1 draft`, list those commitments under Open gaps as unconfirmed, and do not describe them as confirmed anywhere.

## Review mode

Use when `docs/policies/` (or any `policies/` directory) already holds policies, or when the user asks to review existing documents.

1. Match each existing file to a template by slug stem (`access-control`, `incident-response`, and so on). Note unmatched policies and any of the 18 that are missing.
2. For each matched policy, compare its content against the template's numbered statements. A statement counts as covered only if the policy states the same requirement concretely (the numbers can differ). Vague wording ("appropriate measures", "regularly") is reported as not covered. Compute coverage per policy as covered statements divided by applicable statements.
3. Report missing statements with their control tags, grouped by policy.
4. Check the policy header for owner, approver, approval date, version, effective date, review cadence and next review date, and flag a missing approval or an effective date older than the stated cadence. A policy with no named approver and date is not evidence of management approval.
5. Coverage below 25 percent for a policy: recommend replacing it with the generated template instead of appending statements. Offer to move the existing file to `docs/policies/_backup/<slug>-<date>.md` first, and write the new policy only after the user agrees. Never overwrite without the backup.
6. Coverage of 25 percent or more: offer to append the missing statements; edit existing files only after the user agrees.

## Output contract

Finish with:

1. The list of files written or reviewed, as paths under `docs/policies/`.
2. A table `policy | control IDs covered | TSC criteria`, built from the tags in the written files.
3. Commitments to confirm: the explicit top-10 table (`policy | statement # | commitment | default | confirmed?`), followed by the "applies as written" table for the rest. Include conditional statements that were kept or dropped by scope.
4. Open gaps: statements the user said they cannot meet, small-team rewrites made, statements that contradict scan signals, placeholders still to confirm (including `Pending` approver and approval date), unconfirmed commitments, and policies skipped because privacy is out of scope.
5. A reminder that policies need leadership approval (name and date recorded in each header) and employee acknowledgement within 30 days of hire, annually, and within 30 days of a material change, to count as evidence, and that the disclaimer above applies.
