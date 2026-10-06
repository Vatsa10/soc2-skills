# Data Retention and Disposal Policy

| Field | Value |
|---|---|
| Company | {{company}} |
| Policy owner | {{owner}} |
| Effective date | {{effective_date}} |
| Review cadence | {{review_cadence}} |

## Purpose

This policy sets how long {{company}} keeps data and how it is securely destroyed afterward, so data is neither deleted too early nor kept longer than needed.

## Scope

All customer, employee, business and system data held by {{company}} or its sub-processors, including backups and logs.

## Policy statements

1. Retention periods are: customer data for the term of the contract plus 30 days after termination; application logs 12 months; security and audit logs 12 months (hot 90 days); backups 35 days; financial records 7 years; employee records 7 years after separation. [CF-01 → C1.1]
2. Customer data is deleted from production systems within 30 days of contract termination or a verified deletion request, and from backups when they expire. [CF-02 → C1.1]
3. Deletion is automated where possible (lifecycle rules, scheduled jobs), and {{owner}} checks at least annually that the jobs ran as designed. [CF-03 → C1.2]
4. Cloud storage and databases are deleted using the provider's deletion service; for physical media, drives are wiped using NIST 800-88 methods or physically destroyed. [CF-04 → C1.2]
5. Company laptops are wiped before reuse or disposal and a record of the asset ID, date and method is kept. [CF-04 → C1.2]
6. Where a legal hold applies, deletion for the affected data is suspended until Legal releases the hold in writing. [CF-02 → C1.1]
7. Customers can request deletion or export of their data, and requests are fulfilled and logged within 30 days. [PR-01 → P1.1]
8. Personal data is retained only as long as needed for the purpose stated in the privacy notice. [PR-02 → P3.1]
9. Sub-processors are contractually required to delete or return {{company}} data at the end of the engagement. [VND-01 → CC9.2]
10. A certificate or log entry evidencing disposal is kept for each decommissioned device or data set containing Restricted data. [CF-03 → C1.2]
11. Retention schedules are reviewed annually and whenever a new system or data type is added. [CF-01 → C1.1]

## Roles

| Role | Responsibility |
|---|---|
| {{owner}} | Owns the retention schedule. |
| Engineering lead | Implements deletion jobs and verifies them. |
| Legal | Issues and releases legal holds. |

## Exceptions

Exceptions to this policy must be requested in writing, state the business reason and compensating controls, and be approved by {{owner}} (and by the CEO for exceptions affecting Restricted data). Each exception expires after at most 12 months and is recorded in the exceptions register.

## Enforcement

Violations are investigated by {{owner}} and People Operations. Confirmed violations may result in access removal, retraining, disciplinary action up to termination, and termination of contractor agreements. Violations that expose customer data are handled under the Incident Response Policy.

## Review

This policy is reviewed on the cadence in the header ({{review_cadence}}), and also after any major incident or material change to systems or scope. The effective date and approver are recorded in version control history. Next review is due before the end of the cadence period following {{effective_date}}.
