# Risk Assessment Policy

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

This policy establishes a repeatable process to identify, rate, treat and monitor risks to {{company}} objectives, including security, availability and fraud risk.

## Scope

All business and technology risks associated with the in-scope services, vendors and people.

## Policy statements

_Numbers and timeframes in these statements are defaults. {{owner}} must confirm {{company}} can meet each one before approving this policy, because an auditor tests against the policy as written. Statements that start with "(if ... in scope)" apply only when that category is in the audit scope._

1. A formal risk assessment is performed at least annually and after any significant change (new product, new cloud provider, acquisition, major incident). [RSK-01 → CC3.1]
2. Risks are recorded in a risk register with description, asset, threat, likelihood (1-5), impact (1-5), score, owner, treatment and due date. [RSK-02 → CC3.2]
3. Risk scoring is the product of likelihood and impact; scores of 15 or higher are High and must have a treatment plan approved within 30 days. [RSK-02 → CC3.2]
4. Each risk is treated by one of four options: mitigate, transfer, avoid or accept; acceptance of a High risk requires written approval from the most senior executive. [RSK-02 → CC3.2]
5. The assessment explicitly considers fraud risk, including incentives, opportunity and rationalization, for finance, access and customer data. [RSK-03 → CC3.3]
6. The assessment considers changes in the business, technology, regulation and leadership that could affect controls. [RSK-04 → CC3.4]
7. Vendor and sub-processor risk is assessed as part of the annual assessment. [RSK-01 → CC3.2]
8. Business disruption risk, with insurance coverage reviewed annually, is included in the risk register. [RSK-05 → CC9.1]
9. The risk register is reviewed by the leadership team at least quarterly and the outcome is recorded in minutes. [RSK-02 → CC3.2] [GOV-03 → CC1.2]
10. Vulnerability scan results and penetration test findings are entered into the risk register when not remediated within policy timeframes. [MON-03 → CC4.2]
11. Security objectives are reviewed against assessment results to confirm they remain relevant. [RSK-01 → CC3.1]

## Roles

| Role | Responsibility |
|---|---|
| {{owner}} | Facilitates the assessment and maintains the risk register. |
| Leadership team | Reviews and approves risk treatment and accepts residual risk. |
| Risk owners | Implement treatment actions by the due date. |

## Exceptions

Exceptions to this policy must be requested in writing, state the business reason and compensating controls, and be approved by {{owner}} (and by the most senior executive for exceptions affecting Restricted data). Each exception expires after at most 12 months and is recorded in the exceptions register, a dated list kept by {{owner}} with requester, reason, compensating controls, approver and expiry.

## Enforcement

Violations are investigated by {{owner}} and People Operations (or whoever handles HR). Confirmed violations may result in access removal, retraining, disciplinary action up to termination, and termination of contractor agreements. Violations that expose customer data are handled under the Incident Response Policy.

## Review and approval

This policy is reviewed on the cadence in the header ({{review_cadence}}), and also after any major incident or material change to systems or scope. Approval (approver name and date) is recorded in the header and in the revision history below; version-control history alone is not evidence of approval. After a material change, all personnel re-acknowledge the policy set within 30 days (Information Security Policy, statement 5). Next review is due by the date in the header.

| Version | Date | Change | Approved by |
|---|---|---|---|
| {{version}} | {{effective_date}} | Initial issue | {{approver}} |
