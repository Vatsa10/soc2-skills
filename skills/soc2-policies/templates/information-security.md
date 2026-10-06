# Information Security Policy

| Field | Value |
|---|---|
| Company | {{company}} |
| Policy owner | {{owner}} |
| Effective date | {{effective_date}} |
| Review cadence | {{review_cadence}} |

## Purpose

This policy establishes how {{company}} protects the confidentiality, integrity and availability of its systems and data, and sets the governance framework for every other security policy.

## Scope

All {{company}} employees, contractors and interns, and all systems, applications, cloud accounts and data that support the services in the SOC 2 scope.

## Policy statements

_Numbers and timeframes in these statements are defaults. {{owner}} must confirm {{company}} can meet each one before approving this policy, because an auditor tests against the policy as written. Statements that start with "(if ... in scope)" apply only when that category is in the audit scope._

1. Leadership approves this policy and all subordinate security policies in writing before publication, and re-approves them at least once every 12 months. [GOV-07 → CC2.2]
2. {{company}} designates {{owner}} as the accountable owner of the information security program, with authority to block releases and access grants that violate policy. [GOV-04 → CC1.3]
3. Security responsibilities are written into job descriptions or role charters for every engineering, IT and people-operations role. [GOV-04 → CC1.3]
4. Leadership reviews security metrics (open vulnerabilities, access review completion, incident count, training completion) at least quarterly and records the review in meeting minutes. [GOV-03 → CC1.2]
5. All policies are published in a central location that every employee can read, and each employee acknowledges the policy set in writing within 30 days of hire and annually thereafter. [GOV-07 → CC2.2]
6. The security program is risk-based: a documented risk assessment, performed at least annually, drives control selection and priorities. [RSK-01 → CC3.1]
7. Security objectives are documented, measurable and reviewed annually, including target time-to-patch, target access-review completion and target incident response times. [RSK-01 → CC3.1]
8. Controls are mapped to the Trust Services Criteria in scope and each control has a named owner. [CTL-01 → CC5.1]
9. Control deficiencies are logged in a remediation tracker with an owner and due date, and are reported to leadership if they remain open beyond 30 days. [MON-03 → CC4.2]
10. Customer-facing commitments about security are documented in the terms of service or security page and are reviewed by {{owner}} whenever they change. [GOV-09 → CC2.3]
11. An external channel (security@ mailbox or support form) is published so customers and researchers can report security issues, and reports are triaged within 2 business days. [GOV-09 → CC2.3]
12. (if processing_integrity in scope) {{company}} documents processing specifications (inputs, rules, outputs and error handling) for each customer-facing function and publishes API documentation and a changelog to customers. [PI-01 → PI1.1]

## Roles

| Role | Responsibility |
|---|---|
| Executive sponsor (most senior executive) | Approves this policy and funds the security program. |
| Policy owner ({{owner}}) | Maintains the policy set, runs the annual review and reports security status to leadership quarterly. |
| All personnel | Complete training, follow policies and report suspected incidents. |

## Exceptions

Exceptions to this policy must be requested in writing, state the business reason and compensating controls, and be approved by {{owner}} (and by the most senior executive for exceptions affecting Restricted data). Each exception expires after at most 12 months and is recorded in the exceptions register, a dated list kept by {{owner}} with requester, reason, compensating controls, approver and expiry.

## Enforcement

Violations are investigated by {{owner}} and People Operations (or whoever handles HR). Confirmed violations may result in access removal, retraining, disciplinary action up to termination, and termination of contractor agreements. Violations that expose customer data are handled under the Incident Response Policy.

## Review

This policy is reviewed on the cadence in the header ({{review_cadence}}), and also after any major incident or material change to systems or scope. The effective date and approver are recorded in version control history. Next review is due before the end of the cadence period following {{effective_date}}.
