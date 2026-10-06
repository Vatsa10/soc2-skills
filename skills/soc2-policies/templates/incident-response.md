# Incident Response Policy

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

This policy defines how {{company}} detects, triages, contains, communicates and learns from security incidents.

## Scope

All security events and incidents affecting {{company}} systems, data, personnel or customers, including incidents at sub-processors that affect {{company}} data.

## Policy statements

_Numbers and timeframes in these statements are defaults. {{owner}} must confirm {{company}} can meet each one before approving this policy, because an auditor tests against the policy as written. Statements that start with "(if ... in scope)" apply only when that category is in the audit scope._

1. Anyone who suspects an incident reports it through the designated channel (security@ mailbox or #security-incidents chat channel) immediately and no later than 1 hour after discovery. [OPS-09 → CC7.3]
2. Each reported event is triaged within 1 hour of the report (at any hour for alerts that page on-call) and assigned a severity: SEV1 (confirmed data exposure or outage), SEV2 (contained compromise), SEV3 (suspicious, no impact). [OPS-09 → CC7.3]
3. An incident commander is named for every SEV1 and SEV2 incident and maintains a timestamped log of actions in the incident ticket. [OPS-10 → CC7.4]
4. Containment steps (credential revocation, host isolation, key rotation) start before root cause is complete for SEV1 incidents. [OPS-10 → CC7.4]
5. Evidence (logs, snapshots, ticket history) is preserved for at least 12 months for SEV1 and SEV2 incidents. [OPS-10 → CC7.4]
6. Affected customers are notified without undue delay and no later than 72 hours after {{company}} confirms their data was affected, or sooner if contract or law requires. [OPS-13 → CC7.4] [OPS-13 → CC2.3]
7. Every SEV1 and SEV2 incident receives a blameless postmortem within 10 business days, with corrective actions tracked to closure. [OPS-12 → CC7.5]
8. The incident response plan, contact list and escalation tree are tested by a tabletop exercise at least annually and updated within 30 days of any gap found. [OPS-11 → CC7.5]
9. Monitoring alerts for authentication anomalies, privilege changes and data egress route to the on-call engineer 24x7. [OPS-08 → CC7.2] [OPS-14 → CC7.4]
10. (if privacy in scope) Personal data incidents are assessed for notification duties under applicable breach laws within 24 hours of confirmation. [PR-12 → P6.3]
11. Availability incidents are reported on the status page within 30 minutes of confirmation. [GOV-09 → CC2.3]

## Roles

| Role | Responsibility |
|---|---|
| Incident commander | Leads response, assigns severity and owns the timeline. |
| {{owner}} | Owns this policy, runs annual tabletop exercises and approves postmortems. |
| Communications lead | Drafts customer, regulator and public notices. |
| All personnel | Report suspected incidents immediately. |

## Exceptions

Exceptions to this policy must be requested in writing, state the business reason and compensating controls, and be approved by {{owner}} (and by the most senior executive for exceptions affecting Restricted data). Each exception expires after at most 12 months and is recorded in the exceptions register, a dated list kept by {{owner}} with requester, reason, compensating controls, approver and expiry.

## Enforcement

Violations are investigated by {{owner}} and People Operations (or whoever handles HR). Confirmed violations may result in access removal, retraining, disciplinary action up to termination, and termination of contractor agreements. Violations that expose customer data are handled under the Incident Response Policy.

## Review and approval

This policy is reviewed on the cadence in the header ({{review_cadence}}), and also after any major incident or material change to systems or scope. Approval (approver name and date) is recorded in the header and in the revision history below; version-control history alone is not evidence of approval. After a material change, all personnel re-acknowledge the policy set within 30 days (Information Security Policy, statement 5). Next review is due by the date in the header.

| Version | Date | Change | Approved by |
|---|---|---|---|
| {{version}} | {{effective_date}} | Initial issue | {{approver}} |
