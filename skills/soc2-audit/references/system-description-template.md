# DRAFT System Description: <system name> (for management and CPA review)

> This skill prepares for a SOC 2 audit; it is not an attestation. Only a licensed CPA firm can issue a SOC 2 Type 1 or Type 2 report.
>
> DRAFT prepared from the repository and `.soc2/state.json`. Management owns this description (Section III of the SOC 2 report) and must review, correct, and approve it. Your CPA firm will review it against the AICPA description criteria (DC 200) and may require changes. Keep it current per GOV-13 → CC2.2.

Company: <company> | System owner: <role/name> | Report type: <Type 1 as of YYYY-MM-DD / Type 2 for YYYY-MM-DD to YYYY-MM-DD> | Version: <n> | Approved by: <name, date>

## 1. Types of services provided (DC1)

<What the system does for customers, in plain language; who the user entities are.>

## 2. Principal service commitments and system requirements (DC2)

- Service commitments (made to customers in contracts, SLAs, terms, privacy notice, security page): <e.g. availability target, encryption of customer data, breach notification timing, data deletion on termination>
- System requirements (internal requirements needed to meet those commitments, from policies, laws, regulations): <e.g. MFA for workforce, backups daily with 30-day retention>
- Where communicated: <contract section, URL>

## 3. Components of the system (DC3)

- Infrastructure: <cloud(s), regions, networks, managed services; from `system.cloud`>
- Software: <applications, databases, CI/CD, monitoring>
- People: <roles and team structure; workforce size>
- Procedures: <automated and manual procedures: change management, access, incident response, backups>
- Data: <data classes, flows in and out, storage and retention>
- System boundaries: <what is in and out of scope, with reasons>

## 4. System incidents (DC4)

<Identified system incidents that resulted from controls not suitably designed or not operating effectively, or that caused a significant failure to achieve a service commitment or system requirement, as of the date (Type 1) or during the period (Type 2): nature, timing, extent, disposition. If none: "None identified.">

## 5. Applicable trust services criteria and related controls (DC5)

In-scope categories: <Security, ...>. Controls designed to meet each criterion are listed in the CPA firm's Section IV mapping. Reference: `docs/soc2/` control matrix; cite `<ID> → <TSC>`.

## 6. Complementary user entity controls (CUECs) (DC6)

Controls your customers must operate for the commitments to be met (GOV-12 → CC2.3), for example:
- Customers manage their own users' access and remove departed users promptly.
- Customers protect their own credentials and API keys and enable MFA where offered.
- Customers notify <company> of suspected security incidents involving the service.

## 7. Subservice organizations and complementary subservice organization controls (CSOCs) (DC7)

Method: <carve-out (default) / inclusive>. Under carve-out, the subservice organization's controls are excluded from this description and the auditor's testing, and the CSOCs we rely on are listed. Under inclusive, its controls are included and it must provide its own written assertion. (GOV-11 → CC9.2)

| Subservice organization | Service provided | Method | CSOCs relied on | How we monitor (VND-03) |
|---|---|---|---|---|
| <cloud provider> | Hosting, physical security | carve-out | Physical access to data centers restricted; hardware disposal | Annual review of its SOC 2 report and bridge letter |

## 8. Criteria not relevant to the system (DC8)

| Criterion | Reason not relevant |
|---|---|
| <e.g. P-series> | <Privacy category not in scope> |

Taken from controls marked `n/a` in the gap assessment, with their reasons.

## 9. Significant changes during the period (DC9, Type 2 only)

<Significant changes to the system or controls during the period, with dates. If none: "None.">

---

This skill prepares for a SOC 2 audit; it is not an attestation. Only a licensed CPA firm can issue a SOC 2 Type 1 or Type 2 report.
