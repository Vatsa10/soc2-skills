# Business Continuity and Disaster Recovery Policy

| Field | Value |
|---|---|
| Company | {{company}} |
| Policy owner | {{owner}} |
| Effective date | {{effective_date}} |
| Review cadence | {{review_cadence}} |

## Purpose

This policy ensures {{company}} can keep delivering its services, or restore them within agreed objectives, after a disruption.

## Scope

All production systems, data stores, supporting vendors and personnel needed to deliver the in-scope services.

## Policy statements

1. {{company}} documents a recovery time objective (RTO) and recovery point objective (RPO) for each production service; defaults are RTO 8 hours and RPO 24 hours unless a customer contract specifies otherwise. [RSK-05 → A1.2] [RSK-05 → CC9.1]
2. Production databases and object storage are backed up automatically at least daily, with point-in-time recovery enabled where the platform supports it. [AV-03 → A1.2] [AV-03 → PI1.5]
3. Backups are encrypted, stored in a different region or account than the primary data, and retained for at least 35 days. [AV-03 → A1.2] [AC-09 → C1.1]
4. Restoration from backup is tested at least annually, and the test records date, data set, time taken and any failure. [AV-04 → A1.3]
5. Production is deployed across at least two availability zones where the cloud provider offers them. [AV-02 → A1.2]
6. Capacity and availability are monitored, with alerts when CPU, memory, storage or error rate exceeds documented thresholds. [AV-01 → A1.1]
7. A written disaster recovery runbook lists step-by-step recovery for loss of a region, a database and the primary cloud account, and is stored where it is accessible if production is down. [AV-05 → A1.2]
8. A continuity tabletop exercise is performed at least annually, and the plan is updated within 30 days of lessons learned. [AV-05 → A1.3]
9. Critical vendors have documented fallback or exit plans reviewed annually. [VND-03 → CC9.2]
10. Employees have the ability to work remotely, and the continuity plan identifies at least two people able to perform each critical role. [RSK-05 → CC9.1]
11. Business impact analysis and the continuity risks it identifies are included in the annual risk assessment. [RSK-01 → CC3.2]

## Roles

| Role | Responsibility |
|---|---|
| {{owner}} | Owns the continuity plan and test schedule. |
| Engineering lead | Owns backup configuration and restoration procedures. |
| Incident commander | Declares a disaster and leads recovery. |

## Exceptions

Exceptions to this policy must be requested in writing, state the business reason and compensating controls, and be approved by {{owner}} (and by the CEO for exceptions affecting Restricted data). Each exception expires after at most 12 months and is recorded in the exceptions register.

## Enforcement

Violations are investigated by {{owner}} and People Operations. Confirmed violations may result in access removal, retraining, disciplinary action up to termination, and termination of contractor agreements. Violations that expose customer data are handled under the Incident Response Policy.

## Review

This policy is reviewed on the cadence in the header ({{review_cadence}}), and also after any major incident or material change to systems or scope. The effective date and approver are recorded in version control history. Next review is due before the end of the cadence period following {{effective_date}}.
