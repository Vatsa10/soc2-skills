# Data Classification Policy

| Field | Value |
|---|---|
| Company | {{company}} |
| Policy owner | {{owner}} |
| Effective date | {{effective_date}} |
| Review cadence | {{review_cadence}} |

## Purpose

This policy defines classification levels so data is handled according to its sensitivity.

## Scope

All data created, received, stored or transmitted by {{company}}, in any format and location, including customer data.

## Policy statements

_Numbers and timeframes in these statements are defaults. {{owner}} must confirm {{company}} can meet each one before approving this policy, because an auditor tests against the policy as written. Statements that start with "(if ... in scope)" apply only when that category is in the audit scope._

1. {{company}} uses four classification levels: Restricted (customer data, credentials, keys, personal data), Confidential (source code, financials, contracts), Internal (internal documents, non-public plans) and Public (marketing material, published documentation). [CF-01 → C1.1]
2. Every data store and system in the inventory is assigned a classification by its data owner, and customer data is always at least Confidential. [CF-01 → C1.1]
3. Restricted data must be encrypted in transit with TLS 1.2 or higher and at rest with AES-256 or provider-managed equivalent. [AC-09 → C1.1] [AC-10 → CC6.7]
4. Restricted data may not be stored on laptops, removable media, personal devices, personal cloud storage or in chat tools. [AC-15 → CC6.7]
5. Production customer data may not be copied to development or test environments unless it is anonymized or masked. [CF-06 → C1.1]
6. Access to Restricted data requires explicit approval from the data owner and is reviewed quarterly. [CF-02 → C1.1] [AC-05 → CC6.3]
7. Documents and repositories containing Restricted or Confidential data carry a visible label or are located in a labeled workspace. [CF-01 → C1.1]
8. Sharing Restricted or Confidential data with third parties requires a signed NDA or contract with confidentiality terms. [VND-04 → C1.1]
9. (if privacy in scope) Data that falls in scope for privacy commitments (personal data) is tagged so notice, consent and deletion obligations can be located. [PR-03 → P3.1]
10. Classification is reviewed annually and when a new data type is introduced. [CF-01 → C1.1]
11. Confidentiality commitments in customer contracts are tracked and compared against the classification scheme at least annually. [GOV-09 → CC2.3]

## Roles

| Role | Responsibility |
|---|---|
| {{owner}} | Owns the classification scheme and approves exceptions. |
| Data owners | Assign a classification to each data set they own. |
| All personnel | Handle data according to its label. |

## Exceptions

Exceptions to this policy must be requested in writing, state the business reason and compensating controls, and be approved by {{owner}} (and by the most senior executive for exceptions affecting Restricted data). Each exception expires after at most 12 months and is recorded in the exceptions register, a dated list kept by {{owner}} with requester, reason, compensating controls, approver and expiry.

## Enforcement

Violations are investigated by {{owner}} and People Operations (or whoever handles HR). Confirmed violations may result in access removal, retraining, disciplinary action up to termination, and termination of contractor agreements. Violations that expose customer data are handled under the Incident Response Policy.

## Review

This policy is reviewed on the cadence in the header ({{review_cadence}}), and also after any major incident or material change to systems or scope. The effective date and approver are recorded in version control history. Next review is due before the end of the cadence period following {{effective_date}}.
