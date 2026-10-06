# Human Resources Security Policy

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

This policy ensures that personnel are trustworthy, trained, and accountable for security from hire through separation.

## Scope

All {{company}} employees, contractors and interns, throughout the employment lifecycle.

## Policy statements

_Numbers and timeframes in these statements are defaults. {{owner}} must confirm {{company}} can meet each one before approving this policy, because an auditor tests against the policy as written. Statements that start with "(if ... in scope)" apply only when that category is in the audit scope._

1. Background checks (identity, employment history, and criminal record where lawful) are completed and cleared before access to production or customer data is granted. [GOV-02 → CC1.4]
2. All personnel sign a confidentiality agreement and acknowledge the security policies before receiving system access. [CF-05 → C1.1] [GOV-07 → CC2.2]
3. Written job descriptions define security responsibilities for each role. [GOV-04 → CC1.3]
4. New hires complete security awareness training within 30 days of start, and all personnel complete it annually, with completion tracked by {{owner}}. [GOV-05 → CC1.4]
5. Engineers complete secure development training annually, covering the Secure Development Lifecycle Policy. [GOV-05 → CC1.4]
6. Phishing simulations or equivalent exercises are conducted at least twice a year, and personnel who fail are retrained within 30 days. [GOV-05 → CC2.2]
7. Accounts are provisioned only after onboarding steps are complete and removed within 24 hours of termination; HR notifies IT on the effective date. [AC-03 → CC6.2] [AC-04 → CC6.2]
8. Company devices, badges and tokens are collected at or before the last day of employment. [AC-04 → CC6.2]
9. Performance reviews address accountability for security responsibilities, and violations follow documented disciplinary steps. [GOV-06 → CC1.5]
10. A code of conduct (see the Code of Conduct Policy) is provided to all personnel, acknowledged annually, and includes how to report concerns anonymously. [GOV-01 → CC1.1] [GOV-10 → CC2.2]
11. Performance expectations and competence requirements are reviewed when roles change. [GOV-04 → CC1.3]

## Roles

| Role | Responsibility |
|---|---|
| People operations | Runs screening, onboarding, offboarding and training records. |
| {{owner}} | Owns security training content and policy acknowledgements. |
| Managers | Ensure team members complete training and notify HR of changes. |

## Exceptions

Exceptions to this policy must be requested in writing, state the business reason and compensating controls, and be approved by {{owner}} (and by the most senior executive for exceptions affecting Restricted data). Each exception expires after at most 12 months and is recorded in the exceptions register, a dated list kept by {{owner}} with requester, reason, compensating controls, approver and expiry.

## Enforcement

Violations are investigated by {{owner}} and People Operations (or whoever handles HR). Confirmed violations may result in access removal, retraining, disciplinary action up to termination, and termination of contractor agreements. Violations that expose customer data are handled under the Incident Response Policy.

## Review and approval

This policy is reviewed on the cadence in the header ({{review_cadence}}), and also after any major incident or material change to systems or scope. Approval (approver name and date) is recorded in the header and in the revision history below; version-control history alone is not evidence of approval. After a material change, all personnel re-acknowledge the policy set within 30 days (Information Security Policy, statement 5). Next review is due by the date in the header.

| Version | Date | Change | Approved by |
|---|---|---|---|
| {{version}} | {{effective_date}} | Initial issue | {{approver}} |
