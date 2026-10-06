# Vendor Management Policy

| Field | Value |
|---|---|
| Company | {{company}} |
| Policy owner | {{owner}} |
| Effective date | {{effective_date}} |
| Review cadence | {{review_cadence}} |

## Purpose

This policy controls the risk introduced by suppliers and sub-processors that store, process or access {{company}} or customer data, or support the in-scope services.

## Scope

All third parties that provide infrastructure, software, services or personnel to {{company}}, including cloud providers, SaaS tools, contractors and sub-processors.

## Policy statements

1. {{company}} maintains a vendor inventory recording vendor name, service, data types shared, business owner, risk tier, contract end date and last review date. [VND-01 → CC9.2]
2. No vendor may access production or customer data until the intake process (security questionnaire and risk tier) is complete and approved by {{owner}}. [VND-02 → CC9.2]
3. Vendors are tiered: Tier 1 handles customer or confidential data or is critical to availability; Tier 2 handles internal data only; Tier 3 has no data access. [VND-02 → CC9.2]
4. For Tier 1 vendors, {{company}} obtains and reviews a current SOC 2 Type 2 report, ISO 27001 certificate or equivalent assessment before onboarding and annually, and documents exceptions and complementary user entity controls. [VND-03 → CC9.2]
5. Contracts with Tier 1 vendors include confidentiality, security requirements, breach notification within 72 hours, and the right to terminate for security failure. [VND-04 → CC9.2]
6. Contracts with vendors that process personal data include a data processing agreement. [PR-01 → P1.1]
7. Vendor access is limited to the minimum required, uses named accounts with MFA, and is reviewed quarterly with the user access review. [AC-03 → CC6.1]
8. Tier 1 vendors are reassessed annually and Tier 2 vendors every 2 years; reassessment results are recorded in the inventory. [VND-05 → CC9.2]
9. When a vendor relationship ends, access is revoked within 24 hours and data is returned or deleted with written confirmation. [VND-05 → CC9.2]
10. Vendor incidents and outages are logged and considered in the next vendor review. [MON-01 → CC4.1]
11. The vendor list of sub-processors is published to customers and customers are notified of changes at least 30 days in advance where contracts require it. [GOV-05 → CC2.3]

## Roles

| Role | Responsibility |
|---|---|
| {{owner}} | Owns the vendor inventory and annual review. |
| Business owners | Request vendors, complete the intake questionnaire and monitor performance. |
| Legal | Reviews contract terms and data processing agreements. |

## Exceptions

Exceptions to this policy must be requested in writing, state the business reason and compensating controls, and be approved by {{owner}} (and by the CEO for exceptions affecting Restricted data). Each exception expires after at most 12 months and is recorded in the exceptions register.

## Enforcement

Violations are investigated by {{owner}} and People Operations. Confirmed violations may result in access removal, retraining, disciplinary action up to termination, and termination of contractor agreements. Violations that expose customer data are handled under the Incident Response Policy.

## Review

This policy is reviewed on the cadence in the header ({{review_cadence}}), and also after any major incident or material change to systems or scope. The effective date and approver are recorded in version control history. Next review is due before the end of the cadence period following {{effective_date}}.
