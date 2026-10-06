---
name: soc2-architect
description: Design systems from the ground up to SOC 2 Type 1/Type 2 across all five TSC. Use during brainstorming, greenfield architecture, or when adding a new component/service, so controls are designed in rather than bolted on.
---

# soc2-architect

This skill prepares for a SOC 2 audit; it is not an attestation. Only a licensed CPA firm can issue a SOC 2 Type 1 or Type 2 report.

Use while a system is being designed (or a component added) so the required controls and their Type 2 evidence are part of the architecture. Works the same in Claude Code and Codex; paths below are relative to the skill folder and the user's repo.

## Shared references

- Control catalog (single source of truth for IDs, TSC mapping, tests, evidence, pass rules): `../soc2/references/control-catalog.md`
- Criteria list: `../soc2/references/tsc-criteria.md`
- Component to control map: `references/component-controls.md`
- ADR template: `references/adr-template.md`

Rules: cite every control as `ID → TSC` (for example `AC-02 → CC6.1, CC6.2`). Take the TSC only from the control's `TSC:` line in the catalog; never guess an ID or mapping, and never invent pass criteria. Look the ID up first.

## Step 0: Read state

Read `.soc2/state.json` if it exists. Anything already answered there (`tsc_scope`, `report_type`, `audit_period`, `system.name`, `system.cloud`, `system.data_classes`) is never asked again. Follow the router's First-run rule (`../soc2/SKILL.md`): ask first, then write. If `.soc2/state.json` does not exist, create it containing only the keys the user answered (or whose offered default they explicitly accepted); omit unanswered keys so they are asked again next time. `decisions: []` and `completed: []` may be initialized.

## Step 1: Questions

Ask one question at a time, waiting for the answer, and skip any already in state. Offer concrete choices where possible.

1. System type: what is being built and who uses it (B2B SaaS, internal tool, data platform, mobile backend, API product, AI/ML service)?
2. Data classes: which does it handle (public, internal, confidential customer data, PII, sensitive PII, PHI, cardholder data)? If PHI or cardholder data, state that HIPAA or PCI DSS applies separately and SOC 2 does not replace them.
3. Cloud: AWS, GCP, Azure, multi-cloud, or on-premises (and the SaaS tools in play: IdP, SCM, CI, ticketing, monitoring)?
4. Users and tenancy: workforce size, customer count, single- or multi-tenant, admin/support access to customer data?
5. TSC scope and report type: offer the router's default of all five criteria (Security, Availability, Processing Integrity, Confidentiality, Privacy) and let the user accept or narrow it (Security is always in scope). Type 1 (a point in time) or Type 2 (an observation period, and its start date)?

Save each confirmed answer to `.soc2/state.json` as soon as it is given. Never write a value the user did not give or accept; a skipped question leaves its key absent.

## Step 2: Procedure

1. List components. Enumerate every component in the design: identity provider, edge/gateway, app services, databases, object storage, queues, CI/CD, secrets/keys, logging/SIEM, monitoring/alerting, backups/DR, endpoints, third-party SaaS/vendors, data pipelines, PII stores. Also list external actors and where each data class lives.
2. Map each component. For each, find its row in `references/component-controls.md`; merge rows when a component matches several. Add the cross-cutting controls and any data-class triggers.
3. Pull catalog entries. Read the catalog entry for every mapped ID (Applies when, Implement, Type 1/Type 2 test, Evidence, Pass rule). Drop controls whose `Applies when` is false or that are out of scope under the catalog's Scope selection rule (`../soc2/references/control-catalog.md`): a control is in scope when any criterion on its `TSC:` line belongs to an in-scope category by series (CC → security, A1 → availability, PI1 → processing_integrity, C1 → confidentiality, P → privacy), and record the exclusion with a reason.
4. Choose concrete services. Use the AWS/GCP/Azure examples in the map for the user's cloud. Prefer designs that make evidence automatic.
5. Produce the Mermaid diagram (see Output contract) with trust boundaries and data flows, labeling flows with the data class and encryption (`AC-10 → CC6.1, CC6.7`) and marking where the log/evidence streams go.
6. Produce the component to control table (see Output contract).
7. Write one ADR per significant choice using `references/adr-template.md` (IdP, encryption/key management, tenancy isolation, logging pipeline, backup/DR strategy, CI/CD and change control, vendor selection). Present the design and ADR list to the user for confirmation before writing files if any choice was ambiguous.

## Type 2 by design rule

Every control in the design must name its automated evidence source (for example an IdP API export, CloudTrail, an AWS Config rule, a pipeline log, a ticket query). If a control has no automated source, flag it in the table as `NO AUTOMATED EVIDENCE`, state the manual evidence and who owns it, and add it to the ADR's gap list. Do this for Type 1 projects too, because evidence collection must begin when the observation period starts. Retain logs for at least one year (`OPS-07 → CC7.2`).

## Output contract

Write these files in the user's repo (create directories as needed):

1. `docs/soc2/architecture.md` containing, in order:
   - Disclaimer line (verbatim, as above).
   - Scope: system name, system type, cloud, data classes, tenancy, TSC scope, report type, audit period.
   - Mermaid diagram (`flowchart`) with a `subgraph` per trust boundary (internet, edge/DMZ, application, data, management/CI, third parties), arrows labeled with data class and protection, and the logging/evidence stream.
   - Component to control table with these columns: `Component | Service chosen | Control → TSC | Evidence this produces for Type 2 (source, frequency)`. One row per component and control; mark gaps `NO AUTOMATED EVIDENCE`.
   - Excluded controls with reasons; inherited controls (`AC-13 → CC6.4`, `AV-06 → A1.2`) with the provider and the report to collect.
   - Open gaps and assumptions.
   - ADR index linking each `docs/soc2/adr/NNNN-<slug>.md`.
2. `docs/soc2/adr/NNNN-<slug>.md`, one per significant decision, numbered from the next free number.
3. `.soc2/state.json` updated per below.

## Update state

Edit `.soc2/state.json` (keep unrelated keys untouched):

- `system`: set `name`, `cloud` (array: `aws`, `gcp`, `azure`), `data_classes` (array).
- `tsc_scope`, `report_type`, `audit_period` only when answered or explicitly accepted; leave skipped keys absent.
- `decisions`: append `{"control": "<ID>", "choice": "<short choice>", "date": "<YYYY-MM-DD>"}` per control satisfied by each ADR.
- `completed`: add `"soc2-architect"` if not present.

Valid `tsc_scope` values: `security`, `availability`, `processing_integrity`, `confidentiality`, `privacy`. `report_type` is `type1` or `type2`.

Do not pre-fill any key. The full schema is in the router's First run section (`../soc2/SKILL.md`).

When done, suggest the next phase (`soc2-policies`, then `soc2-type1-readiness` once code or IaC exists, then `soc2-type2-operations`) and let the router or the user pick.
