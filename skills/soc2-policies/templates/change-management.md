# Change Management Policy

| Field | Value |
|---|---|
| Company | {{company}} |
| Policy owner | {{owner}} |
| Effective date | {{effective_date}} |
| Review cadence | {{review_cadence}} |

## Purpose

This policy ensures that changes to production systems, infrastructure and code are authorized, tested, reviewed and reversible.

## Scope

All changes to application code, infrastructure-as-code, cloud configuration, databases schemas, CI/CD pipelines and third-party integrations that affect the in-scope services.

## Policy statements

1. All changes are made through version control and a pull request; direct commits to the production branch are blocked by branch protection. [CHG-01 → CC8.1]
2. Every pull request requires at least one approving review from someone other than the author before merge. [CHG-02 → CC8.1]
3. Automated tests and security checks (dependency scan, secret scan, static analysis) must pass in CI before a change can be merged or deployed. [CHG-03 → CC8.1]
4. Each change has a ticket or pull request description stating purpose, risk, test evidence and rollback plan. [CHG-01 → CC8.1]
5. Production deployments are performed by the CI/CD pipeline using a service identity; engineers do not deploy from laptops. [CHG-02 → CC8.1]
6. Infrastructure changes are expressed as code, reviewed like application code, and applied by the pipeline. [CHG-03 → CC8.1]
7. Emergency changes may be deployed after verbal approval from the engineering lead, and must receive retrospective review within 2 business days. [CHG-04 → CC8.1]
8. Separate environments are used for development, staging and production, and production data is not used in non-production environments unless masked. [CHG-05 → CC8.1]
9. Developers do not have standing write access to production; elevated access is time-bound and logged. [AC-02 → CC6.2]
10. Each quarter {{owner}} samples at least 10 production changes (or all, if fewer) and verifies review, testing and approval evidence. [MON-01 → CC4.1]
11. Software dependencies are inventoried, and critical vulnerabilities are patched within 7 days and high within 30 days. [OPS-01 → CC7.2]

## Roles

| Role | Responsibility |
|---|---|
| Engineering lead | Owns the change process and approves emergency changes. |
| Authors | Raise changes, write tests and describe rollback. |
| Reviewers | Perform independent peer review before merge. |
| {{owner}} | Samples changes quarterly to confirm the process was followed. |

## Exceptions

Exceptions to this policy must be requested in writing, state the business reason and compensating controls, and be approved by {{owner}} (and by the CEO for exceptions affecting Restricted data). Each exception expires after at most 12 months and is recorded in the exceptions register.

## Enforcement

Violations are investigated by {{owner}} and People Operations. Confirmed violations may result in access removal, retraining, disciplinary action up to termination, and termination of contractor agreements. Violations that expose customer data are handled under the Incident Response Policy.

## Review

This policy is reviewed on the cadence in the header ({{review_cadence}}), and also after any major incident or material change to systems or scope. The effective date and approver are recorded in version control history. Next review is due before the end of the cadence period following {{effective_date}}.
