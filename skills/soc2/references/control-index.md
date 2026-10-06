# SOC 2 Control Index

> This skill prepares for a SOC 2 audit; it is not an attestation. Only a licensed CPA firm can issue a SOC 2 Type 1 or Type 2 report.

One row per control in `control-catalog.md` (106 controls). Read this index first to scope and plan. Open a full catalog entry only for a control you evaluate, by searching `control-catalog.md` for `### <ID>`; never load the whole catalog at once. Scope rule: a control is in scope when any criterion in its TSC column belongs to an in-scope category (see the catalog's Scope selection rule). Frequency and Owner are defaults. Cite a control as `<ID> → <TSC>` using the TSC column.

| ID | Title | TSC | Category | Frequency | Owner | Scan signals |
|---|---|---|---|---|---|---|
| GOV-01 | Code of conduct acknowledged by all personnel | CC1.1, CC1.5 | Security | Per event | People ops | policies |
| GOV-02 | Background checks before access is granted | CC1.1, CC1.4 | Security | Per event | People ops | none |
| GOV-03 | Board or executive oversight of the security program | CC1.2, CC4.2 | Security | Quarterly | Leadership (CEO) | none |
| GOV-04 | Organizational chart and security roles defined | CC1.3 | Security | Annual | People ops | none |
| GOV-05 | Security awareness training at hire and annually | CC1.4, CC2.2 | Security | Per event | People ops | none |
| GOV-06 | Performance reviews and disciplinary process cover security | CC1.5 | Security | Annual | People ops | none |
| GOV-07 | Information security policies approved, published, and acknowledged | CC2.2, CC5.3 | Security | Annual | Security owner | policies |
| GOV-08 | System component inventory and data-flow diagrams maintained | CC2.1 | Security | Annual | Engineering lead | iac, cloud |
| GOV-09 | External communication of commitments and reporting channel | CC2.3 | Security | Per event | Security owner | incident.runbook |
| GOV-10 | Internal reporting channel for concerns (whistleblower) | CC1.1, CC2.2 | Security | Per event | People ops | none |
| GOV-11 | Subservice organizations and CSOCs identified (carve-out vs inclusive) | CC9.2, CC2.3 | Security | Annual | Compliance owner | cloud, vendors.list_present |
| GOV-12 | Complementary user entity controls (CUECs) communicated to customers | CC2.3 | Security | Annual | Compliance owner | none |
| GOV-13 | System description (DC 200) and management assertion kept current | CC2.2, CC2.3 | Security | Annual | Compliance owner | none |
| RSK-01 | Annual risk assessment against defined objectives | CC3.1, CC3.2 | Security | Annual | Security owner | none |
| RSK-02 | Risk register with owners and treatment plans | CC3.2, CC5.1 | Security | Quarterly | Security owner | none |
| RSK-03 | Fraud risk assessment | CC3.3 | Security | Annual | Security owner | none |
| RSK-04 | Significant change triggers risk reassessment | CC3.4 | Security | Per event | Security owner | none |
| RSK-05 | Business continuity plan with defined RTO/RPO | CC9.1, A1.2 | Security, Availability | Annual | Leadership (CEO) | backups.configured |
| MON-01 | Continuous control monitoring | CC4.1 | Security | Weekly | Compliance owner | cloud, monitoring.alerts |
| MON-02 | Annual third-party penetration test | CC4.1, CC7.1 | Security | Annual | Security owner | none |
| MON-03 | Control deficiencies tracked to remediation | CC4.2 | Security | Per event | Compliance owner | none |
| MON-04 | Periodic internal control assessment | CC4.1 | Security | Annual | Compliance owner | none |
| CTL-01 | Risk-to-control matrix | CC5.1 | Security | Annual | Compliance owner | none |
| CTL-02 | Segregation of duties for production changes and access | CC5.1, CC6.3 | Security | Per event | Engineering lead | change_mgmt.branch_protection, change_mgmt.codeowners |
| CTL-03 | Secure configuration baselines defined as code | CC5.2, CC7.1 | Security | Continuous/automated | Platform/DevOps lead | iac, ci |
| CTL-04 | Procedures documented with owners and timing | CC5.3 | Security | Annual | Compliance owner | policies, incident.runbook |
| AC-01 | Centralized identity with SSO | CC6.1 | Security | Continuous/automated | IT admin | auth.sso, auth.idp |
| AC-02 | MFA enforced for all workforce access | CC6.1 | Security | Continuous/automated | IT admin | auth.sso, auth.mfa_hint |
| AC-03 | Access provisioning requires documented approval | CC6.2, CC6.3 | Security | Per event | IT admin | none |
| AC-04 | Timely access removal on termination | CC6.2, CC6.3 | Security | Per event | People ops | auth.idp |
| AC-05 | Quarterly user access reviews | CC6.2, CC6.3 | Security | Quarterly | Security owner | none |
| AC-06 | Least privilege and role-based access | CC6.1, CC6.3 | Security | Quarterly | Platform/DevOps lead | iac, cloud |
| AC-07 | Privileged and break-glass account controls | CC6.1, CC6.3 | Security | Per event | Security owner | logging.cloud_audit_trail, monitoring.alerts |
| AC-08 | Password and authentication standards | CC6.1 | Security | Continuous/automated | IT admin | auth.idp |
| AC-09 | Encryption at rest | CC6.1, C1.1 | Security, Confidentiality | Continuous/automated | Platform/DevOps lead | encryption.kms, encryption.at_rest_hint |
| AC-10 | Encryption in transit | CC6.1, CC6.7 | Security | Continuous/automated | Platform/DevOps lead | encryption.tls |
| AC-11 | Cryptographic key management | CC6.1 | Security | Annual | Security owner | encryption.kms |
| AC-12 | Network segmentation and least-access firewall rules | CC6.1, CC6.6 | Security | Per event | Platform/DevOps lead | iac, cloud |
| AC-13 | Physical security via certified data centers and office controls | CC6.4 | Security | Annual | Security owner | cloud |
| AC-14 | Secure disposal of hardware and media | CC6.5, C1.2 | Security, Confidentiality | Per event | IT admin | none |
| AC-15 | Endpoint management and disk encryption | CC6.7, CC6.8 | Security | Continuous/automated | IT admin | none |
| AC-16 | Anti-malware / EDR on endpoints and servers | CC6.8 | Security | Continuous/automated | IT admin | none |
| AC-17 | Secrets management and no hardcoded credentials | CC6.1 | Security | Continuous/automated | Engineering lead | secrets.scanning, secrets.hardcoded_hits, auth.ci_oidc |
| AC-18 | External boundary protection | CC6.6 | Security | Continuous/automated | Platform/DevOps lead | iac, cloud |
| OPS-01 | Vulnerability scanning and patch SLAs | CC7.1 | Security | Monthly | Security owner | ci, deps.sast |
| OPS-02 | Dependency vulnerability management | CC7.1 | Security | Continuous/automated | Engineering lead | deps.dependabot_or_renovate |
| OPS-03 | Static application security testing in CI | CC7.1, CC8.1 | Security | Per event | Engineering lead | deps.sast, ci |
| OPS-04 | Configuration drift and misconfiguration detection | CC7.1 | Security | Continuous/automated | Platform/DevOps lead | cloud, monitoring.alerts |
| OPS-05 | Centralized logging of security-relevant events | CC7.2 | Security | Continuous/automated | Platform/DevOps lead | logging.centralized |
| OPS-06 | Cloud audit trail enabled and protected | CC7.2 | Security | Continuous/automated | Platform/DevOps lead | logging.cloud_audit_trail |
| OPS-07 | Log retention of at least one year | CC7.2 | Security | Continuous/automated | Platform/DevOps lead | logging.retention_days |
| OPS-08 | Security monitoring and alerting | CC7.2, CC7.3 | Security | Continuous/automated | Security owner | monitoring.alerts, logging.centralized |
| OPS-09 | Security event triage and incident classification | CC7.3 | Security | Per event | Security owner | incident.runbook |
| OPS-10 | Incident response plan | CC7.4 | Security | Annual | Security owner | incident.runbook |
| OPS-11 | Incident response tabletop exercise | CC7.4, CC7.5 | Security | Annual | Security owner | none |
| OPS-12 | Post-incident review and recovery | CC7.5 | Security | Per event | Engineering lead | incident.runbook |
| OPS-13 | Incident notification to customers and authorities | CC7.4, CC2.3 | Security | Per event | Legal | none |
| OPS-14 | On-call coverage for production | CC7.2, CC7.4 | Security | Weekly | Engineering lead | monitoring.alerts |
| CHG-01 | Change management policy | CC8.1 | Security | Annual | Engineering lead | policies |
| CHG-02 | Peer review enforced by branch protection or rulesets | CC8.1, CC5.1 | Security | Per event | Engineering lead | change_mgmt.branch_protection |
| CHG-03 | Code ownership for sensitive paths | CC8.1 | Security | Per event | Engineering lead | change_mgmt.codeowners |
| CHG-04 | Automated tests and CI checks before merge | CC8.1 | Security | Per event | Engineering lead | ci, change_mgmt.branch_protection |
| CHG-05 | Change documentation and traceability | CC8.1 | Security | Per event | Engineering lead | change_mgmt.pr_template |
| CHG-06 | Separate environments and deployment only via pipeline | CC8.1, CC5.2 | Security | Continuous/automated | Platform/DevOps lead | ci, iac |
| CHG-07 | Emergency change procedure | CC8.1 | Security | Per event | Engineering lead | none |
| VND-01 | Vendor inventory with risk tiering | CC9.2 | Security | Annual | Compliance owner | vendors.list_present |
| VND-02 | Vendor due diligence before onboarding | CC9.2 | Security | Per event | Security owner | none |
| VND-03 | Annual vendor review including SOC reports and CUECs | CC9.2 | Security | Annual | Security owner | vendors.list_present |
| VND-04 | Contracts with security and confidentiality terms | CC9.2, C1.1 | Security, Confidentiality | Per event | Legal | none |
| VND-05 | Vendor offboarding | CC9.2 | Security | Per event | Security owner | none |
| AV-01 | Capacity monitoring and forecasting | A1.1 | Availability | Quarterly | Platform/DevOps lead | monitoring.alerts |
| AV-02 | Redundant infrastructure across failure domains | A1.2 | Availability | Continuous/automated | Platform/DevOps lead | iac, cloud |
| AV-03 | Automated backups | A1.2, PI1.5 | Availability, Processing Integrity | Daily | Platform/DevOps lead | backups.configured, encryption.kms |
| AV-04 | Backup restore testing | A1.3 | Availability | Quarterly | Platform/DevOps lead | backups.restore_test |
| AV-05 | Disaster recovery plan and test | A1.2, A1.3 | Availability | Annual | Engineering lead | incident.runbook, backups.configured |
| AV-06 | Environmental protections via hosting provider | A1.2 | Availability | Annual | Security owner | cloud |
| PI-01 | Processing specifications documented and communicated | PI1.1 | Processing Integrity | Per event | Engineering lead | none |
| PI-02 | Input validation | PI1.2 | Processing Integrity | Continuous/automated | Engineering lead | none |
| PI-03 | Processing completeness monitoring and reconciliation | PI1.3 | Processing Integrity | Daily | Engineering lead | monitoring.alerts |
| PI-04 | Output accuracy and controlled distribution | PI1.4 | Processing Integrity | Per event | Engineering lead | none |
| PI-05 | Stored data integrity | PI1.5 | Processing Integrity | Continuous/automated | Engineering lead | backups.configured, logging.centralized |
| PI-06 | Duplicate and replay protection (idempotency) | PI1.3 | Processing Integrity | Continuous/automated | Engineering lead | none |
| PI-07 | Processing timeliness and completeness SLAs | PI1.4 | Processing Integrity | Daily | Engineering lead | monitoring.alerts |
| CF-01 | Data classification policy and labeling | C1.1, CC2.1 | Confidentiality, Security | Per event | Security owner | policies, privacy.pii_fields |
| CF-02 | Restricted access to confidential data | C1.1, CC6.3 | Confidentiality, Security | Quarterly | Security owner | logging.centralized |
| CF-03 | Retention schedule for confidential information | C1.1, C1.2 | Confidentiality | Continuous/automated | Engineering lead | logging.retention_days |
| CF-04 | Secure deletion at contract end or on request | C1.2, P4.3 | Confidentiality, Privacy | Per event | Engineering lead | privacy.dsar |
| CF-05 | Confidentiality agreements for personnel | C1.1, CC1.1 | Confidentiality, Security | Per event | People ops | none |
| CF-06 | No production confidential data in non-production | C1.1 | Confidentiality | Per event | Engineering lead | privacy.pii_fields |
| PR-01 | Privacy notice published and maintained | P1.1 | Privacy | Per event | Privacy owner | privacy.privacy_notice |
| PR-02 | Consent capture and records | P2.1 | Privacy | Per event | Privacy owner | privacy.privacy_notice |
| PR-03 | Collection limited to stated purposes | P3.1 | Privacy | Per event | Privacy owner | privacy.pii_fields |
| PR-04 | Explicit consent for sensitive personal information | P3.2 | Privacy | Per event | Privacy owner | privacy.pii_fields |
| PR-05 | Use limitation | P4.1 | Privacy | Per event | Privacy owner | none |
| PR-06 | Retention of personal information | P4.2 | Privacy | Continuous/automated | Engineering lead | logging.retention_days, backups.configured |
| PR-07 | Secure disposal of personal information | P4.3 | Privacy | Per event | Privacy owner | privacy.dsar |
| PR-08 | Data subject access requests | P5.1, P6.7 | Privacy | Per event | Privacy owner | privacy.dsar |
| PR-09 | Correction requests | P5.2 | Privacy | Per event | Support lead | privacy.dsar |
| PR-10 | Disclosure to third parties only for stated purposes | P6.1, P6.4 | Privacy | Annual | Privacy owner | vendors.list_present |
| PR-11 | Record of authorized disclosures | P6.2 | Privacy | Per event | Legal | none |
| PR-12 | Breach records and notification | P6.3, P6.6 | Privacy | Per event | Privacy owner | incident.runbook |
| PR-13 | Vendor obligation to report privacy incidents | P6.5 | Privacy | Per event | Legal | none |
| PR-14 | Personal data quality | P7.1 | Privacy | Quarterly | Privacy owner | none |
| PR-15 | Privacy inquiries, complaints, and compliance monitoring | P8.1 | Privacy | Per event | Privacy owner | privacy.privacy_notice |
| PR-16 | Privacy training for personnel handling PII | P8.1, P4.1 | Privacy | Annual | Privacy owner | none |
| PR-17 | Personal information inventory and controller/processor role | P1.1, P3.1 | Privacy | Annual | Privacy owner | privacy.pii_fields |
