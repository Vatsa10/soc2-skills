# SOC 2 Gap Assessment Report: <system name>

> This skill prepares for a SOC 2 audit; it is not an attestation. Only a licensed CPA firm can issue a SOC 2 Type 1 or Type 2 report.

Date: <YYYY-MM-DD> | Assessor: <agent/tool> | Mode: <full gap / Type 2 gap / pre-period readiness> | Scan cache: `.soc2/scan.json` (<scan timestamp>)

## 1. Executive summary

- Do today: <one line per Blocker, e.g. "Rotate the credential at path:line and purge it from history"; or "None">
- Overall readiness: <No gaps found against in-scope catalog controls (not an attestation) / Gaps found, remediation needed / Not ready> for <Type 1 | Type 2>
- Controls evaluated: <N> in scope | designed <n> | partial <n> | missing <n> | needs-evidence <n> | n/a <n> (each n/a has a reason)
- Findings: Blocker <n> | High <n> | Medium <n> | Low <n>
- Period warning (Type 2, if applicable): <window already started or ended and most controls missing: the elapsed part cannot be backfilled; consider a later window or a Type 1>
- Top three risks: <one line each, each citing `ID → TSC`>
- Recommended next step: <one line>

## 2. Scope

| Item | Value |
|---|---|
| TSC in scope | <security, availability, processing_integrity, confidentiality, privacy> |
| Report type | <type1 or type2> |
| As-of date (Type 1) or audit period (Type 2) | <date, or start to end> |
| System | <name, cloud(s), data classes, from `.soc2/state.json`> |
| Subservice organizations and method | <e.g. cloud provider, IdP: carve-out> |
| Out of scope | <components, TSC, with reason> |
| Excluded controls (`state.excluded[]`) | <ID, reason, date; shown as n/a, never listed as findings> |

## 3. Methodology

1. Repository scan (`scan.py`): signals only, treated as hints, not proof.
2. Code and IaC inspection to confirm or contradict each signal.
3. Document review: `docs/soc2/*`, `docs/policies/*`, and evidence the user supplied.
4. Each in-scope catalog control judged against its `Type 1 test` / `Type 1 pass` or `Type 2 test` / `Type 2 pass`.
5. Type 2 gap only: evidence continuity across the whole period and a sampling simulation using the catalog sampling guide (sample sizes are common auditor practice, not AICPA mandates). Pre-period readiness: evidence-live-by dates instead of sampling.

Limits: the assessor sees the repository and supplied documents, not the cloud account, IdP, or HR records. Controls resting on those sources are `needs-evidence` until evidence is supplied. The severity tiers are a readiness rubric; auditors report deviations and may qualify their opinion.

## 4. Findings

Severity: Blocker = live exposure now (secrets in repo, public data, no logging, no production backups; under Security-only the backup gap is cited as `RSK-05 → CC9.1`, with a note that AV-03 and AV-04 apply if Availability is added). High = missing control on a live system, or not backfillable for the Type 2 period. Medium = partial design, manual-only evidence, or not yet built on a pre-production repo. Low = documentation gap.

| # | ID → TSC | Severity | Status | Condition | Criteria | Cause | Effect | Recommendation (for <cloud>) |
|---|---|---|---|---|---|---|---|---|
| 1 | AC-17 → CC6.1 | Blocker | missing | <what was observed; file path, line and kind from `scan.py --secrets` only, never the secret value> | <catalog Type 1 pass or Type 2 pass; TSC criterion> | <why> | <risk if left> | <rotate or revoke, remove, purge history; owner> |
| 2 | OPS-05 → <TSC> | Medium | partial | <observed> | <criterion> | <cause> | <effect> | <fix from the system's cloud-equivalents column> |

Rows above are format examples; replace them. Order: Blockers, then non-backfillable Type 2 controls, then severity; cluster by control family. Every row cites a catalog control ID and the TSC from its catalog TSC line.

### Findings by TSC

| TSC | Evaluated | designed | partial | missing | needs-evidence | n/a |
|---|---|---|---|---|---|---|
| Security (CC1-CC9) | | | | | | |
| Availability (A1) | | | | | | |
| Processing Integrity (PI1) | | | | | | |
| Confidentiality (C1) | | | | | | |
| Privacy (P1-P8) | | | | | | |

Each control is counted once, under its first in-scope criterion; add the footnote "in scope via secondary criterion" where the first-listed criterion is out of scope. The per-TSC rows must sum to the executive-summary total.

## 5. Exceptions likely (Type 2 gap only)

Omit for Type 1 and pre-period readiness.

| ID → TSC | Frequency | Population source (IPE) | Sample size | Simulated result | Why an exception is likely | Period gap |
|---|---|---|---|---|---|---|
| AC-05 → <TSC> | Quarterly | IdP user export, query <params> | 2 | 1 of 2 evidenced | Q2 review has no record | Q2 |

Example row; replace. Include scheduled controls that missed a run (a deviation), annual items lapsing mid-period, and controls changed mid-period. Event-driven controls with no events in the period are "no occurrence, not tested" (keep the empty population report), not exceptions. One failing sample usually means expanded testing or a reported deviation.

### Evidence live by (pre-period readiness only)

| ID → TSC | Frequency | Evidence live by | First in-period run | Risk |
|---|---|---|---|---|

## 6. PBC (provided by client) list

Grouped by source system. Merge key = one artifact that serves several controls.

| Source system | Merge key | Request | Control IDs | Owner | Due |
|---|---|---|---|---|---|
| IdP | idp-users | MFA policy export and enrollment report; user list with query parameters (IPE) | AC-02 → CC6.1 | <role> | <YYYY-MM-DD> |
| IdP | idp-access-reviews | User access review records, one per quarter in the period | AC-05 → <TSC> | <role> | <YYYY-MM-DD> |
| Cloud console | cloud-audit-trail | Audit trail configuration and retention setting | OPS-06 → <TSC>; OPS-07 → <TSC> | <role> | <YYYY-MM-DD> |
| Cloud console | cloud-backups | Backup configuration and latest restore test record | AV-04 → <TSC> | <role> | <YYYY-MM-DD> |
| Git host | git-change-mgmt | Branch protection or rulesets export; merged PRs with approvals; deploy log reconciled to approved PRs | CHG-02 → <TSC>; CHG-04 → CC8.1 | <role> | <YYYY-MM-DD> |
| Ticketing | incidents | Incident response plan, incident population, tabletop record | OPS-10 → <TSC>; OPS-11 → <TSC> | <role> | <YYYY-MM-DD> |
| HR system | hr-training | Security training completion report | GOV-05 → <TSC> | <role> | <YYYY-MM-DD> |
| Vendor files | vendor-soc-reports | Vendor inventory; latest SOC reports (period overlap, opinion, exceptions, carve-outs); bridge letters; CUEC review | VND-03 → <TSC> | <role> | <YYYY-MM-DD> |
| Management | report-deliverables | Draft system description (DC 200), `docs/soc2/system-description.md` | GOV-13 → <TSC> | <role> | <YYYY-MM-DD> |
| Management | report-deliverables | Draft management assertion (Section II) and representation letter, `docs/soc2/management-assertion.md` | GOV-13 → <TSC> | <role> | <YYYY-MM-DD> |
| Management | report-deliverables | Subservice organizations, method (carve-out or inclusive), CSOCs relied on | GOV-11 → <TSC> | <role> | <YYYY-MM-DD> |
| Management | report-deliverables | CUECs published to customers | GOV-12 → <TSC> | <role> | <YYYY-MM-DD> |
| Management | report-deliverables | Own bridge letter for customers (signed by management, unaudited, usually 3 months or less) | GOV-13 → <TSC> | <role> | <YYYY-MM-DD> |

Example rows; build the real list from each evaluated control's `Evidence` field and fill each `<TSC>` from that control's TSC line in the control index. Set due dates before fieldwork. For Type 2, request full populations for the whole period and, for each, record the source system and the query or report parameters so the auditor can re-run it (IPE).

## 7. Remediation roadmap

| Window | Focus | Items (finding # / `ID → TSC`) | Owner | Done when |
|---|---|---|---|---|
| Do today | Blockers | | | |
| 0-30 days (or week 1 of a 2-week plan) | Non-backfillable Type 2 controls; High findings | | | |
| 31-60 days (or week 2) | Medium findings; evidence automation | | | |
| 61-90 days | Low findings; documentation; PBC dry run; system description and assertion review | | | |

"Done when" is the control's `Type 1 pass` or `Type 2 pass` condition. For Type 2, a fix that changes a control mid-period goes through change management with an effective date, or waits for the next period.

## 8. Disclaimer

This skill prepares for a SOC 2 audit; it is not an attestation. Only a licensed CPA firm can issue a SOC 2 Type 1 or Type 2 report.
