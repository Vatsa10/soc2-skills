---
name: soc2-type2-operations
description: Make SOC 2 controls operate continuously and generate evidence across a Type 2 audit period (typically 3–12 months). Use when controls are designed and the user needs evidence collection, monitoring cadence, access reviews, retention, or is preparing for a Type 2 report.
---

# SOC 2 Type 2 operations

This skill prepares for a SOC 2 audit; it is not an attestation. Only a licensed CPA firm can issue a SOC 2 Type 1 or Type 2 report.

A Type 2 report tests whether controls operated effectively over the whole audit period. A control that is designed but leaves no dated evidence fails. This skill turns each in-scope control into a recurring task with an owner, an evidence source, a retention rule, and a known auditor sample.

Shared references (relative to this skill folder):
- `../soc2/references/control-catalog.md`: control IDs, `Type 2 test`, `Evidence`, `Pass rule`, and the Type 2 sampling table in its header.
- `../soc2/references/tsc-criteria.md`: criteria IDs.
- `references/evidence-automation.md`: ready-to-adapt snippets tagged by control ID.

Cite a control ID and TSC criterion for every item (written `<CONTROL-ID> → <TSC ID>` with the Unicode arrow U+2192, for example `AC-02 → CC6.1`, where the TSC ID is one of the criteria on that control's `TSC:` line in the catalog). Look the ID up in the catalog; never guess one.

## Procedure

1. **Read state.** Load `.soc2/state.json` if present. Use its `tsc_scope`, `system`, `decisions`, and `audit_period`. Do not re-ask anything already answered.
2. **Confirm `audit_period`.** If `audit_period.start` and `audit_period.end` are missing, ask for them (one question). Mention that a first Type 2 period is commonly 3 to 6 months, and that 6 or 12 months is typical afterward. Save the answer to state. Write only confirmed answers, per the router's First-run rule (`../soc2/SKILL.md`): never pre-fill an unconfirmed default, and leave skipped keys absent. Warn the user that every control must fire at least once inside the period: an annual control scheduled after the period ends cannot be tested.
3. **List in-scope controls.** Use state (`tsc_scope`, earlier readiness or architecture output such as `docs/soc2/type1-readiness.md`, `docs/soc2/architecture.md`) to pick the catalog controls that apply, selecting them by the catalog's Scope selection rule (`../soc2/references/control-catalog.md`): a control is in scope when any criterion on its `TSC:` line belongs to an in-scope category by series (CC → security, A1 → availability, PI1 → processing_integrity, C1 → confidentiality, P → privacy). Honor each entry's `Applies when`; record N/A controls with a reason.
4. **Define the operating model for each control.** For every in-scope control, record:
   - Frequency: continuous (system-enforced), daily, weekly, monthly, quarterly, annual, or per event.
   - Owner role: a role, not a person's name (for example Head of Engineering, IT Admin, Security Lead).
   - Evidence source: the system that produces the artifact, taken from the catalog `Evidence` field. Prefer automated, system-generated evidence over screenshots.
   - Automated?: yes only if the evidence is produced and stored without a human step.
   - Retention: at least the audit period plus 1 year (log retention of at least one year, OPS-07 → CC7.2, is the floor for logs).
   - Expected sample: read the control's `Type 2 test` and the sampling table in the catalog header (annual 1, quarterly 2, monthly 2-5, weekly 5-15, daily 20-40, many times a day 25-60). State that sample sizes are common practice and the CPA firm sets the real number. Automated, system-enforced controls are usually tested once plus change-management testing of the configuration.
5. **Generate snippets.** Choose the snippets in `references/evidence-automation.md` that match the user's stack (GitHub Actions, Terraform and AWS, issue templates, PR template and CODEOWNERS, IR runbook and tabletop) and adapt names, regions, teams, and org values. **Ask before writing any file into the user's repo**, and list the exact paths first (`.github/workflows/soc2-evidence-*.yml`, issue templates, IaC files). Write only what the user approves. If they decline, leave the snippet in the output document instead.
   - GitHub Actions artifact retention is 1 to 90 days on public repos and up to 400 days on private and internal repos, and artifacts are deletable. Never treat them as the retained evidence; copy exports to object-locked storage (S3 object lock or GCS retention policy) sized to audit period plus 1 year.
   - Scheduled evidence workflows need a token with read access to branch protection and Dependabot alerts, and any labels used by `gh issue create` must exist first.
   - Warn that evidence collection started midway through the period only covers the remaining part of it.
6. **Flag manual-only controls.** List every control whose evidence is only manual (people and process, such as training completion, access review sign-off, vendor review, tabletop). For each, add a calendar reminder or recurring ticket, a named owner, and a "where the artifact is stored" location. Do not mark these as automated.
7. **Write the output** (below) and update state.

## Output contract

Write `docs/soc2/type2-operations.md` in the user's repo with:

1. A header with the audit period, TSC scope, and the disclaimer.
2. The control table:

   | ID | Frequency | Owner | Evidence source | Automated? | Retention | Expected sample |
   |---|---|---|---|---|---|---|

   One row per in-scope control. Write the ID cell as `<CONTROL-ID> → <TSC ID>` (for example `AC-05 → CC6.2`); the TSC mapping is required, not optional.
3. An **operating calendar** grouped by weekly, monthly, quarterly, and annual tasks. Each entry names the control ID, owner, and artifact, and each annual task has a due date inside the audit period. Include the snippet-generated jobs and which ones were written to the repo.
4. A **manual-evidence list** of controls with no automation, with the reminder mechanism for each.
5. An **exceptions procedure**: how a missed or failed control occurrence is recorded (ticket, root cause, remediation), because auditors report exceptions and a documented response matters more than hiding them (MON-03 → CC4.2).

Update `.soc2/state.json`: set `audit_period` if newly confirmed, append decisions (for example the chosen evidence store), and add `soc2-type2-operations` to `completed`. Keep all other fields.

## Rules

- Pass/fail follows the catalog `Pass rule` and `Type 2 test`; do not invent criteria.
- A scan signal is a hint, not evidence. Evidence is a dated artifact.
- Do not claim the user will pass the audit; say what evidence will exist.
- Instructions here are tool-agnostic: use whatever file read, write, and shell tools your agent provides.
