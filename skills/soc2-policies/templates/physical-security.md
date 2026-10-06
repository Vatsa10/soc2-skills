# Physical Security Policy

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

This policy protects the physical locations, equipment and media that store or can reach {{company}} and customer data, whether in an office, a home office or a cloud provider's data center.

## Scope

Any {{company}} office or shared workspace, personnel home offices, company-issued equipment and removable media, and the data centers operated by cloud providers that host in-scope systems.

## Policy statements

_Numbers and timeframes in these statements are defaults. {{owner}} must confirm {{company}} can meet each one before approving this policy, because an auditor tests against the policy as written. Statements that start with "(if ... in scope)" apply only when that category is in the audit scope._

1. Production systems run only in data centers operated by cloud providers that hold a current SOC 2 report or ISO 27001 certificate; {{company}} operates no production servers in its own offices. [AC-13 → CC6.4]
2. {{owner}} obtains each cloud provider's current SOC 2 report at least annually, reviews its scope, exceptions and complementary user entity controls, and records the review. Physical and environmental controls are treated as inherited from the provider only after that review. [VND-03 → CC9.2] [AC-13 → CC6.4]
3. Offices and shared workspaces are locked outside business hours and entered only with a key, badge or code issued to a named person. [AC-13 → CC6.4]
4. Visitors sign in, are escorted, and are recorded in a visitor log (name, company, host, time in and out) that is kept for at least 12 months. Where the workspace is shared with other companies and {{company}} cannot keep its own log, no Restricted data or production access is available on the premises. [AC-13 → CC6.4]
5. Keys, badges and codes are listed in an access register, reviewed at least semi-annually by {{owner}}, and revoked or changed within 24 hours of a termination or loss. [AC-05 → CC6.3] [AC-04 → CC6.2]
6. Screens are locked when unattended, and Restricted data and credentials are not left visible or printed on desks, whiteboards or shared printers (clean desk). [AC-15 → CC6.7]
7. Company laptops are never left unattended in vehicles or public places, and are encrypted so that loss does not expose data. [AC-15 → CC6.7]
8. Home offices follow the same rules for locking screens, using only managed devices for company data, and keeping company equipment from household members and guests. [AC-15 → CC6.7]
9. Equipment and media are tracked from issue to disposal; at end of life or separation they are wiped or destroyed under the Data Retention and Disposal Policy, and a record of asset ID, date and method is kept. [AC-14 → CC6.5]
10. Environmental protections for hosted systems (power, cooling, fire suppression) are provided by the cloud provider and confirmed in its SOC 2 report. [AV-06 → A1.2]
11. Lost or stolen equipment, keys or badges are reported within 1 hour of discovery and handled under the Incident Response Policy. [OPS-09 → CC7.3]

## Roles

| Role | Responsibility |
|---|---|
| {{owner}} | Owns this policy, the access register and the annual provider review. |
| Office or facilities contact | Issues keys and badges and keeps the visitor log. |
| All personnel | Protect equipment and report losses immediately. |

## Exceptions

Exceptions to this policy must be requested in writing, state the business reason and compensating controls, and be approved by {{owner}} (and by the most senior executive for exceptions affecting Restricted data). Each exception expires after at most 12 months and is recorded in the exceptions register, a dated list kept by {{owner}} with requester, reason, compensating controls, approver and expiry.

## Enforcement

Violations are investigated by {{owner}} and People Operations (or whoever handles HR). Confirmed violations may result in access removal, retraining, disciplinary action up to termination, and termination of contractor agreements. Violations that expose customer data are handled under the Incident Response Policy.

## Review and approval

This policy is reviewed on the cadence in the header ({{review_cadence}}), and also after any major incident or material change to systems or scope. Approval (approver name and date) is recorded in the header and in the revision history below; version-control history alone is not evidence of approval. After a material change, all personnel re-acknowledge the policy set within 30 days (Information Security Policy, statement 5). Next review is due by the date in the header.

| Version | Date | Change | Approved by |
|---|---|---|---|
| {{version}} | {{effective_date}} | Initial issue | {{approver}} |
