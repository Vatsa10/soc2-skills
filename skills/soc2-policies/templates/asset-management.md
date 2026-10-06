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

1. {{company}} maintains an inventory of hardware, SaaS applications, cloud accounts and production data stores, with owner, location, classification and status for each. [CTL-01 → CC5.1]
2. Every asset in the inventory has a named owner who confirms the entry at least semi-annually. [CTL-02 → CC5.3]
3. Laptops are procured by IT, enrolled in device management, and recorded in the inventory before being issued. [AC-01 → CC6.1]
4. Unmanaged devices are denied access to production and corporate data. [AC-04 → CC6.7]
5. Cloud resources are tagged with owner, environment and data classification, and untagged resources are reviewed monthly. [CTL-01 → CC5.1]
6. The inventory is reconciled against the cloud account and identity provider at least quarterly. [MON-01 → CC4.1]
7. Software is installed from approved sources and the list of approved software is reviewed annually. [CHG-01 → CC8.1]
8. Assets are classified under the Data Classification Policy and protected accordingly. [CF-01 → C1.1]
9. Lost or stolen devices are reported within 1 hour and remotely locked or wiped within 4 hours. [OPS-01 → CC7.2]
10. Devices are returned at separation and securely wiped before reissue or disposal under the Data Retention and Disposal Policy. [CF-04 → C1.2]
11. Assets approaching end-of-support are identified annually and replaced or upgraded before support ends. [OPS-02 → CC7.3]

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
