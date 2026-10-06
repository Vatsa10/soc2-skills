---
name: soc2-architect
description: Design systems from the ground up to SOC 2 Type 1/Type 2 across all five TSC. Use during brainstorming, greenfield architecture, data or invoice/billing/payment pipelines, enterprise security-review prep, or when adding a new component/service, so controls are designed in rather than bolted on.
---

# soc2-architect

This skill prepares for a SOC 2 audit; it is not an attestation. Only a licensed CPA firm can issue a SOC 2 Type 1 or Type 2 report.

Use while a system is being designed (or a component added) so the required controls and their Type 2 evidence are part of the architecture, and so developers get a build spec (modules, tests, IaC), not generic advice. Works the same in Claude Code and Codex, and is tool-agnostic: examples name products, any equivalent works. Paths below are relative to the skill folder and the user's repo.

## Shared references

- Control index (one row per control: ID, title, TSC, category, frequency, owner, scan signals). Read this FIRST: `../soc2/references/control-index.md`
- Control catalog (full entries, field order: TSC, Applies when, Implement, Scan signals, Frequency, Owner, Type 1 test, Type 2 test, Evidence, Type 1 pass, Type 2 pass). Never read it whole; open only the entries you evaluate by searching `### <ID>`: `../soc2/references/control-catalog.md`
- Cloud service equivalents (AWS, GCP, Azure per control family, current names): `../soc2/references/cloud-equivalents.md`
- Criteria list: `../soc2/references/tsc-criteria.md`
- Component to control map: `references/component-controls.md`
- ADR template: `references/adr-template.md`

Rules: cite every control as `ID → TSC` using U+2192 (for example `AC-02 → CC6.1`, `AC-10 → CC6.1, CC6.7`). Take the TSC only from the control's `TSC:` line in the catalog; never guess an ID or mapping, never invent pass criteria, and use the catalog's `Type 1 pass` and `Type 2 pass` fields when stating what passes. Look the ID up first.

## Step 0: Read state

Read `.soc2/state.json` if it exists (the router owns the schema). Anything already present (`tsc_scope`, `report_type`, `audit_period`, `type1_report_date`, `system.name`, `system.company`, `system.owner`, `system.cloud`, `system.type`, `system.tenancy`, `system.workforce`, `system.tools`, `system.data_classes`) is never asked again. If the user already stated something in conversation (for example "we are on Azure"), treat it as answered and echo it back instead of asking. "Small team" means `system.workforce` of 10 or fewer: recommend lighter choices (managed services, SaaS tooling, fewer bespoke controls) and mark organisational controls that need roles the company lacks as `Excluded` or shared-owner with a reason.

If `.soc2/state.json` does not exist, create it containing only the keys the user answered (or whose offered default they explicitly accepted); omit unanswered keys so they are asked again next time. `decisions: []` and `completed: []` may be initialized.

## Step 1: Questions (one message, at most 4)

Ask only keys that are missing from state and the conversation, in ONE message of at most four plain-language questions, in the router's wording. If invoked through the router, the router already asked; ask nothing it covered. Do not ask one question at a time.

1. Report type, explained in three lines: Type 1 is a snapshot (are the controls designed and in place on one date?); Type 2 is a movie (did the controls keep working over a period, usually 3 to 12 months?); ask your customer which one they accept. Rule of thumb: first report, or a deal is waiting, take Type 1 now and Type 2 next; if the customer demands Type 2, go straight to it. Deadline arithmetic: a Type 2 window should be at least 3 months and starts only after the controls are live. If the customer deadline minus the time to build the controls leaves less than 3 months, recommend a Type 1 now plus a Type 2 window afterwards (`next_report`: `type2 after type1`), and state the actual dates. (Skip the explanation if `report_type` is known; if it is absent when you need it, ask just that one question with two options, accept a plain-English answer, and echo it back.)
2. Date: the Type 1 as-of date, or the Type 2 window start and end. Ask for the as-of date only when `report_type` is `type1` or the user asks for a Type 1 report.
3. Cloud(s): AWS, GCP, Azure, other, or none yet (several may apply).
4. System or product name, company name, who owns the project, and team size (workforce).

TSC scope (inside question 1's message, not a fifth question): Security is the default and always in scope, plus one line each for Availability (uptime and recovery promises), Processing Integrity (data processed completely and accurately, such as invoices and payments), Confidentiality (protecting data marked confidential), Privacy (personal information handled per your notice). Accept or narrow it. Then infer, do not interrogate: system type, tenancy, tools and data classes come from what the user already described or from the repo. If a data class is unclear and it changes controls (PHI, cardholder data, government IDs), ask it inside the same message as a fifth clause of question 4 only when necessary.

### Payments (when the user says payments, billing, invoices or payouts)

"Payments" is ambiguous, so add one clause to question 4's message: is the money coming in (customers pay you: billing, invoices, subscriptions), going out (payroll, vendor or customer payouts), or both? And do card or bank account numbers ever reach your code or database, or only a provider's hosted page or API?

- Money in, card data: use a provider-hosted payment page or fields, so the card number never touches your servers. That keeps you at PCI DSS SAQ A, the smallest scope; handling card numbers yourself means SAQ D and a far larger scope. Keep only the provider's token and last-4. PCI DSS applies separately from SOC 2.
- Money out (payouts, payroll): bank account and routing numbers are sensitive; prefer the provider's tokenized payout API (the provider holds the account number) over storing them. US ACH payouts also fall under NACHA rules and your bank's or processor's requirements (authorization records, return handling); confirm with them, SOC 2 does not cover this.
- Either direction: flag Processing Integrity (PI-01 to PI-07, with idempotency `PI-06 → PI1.3` and reconciliation to the cent) in the scope-gap check below, and record the money direction and the card or bank data path in the data minimisation ADR.

If PHI or cardholder data is in play, state that HIPAA or PCI DSS applies separately and SOC 2 does not replace them.

Save each confirmed answer to `.soc2/state.json` as soon as it is given, and never write a value the user did not give or accept.

### Scope-gap flag (once, plus one standing flag)

Standing backup flag: whenever a database or other persistent store exists and Availability is out of scope (for example a Security-only report), always flag that backups, restore testing and recovery would not be examined as AV controls. Cite the gap as `RSK-05 → CC9.1` (business continuity, in scope through Security) and say that `AV-03` and `AV-04` apply if Availability is added. Do not remap the catalog; still design the backup and a restore test, and if the user declines, record it as excluded (scope choice).

After the data classes are known, compare them with the chosen TSC scope and flag each mismatch once, with a reason to confirm: personal information or sensitive PII with Privacy excluded (customers and enterprise security questionnaires commonly ask about it; PR controls would not be examined); customer-supplied confidential data with Confidentiality excluded; a data or financial pipeline with Processing Integrity excluded; uptime commitments in contracts with Availability excluded. The user may keep the exclusion; record it as "scope choice, data suggests <category>" in the architecture's Excluded section and in `.soc2/state.json` `excluded` (see Update state) so the audit and policy skills do not re-raise it.

## Step 2: Procedure

1. List components. Enumerate every component: identity provider, edge/gateway, app services, serverless functions, databases, object storage, queues, intake and delivery channels, pipelines, CI/CD, secrets/keys, logging/SIEM, monitoring/alerting, backups/DR, endpoints, third-party SaaS/vendors and sub-processors, PII stores. Also list external actors and where each data class lives.
2. Data minimisation pass. Before mapping controls, challenge stored data: does the system need it? For government identifiers (SSN, national ID) prefer a tokenization vendor, or last-4 only; for card data prefer a hosted payment page; set shortest viable retention. Record accepted minimisation as an ADR.
3. Map each component. For each, find its row in `references/component-controls.md` (rows exist for serverless pipelines and intake/delivery as well as managed pipelines); merge rows when a component matches several. Add the cross-cutting controls and data-class triggers.
4. Unmapped-control diff. Read `control-index.md` and list every control ID not mapped to any component or cross-cutting group. For each, either add it (and say where) or list it under `Excluded` with a one-line reason. A reason must be specific to this company (for example "no board; 4-person company, founder reviews quarterly" for GOV-03); "not needed yet" is not a reason for a Security control. Nothing may be silently dropped.
5. Pull catalog entries. For each mapped ID search `### <ID>` and read Applies when, Implement, Frequency, Owner, Type 1 test, Type 2 test, Evidence, Type 1 pass, Type 2 pass. Drop controls whose `Applies when` is false or that are out of scope under the catalog's scope selection rule (a control is in scope when any criterion on its `TSC:` line belongs to an in-scope category by series: CC security, A1 availability, PI1 processing_integrity, C1 confidentiality, P privacy), and record each exclusion with a reason.
6. Choose concrete services using `cloud-equivalents.md` for each cloud in `system.cloud` (GCP and Azure get the same depth as AWS). Prefer designs that make evidence automatic. Use current names (see the note in `component-controls.md`: for example Google Security Operations, Knowledge Catalog, Security Hub CSPM, Iru, Trivy config instead of tfsec, PagerDuty or Jira Service Management rather than Opsgenie). If you are unsure a service name or API is current, say so rather than assert it.
7. Produce the Mermaid diagram with trust boundaries and data flows, labeling flows with the data class and encryption (`AC-10 → CC6.1, CC6.7`) and marking where log/evidence streams go.
8. Produce the component table, the Top 10 list and the implementation spec (see Output contract).
9. Write one ADR per significant choice using `references/adr-template.md` (IdP, encryption/key management, tenancy isolation, logging pipeline, backup/DR, CI/CD and change control, vendor and sub-processor carve-out vs inclusive (GOV-11), data minimisation). Present the design and ADR list for confirmation before writing files if any choice was ambiguous.

## Type 2 by design rule

Every control in the design must name its automated evidence source (for example an IdP API export, cloud audit trail, a config-rule export, a pipeline log, a ticket query), its `Frequency` and its `Owner` role from the catalog. If a control has no automated source, flag it as `NO AUTOMATED EVIDENCE`, state the manual evidence and who owns it, and add it to the ADR's gap list. Do this for Type 1 projects too, because evidence collection must begin when the observation period starts. Retention of logs: state the 365-day floor (`OPS-07 → CC7.2`); recommend about 400 days so the floor is never missed.

## Output contract

Write these files in the user's repo (create directories as needed):

1. `docs/soc2/architecture.md` containing, in order:
   - Disclaimer line (verbatim, as above).
   - Scope: system name, system type, cloud, data classes, tenancy, workforce, TSC scope, report type, audit period (and as-of date only when applicable).
   - Mermaid diagram (`flowchart`) with a `subgraph` per trust boundary (internet, edge/DMZ, application, data, management/CI, third parties), arrows labeled with data class and protection, and the logging/evidence stream.
   - Top 10 to build first: the ten controls to build first, ranked by (a) live exposure if absent (secrets, public data, no logging, no backups), then (b) controls that cannot be backfilled for a Type 2 period (logging, change history, access reviews start dates, backups with restore tests), then (c) cheapest to automate. Each line: `ID → TSC`, what to build, owner role, and the first evidence artifact.
   - Component to control table with columns `Component | Service chosen | Controls (ID → TSC) | Evidence this produces for Type 2 (source, frequency, owner)`. ONE ROW PER COMPONENT; put its control list in the one cell, grouped by theme. Mark gaps `NO AUTOMATED EVIDENCE`. Do not expand to a row per component and control.
   - Implementation spec (below).
   - Excluded controls with reasons (including the unmapped-control diff and scope-gap exclusions); inherited controls (`AC-13 → CC6.4`, `AV-06 → A1.2`) with the provider, GOV-11 carve-out method, the SOC report to collect, and CUECs to map (GOV-12 → CC2.3 when customers must be told what they are responsible for).
   - System description inputs (GOV-13 → CC2.2, CC2.3): principal service commitments, system requirements, components, boundaries; the audit skill turns these into the DC 200 description.
   - Open gaps and assumptions.
   - ADR index linking each `docs/soc2/adr/NNNN-<slug>.md`.
2. `docs/soc2/adr/NNNN-<slug>.md`, one per significant decision, numbered from the next free number.
3. `.soc2/state.json` updated per below. ADR numbers are four-digit strings ("0003"), never paths.

### Implementation spec (developer deliverable)

For each component that carries code or IaC, write concrete items a developer can build, in the stack the user chose (or, if no stack is chosen, ask once, then use it):

- Modules: named modules or files with one-line responsibility (for example `intake/validate`, `pipeline/idempotency`, `pipeline/reconcile`, `delivery/signed_output`, `audit/log_event`, `infra/logging`, `infra/backup`).
- Interfaces and data contracts: schema for each input and output, rejection reasons, idempotency key definition, error classes (PI-02 → PI1.2, PI-06 → PI1.3).
- Acceptance tests per control, each pass/fail and runnable in CI: for example invalid or oversized input is rejected and logged with a reason; replaying the same file or message twice produces one result and the second attempt is logged as `duplicate_ignored` (PI-06 → PI1.3; on Azure this is the Cosmos create-if-not-exists test, not a Service Bus test); row counts and control totals in equal output (PI-03 → PI1.3); money rounding follows one documented rule and totals reconcile to the cent (PI-02 → PI1.2); a run that misses its SLA raises an alert (PI-07 → PI1.4); output is delivered only to the authorised recipient through an expiring link (PI-04 → PI1.4); cross-tenant read returns 403 (AC-06); no secrets in the repo and no secrets in local settings files (AC-17 → CC6.1); unauthenticated request to a data endpoint fails.
- IaC and CI: resources to define (log sinks/diagnostic settings with retention, backup plan, alert rules, KMS or Key Vault keys, branch protection or rulesets as code, required status checks, Trivy config or Checkov on the IaC, dependency and secret scanning), with naming that cannot collide with existing resources. Include the evidence query or export for each (for example a KQL or CLI query that lists rejected records per day).
- Order of work: map the Top 10 onto this spec as a first sprint.

Then offer: "I can scaffold these modules, tests and IaC in this repo now." Scaffold only on a yes, and never overwrite existing files: check for name collisions first and merge (for example an existing CODEOWNERS at root, `.github/` or `docs/`).

## Adding a component (incremental mode)

If `.soc2/state.json` has `completed` containing `soc2-architect` and `docs/soc2/architecture.md` exists, a request to add a service, store, pipeline or vendor does NOT rerun the whole design (completed never blocks a new-component request). Instead:

1. Read the existing architecture and ADR index; reuse state (no re-asked keys).
2. Ask only component-specific questions (what data it touches, who calls it, where it runs, new vendor?), in one message.
3. Map just that component, apply the unmapped-control diff only to controls the component newly touches, and apply the scope-gap flag if it introduces a new data class.
4. Append one row to the component table and its node and flows to the diagram; append to the implementation spec and Top 10 if it changes the ranking; add ADRs only for significant decisions (next free number).
5. List downstream documents to refresh: vendor register and sub-processor carve-out (VND-01, GOV-11), risk reassessment for a significant change (RSK-04), system description (GOV-13), CUECs if customer responsibilities change (GOV-12), readiness check and evidence automation for the new resources.

## Update state

Edit `.soc2/state.json` (keep unrelated keys untouched):

- `system`: set `name`, `company`, `owner`, `cloud` (array: `aws`, `gcp`, `azure`, `other`), `type`, `tenancy`, `workforce`, `tools`, `data_classes` (arrays where the router schema uses arrays), only for values answered or inferred and confirmed.
- `tsc_scope`, `report_type`, `audit_period`, `type1_report_date` (only when `report_type` is `type1` or the user asked for a Type 1 report) only when answered or explicitly accepted; leave skipped keys absent. If the user wants Type 1 now and Type 2 later, set `next_report` to `type2 after type1`.
- `decisions`: append `{"control": "<ID>", "choice": "<short choice>", "date": "<YYYY-MM-DD>", "adr": "<NNNN>"}` per control satisfied by each ADR; `adr` is the 4-digit number string, for example "0003" (not a path, not "3").
- `excluded`: append `{"control": "<ID>", "reason": "<specific reason>", "date": "<YYYY-MM-DD>"}` for every control listed under Excluded (unmapped-control diff, scope exclusions, small-team exclusions); skip an ID already present. Later skills show these as n/a with the stored reason and never re-list them.
- `completed`: add `"soc2-architect"` if not present.

Valid `tsc_scope` values: `security`, `availability`, `processing_integrity`, `confidentiality`, `privacy`. `report_type` is `type1` or `type2`.

Do not pre-fill any key. The full schema is in the router (`../soc2/SKILL.md`).

When done, suggest the next phase (`soc2-policies`, then `soc2-type1-readiness` once code or IaC exists, then `soc2-type2-operations`) and let the router or the user pick.
