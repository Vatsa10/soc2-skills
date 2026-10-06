# Logging and Monitoring Policy

| Field | Value |
|---|---|
| Company | {{company}} |
| Policy owner | {{owner}} |
| Effective date | {{effective_date}} |
| Review cadence | {{review_cadence}} |

## Purpose

This policy ensures {{company}} records security-relevant events, protects those records, and detects and responds to anomalies.

## Scope

All production systems, cloud accounts, identity providers, endpoints and network devices in scope.

## Policy statements

1. The following events are logged with timestamp, actor, source and outcome: authentication success and failure, privilege and permission changes, access to Restricted data, configuration changes, and administrative actions. [OPS-05 → CC7.2]
2. Cloud audit logs (such as AWS CloudTrail, Google Cloud Audit Logs or Azure Activity Log) are enabled in all accounts and regions. [OPS-06 → CC7.2]
3. Logs are forwarded to a central log platform and retained for at least 12 months, with the most recent 90 days immediately searchable. [OPS-07 → CC7.2]
4. Log storage is access-controlled, and write-once or tamper-evident settings are used so that engineers cannot alter or delete logs. [OPS-06 → CC7.2]
5. System clocks are synchronized to a trusted NTP source. [OPS-05 → CC7.2]
6. Alerts are configured for repeated failed logins, new administrator creation, root account use, disabled logging, and unusual data egress; alerts page the on-call engineer. [OPS-08 → CC7.2]
7. Alerts are acknowledged within 15 minutes and triaged within 1 hour; resolution is recorded in the ticket. [OPS-08 → CC7.3]
8. Vulnerability scans of production are run at least weekly, and external penetration tests at least annually. [OPS-01 → CC7.1] [MON-02 → CC7.1]
9. Critical vulnerabilities are remediated within 7 days, high within 30 days and medium within 90 days; exceptions are risk-accepted in writing. [OPS-01 → CC7.1]
10. Uptime, latency and error-rate monitoring covers all customer-facing services, with alerts on breaching service-level thresholds. [AV-01 → A1.1]
11. Log coverage and alert rules are reviewed at least annually, and after every SEV1 or SEV2 incident. [MON-04 → CC4.1]
12. Control monitoring checks (for example, MFA coverage and encryption settings) are run automatically at least monthly and failures are ticketed. [MON-01 → CC4.1]
13. Data processing jobs are monitored for failure and lag, record counts in and out are reconciled daily for critical data flows, and discrepancies are ticketed and resolved. [PI-03 → PI1.3]

## Roles

| Role | Responsibility |
|---|---|
| {{owner}} | Owns logging standards and alert coverage. |
| On-call engineer | Triages alerts 24x7. |
| Engineering lead | Implements log sources and retention. |

## Exceptions

Exceptions to this policy must be requested in writing, state the business reason and compensating controls, and be approved by {{owner}} (and by the CEO for exceptions affecting Restricted data). Each exception expires after at most 12 months and is recorded in the exceptions register.

## Enforcement

Violations are investigated by {{owner}} and People Operations. Confirmed violations may result in access removal, retraining, disciplinary action up to termination, and termination of contractor agreements. Violations that expose customer data are handled under the Incident Response Policy.

## Review

This policy is reviewed on the cadence in the header ({{review_cadence}}), and also after any major incident or material change to systems or scope. The effective date and approver are recorded in version control history. Next review is due before the end of the cadence period following {{effective_date}}.
