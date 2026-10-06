# Logging and Monitoring Policy

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

This policy ensures {{company}} records security-relevant events, protects those records, and detects and responds to anomalies.

## Scope

All production systems, cloud accounts, identity providers, endpoints and network devices in scope.

## Policy statements

_Numbers and timeframes in these statements are defaults. {{owner}} must confirm {{company}} can meet each one before approving this policy, because an auditor tests against the policy as written. Statements that start with "(if ... in scope)" apply only when that category is in the audit scope._

1. The following events are logged with timestamp, actor, source and outcome: authentication success and failure, privilege and permission changes, access to Restricted data, configuration changes, and administrative actions. [OPS-05 → CC7.2]
2. Cloud audit logs ({{cloud_audit_trail}}) are enabled in all accounts, projects or subscriptions, and regions. [OPS-06 → CC7.2]
3. Logs are forwarded to a central log platform and retained for at least 12 months, with the most recent 90 days immediately searchable. [OPS-07 → CC7.2]
4. Log storage is access-controlled, and write-once or tamper-evident settings are used so that engineers cannot alter or delete logs. [OPS-06 → CC7.2]
5. System clocks are synchronized to a trusted NTP source. [OPS-05 → CC7.2]
6. Alerts are configured for repeated failed logins, new administrator creation, root account use, disabled logging, and unusual data egress; alerts page the on-call engineer (coverage: {{oncall_hours}}). [OPS-08 → CC7.2]
7. Alerts are acknowledged within 15 minutes and triaged within 1 hour; resolution is recorded in the ticket. [OPS-08 → CC7.3]
8. Vulnerability scans of production are run at least monthly, and external penetration tests at least annually. [OPS-01 → CC7.1] [MON-02 → CC7.1]
9. Vulnerability remediation deadlines (the single source for all policies) are: critical within 15 days, high within 30 days, medium within 90 days and low within 180 days or risk-accepted in writing. The clock starts when the vulnerability is detected, or when the vendor patch is released if that is later. A vulnerability listed in the CISA Known Exploited Vulnerabilities catalogue, or known to be exploited in the wild, is remediated or mitigated within 7 days (a {{company}} commitment based on common practice, not a standard). Exceptions are risk-accepted in writing with an expiry date. [OPS-01 → CC7.1]
10. (if availability in scope) Uptime, latency and error-rate monitoring covers all customer-facing services, with alerts on breaching service-level thresholds. [AV-01 → A1.1]
11. Log coverage and alert rules are reviewed at least annually, and after every SEV1 or SEV2 incident. [MON-04 → CC4.1]
12. Control monitoring checks (for example, MFA coverage and encryption settings) are run automatically at least monthly and failures are ticketed. [MON-01 → CC4.1]
13. (if processing_integrity in scope) Data processing jobs are monitored for failure and lag, record counts in and out are reconciled daily for critical data flows, and discrepancies are ticketed and resolved. [PI-03 → PI1.3]

## Roles

| Role | Responsibility |
|---|---|
| {{owner}} | Owns logging standards and alert coverage. |
| On-call engineer | Triages alerts (coverage: {{oncall_hours}}). |
| Engineering lead | Implements log sources and retention. |

## Exceptions

Exceptions to this policy must be requested in writing, state the business reason and compensating controls, and be approved by {{owner}} (and by the most senior executive for exceptions affecting Restricted data). Each exception expires after at most 12 months and is recorded in the exceptions register, a dated list kept by {{owner}} with requester, reason, compensating controls, approver and expiry.

## Enforcement

Violations are investigated by {{owner}} and People Operations (or whoever handles HR). Confirmed violations may result in access removal, retraining, disciplinary action up to termination, and termination of contractor agreements. Violations that expose customer data are handled under the Incident Response Policy.

## Review and approval

This policy is reviewed on the cadence in the header ({{review_cadence}}), and also after any major incident or material change to systems or scope. Approval (approver name and date) is recorded in the header and in the revision history below; version-control history alone is not evidence of approval. After a material change, all personnel re-acknowledge the policy set within 30 days (Information Security Policy, statement 5). Next review is due by the date in the header.

| Version | Date | Change | Approved by |
|---|---|---|---|
| {{version}} | {{effective_date}} | Initial issue | {{approver}} |
