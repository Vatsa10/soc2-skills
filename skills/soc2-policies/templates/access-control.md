# Access Control Policy

| Field | Value |
|---|---|
| Company | {{company}} |
| Policy owner | {{owner}} |
| Effective date | {{effective_date}} |
| Review cadence | {{review_cadence}} |

## Purpose

This policy restricts access to systems and data to authorized individuals, on a least-privilege and need-to-know basis.

## Scope

All {{company}} production systems, cloud accounts, corporate applications, source repositories, databases and the people (employees, contractors, service accounts) that use them.

## Policy statements

_Numbers and timeframes in these statements are defaults. {{owner}} must confirm {{company}} can meet each one before approving this policy, because an auditor tests against the policy as written. Statements that start with "(if ... in scope)" apply only when that category is in the audit scope._

1. Every person and service has a unique identifier; shared accounts and shared credentials are prohibited. [AC-01 → CC6.1]
2. Access is granted by role, using least privilege, after written approval from the system owner recorded in a ticket or the identity provider. [AC-03 → CC6.2] [AC-06 → CC6.3]
3. Multi-factor authentication is required for the identity provider, cloud consoles, source control, production infrastructure, VPN and email for all users, including administrators; the only exceptions are documented break-glass accounts, which are vaulted, alerted on and reviewed (statement 13). [AC-02 → CC6.1]
4. Single sign-on through the identity provider is used for every business application that supports SAML or OIDC. [AC-01 → CC6.1]
5. Passwords must be at least 12 characters, checked against known-breached lists, and must not be rotated on a fixed schedule unless compromise is suspected. [AC-08 → CC6.1]
6. Administrative and production access is granted only to named individuals, uses separate privileged accounts, and is reviewed quarterly with the user access review. [AC-07 → CC6.3] [AC-06 → CC6.3]
7. Access is removed within 24 hours of a termination and within 5 business days of a role change that no longer requires it. [AC-04 → CC6.2]
8. Access reviews of all in-scope systems are performed at least quarterly by system owners, and the evidence (reviewer, date, changes made) is retained for the audit period. [AC-05 → CC6.3]
9. Production data may be accessed only from managed devices with disk encryption and screen lock enabled. [AC-15 → CC6.7]
10. Network access to production is denied by default; inbound rules are limited to documented ports and sources, and administrative ports (SSH, RDP, database) are never open to 0.0.0.0/0. [AC-12 → CC6.6]
11. Service account keys and API tokens are stored in a secrets manager, rotated at least every 90 days, and never committed to source code. [AC-17 → CC6.1]
12. Physical access to any {{company}} office or equipment room is limited to authorized personnel; where production runs in a cloud provider, physical controls are inherited from that provider's SOC 2 report. [AC-13 → CC6.4]
13. The cloud root account, identity-provider super-admin and database superuser credentials are vaulted with hardware MFA, any use triggers an alert to {{owner}}, and each use is reviewed and ticketed within 2 business days. [AC-07 → CC6.1]

## Roles

| Role | Responsibility |
|---|---|
| {{owner}} | Owns this policy and the quarterly access review process. |
| System owners | Approve access to their systems and complete access reviews. |
| People operations | Notify IT of hires, transfers and terminations on the day they are effective. |

## Exceptions

Exceptions to this policy must be requested in writing, state the business reason and compensating controls, and be approved by {{owner}} (and by the most senior executive for exceptions affecting Restricted data). Each exception expires after at most 12 months and is recorded in the exceptions register, a dated list kept by {{owner}} with requester, reason, compensating controls, approver and expiry.

## Enforcement

Violations are investigated by {{owner}} and People Operations (or whoever handles HR). Confirmed violations may result in access removal, retraining, disciplinary action up to termination, and termination of contractor agreements. Violations that expose customer data are handled under the Incident Response Policy.

## Review

This policy is reviewed on the cadence in the header ({{review_cadence}}), and also after any major incident or material change to systems or scope. The effective date and approver are recorded in version control history. Next review is due before the end of the cadence period following {{effective_date}}.
