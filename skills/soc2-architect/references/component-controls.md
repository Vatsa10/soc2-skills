# Component to Control Map

> This skill prepares for a SOC 2 audit; it is not an attestation. Only a licensed CPA firm can issue a SOC 2 Type 1 or Type 2 report.

Use this table to map each system component to the controls it must satisfy. Control IDs are defined in `../../soc2/references/control-catalog.md`; read the entry there for the `TSC:` line, Type 1/Type 2 tests, evidence, and pass rule. Never copy a TSC mapping from this file: always take it from the catalog entry.

Reference implementations name concrete services. They are examples that satisfy the control, not the only acceptable choice. Each is chosen so it can emit machine-readable evidence (the Type 2 requirement).

## Cross-cutting controls (apply to every design)

These apply regardless of component. Add them once to the architecture, not per component.

| Area | Control IDs |
|---|---|
| Governance and system description | GOV-04, GOV-07, GOV-08, CTL-01, CTL-04 |
| Risk | RSK-01, RSK-02, RSK-04 |
| Monitoring of controls | MON-01, MON-03 |
| People | GOV-01, GOV-02, GOV-05, CF-05 |

## Component table

| Component | Control IDs | AWS | GCP | Azure |
|---|---|---|---|---|
| Identity / IdP (workforce) | AC-01, AC-02, AC-03, AC-04, AC-05, AC-06, AC-07, AC-08 | IAM Identity Center federated to Okta/Entra/Google Workspace; no IAM users with console passwords; Access Analyzer; credential report | Cloud Identity / Google Workspace SSO with 2-Step Verification enforced; IAM Recommender; Cloud Asset Inventory IAM export | Microsoft Entra ID with Conditional Access requiring MFA; Privileged Identity Management (PIM) for just-in-time roles; Access Reviews |
| API gateway / edge | AC-10, AC-12, AC-18, OPS-08, AV-02 | CloudFront + AWS WAF + Shield; API Gateway or ALB with TLS policy; WAF logs to S3 | Cloud Load Balancing + Cloud Armor; Cloud CDN; Armor policy logs | Front Door + Azure WAF; Application Gateway; DDoS Protection; diagnostic logs to Log Analytics |
| App services (compute) | AC-06, AC-12, AC-16, CTL-03, OPS-01, OPS-04, AV-01, AV-02, CHG-06 | ECS/EKS/Lambda in private subnets across 2+ AZs; Security Groups least-access; Inspector for vulnerabilities; AWS Config rules | GKE/Cloud Run/GCE in private VPC across 2+ zones; firewall rules and hierarchical policies; Artifact Registry vulnerability scanning; Security Command Center | AKS/App Service/Functions in VNet across availability zones; NSGs; Defender for Cloud; Azure Policy |
| Databases (relational / NoSQL) | AC-06, AC-09, AC-10, AC-12, AV-02, AV-03, AV-04, PI-05, CF-02, CF-06 | RDS/Aurora/DynamoDB with KMS encryption, Multi-AZ, automated backups and PITR, private subnets, IAM auth; AWS Backup | Cloud SQL/Spanner/Firestore with CMEK, HA configuration, automated backups and PITR, private IP only | Azure SQL/Cosmos DB with TDE and customer-managed keys, zone redundancy, automated backups and PITR, Private Endpoint |
| Object storage | AC-06, AC-09, AC-10, AC-14, CF-02, CF-03, CF-04, AV-03, PI-05 | S3 with Block Public Access, default KMS encryption, versioning, lifecycle rules, Object Lock where retention is mandated, bucket policy requiring TLS | Cloud Storage with uniform bucket-level access, public access prevention, CMEK, object versioning, lifecycle and retention policies | Storage Account with public network access disabled, secure transfer required and minimum TLS version 1.2, encryption with Key Vault keys, blob versioning, lifecycle management, immutability policies |
| Queues / streaming | AC-06, AC-09, AC-10, PI-03, AV-01, AV-02 | SQS/SNS/Kinesis/MSK with KMS encryption, dead-letter queues, CloudWatch depth/age alarms | Pub/Sub with CMEK, dead-letter topics, Cloud Monitoring backlog alerts | Service Bus/Event Hubs with encryption, dead-letter queues, Azure Monitor alerts |
| CI/CD pipeline | CHG-01, CHG-02, CHG-03, CHG-04, CHG-05, CHG-06, CHG-07, OPS-02, OPS-03, CTL-02, AC-17 | GitHub/GitLab with branch protection, CODEOWNERS, required checks; OIDC federation to AWS (no long-lived keys); CodePipeline/CodeBuild or Actions; Dependabot or Renovate; CodeQL/Semgrep | Same SCM controls; Workload Identity Federation to GCP; Cloud Build/Cloud Deploy with approvals; Artifact Analysis | Same SCM controls; workload identity federation to Entra; Azure DevOps/Actions with environment approvals; Defender for DevOps |
| Secrets manager and keys | AC-11, AC-17, AC-07, AC-09 | AWS Secrets Manager with rotation; KMS with key rotation and key policies; Parameter Store SecureString for non-rotating config | Secret Manager with rotation topics; Cloud KMS with rotation period and IAM-scoped keys | Key Vault (RBAC mode) with soft delete and purge protection; managed identities instead of secrets |
| Logging / SIEM | OPS-05, OPS-06, OPS-07, OPS-14, MON-01 | CloudTrail (multi-region, log file validation, to a locked-down S3 bucket); CloudWatch Logs; Security Lake or OpenSearch/third-party SIEM; retention at least 1 year | Cloud Audit Logs (Admin Activity and Data Access) with log sinks to a retention-locked bucket or BigQuery; Chronicle or third-party SIEM | Activity Log and Entra sign-in logs exported to Log Analytics/Storage; Microsoft Sentinel; retention at least 1 year |
| Monitoring / alerting / incident response | OPS-08, OPS-09, OPS-10, OPS-11, OPS-12, OPS-13, OPS-14, MON-02, AV-01 | CloudWatch alarms; GuardDuty; Security Hub; EventBridge to PagerDuty/Opsgenie; incident tickets in Jira/Linear | Cloud Monitoring alert policies; Security Command Center Threat Detection; Pub/Sub to PagerDuty/Opsgenie | Azure Monitor alerts; Defender for Cloud; Sentinel analytics rules and incidents; Action Groups to PagerDuty/Opsgenie |
| Backups / DR | AV-02, AV-03, AV-04, AV-05, AV-06, RSK-05 | AWS Backup plans with cross-region copy and Vault Lock; scheduled restore test (Lambda/Step Functions) logging results; multi-AZ design; Route 53 failover | Backup and DR Service; cross-region snapshots and buckets; scheduled restore tests via Cloud Scheduler/Workflows | Azure Backup with GRS vaults and immutable vaults; Site Recovery; scheduled restore tests via Automation/Logic Apps |
| Endpoints / laptops | AC-15, AC-16, AC-04, GOV-05 | Device management by Jamf/Kandji/Intune/Fleet with enforced disk encryption, screen lock, EDR (CrowdStrike/SentinelOne/Defender); device compliance gates IdP access | Google endpoint management or Jamf/Kandji/Intune with the same baseline; context-aware access | Intune compliance policies with Conditional Access device compliance; Defender for Endpoint; BitLocker/FileVault enforced |
| Third-party SaaS / vendors | VND-01, VND-02, VND-03, VND-04, VND-05, PR-13, PR-10 | Vendor register (GRC tool or version-controlled YAML) with risk tier, data shared, SOC report date, and review date; SSO/SCIM for every SaaS in scope | Same register; Workspace/Cloud Identity SSO and SCIM for SaaS | Same register; Entra enterprise applications with SCIM provisioning |
| Data pipelines (Processing Integrity) | PI-01, PI-02, PI-03, PI-04, PI-05, CHG-04, AV-03 | Glue/Step Functions/MWAA with schema validation, row-count and checksum reconciliation, DLQs, Great Expectations or Deequ checks, job-run metrics | Dataflow/Composer/Dataform with schema validation, reconciliation queries, DLQs, Dataplex data quality | Data Factory/Synapse/Databricks with schema validation, reconciliation checks, Purview data quality, failure alerts |
| PII stores (Privacy) | PR-01, PR-02, PR-03, PR-04, PR-05, PR-06, PR-07, PR-08, PR-09, PR-10, PR-11, PR-12, PR-14, PR-15, PR-16, CF-01, CF-02, CF-04, AC-09 | Macie for PII discovery in S3; tagged PII tables with field-level encryption (KMS/AWS Encryption SDK); DSAR automation via Step Functions across stores; consent records in DynamoDB/RDS; TTL or lifecycle for retention | Sensitive Data Protection (DLP) for discovery and de-identification; Data Catalog policy tags; DSAR workflow via Workflows; consent records in Firestore/Cloud SQL | Purview for classification and DSAR support; Azure SQL dynamic data masking and Always Encrypted; consent records in Cosmos DB/SQL; retention policies |

## Data-class triggers

| If the system handles | Add these controls | Note |
|---|---|---|
| Any personal information | PR-01 through PR-16 (select per catalog `Applies when`), CF-01 | Privacy TSC must be in scope for PR controls to be examined |
| Sensitive personal information (health, financial, government ID, children) | PR-04, CF-02, AC-09, AC-10 | Explicit consent and tighter access |
| Cardholder data | Flag to the user that PCI DSS applies separately; keep CDE segmentation (AC-12) and encryption (AC-09, AC-10) | SOC 2 does not replace PCI DSS |
| Protected health information | Flag to the user that HIPAA applies separately; add business associate terms (VND-04) | SOC 2 does not replace HIPAA |
| Multi-tenant customer data | AC-06, AC-12, CF-02, PI-05 | Tenant isolation must be designed and testable |
| Customer-supplied confidential data | CF-01, CF-02, CF-03, CF-04, CF-06 | Confidentiality TSC |

## Notes for the model

- A component may match several rows (for example a managed Postgres holding PII matches Databases and PII stores). Merge the control lists and deduplicate.
- If a component has no row, treat it as the nearest type, then state the assumption in the architecture document.
- If the user is on a cloud not listed (for example on-premises, Oracle, Cloudflare), keep the control IDs and propose equivalent services; mark them as "equivalent, confirm with auditor".
- Physical security (AC-13) and environmental controls (AV-06) are inherited from the hosting provider. Record them as carved-out/inherited and note that the provider's SOC 2 report must be collected under VND-03.
- Scope filter: drop controls whose TSC lines fall only in categories the user excluded. Security (CC) controls are always in scope.
