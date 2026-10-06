# Asset Management Policy

| Field | Value |
|---|---|
| Company | {{company}} |
| Policy owner | {{owner}} |
| Effective date | {{effective_date}} |
| Review cadence | {{review_cadence}} |

## Purpose

This policy ensures {{company}} knows what hardware, software, cloud resources and data it has, who owns them, and how they are protected through their lifecycle.

## Scope

All company-owned or managed laptops, mobile devices, servers, cloud resources, SaaS applications, data stores and network equipment.

## Policy statements

1. {{company}} maintains an inventory of hardware, SaaS applications, cloud accounts and production data stores, with owner, location, classification and status for each. [GOV-08 → CC2.1]
2. Every asset in the inventory has a named owner who confirms the entry at least semi-annually. [GOV-08 → CC2.1]
3. Laptops are procured by IT, enrolled in device management, and recorded in the inventory before being issued. [AC-15 → CC6.7]
4. Unmanaged devices are denied access to production and corporate data. [AC-15 → CC6.7]
5. Cloud resources are tagged with owner, environment and data classification, and untagged resources are reviewed monthly. [GOV-08 → CC2.1]
6. The inventory is reconciled against the cloud account and identity provider at least quarterly. [GOV-08 → CC2.1] [MON-01 → CC4.1]
7. Software is installed from approved sources and the list of approved software is reviewed annually. [AC-16 → CC6.8]
8. Assets are classified under the Data Classification Policy and protected accordingly. [CF-01 → C1.1]
9. Lost or stolen devices are reported within 1 hour and remotely locked or wiped within 4 hours. [AC-15 → CC6.7] [OPS-09 → CC7.3]
10. Devices are returned at separation and securely wiped before reissue or disposal under the Data Retention and Disposal Policy. [AC-14 → CC6.5]
11. Assets approaching end-of-support are identified annually and replaced or upgraded before support ends. [OPS-01 → CC7.1]

## Roles

| Role | Responsibility |
|---|---|
| {{owner}} | Owns the asset inventory process. |
| IT administrator | Procures, enrolls, tracks and retires devices. |
| Asset owners | Confirm entries and classification for assets they own. |

## Exceptions

Exceptions to this policy must be requested in writing, state the business reason and compensating controls, and be approved by {{owner}} (and by the CEO for exceptions affecting Restricted data). Each exception expires after at most 12 months and is recorded in the exceptions register.

## Enforcement

Violations are investigated by {{owner}} and People Operations. Confirmed violations may result in access removal, retraining, disciplinary action up to termination, and termination of contractor agreements. Violations that expose customer data are handled under the Incident Response Policy.

## Review

This policy is reviewed on the cadence in the header ({{review_cadence}}), and also after any major incident or material change to systems or scope. The effective date and approver are recorded in version control history. Next review is due before the end of the cadence period following {{effective_date}}.
