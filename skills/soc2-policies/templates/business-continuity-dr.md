# Business Continuity and Disaster Recovery Policy

| Field | Value |
|---|---|
| Company | {{company}} |
| Policy owner | {{owner}} |
| Approver | {{approver}} |
| Approval date | {{approval_date}} |
| Version | {{version}} |
| Effective date | {{effective_date}} |
| Review cadence | {{review_cadence}} |
| Next review due | {{next_review}} |

## Purpose

This policy ensures {{company}} can keep delivering its services, or restore them within agreed objectives, after a disruption.

## Scope

All production systems, data stores, supporting vendors and personnel needed to deliver the in-scope services.

## Policy statements

_Numbers and timeframes in these statements are defaults. {{owner}} must confirm {{company}} can meet each one before approving this policy, because an auditor tests against the policy as written. Statements that start with "(if ... in scope)" apply only when that category is in the audit scope._

1. {{company}} documents a recovery time objective (RTO) and recovery point objective (RPO) for each production service; defaults are RTO 8 hours and RPO 24 hours unless a customer contract specifies otherwise. [RSK-05 → A1.2] [RSK-05 → CC9.1]
2. Production databases and object storage are backed up automatically at least daily, with point-in-time recovery enabled where the platform supports it. [AV-03 → A1.2]
3. Backups ({{cloud_backup}}) are encrypted, stored in a different region or account than the primary data, and retained for at least 35 days. [AV-03 → A1.2] [AC-09 → C1.1]
4. Restoration from backup is tested at least annually, and the test records date, data set, time taken and any failure. [AV-04 → A1.3]
5. (if availability in scope) Production is deployed across at least two availability zones where the cloud provider offers them. [AV-02 → A1.2]
6. (if availability in scope) Capacity and availability are monitored, with alerts when CPU, memory, storage or error rate exceeds documented thresholds. [AV-01 → A1.1]
7. A written disaster recovery runbook lists step-by-step recovery for loss of a region, a database and the primary cloud account, and is stored where it is accessible if production is down. [AV-05 → A1.2]
8. A continuity tabletop exercise is performed at least annually, and the plan is updated within 30 days of lessons learned. [AV-05 → A1.3]
9. Critical vendors have documented fallback or exit plans reviewed annually. [VND-03 → CC9.2]
10. The continuity plan names a primary and a backup person for each critical role, and states how staff work if the office is unavailable. [RSK-05 → CC9.1]
11. Business impact analysis and the continuity risks it identifies are included in the annual risk assessment. [RSK-01 → CC3.2]
12. (if processing_integrity in scope) Backups are verified for integrity (checksums or successful test restore) so stored data is complete and accurate after recovery. [AV-03 → PI1.5]

## Roles

| Role | Responsibility |
|---|---|
| {{owner}} | Owns the continuity plan and test schedule. |
| Engineering lead | Owns backup configuration and restoration procedures. |
| Incident commander | Declares a disaster and leads recovery. |

## Exceptions

Exceptions to this policy must be requested in writing, state the business reason and compensating controls, and be approved by {{owner}} (and by the most senior executive for exceptions affecting Restricted data). Each exception expires after at most 12 months and is recorded in the exceptions register, a dated list kept by {{owner}} with requester, reason, compensating controls, approver and expiry.

## Enforcement

Violations are investigated by {{owner}} and People Operations (or whoever handles HR). Confirmed violations may result in access removal, retraining, disciplinary action up to termination, and termination of contractor agreements. Violations that expose customer data are handled under the Incident Response Policy.

## Review and approval

This policy is reviewed on the cadence in the header ({{review_cadence}}), and also after any major incident or material change to systems or scope. Approval (approver name and date) is recorded in the header and in the revision history below; version-control history alone is not evidence of approval. After a material change, all personnel re-acknowledge the policy set within 30 days (Information Security Policy, statement 5). Next review is due by the date in the header.

| Version | Date | Change | Approved by |
|---|---|---|---|
| {{version}} | {{effective_date}} | Initial issue | {{approver}} |
