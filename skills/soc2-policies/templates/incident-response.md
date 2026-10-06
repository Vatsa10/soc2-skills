# Incident Response Policy

| Field | Value |
|---|---|
| Company | {{company}} |
| Policy owner | {{owner}} |
| Effective date | {{effective_date}} |
| Review cadence | {{review_cadence}} |

## Purpose

This policy defines how {{company}} detects, triages, contains, communicates and learns from security incidents.

## Scope

All security events and incidents affecting {{company}} systems, data, personnel or customers, including incidents at sub-processors that affect {{company}} data.

## Policy statements

1. Anyone who suspects an incident reports it through the designated channel (security@ mailbox or #security-incidents chat channel) immediately and no later than 1 hour after discovery. [OPS-01 → CC7.2]
2. Each reported event is triaged within 1 hour during business hours and assigned a severity: SEV1 (confirmed data exposure or outage), SEV2 (contained compromise), SEV3 (suspicious, no impact). [OPS-02 → CC7.3]
3. An incident commander is named for every SEV1 and SEV2 incident and maintains a timestamped log of actions in the incident ticket. [OPS-03 → CC7.4]
4. Containment steps (credential revocation, host isolation, key rotation) start before root cause is complete for SEV1 incidents. [OPS-03 → CC7.4]
5. Evidence (logs, snapshots, ticket history) is preserved for at least 12 months for SEV1 and SEV2 incidents. [OPS-04 → CC7.5]
6. Affected customers are notified without undue delay and no later than 72 hours after {{company}} confirms their data was affected, or sooner if contract or law requires. [OPS-05 → CC7.1]
7. Every SEV1 and SEV2 incident receives a blameless postmortem within 10 business days, with corrective actions tracked to closure. [OPS-04 → CC7.5]
8. The incident response plan, contact list and escalation tree are tested by a tabletop exercise at least annually and updated within 30 days of any gap found. [OPS-05 → CC7.1]
9. Monitoring alerts for authentication anomalies, privilege changes and data egress route to the on-call engineer 24x7. [MON-01 → CC4.1]
10. Personal data incidents are assessed for notification duties under applicable breach laws within 24 hours of confirmation. [PR-01 → P1.1]
11. Availability incidents are reported on the status page within 30 minutes of confirmation. [AV-01 → A1.1]

## Roles

| Role | Responsibility |
|---|---|
| Incident commander | Leads response, assigns severity and owns the timeline. |
| {{owner}} | Owns this policy, runs annual tabletop exercises and approves postmortems. |
| Communications lead | Drafts customer, regulator and public notices. |
| All personnel | Report suspected incidents immediately. |

## Exceptions

Exceptions to this policy must be requested in writing, state the business reason and compensating controls, and be approved by {{owner}} (and by the CEO for exceptions affecting Restricted data). Each exception expires after at most 12 months and is recorded in the exceptions register.

## Enforcement

Violations are investigated by {{owner}} and People Operations. Confirmed violations may result in access removal, retraining, disciplinary action up to termination, and termination of contractor agreements. Violations that expose customer data are handled under the Incident Response Policy.

## Review

This policy is reviewed on the cadence in the header ({{review_cadence}}), and also after any major incident or material change to systems or scope. The effective date and approver are recorded in version control history. Next review is due before the end of the cadence period following {{effective_date}}.
