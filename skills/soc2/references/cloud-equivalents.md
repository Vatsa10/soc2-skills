# Cloud Service Equivalents (AWS | GCP | Azure)

> This skill prepares for a SOC 2 audit; it is not an attestation. Only a licensed CPA firm can issue a SOC 2 Type 1 or Type 2 report.

The control catalog names AWS services as examples. Use this table to translate a control's `Implement` line to the user's cloud (`system.cloud` in state). Service names were checked on 2026-10-06; cloud vendors rename services often, so confirm a name in the provider's documentation before putting it in an auditor-facing document. Any equivalent that meets the control objective is acceptable; SOC 2 does not require a specific product.

Recent renames to watch:
- AWS: the original "AWS Security Hub" (standards and posture checks) is now **AWS Security Hub CSPM**; since June 2025 "AWS Security Hub" names a newer service that correlates findings from Security Hub CSPM, GuardDuty, Inspector, and Macie.
- GCP: Chronicle is now **Google Security Operations (Google SecOps)** (April 2024). Dataplex Universal Catalog is now **Knowledge Catalog** (April 2026); BigQuery policy tags (Policy Tag Manager) remain the column-level classification mechanism.
- Azure: Azure AD is **Microsoft Entra ID**; Microsoft Sentinel is increasingly managed in the Microsoft Defender portal.
- Tools: tfsec is now part of **Trivy** (`trivy config`); Atlassian Opsgenie reaches end of support on 2027-04-05 (successor: Jira Service Management); Kandji is now **Iru**.

## By control family

| Control family (catalog IDs) | AWS | GCP | Azure |
|---|---|---|---|
| Workforce identity and SSO (AC-01, AC-02, AC-08) | IAM Identity Center federated to the IdP; no IAM users with console passwords | Cloud Identity or Google Workspace; Workforce Identity Federation for an external IdP | Microsoft Entra ID with Conditional Access |
| Privileged and break-glass access (AC-06, AC-07) | Root account with hardware MFA, IAM Access Analyzer, AWS Organizations SCPs | Organization policy constraints, IAM Recommender, Privileged Access Manager | Entra Privileged Identity Management (PIM), Entra ID Governance access reviews |
| Workload identity for CI (AC-17, CHG-06) | IAM OIDC identity provider for GitHub Actions/GitLab | Workload Identity Federation | Entra workload identity federation |
| Secrets (AC-17) | AWS Secrets Manager, SSM Parameter Store (SecureString) | Secret Manager | Azure Key Vault (secrets) |
| Keys and encryption at rest (AC-09, AC-11) | AWS KMS (provider-managed or customer-managed keys) | Cloud KMS (Google-managed or CMEK) | Azure Key Vault / Managed HSM (platform-managed or customer-managed keys) |
| Encryption in transit and certificates (AC-10) | AWS Certificate Manager, ELB TLS security policies | Certificate Manager, Google-managed SSL certificates, SSL policies | App Service managed certificates, Key Vault certificates, minimum TLS version settings |
| Network segmentation (AC-12) | VPC, security groups, network ACLs, separate accounts | VPC, firewall rules, separate projects, VPC Service Controls | Virtual Network, network security groups, separate subscriptions |
| Boundary protection and remote admin (AC-18) | AWS WAF, AWS Shield, CloudFront, SSM Session Manager | Cloud Armor, Cloud Load Balancing, Identity-Aware Proxy (IAP) | Azure Web Application Firewall, Azure DDoS Protection, Front Door, Azure Bastion |
| Cloud audit trail (OPS-06; scan signal `logging.cloud_audit_trail`) | AWS CloudTrail (organization trail, all regions, log file validation) | Cloud Audit Logs with an aggregated log sink to a locked bucket | Azure Activity Log exported through diagnostic settings |
| Central logging and retention (OPS-05, OPS-07) | CloudWatch Logs, S3 with Object Lock, Security Lake or OpenSearch | Cloud Logging buckets with retention, Cloud Storage bucket retention lock | Azure Monitor Logs (Log Analytics workspace), immutable Blob Storage |
| Threat detection and SIEM (OPS-08) | Amazon GuardDuty, AWS Security Hub | Security Command Center threat detection, Google Security Operations (Google SecOps) | Microsoft Defender for Cloud, Microsoft Sentinel |
| Posture and misconfiguration (MON-01, OPS-04, CTL-03) | AWS Config, AWS Security Hub CSPM | Security Command Center, Organization Policy | Microsoft Defender for Cloud, Azure Policy |
| Vulnerability scanning (OPS-01) | Amazon Inspector, Amazon ECR image scanning | Artifact Analysis (container scanning), Security Command Center | Microsoft Defender for Cloud (Defender for Servers, Defender for Containers) |
| Alerting and on-call (OPS-08, OPS-14, AV-01, PI-07) | CloudWatch alarms, Amazon SNS | Cloud Monitoring alerting policies | Azure Monitor alerts, action groups |
| Backups and restore tests (AV-03, AV-04) | AWS Backup (plans, vaults, restore testing), RDS automated backups | Backup and DR Service, Cloud SQL automated backups | Azure Backup, Recovery Services vault |
| Redundancy and DR (AV-02, AV-05) | Multi-AZ, cross-region replication | Regional/multi-zone resources, cross-region replication | Availability zones, Azure Site Recovery |
| Data classification and discovery (CF-01, PR-03, PR-17) | Amazon Macie, resource tags | Sensitive Data Protection, BigQuery policy tags, Knowledge Catalog | Microsoft Purview |
| Endpoint management (AC-15, AC-16) | n/a (workforce endpoints: Jamf, Iru, Intune, Fleet; EDR: CrowdStrike, SentinelOne, Microsoft Defender for Endpoint) | same | Microsoft Intune, Microsoft Defender for Endpoint |
| Change and deploy evidence (CHG-02, CHG-06) | CloudTrail queries for console changes, CodePipeline/CI logs | Cloud Audit Logs (Admin Activity), Cloud Deploy/Cloud Build logs | Activity Log, Azure DevOps or GitHub deployment logs |
| Subservice SOC reports (AC-13, AV-06, GOV-11, VND-03) | AWS Artifact | Compliance Reports Manager | Service Trust Portal |
