# SOC 2 Gap Assessment Report: <system name>

> This skill prepares for a SOC 2 audit; it is not an attestation. Only a licensed CPA firm can issue a SOC 2 Type 1 or Type 2 report.

Date: <YYYY-MM-DD> | Assessor: <agent/tool> | Scan cache: `.soc2/scan.json` (<scan timestamp>)

## 1. Executive summary

- Overall readiness: <Ready / Ready with remediation / Not ready> for <Type 1 | Type 2>
- Controls evaluated: <N> in scope | PASS <n> | PARTIAL <n> | FAIL <n> | N/A <n> (each N/A has a reason)
- Findings: High <n> | Medium <n> | Low <n>
- Top three risks: <one line each, each citing `ID -> TSC`>
- Recommended next step: <one line>

## 2. Scope

| Item | Value |
|---|---|
| TSC in scope | <security, availability, processing_integrity, confidentiality, privacy> |
| Report type | <type1 or type2> |
| Point in time (Type 1) or audit period (Type 2) | <date, or start to end> |
| System | <name, cloud(s), data classes, from `.soc2/state.json`> |
| Out of scope | <components, TSC, with reason> |

## 3. Methodology

1. Repository scan (`scan.py`): signals only, treated as hints, not proof.
2. Code and IaC inspection to confirm or contradict each signal.
3. Document review: `docs/soc2/*`, `docs/policies/*`, and evidence the user supplied.
4. Each in-scope catalog control evaluated against its `Pass rule`, using the Type 1 test or Type 2 test column per report type.
5. Type 2 only: evidence-existence check across the whole period and a sampling simulation using the catalog sampling guide (sample sizes are common auditor practice, not AICPA mandates).

Limits: the assessor sees the repository and supplied documents, not the cloud account, IdP, or HR records. Controls that rest on those sources are rated on the evidence provided.

## 4. Findings

Severity: High = missing control for a criterion, hardcoded secrets, or no logging. Medium = partial design or manual-only evidence. Low = documentation gap.

| # | ID -> TSC | Severity | Condition | Criteria | Cause | Effect | Recommendation |
|---|---|---|---|---|---|---|---|
| 1 | AC-17 -> CC6.1 | High | <what was observed; file path and line only, never the secret value> | <the catalog Pass rule / TSC criterion> | <why it happened> | <risk if left> | <specific fix, owner> |
| 2 | OPS-05 -> CC7.2 | Medium | <observed> | <criterion> | <cause> | <effect> | <fix> |

Rows above are format examples; replace them. Order by severity, then by TSC. Every row cites a catalog control ID and a TSC criterion.

### Findings by TSC

| TSC | Controls evaluated | PASS | PARTIAL | FAIL | N/A |
|---|---|---|---|---|---|
| Security (CC1-CC9) | | | | | |
| Availability (A1) | | | | | |
| Processing Integrity (PI1) | | | | | |
| Confidentiality (C1) | | | | | |
| Privacy (P1-P8) | | | | | |

## 5. Exceptions likely (Type 2 only)

Omit this section for Type 1. For each control where the simulated sample would fail:

| ID -> TSC | Frequency | Sample size | Simulated result | Why an exception is likely | Period gap |
|---|---|---|---|---|---|
| AC-05 -> CC6.2 | Quarterly | 2 | 1 of 2 evidenced | Q2 review has no record | Q2 |

Example row; replace. Include controls that have not fired inside the period (cannot be tested) and controls changed mid-period.

## 6. PBC (provided by client) list

| Request | Control IDs | Owner | Due |
|---|---|---|---|
| IdP MFA policy export and enrollment report | AC-02 | <name/role> | <YYYY-MM-DD> |
| User access review records, one per quarter in the period | AC-05 | <name/role> | <YYYY-MM-DD> |
| Cloud audit trail configuration and retention setting | OPS-06, OPS-07 | <name/role> | <YYYY-MM-DD> |
| Branch protection settings and sample of merged PRs with approvals | CHG-02, CHG-05 | <name/role> | <YYYY-MM-DD> |
| Latest restore test record | AV-04 | <name/role> | <YYYY-MM-DD> |
| Incident response plan and tabletop exercise record | OPS-10, OPS-11 | <name/role> | <YYYY-MM-DD> |
| Security training completion report | GOV-05 | <name/role> | <YYYY-MM-DD> |
| Vendor inventory with latest SOC reports and CUEC review | VND-03 | <name/role> | <YYYY-MM-DD> |

Example rows; build the real list from each evaluated control's `Evidence` field. Set due dates before fieldwork. For Type 2, request full population lists for the whole period, not only samples.

## 7. Remediation roadmap

| Window | Focus | Items (finding # / control ID) | Owner |
|---|---|---|---|
| 0-30 days | All High findings; anything blocking the report date | | |
| 31-60 days | Medium findings; start evidence automation for Type 2 | | |
| 61-90 days | Low findings; documentation; dry run of the PBC list | | |

For Type 2, flag any fix that changes a control mid-period: record it through change management with an effective date, or defer it to the next period.

## 8. Disclaimer

This skill prepares for a SOC 2 audit; it is not an attestation. Only a licensed CPA firm can issue a SOC 2 Type 1 or Type 2 report.
