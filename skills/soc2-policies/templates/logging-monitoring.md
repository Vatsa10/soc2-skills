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

1. The following events are logged with timestamp, actor, source and outcome: authentication success and failure, privilege and permission changes, access to Restricted data, configuration changes, and administrative actions. [OPS-01 → CC7.2]
2. Cloud audit logs (such as AWS CloudTrail, Google Cloud Audit Logs or Azure Activity Log) are enabled in all accounts and regions. [OPS-02 → CC7.3]
3. Logs are forwarded to a central log platform and retained for at least 12 months, with the most recent 90 days immediately searchable. [OPS-03 → CC7.4]
4. Log storage is access-controlled, and write-once or tamper-evident settings are used so that engineers cannot alter or delete logs. [AC-01 → CC6.1]
5. System clocks are synchronized to a trusted NTP source. [OPS-02 → CC7.3]
6. Alerts are configured for repeated failed logins, new administrator creation, root account use, disabled logging, and unusual data egress; alerts page the on-call engineer. [OPS-04 → CC7.5]
7. Alerts are acknowledged within 15 minutes and triaged within 1 hour; resolution is recorded in the ticket. [OPS-04 → CC7.5]
8. Vulnerability scans of production are run at least weekly, and external penetration tests at least annually. [OPS-05 → CC7.1]
9. Critical vulnerabilities are remediated within 7 days, high within 30 days and medium within 90 days; exceptions are risk-accepted in writing. [OPS-05 → CC7.1]
10. Uptime, latency and error-rate monitoring covers all customer-facing services, with alerts on breaching service-level thresholds. [AV-01 → A1.1]
11. Log coverage and alert rules are reviewed at least annually, and after every SEV1 or SEV2 incident. [MON-02 → CC4.2]
12. Control monitoring checks (for example, MFA coverage and encryption settings) are run automatically at least monthly and failures are ticketed. [MON-01 → CC4.1]

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
