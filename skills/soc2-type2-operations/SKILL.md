---
name: soc2-type2-operations
description: Make SOC 2 controls operate continuously and generate evidence across a Type 2 audit period (typically 3 to 12 months). Use when controls are designed and the user needs evidence collection, monitoring cadence, access reviews, retention, or is preparing for a Type 2 report.
---

# SOC 2 Type 2 operations

This skill prepares for a SOC 2 audit; it is not an attestation. Only a licensed CPA firm can issue a SOC 2 Type 1 or Type 2 report.

A Type 2 report tests whether controls operated effectively over the whole audit period. A control that is designed but leaves no dated evidence fails. This skill turns each in-scope control into a recurring task with an owner, an evidence source, a retention rule, a population, and a known auditor sample.

Shared references (resolve `../soc2` against the directory containing this SKILL.md, not the shell's cwd):
- `../soc2/references/control-index.md`: one row per control (ID, Title, TSC, Category, Frequency, Owner, Scan signals). Read this first. It selects controls and supplies the default Frequency and Owner.
- `../soc2/references/control-catalog.md`: the full entries. Never read it whole; for each control you detail, search for `### <ID>` and read that entry. Fields: TSC, Applies when, Implement, Scan signals, Frequency, Owner, Type 1 test, Type 2 test, Evidence, Type 1 pass, Type 2 pass. The Type 2 sampling table is in the catalog header.
- `../soc2/references/tsc-criteria.md`: criteria IDs.
- `../soc2/references/cloud-equivalents.md`: AWS, GCP, and Azure service names per control family.
- `references/evidence-automation.md` (in this skill folder): ready-to-adapt snippets tagged by control ID, for GitHub Actions, GitLab CI, AWS, GCP, Azure, and Processing Integrity.

On Windows read and write files as UTF-8 and set `PYTHONIOENCODING=utf-8` for any script.

Cite a control ID and TSC criterion for every item (written `<CONTROL-ID> → <TSC ID>` with the Unicode arrow U+2192, for example `AC-02 → CC6.1`, where the TSC ID is one of the criteria on that control's `TSC:` line in the catalog). Look the ID up in the catalog; never guess one.

## Procedure

1. **Read state.** Load `.soc2/state.json` if present. Use its `tsc_scope`, `report_type`, `system` (cloud, workforce, tools), `decisions`, and `audit_period`. Do not re-ask anything already answered.
2. **Confirm `audit_period`.** If `audit_period.start` and `audit_period.end` are missing, ask for them in the router's plain wording (`../soc2/SKILL.md`, First run question 2; one question). Mention that a first Type 2 period is commonly 3 to 6 months, 6 or 12 months is typical afterward, and that the CPA firm must agree the window. Save the answer to state. Write only confirmed answers, per the router's First-run rule (`../soc2/SKILL.md`): never pre-fill an unconfirmed default, and leave skipped keys absent. Then pick the mode from today's date:
   - **Pre-period readiness** (window start is after today): do not simulate sampling. Report, per control, the date its evidence must be live (the window start, or the first scheduled occurrence before it). Prioritize automation that must be running before day one.
   - **Window running or ended**: check which controls already have evidence for the part of the window that has passed, and give each a status from the shared vocabulary: `designed` | `partial` | `missing` | `needs-evidence` | `n/a` (with a reason). If most controls fail (no evidence for the elapsed part), say so plainly and offer a later window start or a Type 1 report first. Evidence collection started midway only covers the remaining part of the period.
3. **List in-scope controls.** Use state (`tsc_scope`, earlier readiness or architecture output such as `docs/soc2/type1-readiness.md`, `docs/soc2/architecture.md`) and the index to pick the controls that apply, using the catalog's Scope selection rule: a control is in scope when any criterion on its `TSC:` line belongs to an in-scope category by series (CC → security, A1 → availability, PI1 → processing_integrity, C1 → confidentiality, P → privacy). Honor each entry's `Applies when`; record N/A controls with a reason.
4. **Define the operating model for each control.** For every in-scope control, take **Frequency** and **Owner** from the catalog entry (the index has them) and record:
   - Frequency: Continuous/automated, Per event, Daily, Weekly, Monthly, Quarterly, or Annual. Keep the catalog value unless the user's `decisions` say otherwise.
   - Owner role: a role from the catalog `Owner` field (for example Engineering lead, People ops, Security owner), never a person's name. With `system.workforce` of 10 or fewer, map roles onto the people who exist (one person may hold several) and flag any control whose owner would review their own work.
   - Evidence source: the system that produces the artifact, from the catalog `Evidence` field. Prefer automated, system-generated evidence over screenshots.
   - Automated?: yes only if the evidence is produced and stored without a human step.
   - Retention: audit period plus 1 year (common practice, not an AICPA rule). Logs: at least 365 days (OPS-07 → CC7.2) is the floor; 400 days is the recommended value.
   - Population: what the auditor samples from, and how you will prove the list is complete (for example "every merged PR in the period, from the Git host API", "every hire from the HRIS export", "every deploy from the pipeline run history"). The listing must be produced by the system, not by hand.
   - Expected sample: read the control's `Type 2 test` and the sampling table in the catalog header (annual 1, quarterly 2, monthly 2 to 5, weekly 5 to 15, daily 20 to 40, per event about 25 or the whole population when it is small, many times a day 25 to 60). Sample sizes are common practice and the CPA firm sets the real number. Automated, system-enforced controls are usually tested once, relying on effective IT general controls (change management and access to the configuration) for the whole period.
   - **Low-occurrence warning.** Count the occurrences that fit in the period (a monthly control in a 6-month window has 6; a quarterly one has 2). When the count is at or below the expected sample, or when one miss would leave too few, warn that the CPA firm will test every occurrence and one exception becomes a reported deviation. Where possible raise the frequency (for example run a weekly access-review check, not only quarterly).
   - **Annual items lapsing mid-period.** An annual control (policy review, tabletop, pen test, risk assessment, vendor review, training) must fire inside the window. List each with its last completion date and compute whether it lapses before the window ends or has no occurrence inside it; if so schedule it in the window, with a due date.
   - **No-occurrence handling.** For event-driven controls (terminations, incidents, emergency changes, new vendors, DSARs), an event may never occur in the period. Record "no occurrence in the period" evidence (for example an HRIS report showing no leavers, a ticket query returning zero incidents, signed by the owner) and tell the user the auditor tests only that the procedure exists and that the population is genuinely empty. Do not call a control failed for having no occurrences, and do not invent an occurrence.
5. **Generate snippets.** Choose the snippets in `references/evidence-automation.md` that match the user's stack and cloud (GitHub Actions or GitLab CI; AWS, GCP, or Azure; issue templates, PR template and CODEOWNERS, IR runbook and tabletop; Processing Integrity evidence) and adapt names, regions, teams, and org values. When no snippet matches the stack, generate the artifact from the patterns in its section 7 and say it is generated rather than tested. Validate what you write: parse YAML (`python -c "import yaml,sys; yaml.safe_load(open(sys.argv[1]))" <file>` when PyYAML is installed, otherwise review carefully), run `terraform fmt -check` and `terraform validate` when Terraform is present, and `bash -n` for shell.
   - **Collision check before writing.** List the exact paths and resource names first and check each: existing workflow files with the same name; existing Terraform resource addresses and cloud resource names (use the `soc2_` prefix, no `terraform {}` or `provider` block); existing issue and PR templates. CODEOWNERS can live at the root, `.github/`, or `docs/`; if any exists, merge the new rules into it and never write a second file (a new `.github/CODEOWNERS` shadows a root one). Never overwrite a user file; merge or rename.
   - **Ask before writing any file into the user's repo**, and list the exact paths first (`.github/workflows/soc2-evidence-*.yml`, issue templates, IaC files). Write only what the user approves. If they decline, leave the snippet in the output document instead.
   - GitHub Actions artifact retention is 1 to 90 days on public repos and up to 400 days on private and internal repos, and artifacts are deletable. Never treat them as the retained evidence; copy exports to locked storage (S3 Object Lock, GCS bucket retention policy with lock, Azure immutable blob) sized to audit period plus 1 year.
   - Scheduled evidence workflows need a token that can read branch protection and rulesets (Administration read) and Dependabot alerts, and any labels used by `gh issue create` must exist first (the snippets create them). Work through the prerequisites checklist in section 0 of the snippets file with the user.
   - Warn that evidence collection started midway through the period only covers the remaining part of it.
6. **Flag manual-only controls.** List every control whose evidence is only manual (people and process, such as training completion, access review sign-off, vendor review, tabletop). For each, add a calendar reminder or recurring ticket, a named owner role, and a "where the artifact is stored" location. Do not mark these as automated.
7. **Write the output** (below) and update state.

## Output contract

Write `docs/soc2/type2-operations.md` in the user's repo with:

1. A header with the audit period, mode (pre-period readiness, or in-window with the elapsed share), TSC scope, and the disclaimer.
2. The control table:

   | ID | Frequency | Owner | Evidence source | Automated? | Retention | Population / completeness | Occurrences in period | Expected sample |
   |---|---|---|---|---|---|---|---|---|

   One row per in-scope control. Write the ID cell as `<CONTROL-ID> → <TSC ID>` (for example `AC-05 → CC6.2`); the TSC mapping is required. The `Occurrences in period` cell carries a low-occurrence warning marker when the count is at or below the sample. In pre-period mode add an `Evidence live by` column instead of simulating samples.
3. An **operating calendar** grouped by weekly, monthly, quarterly, and annual tasks. Each entry names the control ID, owner, and artifact, and each annual task has a due date inside the audit period (flag any that would lapse). Include the snippet-generated jobs and which ones were written to the repo.
4. A **manual-evidence list** of controls with no automation, with the reminder mechanism for each.
5. A **no-occurrence list**: event-driven controls and how "nothing happened" will be evidenced.
6. An **exceptions procedure**: how a missed or failed control occurrence is recorded (ticket, root cause, remediation), because auditors report exceptions and a documented response matters more than hiding them (MON-03 → CC4.2). One exception in a sample usually leads the CPA firm to expand the sample or report a deviation.

Update `.soc2/state.json`: set `audit_period` if newly confirmed, append decisions (for example `{"control": "OPS-07", "choice": "S3 Object Lock evidence bucket", "date": "<today>", "adr": "<number if one exists>"}`), and add `soc2-type2-operations` to `completed`. Keep all other fields.

## Rules

- Pass/fail follows the catalog `Type 2 pass` and `Type 2 test`; do not invent criteria. The Type 1 fields do not apply here.
- A scan signal is a hint, not evidence. Evidence is a dated artifact.
- Do not claim the user will pass the audit; say what evidence will exist.
- Instructions here are tool-agnostic: use whatever file read, write, and shell tools your agent provides.
