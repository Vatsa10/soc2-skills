# SOC 2 Control Catalog

> This skill prepares for a SOC 2 audit; it is not an attestation. Only a licensed CPA firm can issue a SOC 2 Type 1 or Type 2 report.

## Purpose

A catalog of 100 auditor-realistic controls mapped to every one of the 61 AICPA Trust Services Criteria (see `tsc-criteria.md`). Skills use it to scope controls, map repository scan results to controls, plan evidence collection, and run readiness self-tests. The final control set, wording, and test procedures are agreed with your CPA firm; a control here is a strong starting point, not a guarantee that an auditor will accept it unchanged.

## Field legend

Every entry has exactly these fields, in this order:

| Field | Meaning |
|---|---|
| TSC | Criteria IDs the control addresses, then ` \| Category: <name>` |
| Applies when | The scope trigger; if it does not apply, record the control as N/A with a reason in the system description |
| Implement | Concrete implementation, with example tooling |
| Scan signals | Dotted keys from the repository scanner (`scripts/scan.py`) that hint at the control, or `none` when only people/process evidence can show it |
| Type 1 test | What the auditor checks for design and implementation on the report date |
| Type 2 test | What the auditor checks for operating effectiveness across the observation period |
| Evidence | Artifacts to hand the auditor |
| Pass rule | The self-test rule for marking the control PASS in readiness work |

A scan signal is a hint, never proof: the scanner sees the repository, not the cloud account, the IdP, or HR records. A control backed only by a scan signal is at best "likely implemented" until evidence is collected.

## ID prefixes

| Prefix | Area | Criteria |
|---|---|---|
| GOV | Governance, control environment, communication | CC1–CC2 |
| RSK | Risk assessment and business disruption | CC3, CC9.1 |
| MON | Monitoring activities | CC4 |
| CTL | Control activities | CC5 |
| AC | Logical and physical access | CC6 |
| OPS | System operations, detection, incident response | CC7 |
| CHG | Change management | CC8 |
| VND | Vendor and business-partner risk | CC9.2 |
| AV | Availability | A1 |
| PI | Processing integrity | PI1 |
| CF | Confidentiality | C1 |
| PR | Privacy | P1–P8 |

## Type 1 vs Type 2

- Type 1 reports on whether controls are suitably designed and implemented as of a single date. The auditor typically tests one instance of each control (inquiry plus inspection or observation).
- Type 2 reports on whether controls operated effectively over an observation period (commonly 3 to 12 months; 6 or 12 is most common after a first report). The auditor samples occurrences across the whole period, and every exception is reported with management's response.
- A control that has not run at least once inside the period (for example an annual review scheduled after period end) cannot be tested and is reported as not operating; plan cadences so each control fires inside the window.

## Type 2 sampling guide

Sample sizes below are common auditor practice, not AICPA mandates; each CPA firm sets its own methodology, and populations of system-enforced (automated) controls are often tested once plus change-management testing of the configuration.

| Control frequency | Typical sample |
|---|---|
| Annual | 1 |
| Quarterly | 2 |
| Monthly | 2–5 |
| Weekly | 5–15 |
| Daily | 20–40 |
| Many times/day | 25–60 |

## Security — Governance (CC1–CC2)

### GOV-01 — Code of conduct acknowledged by all personnel
- TSC: CC1.1, CC1.5 | Category: Security
- Applies when: always (any employee or contractor with system access)
- Implement: written code of conduct covering ethics, conflicts of interest, acceptable use, and sanctions; e-signature acknowledgement at hire and annually via HRIS (Rippling/BambooHR/Gusto)
- Scan signals: policies
- Type 1 test: code of conduct exists, is approved by management, and the acknowledgement workflow is configured for new hires
- Type 2 test: sample new hires and existing staff per frequency table; each signed within 30 days of start and within the annual cycle
- Evidence: approved code of conduct with version date, acknowledgement report listing every person and signature date, new-hire roster for the period
- Pass rule: PASS only if 100% of sampled personnel acknowledged within the defined window AND the document was approved within the last 12 months

### GOV-02 — Background checks before access is granted
- TSC: CC1.1, CC1.4 | Category: Security
- Applies when: hiring employees or long-term contractors who receive production or customer-data access
- Implement: background screening (Checkr/Certn/HireRight) to the extent local law permits, completed before the start date or before production access is provisioned
- Scan signals: none
- Type 1 test: screening policy defines who is screened and when; one completed check exists for a recent hire
- Type 2 test: sample new hires in the period; confirm a completed check dated on or before the access grant date
- Evidence: screening policy, vendor completion report (pass/fail only, no sensitive detail), hire roster with start and access dates
- Pass rule: PASS only if every sampled hire has a completed check dated before production access, or a documented legal exception approved by HR

### GOV-03 — Board or executive oversight of the security program
- TSC: CC1.2, CC4.2 | Category: Security
- Applies when: always; for startups without an independent board, a documented executive or advisory committee is the common substitute
- Implement: at least quarterly security briefing to the board or leadership committee covering risk register, incidents, audit status, and open deficiencies, with minutes
- Scan signals: none
- Type 1 test: charter or written mandate for oversight exists; most recent meeting minutes show security agenda items
- Type 2 test: inspect minutes for each quarter in the period (sample 2 per frequency table); confirm security topics and action items
- Evidence: governance charter, dated meeting minutes or decks, attendee list
- Pass rule: PASS only if oversight meetings occurred at the stated cadence throughout the period AND minutes record security review and decisions

### GOV-04 — Organizational chart and security roles defined
- TSC: CC1.3 | Category: Security
- Applies when: always
- Implement: current org chart from HRIS; named security owner (CISO/Head of Security or designated lead); RACI for key controls; written job descriptions for security-relevant roles
- Scan signals: none
- Type 1 test: org chart is current as of the report date and the security owner's responsibilities are documented
- Type 2 test: org chart is maintained (reviewed at least annually or on reorganisation); role changes during the period are reflected
- Evidence: dated org chart, security role description, control-owner RACI
- Pass rule: PASS only if the org chart matches HRIS headcount on the test date AND every in-scope control has a named owner

### GOV-05 — Security awareness training at hire and annually
- TSC: CC1.4, CC2.2 | Category: Security
- Applies when: always (all workforce members with system access)
- Implement: LMS-tracked training (KnowBe4/Curricula/Vanta/Drata training) within 30 days of hire and every 12 months; phishing simulations recommended; developers also take secure-coding training
- Scan signals: none
- Type 1 test: training content and assignment rules exist; completion tracking is configured
- Type 2 test: sample new hires and existing staff; confirm completion dates within 30 days of hire and within 12 months of prior completion
- Evidence: training content or syllabus, LMS completion report with dates, escalation records for overdue users
- Pass rule: PASS only if every sampled person completed training on time; overdue staff must have documented escalation and completion before period end

### GOV-06 — Performance reviews and disciplinary process cover security
- TSC: CC1.5 | Category: Security
- Applies when: always
- Implement: annual performance reviews that include adherence to policies; documented sanctions policy for violations applied consistently
- Scan signals: none
- Type 1 test: sanctions/disciplinary policy exists and review template references policy compliance
- Type 2 test: sample employees for a completed review in the cycle; inspect any security-violation cases for documented action
- Evidence: disciplinary policy, review template, review completion report, anonymised violation case log
- Pass rule: PASS only if review completion is ≥ 95% for the cycle AND every recorded violation has a documented outcome

### GOV-07 — Information security policies approved, published, and acknowledged
- TSC: CC2.2, CC5.3 | Category: Security
- Applies when: always
- Implement: policy set (information security, access control, change management, incident response, BC/DR, data classification, vendor management, acceptable use) with owner, version, and approval date; published on intranet; reviewed at least annually
- Scan signals: policies
- Type 1 test: each policy exists, is approved, is accessible to staff, and has a named owner
- Type 2 test: confirm annual review/approval occurred in the period; sample personnel acknowledgements
- Evidence: policy documents with version history, approval records, acknowledgement report
- Pass rule: PASS only if every required policy was approved within the last 12 months AND sampled personnel have acknowledged the current versions

### GOV-08 — System description and data-flow inventory maintained
- TSC: CC2.1 | Category: Security
- Applies when: always (this becomes Section III of the SOC 2 report)
- Implement: written system description covering services, infrastructure, software, people, data, and processes; architecture and data-flow diagrams; inventory of production components generated from IaC or cloud asset inventory
- Scan signals: iac, cloud
- Type 1 test: system description and diagrams match the production environment on the report date
- Type 2 test: description and inventory were updated for significant changes during the period (compare against change log)
- Evidence: system description draft, architecture diagram, data-flow diagram, asset inventory export
- Pass rule: PASS only if every production component in the cloud inventory appears in the description or inventory AND diagrams are dated within the last 12 months

### GOV-09 — External communication of commitments and reporting channel
- TSC: CC2.3 | Category: Security
- Applies when: the system serves external customers
- Implement: published security page or trust center, terms/MSA and SLA stating security and availability commitments, public status page, security contact (security@ or security.txt) and responsible-disclosure policy
- Scan signals: incident.runbook
- Type 1 test: commitments are documented in customer agreements and a working external reporting channel exists
- Type 2 test: sample customer notifications sent in the period (incidents, material changes) and confirm they followed the communication procedure
- Evidence: MSA/terms excerpt, trust page URL capture, status-page history, security.txt, sample customer notices
- Pass rule: PASS only if commitments are written AND an external reporting channel is monitored with a defined owner

### GOV-10 — Internal reporting channel for concerns (whistleblower)
- TSC: CC1.1, CC2.2 | Category: Security
- Applies when: always
- Implement: anonymous reporting option (EthicsPoint/Navex/a monitored form) plus a named escalation contact; non-retaliation statement in the code of conduct
- Scan signals: none
- Type 1 test: channel exists, is communicated to staff, and reports route to someone independent of the reported party
- Type 2 test: inspect the report log for the period; confirm each report was triaged and closed with documentation
- Evidence: channel description in handbook, routing configuration, anonymised report log
- Pass rule: PASS only if the channel is available and communicated AND every report in the period has a documented disposition

## Security — Risk Assessment (CC3, CC9.1)

### RSK-01 — Annual risk assessment against defined objectives
- TSC: CC3.1, CC3.2 | Category: Security
- Applies when: always
- Implement: documented methodology (likelihood × impact scale, risk appetite/tolerance statement); at least annual assessment covering threats to security, availability, and confidentiality objectives, including vendor risks; results approved by leadership
- Scan signals: none
- Type 1 test: methodology and a dated risk assessment with leadership approval exist
- Type 2 test: assessment was performed within the period and within 12 months of the prior one; outputs feed the risk register
- Evidence: risk methodology, risk assessment report with approval date, risk appetite statement
- Pass rule: PASS only if an approved assessment is dated within the last 12 months AND states objectives and risk tolerance

### RSK-02 — Risk register with owners and treatment plans
- TSC: CC3.2, CC5.1 | Category: Security
- Applies when: always
- Implement: register (spreadsheet or GRC tool) listing each risk, inherent and residual rating, owner, treatment decision (accept/mitigate/transfer/avoid), linked controls, and due dates; reviewed quarterly
- Scan signals: none
- Type 1 test: register exists, every risk has an owner and treatment, and high risks map to controls
- Type 2 test: sample quarterly reviews per frequency table; confirm updates and status changes recorded
- Evidence: risk register export with change history, quarterly review minutes, risk-acceptance sign-offs
- Pass rule: PASS only if every high/critical risk has an owner, a treatment, and either mapped controls or a signed acceptance

### RSK-03 — Fraud risk assessment
- TSC: CC3.3 | Category: Security
- Applies when: always
- Implement: fraud scenarios (insider data theft, unauthorized privilege escalation, financial manipulation, fake vendor) assessed in the annual risk assessment with linked mitigations
- Scan signals: none
- Type 1 test: risk assessment explicitly includes fraud scenarios with incentive/opportunity analysis
- Type 2 test: fraud section updated in the period's assessment
- Evidence: fraud section of the risk assessment, linked controls list
- Pass rule: PASS only if at least insider-misuse and unauthorized-access fraud scenarios are assessed with mitigating controls

### RSK-04 — Significant change triggers risk reassessment
- TSC: CC3.4 | Category: Security
- Applies when: always
- Implement: defined triggers (new product line, acquisition, new critical vendor, cloud migration, leadership change, new regulation) that require a documented risk review before or soon after the change
- Scan signals: none
- Type 1 test: procedure lists triggers and the review responsible party
- Type 2 test: identify significant changes in the period (from change log, vendor list, org changes) and confirm each had a risk review
- Evidence: change-risk procedure, risk review records tied to each significant change
- Pass rule: PASS only if every identified significant change in the period has a dated risk review

### RSK-05 — Business continuity plan with defined RTO/RPO
- TSC: CC9.1, A1.2 | Category: Security
- Applies when: always
- Implement: BCP covering critical services, roles, communication tree, RTO/RPO targets, alternate work arrangements; reviewed annually; cyber insurance considered as risk transfer
- Scan signals: backups.configured
- Type 1 test: BCP exists, is approved, and defines RTO/RPO for in-scope services
- Type 2 test: annual review or exercise occurred in the period with documented results
- Evidence: approved BCP, business impact analysis, exercise report, insurance certificate if used
- Pass rule: PASS only if the BCP is approved within 12 months AND defines RTO/RPO that match customer commitments

## Security — Monitoring Activities (CC4)

### MON-01 — Continuous control monitoring
- TSC: CC4.1 | Category: Security
- Applies when: always
- Implement: automated compliance monitoring (Vanta/Drata/Secureframe or AWS Config/Security Hub conformance packs) with a named reviewer who checks failing tests at least weekly
- Scan signals: cloud, monitoring.alerts
- Type 1 test: monitoring is configured against in-scope controls and failures notify an owner
- Type 2 test: sample weekly reviews per frequency table; confirm failing checks were triaged
- Evidence: tool configuration, failing-check history, review log or tickets
- Pass rule: PASS only if monitoring covers in-scope systems AND sampled failures have a documented response

### MON-02 — Annual third-party penetration test
- TSC: CC4.1, CC7.1 | Category: Security
- Applies when: the system exposes applications or APIs to customers or the internet
- Implement: independent pentest of production-like application and external infrastructure at least annually and after major architecture changes; findings tracked to remediation by severity SLA
- Scan signals: none
- Type 1 test: most recent report exists, scope covers in-scope systems, and findings are tracked
- Type 2 test: pentest performed within the period; critical/high findings remediated within SLA or risk-accepted
- Evidence: pentest report (with tester independence statement), remediation tickets, retest letter
- Pass rule: PASS only if a pentest is dated within 12 months AND no critical/high finding is open past its SLA without signed risk acceptance

### MON-03 — Control deficiencies tracked to remediation
- TSC: CC4.2 | Category: Security
- Applies when: always
- Implement: deficiency log (Jira/Linear project) for findings from audits, pentests, monitoring, and incidents; each item has severity, owner, due date; overdue items escalated to leadership
- Scan signals: none
- Type 1 test: log exists with required fields and an escalation rule
- Type 2 test: sample deficiencies raised during the period; confirm remediation or escalation by due date
- Evidence: deficiency log export, escalation records, leadership reporting
- Pass rule: PASS only if every sampled deficiency has an owner and due date AND none is past due without escalation

### MON-04 — Periodic internal control assessment
- TSC: CC4.1 | Category: Security
- Applies when: always
- Implement: at least annual internal readiness review or internal audit by someone independent of the control operator (internal audit, compliance lead, or outside consultant), results reported to leadership
- Scan signals: none
- Type 1 test: assessment plan exists and assigns an independent assessor
- Type 2 test: assessment completed within the period with findings fed into MON-03
- Evidence: assessment plan, report, findings in deficiency log
- Pass rule: PASS only if an independent assessment is dated within 12 months AND its findings are tracked

## Security — Control Activities (CC5)

### CTL-01 — Risk-to-control matrix
- TSC: CC5.1 | Category: Security
- Applies when: always
- Implement: matrix mapping each significant risk to preventive and detective controls and to TSC criteria; reviewed with the annual risk assessment
- Scan signals: none
- Type 1 test: matrix exists and every high risk maps to at least one control
- Type 2 test: matrix updated after the period's risk assessment
- Evidence: control matrix with version date
- Pass rule: PASS only if every in-scope criterion and every high risk maps to at least one implemented control

### CTL-02 — Segregation of duties for production changes and access
- TSC: CC5.1, CC6.3 | Category: Security
- Applies when: always
- Implement: authors cannot approve or merge their own code; access requests approved by someone other than the requester; admins of the IdP are not the sole reviewers of their own access
- Scan signals: change_mgmt.branch_protection, change_mgmt.codeowners
- Type 1 test: technical settings and procedures enforce separation (branch protection requires non-author approval)
- Type 2 test: sample merged changes and access grants; confirm approver differs from requester
- Evidence: repository protection settings, sample PRs, access tickets
- Pass rule: PASS only if no sampled change or access grant was self-approved; small-team exceptions require documented compensating detective review

### CTL-03 — Secure configuration baselines defined as code
- TSC: CC5.2, CC7.1 | Category: Security
- Applies when: the system runs on cloud infrastructure or managed hosts
- Implement: infrastructure defined in Terraform/CloudFormation/Pulumi with hardened modules; CIS benchmark-aligned baselines; policy-as-code checks (tfsec/Checkov) in CI
- Scan signals: iac, ci
- Type 1 test: baseline standard exists and production resources are deployed from IaC
- Type 2 test: sample infrastructure changes; confirm they went through IaC and passed policy checks
- Evidence: baseline standard, IaC repository, CI policy-check logs
- Pass rule: PASS only if production infrastructure is defined in IaC AND drift from baseline is detected or blocked

### CTL-04 — Procedures documented with owners and timing
- TSC: CC5.3 | Category: Security
- Applies when: always
- Implement: runbooks for recurring controls (access review, backup test, vendor review) listing owner, frequency, steps, and evidence to retain; tracked in a compliance calendar
- Scan signals: policies, incident.runbook
- Type 1 test: procedures exist for each recurring control with owner and frequency
- Type 2 test: compliance calendar shows each recurring control executed on schedule
- Evidence: runbooks, compliance calendar, completion records
- Pass rule: PASS only if every recurring in-scope control has a written procedure AND the calendar shows on-time execution

## Security — Logical and Physical Access (CC6)

### AC-01 — Centralized identity with SSO
- TSC: CC6.1 | Category: Security
- Applies when: any workforce access to production, admin tools, source control, or cloud console
- Implement: single IdP (Okta/Entra ID/Google Workspace) with SAML/OIDC SSO to cloud console, source control, and critical SaaS; local accounts disabled or inventoried as break-glass
- Scan signals: auth.sso, auth.idp
- Type 1 test: critical systems authenticate through the IdP on the report date
- Type 2 test: SSO configuration unchanged or changes approved; no unauthorized local accounts created during the period
- Evidence: IdP application list, SSO configuration screenshots, local account inventory
- Pass rule: PASS only if every critical system uses SSO AND every local account is a documented break-glass account

### AC-02 — MFA enforced for all workforce access
- TSC: CC6.1, CC6.2 | Category: Security
- Applies when: any human login to prod, admin tools, or cloud console
- Implement: IdP MFA policy (Okta/Entra/Google Workspace); cloud console via SSO only; no IAM users with console passwords
- Scan signals: auth.sso, auth.mfa_hint
- Type 1 test: MFA policy exists and is enforced (not optional) at the IdP on the report date
- Type 2 test: MFA enforced across the period; inspect IdP policy change log and sample logins per frequency table
- Evidence: IdP policy export, MFA enrollment report, quarterly access review records
- Pass rule: PASS only if MFA is enforced for all users AND no bypass/break-glass account lacks compensating control

### AC-03 — Access provisioning requires documented approval
- TSC: CC6.2, CC6.3 | Category: Security
- Applies when: granting any user access to in-scope systems
- Implement: access requests via ticket or IdP workflow naming system, role, and justification; approved by manager or system owner before grant
- Scan signals: none
- Type 1 test: provisioning procedure exists and a sample grant shows approval before access
- Type 2 test: sample new hires and access changes; compare approval timestamp to grant timestamp from IdP or system logs
- Evidence: access request tickets, IdP provisioning logs, new-hire roster
- Pass rule: PASS only if every sampled grant has approval dated on or before the grant

### AC-04 — Timely access removal on termination
- TSC: CC6.2, CC6.3 | Category: Security
- Applies when: any employee or contractor departs or changes role
- Implement: HRIS-to-IdP deprovisioning (SCIM) disabling accounts within 24 hours of termination (immediately for involuntary); checklist for non-SSO systems and shared secrets
- Scan signals: auth.idp
- Type 1 test: offboarding procedure defines the SLA and covers non-SSO systems
- Type 2 test: sample terminations; compare HR termination date to account disable timestamps in IdP and critical systems
- Evidence: termination roster from HRIS, IdP deactivation log, offboarding checklists
- Pass rule: PASS only if every sampled leaver lost access within the stated SLA (24 hours) across IdP and non-SSO systems

### AC-05 — Quarterly user access reviews
- TSC: CC6.2, CC6.3 | Category: Security
- Applies when: always (production, cloud console, databases, source control, critical SaaS)
- Implement: quarterly review by system owners of every account and role; inappropriate access removed and the removal ticketed
- Scan signals: none
- Type 1 test: review procedure exists and the most recent review is complete with sign-off
- Type 2 test: inspect 2 quarterly reviews (per frequency table); confirm completeness of user lists and remediation of flagged items
- Evidence: user listings with extraction date, reviewer sign-off, removal tickets
- Pass rule: PASS only if each quarter's review covered all in-scope systems, was signed off, AND flagged access was removed within 30 days

### AC-06 — Least privilege and role-based access
- TSC: CC6.1, CC6.3 | Category: Security
- Applies when: always
- Implement: role definitions per system; production write access limited to an on-call/admin group; IAM policies without wildcard admin for workloads; just-in-time elevation for sensitive actions
- Scan signals: iac, cloud
- Type 1 test: role matrix exists and production admin membership is restricted to named roles
- Type 2 test: sample production admin accounts across the period and confirm membership matches role justification
- Evidence: role matrix, admin group membership exports, IAM policy documents
- Pass rule: PASS only if every production admin has a documented role-based justification AND no workload role grants unrestricted admin without approval

### AC-07 — Privileged and break-glass account controls
- TSC: CC6.1, CC6.3 | Category: Security
- Applies when: root/owner accounts or emergency accounts exist (cloud root, IdP super-admin, database superuser)
- Implement: root credentials vaulted with hardware MFA; break-glass use triggers an alert and a post-use review; privileged sessions logged
- Scan signals: logging.cloudtrail, monitoring.alerts
- Type 1 test: privileged accounts inventoried, MFA-protected, and alerting configured on use
- Type 2 test: inspect all root/break-glass usage events in the period; confirm each has a ticket and review
- Evidence: privileged account inventory, alert rule, usage log and review tickets
- Pass rule: PASS only if every privileged/break-glass use in the period is alerted and reviewed AND root has MFA

### AC-08 — Password and authentication standards
- TSC: CC6.1 | Category: Security
- Applies when: any system that cannot use SSO, and the IdP itself
- Implement: minimum 12 characters or passphrases, breached-password screening, lockout or throttling after repeated failures, password manager for shared credentials (1Password/Bitwarden)
- Scan signals: auth.idp
- Type 1 test: password standard documented and configured in IdP and non-SSO systems
- Type 2 test: configuration unchanged or changes approved during the period
- Evidence: password policy, IdP and system configuration screenshots
- Pass rule: PASS only if configured settings meet the documented standard on every in-scope system

### AC-09 — Encryption at rest with managed keys
- TSC: CC6.1, C1.1 | Category: Security
- Applies when: any datastore holding customer data (databases, object storage, volumes, backups)
- Implement: AES-256 encryption at rest via cloud KMS (AWS KMS/GCP KMS/Azure Key Vault) for RDS, S3, EBS, and backups; default encryption enforced by IaC or organization policy
- Scan signals: encryption.kms, encryption.at_rest_hint
- Type 1 test: every in-scope datastore shows encryption enabled on the report date
- Type 2 test: new datastores created during the period are encrypted (inspect config rules or IaC changes)
- Evidence: KMS key list, datastore encryption configuration exports, AWS Config/equivalent rule results
- Pass rule: PASS only if 100% of in-scope datastores and backups are encrypted at rest

### AC-10 — Encryption in transit
- TSC: CC6.1, CC6.7 | Category: Security
- Applies when: any network transmission of customer data, including internal service-to-service traffic crossing untrusted networks
- Implement: TLS 1.2+ on all public endpoints, HSTS, HTTP redirected to HTTPS, managed certificates (ACM/Let's Encrypt) with expiry monitoring; database connections require TLS
- Scan signals: encryption.tls
- Type 1 test: external endpoints accept only TLS 1.2+ (SSL Labs or equivalent scan) and DB connections enforce TLS
- Type 2 test: certificate renewals and TLS configuration remained compliant through the period
- Evidence: TLS scan results, load-balancer listener configuration, certificate inventory
- Pass rule: PASS only if no in-scope endpoint accepts plaintext or TLS below 1.2

### AC-11 — Cryptographic key management
- TSC: CC6.1 | Category: Security
- Applies when: the entity manages encryption keys or signing keys
- Implement: keys held in KMS/HSM, not in code; automatic annual rotation for customer-managed keys; key administration separated from key use; key deletion requires approval
- Scan signals: encryption.kms
- Type 1 test: key management procedure exists; rotation enabled on KMS keys
- Type 2 test: rotation occurred as scheduled; key policy changes in the period were approved
- Evidence: KMS rotation status, key policies, key management procedure
- Pass rule: PASS only if every customer-managed key has rotation enabled or a documented exception AND no keys are stored in source code

### AC-12 — Network segmentation and least-access firewall rules
- TSC: CC6.1, CC6.6 | Category: Security
- Applies when: always for cloud or on-prem networks
- Implement: production in a separate VPC/account from non-production; databases in private subnets; security groups deny by default; no 0.0.0.0/0 on admin ports (22, 3389, DB ports)
- Scan signals: iac, cloud
- Type 1 test: network diagram matches configuration; no public admin ports on the report date
- Type 2 test: sample firewall/security group changes in the period; confirm approval and compliance with standard
- Evidence: network diagram, security group exports, change tickets
- Pass rule: PASS only if no in-scope resource exposes admin or database ports to the internet AND prod is isolated from non-prod

### AC-13 — Physical security via certified data centers and office controls
- TSC: CC6.4 | Category: Security
- Applies when: always; for cloud-only companies the data-center portion is carved out to the cloud provider (subservice organization)
- Implement: production hosted with a provider holding a current SOC 2 report covering physical security; offices use badge access and visitor logs if they store sensitive assets
- Scan signals: cloud
- Type 1 test: subservice provider's SOC 2 report is current and physical controls are identified as carved out; office controls exist where applicable
- Type 2 test: provider report covers the period (or a bridge letter exists); office badge reviews performed
- Evidence: cloud provider SOC 2 report and bridge letter, office badge access list and reviews
- Pass rule: PASS only if the provider's report covers the period with no relevant qualified opinion AND office controls exist where sensitive assets are stored

### AC-14 — Secure disposal of hardware and media
- TSC: CC6.5, C1.2 | Category: Security
- Applies when: the entity retires laptops, drives, or other media that held company or customer data
- Implement: encrypted endpoints wiped (crypto-erase) before reuse; certified disposal vendor issues certificates of destruction; cloud media disposal relies on provider's SOC 2
- Scan signals: none
- Type 1 test: disposal procedure exists
- Type 2 test: sample disposed assets in the period from the asset inventory; confirm wipe or destruction certificate
- Evidence: disposal procedure, asset inventory with disposal status, certificates of destruction
- Pass rule: PASS only if every sampled retired asset has a wipe record or destruction certificate

### AC-15 — Endpoint management and disk encryption
- TSC: CC6.7, CC6.8 | Category: Security
- Applies when: workforce laptops or desktops access production or customer data
- Implement: MDM (Jamf/Kandji/Intune) enforcing full-disk encryption, screen lock ≤ 15 minutes, OS auto-update, firewall; removable media restricted
- Scan signals: none
- Type 1 test: MDM policy enforces settings; device inventory matches headcount
- Type 2 test: sample devices across the period; confirm compliance status and encryption
- Evidence: MDM compliance report, device inventory, policy profiles
- Pass rule: PASS only if every sampled in-scope device is MDM-enrolled with disk encryption on

### AC-16 — Anti-malware / EDR on endpoints and servers
- TSC: CC6.8 | Category: Security
- Applies when: endpoints or servers that run general-purpose operating systems are in scope (immutable containers may rely on image scanning instead)
- Implement: EDR (CrowdStrike/SentinelOne/Microsoft Defender) with automatic signature updates and alerting to security; container images scanned before deploy
- Scan signals: none
- Type 1 test: EDR deployed and alerting configured on the report date
- Type 2 test: sample devices for agent presence and update status; inspect alerts in the period for triage
- Evidence: EDR console coverage report, alert triage tickets, image-scan logs
- Pass rule: PASS only if EDR coverage is ≥ 98% of in-scope devices AND all high alerts were triaged

### AC-17 — Secrets management and no hardcoded credentials
- TSC: CC6.1, CC6.7 | Category: Security
- Applies when: applications use API keys, database passwords, tokens, or certificates
- Implement: secrets stored in a manager (AWS Secrets Manager/Vault/Doppler); secret scanning (GitHub secret scanning/gitleaks/trufflehog) in CI and push protection; leaked secrets rotated immediately; service-account keys inventoried and rotated
- Scan signals: secrets.scanning, secrets.hardcoded_hits
- Type 1 test: secret manager in use, scanning enabled, and no live secrets in the repository on the report date
- Type 2 test: inspect secret-scanning alerts in the period; confirm each was rotated and closed
- Evidence: secret manager inventory, scanning configuration, alert history with rotation tickets
- Pass rule: PASS only if secrets.hardcoded_hits is 0 (or every hit is confirmed revoked) AND secret scanning runs on every push

### AC-18 — External boundary protection
- TSC: CC6.6 | Category: Security
- Applies when: services are exposed to the internet
- Implement: WAF and DDoS protection (Cloudflare/AWS WAF + Shield), rate limiting, remote admin only through VPN or zero-trust proxy (Tailscale/Cloudflare Access/SSM Session Manager) with SSO and MFA
- Scan signals: iac, cloud
- Type 1 test: boundary controls configured on public endpoints; admin access path requires SSO/MFA
- Type 2 test: rule changes in the period approved; blocked-event logs show the control operated
- Evidence: WAF configuration, VPN/zero-trust access policy, change tickets
- Pass rule: PASS only if every public endpoint sits behind boundary protection AND no direct internet admin access exists

## Security — System Operations (CC7)

### OPS-01 — Vulnerability scanning and patch SLAs
- TSC: CC7.1 | Category: Security
- Applies when: always
- Implement: authenticated infrastructure and container scanning at least monthly (Inspector/Wiz/Qualys/Trivy); remediation SLAs critical 15 days, high 30 days, medium 90 days; OS patching automated
- Scan signals: ci, deps.sast
- Type 1 test: scanning configured across in-scope assets and SLA policy documented
- Type 2 test: sample monthly scans; trace critical/high findings to remediation within SLA
- Evidence: scan schedules and reports, remediation tickets, SLA policy, exception approvals
- Pass rule: PASS only if scans ran at the stated cadence AND no critical/high finding exceeded SLA without approved exception

### OPS-02 — Dependency vulnerability management
- TSC: CC7.1 | Category: Security
- Applies when: the application uses third-party packages
- Implement: Dependabot or Renovate enabled on all production repositories; SCA results reviewed; critical dependency CVEs patched within the OPS-01 SLA
- Scan signals: deps.dependabot_or_renovate
- Type 1 test: automated dependency updates enabled on in-scope repositories
- Type 2 test: sample critical/high dependency alerts in the period; confirm fix or exception within SLA
- Evidence: Dependabot/Renovate configuration, alert history, merged update PRs
- Pass rule: PASS only if every production repository has automated dependency alerts AND no critical alert is open past SLA

### OPS-03 — Static application security testing in CI
- TSC: CC7.1, CC8.1 | Category: Security
- Applies when: the entity develops software that runs in production
- Implement: SAST (CodeQL/Semgrep/SonarQube) runs on every pull request; high-severity findings block merge or require documented triage
- Scan signals: deps.sast, ci
- Type 1 test: SAST job is configured and required in CI
- Type 2 test: sample merged PRs; confirm SAST ran and high findings were resolved or triaged
- Evidence: CI configuration, SAST results per PR, triage records
- Pass rule: PASS only if SAST ran on every sampled PR AND no high finding merged without triage

### OPS-04 — Configuration drift and misconfiguration detection
- TSC: CC7.1 | Category: Security
- Applies when: cloud infrastructure is in scope
- Implement: CSPM or config rules (AWS Config/Security Hub/GCP SCC/Wiz) alerting on public buckets, unencrypted storage, open security groups, disabled logging
- Scan signals: cloud, monitoring.alerts
- Type 1 test: detection rules enabled on all in-scope accounts with alert routing
- Type 2 test: sample findings in the period; confirm triage and remediation
- Evidence: rule set, finding history, remediation tickets
- Pass rule: PASS only if detection covers all production accounts AND high findings were remediated or accepted

### OPS-05 — Centralized logging of security-relevant events
- TSC: CC7.2 | Category: Security
- Applies when: always
- Implement: application, IdP, cloud control-plane, database, and network logs shipped to a central store (Datadog/Splunk/ELK/CloudWatch/Panther) with restricted delete access
- Scan signals: logging.centralized
- Type 1 test: in-scope log sources are flowing to the central store on the report date
- Type 2 test: sample dates across the period and confirm logs exist for each source (no gaps)
- Evidence: log source inventory, sample log queries by date, access policy on log store
- Pass rule: PASS only if every in-scope source logs centrally AND sampled dates show no unexplained gaps

### OPS-06 — Cloud audit trail enabled and protected
- TSC: CC7.2 | Category: Security
- Applies when: cloud infrastructure is in scope
- Implement: AWS CloudTrail (all regions, organization trail, log file validation) or GCP Cloud Audit Logs / Azure Activity Log, delivered to a locked bucket in a separate account
- Scan signals: logging.cloudtrail
- Type 1 test: audit trail enabled across all accounts and regions with integrity validation
- Type 2 test: confirm trail remained enabled throughout the period (no StopLogging events, or alerted and reviewed)
- Evidence: trail configuration, bucket policy, log-validation output, event history search
- Pass rule: PASS only if audit logging covered all accounts/regions for the whole period

### OPS-07 — Log retention of at least one year
- TSC: CC7.2 | Category: Security
- Applies when: always
- Implement: security logs retained ≥ 365 days (90 days hot, remainder archived) and immutable where feasible (S3 Object Lock)
- Scan signals: logging.retention_days
- Type 1 test: retention setting configured at ≥ 365 days
- Type 2 test: retrieve logs from the start of the observation period to prove retention
- Evidence: retention configuration, query returning logs from the earliest period date
- Pass rule: PASS only if logging.retention_days ≥ 365 (or a documented, longer contractual requirement is met) AND earliest-period logs are retrievable

### OPS-08 — Security monitoring and alerting
- TSC: CC7.2, CC7.3 | Category: Security
- Applies when: always
- Implement: alerts for root login, IAM policy changes, disabled logging, impossible travel, mass data download, and threat detection findings (GuardDuty/Defender/SCC) routed to on-call (PagerDuty/Opsgenie)
- Scan signals: monitoring.alerts, logging.centralized
- Type 1 test: alert rules exist for defined events and route to an on-call rotation
- Type 2 test: sample alerts in the period; confirm acknowledgement and triage within defined time
- Evidence: alert rule list, on-call schedule, alert history with triage notes
- Pass rule: PASS only if defined alert rules are active AND every sampled alert was triaged with a documented outcome

### OPS-09 — Security event triage and incident classification
- TSC: CC7.3 | Category: Security
- Applies when: always
- Implement: documented severity matrix (SEV1–SEV4) and criteria for declaring a security incident; triaged events recorded in a ticket system
- Scan signals: incident.runbook
- Type 1 test: classification criteria documented and a ticket workflow exists
- Type 2 test: sample security events in the period; confirm classification and escalation followed the matrix
- Evidence: severity matrix, event/incident tickets
- Pass rule: PASS only if every sampled event has a recorded classification consistent with the matrix

### OPS-10 — Incident response plan
- TSC: CC7.4 | Category: Security
- Applies when: always
- Implement: IR plan with roles (incident commander, comms, scribe), containment/eradication/recovery steps, evidence preservation, legal and customer notification paths; reviewed annually
- Scan signals: incident.runbook
- Type 1 test: plan exists, approved within 12 months, names responders and contact methods
- Type 2 test: sample incidents in the period; confirm the plan was followed (timeline, roles, communications)
- Evidence: IR plan, incident tickets and timelines, communication records
- Pass rule: PASS only if the plan is approved within 12 months AND every sampled incident followed it

### OPS-11 — Incident response tabletop exercise
- TSC: CC7.4, CC7.5 | Category: Security
- Applies when: always
- Implement: at least annual tabletop exercise with realistic scenario (ransomware, credential leak), attendance record, and action items tracked
- Scan signals: none
- Type 1 test: exercise plan exists or a recent exercise report is available
- Type 2 test: exercise held within the period; action items tracked to closure
- Evidence: exercise report, attendee list, action items
- Pass rule: PASS only if an exercise is dated within 12 months AND its action items are tracked

### OPS-12 — Post-incident review and recovery
- TSC: CC7.5 | Category: Security
- Applies when: any security or availability incident occurs
- Implement: blameless postmortem within 10 business days for SEV1/SEV2 including root cause, recovery validation, and corrective actions entered in the deficiency log
- Scan signals: incident.runbook
- Type 1 test: postmortem template and requirement documented
- Type 2 test: inspect every SEV1/SEV2 incident in the period for a completed postmortem and tracked actions
- Evidence: postmortem documents, corrective action tickets
- Pass rule: PASS only if every SEV1/SEV2 incident has a postmortem AND corrective actions are tracked

### OPS-13 — Incident notification to customers and authorities
- TSC: CC7.4, CC2.3 | Category: Security
- Applies when: customer contracts or laws require notification of security incidents
- Implement: notification matrix listing contractual and regulatory deadlines (e.g. GDPR 72 hours to regulator), approved templates, legal review step
- Scan signals: none
- Type 1 test: matrix and templates exist and match contract terms
- Type 2 test: for incidents requiring notice in the period, confirm notices were sent within deadlines
- Evidence: notification matrix, templates, sent notices with timestamps
- Pass rule: PASS only if every notifiable incident in the period was notified within the contractual or legal deadline

### OPS-14 — On-call coverage for production
- TSC: CC7.2, CC7.4 | Category: Security
- Applies when: the system has availability or security commitments outside business hours
- Implement: 24×7 on-call rotation with escalation policy and paging (PagerDuty/Opsgenie); acknowledgement SLA for critical pages
- Scan signals: monitoring.alerts
- Type 1 test: rotation and escalation policy configured with no coverage gaps
- Type 2 test: sample weeks in the period; confirm continuous coverage and acknowledgement of critical pages within SLA
- Evidence: on-call schedule export, escalation policy, page acknowledgement report
- Pass rule: PASS only if no sampled week had an uncovered shift AND critical pages met the acknowledgement SLA

## Security — Change Management (CC8)

### CHG-01 — Change management policy
- TSC: CC8.1 | Category: Security
- Applies when: always
- Implement: policy covering standard, normal, and emergency changes to code, infrastructure, configuration, and data; required approval, testing, and documentation for each type
- Scan signals: policies
- Type 1 test: policy approved and defines change types and approvals
- Type 2 test: policy reviewed in the period; changes sampled under CHG-02 follow it
- Evidence: approved policy with version history
- Pass rule: PASS only if the policy is approved within 12 months AND covers code, infrastructure, and emergency changes

### CHG-02 — Peer review enforced by branch protection
- TSC: CC8.1, CC5.1 | Category: Security
- Applies when: any code or IaC deployed to production
- Implement: protected default branch requiring at least one approving review from someone other than the author, dismissal of stale approvals, no force pushes, admins included
- Scan signals: change_mgmt.branch_protection
- Type 1 test: branch protection settings on production repositories on the report date
- Type 2 test: sample merged PRs per frequency table (typically 25–60); confirm non-author approval before merge; review protection-setting change audit log
- Evidence: branch protection settings export, sampled PR records, organization audit log
- Pass rule: PASS only if every sampled production change had non-author approval AND protection was never disabled without a recorded emergency change

### CHG-03 — Code ownership for sensitive paths
- TSC: CC8.1 | Category: Security
- Applies when: repositories contain security-sensitive code (auth, IaC, CI configuration)
- Implement: CODEOWNERS file requiring review from designated owners for sensitive directories, with "require review from code owners" enabled
- Scan signals: change_mgmt.codeowners
- Type 1 test: CODEOWNERS exists and code-owner review is required
- Type 2 test: sample changes to sensitive paths; confirm code-owner approval
- Evidence: CODEOWNERS file, branch protection setting, sampled PRs
- Pass rule: PASS only if sensitive paths are covered by CODEOWNERS AND sampled changes had owner approval

### CHG-04 — Automated tests and CI checks before merge
- TSC: CC8.1, PI1.3 | Category: Security
- Applies when: any code deployed to production
- Implement: CI (GitHub Actions/GitLab CI/CircleCI) runs unit/integration tests and security checks; status checks required to pass before merge
- Scan signals: ci, change_mgmt.branch_protection
- Type 1 test: CI pipeline exists and required status checks are configured
- Type 2 test: sample merged PRs; confirm checks passed before merge
- Evidence: CI configuration, required-check settings, sampled PR check results
- Pass rule: PASS only if required checks are configured AND no sampled PR merged with failing checks

### CHG-05 — Change documentation and traceability
- TSC: CC8.1 | Category: Security
- Applies when: always
- Implement: PR template capturing description, risk, testing performed, and linked ticket; release notes for customer-impacting changes
- Scan signals: change_mgmt.pr_template
- Type 1 test: PR template or change record format exists
- Type 2 test: sample changes; confirm description, testing evidence, and ticket link are present
- Evidence: PR template, sampled PRs with linked tickets
- Pass rule: PASS only if every sampled change documents purpose and testing

### CHG-06 — Separate environments and deployment only via pipeline
- TSC: CC8.1, CC5.2 | Category: Security
- Applies when: always
- Implement: dev/staging/prod separated (accounts or projects); production deploys only via CI/CD with restricted deploy credentials; no direct developer write access to prod infrastructure
- Scan signals: ci, iac
- Type 1 test: environments are separated and deploy permissions restricted to the pipeline
- Type 2 test: compare production deploy log to merged changes; investigate any deploy without a matching approved change
- Evidence: environment diagram, deploy role policy, deploy log reconciled to PRs
- Pass rule: PASS only if every sampled production deploy traces to an approved change AND no manual prod changes occurred outside emergency process

### CHG-07 — Emergency change procedure
- TSC: CC8.1 | Category: Security
- Applies when: hotfixes or break-glass changes bypass normal review
- Implement: emergency changes allowed only with incident reference; retroactive review and approval within 2 business days
- Scan signals: none
- Type 1 test: emergency procedure documented including retroactive approval
- Type 2 test: identify all emergency changes in the period; confirm retroactive review within the window
- Evidence: emergency change log, retroactive approvals
- Pass rule: PASS only if every emergency change in the period has retroactive approval within the defined window

## Security — Vendor Management (CC9.2)

### VND-01 — Vendor inventory with risk tiering
- TSC: CC9.2 | Category: Security
- Applies when: always
- Implement: inventory of vendors and subprocessors listing service, data accessed, criticality tier, contract owner, and review date
- Scan signals: vendors.list_present
- Type 1 test: inventory exists and is complete compared to accounts payable and SSO app list
- Type 2 test: new vendors added in the period appear in the inventory with a tier
- Evidence: vendor inventory, AP vendor list, IdP app list reconciliation
- Pass rule: PASS only if every vendor with access to customer data appears in the inventory with a risk tier

### VND-02 — Vendor due diligence before onboarding
- TSC: CC9.2 | Category: Security
- Applies when: onboarding a vendor that will access customer data or support production
- Implement: security review (SOC 2 report or questionnaire) and approval by security before contract signature for high/medium-tier vendors
- Scan signals: none
- Type 1 test: due diligence procedure exists with tier-based requirements
- Type 2 test: sample vendors onboarded in the period; confirm review completed before contract or access
- Evidence: procedure, review records, contract signature dates
- Pass rule: PASS only if every sampled high/medium vendor was reviewed before access

### VND-03 — Annual vendor review including SOC reports and CUECs
- TSC: CC9.2 | Category: Security
- Applies when: high-tier vendors or subservice organizations exist (cloud provider, IdP, payment processor)
- Implement: annual review of each critical vendor's SOC 2/ISO report, exceptions, and complementary user entity controls (CUECs), with CUECs mapped to internal controls
- Scan signals: vendors.list_present
- Type 1 test: latest reports collected and CUEC mapping exists
- Type 2 test: annual review performed within the period for each critical vendor
- Evidence: vendor SOC reports, review memos, CUEC mapping
- Pass rule: PASS only if every critical vendor was reviewed within 12 months AND each CUEC maps to an operating internal control

### VND-04 — Contracts with security and confidentiality terms
- TSC: CC9.2, C1.1 | Category: Security
- Applies when: vendors process or access confidential data
- Implement: contracts/DPAs include confidentiality, security requirements, breach notification, right to audit, subprocessor approval, and return/deletion at termination
- Scan signals: none
- Type 1 test: template terms exist and are in critical vendor contracts
- Type 2 test: sample vendors onboarded or renewed in the period; confirm terms present
- Evidence: contract template, executed contracts/DPAs
- Pass rule: PASS only if every sampled data-processing vendor contract contains confidentiality and breach-notification terms

### VND-05 — Vendor offboarding
- TSC: CC9.2 | Category: Security
- Applies when: a vendor relationship ends
- Implement: offboarding checklist revoking vendor access and API keys and obtaining data return or deletion confirmation
- Scan signals: none
- Type 1 test: offboarding procedure exists
- Type 2 test: sample terminated vendors; confirm access revoked and deletion confirmed
- Evidence: offboarding checklist, revocation records, deletion certificates
- Pass rule: PASS only if every sampled terminated vendor has access revocation AND a data deletion or return confirmation

## Availability (A1)

### AV-01 — Capacity monitoring and forecasting
- TSC: A1.1 | Category: Availability
- Applies when: Availability is in scope
- Implement: dashboards and alerts on CPU, memory, storage, DB connections, and queue depth with thresholds (e.g. 80%); autoscaling; quarterly capacity review
- Scan signals: monitoring.alerts
- Type 1 test: capacity alerts configured and autoscaling or headroom documented
- Type 2 test: sample quarterly capacity reviews; inspect capacity alerts in the period and their resolution
- Evidence: dashboard screenshots, alert rules, capacity review notes
- Pass rule: PASS only if capacity alerts exist for every critical resource AND quarterly reviews occurred

### AV-02 — Redundant infrastructure across failure domains
- TSC: A1.2 | Category: Availability
- Applies when: Availability is in scope
- Implement: multi-AZ databases and load-balanced stateless services across ≥ 2 availability zones; infrastructure defined in IaC for rebuild
- Scan signals: iac, cloud
- Type 1 test: production components deployed across multiple availability zones on the report date
- Type 2 test: configuration remained redundant throughout the period (config history)
- Evidence: architecture diagram, multi-AZ configuration exports
- Pass rule: PASS only if every tier needed to meet the SLA has no single-AZ dependency or a documented accepted risk

### AV-03 — Automated backups
- TSC: A1.2, PI1.5 | Category: Availability
- Applies when: the system stores customer data
- Implement: automated daily backups (point-in-time recovery where available), encrypted, retained per policy (e.g. 35 days), copied to a separate account or region
- Scan signals: backups.configured, encryption.kms
- Type 1 test: backup jobs configured for every production datastore
- Type 2 test: sample days per frequency table (20–40); confirm successful backup and investigate failures
- Evidence: backup configuration, job success history, failure tickets
- Pass rule: PASS only if every production datastore is backed up AND sampled days show success or remediated failure

### AV-04 — Backup restore testing
- TSC: A1.3 | Category: Availability
- Applies when: backups exist for in-scope data
- Implement: restore test at least annually (quarterly recommended) to an isolated environment with data integrity verification and measured restore time vs RTO
- Scan signals: backups.restore_test
- Type 1 test: restore test procedure exists and a recent test record exists
- Type 2 test: restore tests performed at the stated cadence within the period
- Evidence: restore test reports with date, data set, duration, verification result
- Pass rule: PASS only if a successful restore test occurred within the period AND measured restore time met RTO

### AV-05 — Disaster recovery plan and test
- TSC: A1.2, A1.3 | Category: Availability
- Applies when: Availability is in scope
- Implement: DR plan for loss of a region or critical vendor with runbooks, RTO/RPO, roles; annual DR test (failover or simulation) with lessons learned
- Scan signals: incident.runbook, backups.configured
- Type 1 test: DR plan approved and consistent with BCP RTO/RPO
- Type 2 test: DR test executed within the period; results and remediation documented
- Evidence: DR plan, DR test report, remediation items
- Pass rule: PASS only if a DR test is dated within 12 months AND results met RTO/RPO or gaps are tracked

### AV-06 — Environmental protections via hosting provider
- TSC: A1.2 | Category: Availability
- Applies when: Availability is in scope and infrastructure is hosted by a third party
- Implement: rely on cloud/colo provider controls for power, cooling, fire suppression; obtain and review provider SOC 2 covering A1.2
- Scan signals: cloud
- Type 1 test: provider report obtained; environmental controls identified as carved out
- Type 2 test: provider report covers the period or bridge letter exists
- Evidence: provider SOC 2 report, review memo
- Pass rule: PASS only if a current provider report covering environmental protections has been reviewed

## Processing Integrity (PI1)

### PI-01 — Processing specifications documented and communicated
- TSC: PI1.1 | Category: Processing Integrity
- Applies when: Processing Integrity is in scope (e.g. payments, payroll, data pipelines, calculations customers rely on)
- Implement: documented data definitions, processing rules, and output specifications; customer-facing API docs and changelogs
- Scan signals: none
- Type 1 test: specifications exist for in-scope processing and are available to users
- Type 2 test: specification updates in the period were communicated to customers
- Evidence: specification documents, API docs, changelog entries
- Pass rule: PASS only if each in-scope process has documented inputs, rules, and outputs

### PI-02 — Input validation
- TSC: PI1.2 | Category: Processing Integrity
- Applies when: Processing Integrity is in scope
- Implement: schema validation on API and file inputs (type, range, required fields), rejection with error messages, and logging of rejected inputs
- Scan signals: none
- Type 1 test: validation rules implemented on in-scope inputs (code walkthrough or test cases)
- Type 2 test: sample rejected-input logs; confirm invalid data was blocked and errors returned
- Evidence: validation code or schemas, automated test results, rejection logs
- Pass rule: PASS only if every in-scope input path validates data before processing

### PI-03 — Processing completeness monitoring and reconciliation
- TSC: PI1.3 | Category: Processing Integrity
- Applies when: Processing Integrity is in scope
- Implement: job-level monitoring (record counts in vs out, control totals), alerts on job failure or lag, daily reconciliation for financial or critical data
- Scan signals: monitoring.alerts
- Type 1 test: reconciliation and failure alerts configured
- Type 2 test: sample days (20–40); confirm reconciliations ran and discrepancies were resolved
- Evidence: reconciliation reports, job alert history, discrepancy tickets
- Pass rule: PASS only if sampled reconciliations completed AND every discrepancy has a documented resolution

### PI-04 — Output accuracy and controlled distribution
- TSC: PI1.4 | Category: Processing Integrity
- Applies when: Processing Integrity is in scope
- Implement: output validation checks before delivery, delivery only to authenticated recipients, delivery confirmation and timeliness monitoring
- Scan signals: none
- Type 1 test: output checks and access restrictions configured
- Type 2 test: sample outputs; confirm checks passed and delivery reached intended recipients on time
- Evidence: output check logs, delivery logs, access configuration
- Pass rule: PASS only if sampled outputs passed validation AND went only to authorized recipients

### PI-05 — Stored data integrity
- TSC: PI1.5 | Category: Processing Integrity
- Applies when: Processing Integrity is in scope
- Implement: database constraints, write-access restrictions, audit trails of data modifications, checksums or versioning on stored files (S3 versioning/Object Lock)
- Scan signals: backups.configured, logging.centralized
- Type 1 test: integrity mechanisms configured on in-scope stores
- Type 2 test: sample data-change audit records; confirm modifications were authorized
- Evidence: schema constraints, versioning configuration, data-change audit logs
- Pass rule: PASS only if stored in-scope data is protected from unauthorized modification AND changes are logged

## Confidentiality (C1)

### CF-01 — Data classification policy and labeling
- TSC: C1.1, CC2.1 | Category: Confidentiality
- Applies when: Confidentiality is in scope or the entity holds customer confidential data
- Implement: classification levels (Public, Internal, Confidential, Restricted) with handling rules; data stores tagged with classification
- Scan signals: policies, privacy.pii_fields
- Type 1 test: policy exists and in-scope data stores carry classification
- Type 2 test: new data stores in the period were classified
- Evidence: classification policy, data inventory with labels, resource tags
- Pass rule: PASS only if every data store holding confidential data is classified with handling rules applied

### CF-02 — Restricted access to confidential data
- TSC: C1.1, CC6.3 | Category: Confidentiality
- Applies when: Confidentiality is in scope
- Implement: production customer data accessible only to named roles; access logged; support access through audited tooling with customer consent where promised
- Scan signals: logging.centralized
- Type 1 test: access lists for confidential stores restricted to approved roles
- Type 2 test: sample access logs to confidential data; confirm each accessor was authorized
- Evidence: access control lists, data access logs, support-access tickets
- Pass rule: PASS only if every sampled access to confidential data was by an authorized role

### CF-03 — Retention schedule for confidential information
- TSC: C1.1, C1.2 | Category: Confidentiality
- Applies when: Confidentiality is in scope
- Implement: retention schedule per data type aligned with contracts; automated lifecycle rules (S3 lifecycle, DB TTL jobs)
- Scan signals: logging.retention_days
- Type 1 test: schedule exists and lifecycle rules are configured
- Type 2 test: sample data sets; confirm data older than retention was purged
- Evidence: retention schedule, lifecycle configuration, purge job logs
- Pass rule: PASS only if lifecycle rules match the schedule AND sampled data shows no retention beyond limits

### CF-04 — Secure deletion at contract end or on request
- TSC: C1.2, P4.3 | Category: Confidentiality
- Applies when: customers can terminate or request deletion
- Implement: documented deletion procedure within contractual timeframe (e.g. 30 days) covering primary stores, replicas, and noting backup expiry; deletion confirmation sent to customer
- Scan signals: privacy.dsar
- Type 1 test: procedure exists and matches contract terms
- Type 2 test: sample customer terminations and deletion requests; confirm deletion within timeframe
- Evidence: deletion procedure, deletion tickets, confirmation messages
- Pass rule: PASS only if every sampled deletion completed within the committed timeframe with confirmation

### CF-05 — Confidentiality agreements for personnel
- TSC: C1.1, CC1.1 | Category: Confidentiality
- Applies when: always
- Implement: NDA or confidentiality clause in employment and contractor agreements signed before access
- Scan signals: none
- Type 1 test: template agreement includes confidentiality obligations
- Type 2 test: sample new hires and contractors; confirm signed agreements before access
- Evidence: agreement template, signed agreements, access grant dates
- Pass rule: PASS only if every sampled person signed before receiving access

### CF-06 — No production confidential data in non-production
- TSC: C1.1 | Category: Confidentiality
- Applies when: development or test environments exist
- Implement: synthetic or masked data in dev/staging; any production data copy requires approval and masking
- Scan signals: privacy.pii_fields
- Type 1 test: policy prohibits unmasked prod data in non-prod; non-prod datastores inspected
- Type 2 test: sample prod-to-non-prod copy events in the period; confirm approval and masking
- Evidence: policy, masking scripts, approval tickets
- Pass rule: PASS only if no unmasked confidential data exists in non-production environments

## Privacy (P1–P8)

### PR-01 — Privacy notice published and maintained
- TSC: P1.1 | Category: Privacy
- Applies when: Privacy is in scope (the entity collects personal information directly from data subjects)
- Implement: public privacy notice describing purposes, categories collected, retention, sharing, rights, and contact; version history; updated when practices change
- Scan signals: privacy.privacy_notice
- Type 1 test: notice is published and matches actual collection practices
- Type 2 test: notice changes in the period were approved and communicated
- Evidence: notice URL with version date, approval records, change communications
- Pass rule: PASS only if the notice is accessible at the point of collection AND matches documented processing

### PR-02 — Consent capture and records
- TSC: P2.1 | Category: Privacy
- Applies when: processing relies on consent or opt-out choices (marketing, cookies, optional data)
- Implement: consent management (OneTrust/Cookiebot or in-app) recording who consented, to what, when, and the notice version; withdrawal honored
- Scan signals: privacy.privacy_notice
- Type 1 test: consent mechanism and consent records exist
- Type 2 test: sample data subjects; confirm consent record exists before processing and withdrawals were honored
- Evidence: consent logs, consent UI screenshots, withdrawal records
- Pass rule: PASS only if every sampled consent-based processing has a recorded consent AND withdrawals were honored

### PR-03 — Collection limited to stated purposes
- TSC: P3.1 | Category: Privacy
- Applies when: Privacy is in scope
- Implement: data inventory of personal information fields with purpose; new fields require privacy review
- Scan signals: privacy.pii_fields
- Type 1 test: inventory maps each PII field to a purpose in the notice
- Type 2 test: sample schema changes adding PII in the period; confirm privacy review
- Evidence: personal data inventory, privacy review records
- Pass rule: PASS only if every collected PII field maps to a stated purpose

### PR-04 — Explicit consent for sensitive personal information
- TSC: P3.2 | Category: Privacy
- Applies when: the entity collects sensitive data (health, biometrics, government IDs, precise location) or law requires explicit consent
- Implement: separate affirmative opt-in for sensitive data with recorded consent
- Scan signals: privacy.pii_fields
- Type 1 test: explicit consent flow exists for each sensitive category
- Type 2 test: sample sensitive-data subjects; confirm explicit consent recorded before collection
- Evidence: consent flow, consent records
- Pass rule: PASS only if every sampled sensitive-data collection has explicit consent dated before collection

### PR-05 — Use limitation
- TSC: P4.1 | Category: Privacy
- Applies when: Privacy is in scope
- Implement: new uses of personal data (analytics, ML training, marketing) require privacy review against the notice; access to PII restricted by purpose
- Scan signals: none
- Type 1 test: privacy review procedure for new uses exists
- Type 2 test: sample new features or data uses in the period; confirm review and consistency with the notice
- Evidence: privacy review records, notice, feature tickets
- Pass rule: PASS only if every sampled new use of PII was reviewed and is covered by the notice or consent

### PR-06 — Retention of personal information
- TSC: P4.2 | Category: Privacy
- Applies when: Privacy is in scope
- Implement: retention periods per PII category; automated purge jobs; protection against accidental deletion (backups, soft delete)
- Scan signals: logging.retention_days, backups.configured
- Type 1 test: retention periods defined and purge mechanisms configured
- Type 2 test: sample PII records; confirm none retained beyond period
- Evidence: retention schedule, purge job logs
- Pass rule: PASS only if no sampled PII exceeds its defined retention period

### PR-07 — Secure disposal of personal information
- TSC: P4.3 | Category: Privacy
- Applies when: Privacy is in scope
- Implement: deletion procedures for PII at end of retention or on request, including vendor copies; backups expire on schedule
- Scan signals: privacy.dsar
- Type 1 test: disposal procedure covers primary, backup, and vendor copies
- Type 2 test: sample disposal events; confirm deletion from all locations
- Evidence: disposal procedure, deletion logs, vendor deletion confirmations
- Pass rule: PASS only if sampled disposals cover primary stores and vendors AND backups expire within the stated period

### PR-08 — Data subject access requests
- TSC: P5.1, P6.7 | Category: Privacy
- Applies when: Privacy is in scope
- Implement: DSAR intake (form or email), identity verification, response within legal/committed deadline (e.g. 30 days GDPR, 45 days CCPA), including an accounting of disclosures when requested
- Scan signals: privacy.dsar
- Type 1 test: DSAR procedure with verification and deadlines exists
- Type 2 test: sample DSARs in the period; confirm verification and on-time response
- Evidence: DSAR log, verification records, responses with dates
- Pass rule: PASS only if every sampled DSAR was identity-verified and answered within the deadline

### PR-09 — Correction requests
- TSC: P5.2 | Category: Privacy
- Applies when: Privacy is in scope
- Implement: self-service profile edits or support process to correct data; corrections propagated to vendors that received the data where required
- Scan signals: privacy.dsar
- Type 1 test: correction mechanism exists
- Type 2 test: sample correction requests; confirm timely correction and propagation
- Evidence: correction request log, propagation records
- Pass rule: PASS only if every sampled correction was completed within the committed timeframe

### PR-10 — Disclosure to third parties only for stated purposes
- TSC: P6.1, P6.4 | Category: Privacy
- Applies when: personal information is shared with vendors or partners
- Implement: subprocessor list published; DPAs with privacy commitments; new sharing requires privacy review and notice coverage
- Scan signals: vendors.list_present
- Type 1 test: subprocessor list and DPAs exist for vendors receiving PII
- Type 2 test: sample vendors receiving PII; confirm DPA and notice coverage; confirm periodic compliance review
- Evidence: subprocessor list, DPAs, vendor privacy reviews
- Pass rule: PASS only if every vendor receiving PII has a DPA AND is disclosed in the notice or subprocessor list

### PR-11 — Record of authorized disclosures
- TSC: P6.2 | Category: Privacy
- Applies when: personal information is disclosed to third parties, including law enforcement requests
- Implement: log of disclosures with date, recipient, data categories, legal basis; law-enforcement request procedure
- Scan signals: none
- Type 1 test: disclosure log and procedure exist
- Type 2 test: sample disclosures in the period; confirm recorded completely
- Evidence: disclosure log, request procedure
- Pass rule: PASS only if every known disclosure in the period is in the log with recipient and basis

### PR-12 — Breach records and notification
- TSC: P6.3, P6.6 | Category: Privacy
- Applies when: Privacy is in scope
- Implement: register of unauthorized disclosures/breaches; assessment of notification obligations; notices to data subjects and regulators within legal deadlines
- Scan signals: incident.runbook
- Type 1 test: breach register and notification procedure exist
- Type 2 test: inspect all breaches in the period; confirm recording and timely notification
- Evidence: breach register, notification records with timestamps
- Pass rule: PASS only if every breach is recorded AND notifications met legal deadlines

### PR-13 — Vendor obligation to report privacy incidents
- TSC: P6.5 | Category: Privacy
- Applies when: vendors process personal information
- Implement: DPA clause requiring notification of suspected unauthorized disclosure within a fixed period (e.g. 72 hours or less); vendor notices routed into incident process
- Scan signals: none
- Type 1 test: clause present in DPA template and executed DPAs
- Type 2 test: sample vendor DPAs; inspect any vendor incident notices in the period for handling
- Evidence: DPA template, executed DPAs, vendor incident notices
- Pass rule: PASS only if every sampled PII vendor DPA includes a time-bound notification clause

### PR-14 — Personal data quality
- TSC: P7.1 | Category: Privacy
- Applies when: Privacy is in scope
- Implement: validation at collection, periodic data quality checks, and user ability to update records
- Scan signals: none
- Type 1 test: validation and update mechanisms exist
- Type 2 test: sample data quality checks performed in the period
- Evidence: validation rules, data quality reports
- Pass rule: PASS only if accuracy controls exist at collection AND users can update their data

### PR-15 — Privacy inquiries, complaints, and compliance monitoring
- TSC: P8.1 | Category: Privacy
- Applies when: Privacy is in scope
- Implement: privacy contact (privacy@ or DPO); complaint log with resolution; annual privacy compliance review reported to leadership
- Scan signals: privacy.privacy_notice
- Type 1 test: contact channel published and complaint procedure exists
- Type 2 test: sample complaints; confirm resolution and response; annual review performed
- Evidence: complaint log, responses, privacy review report
- Pass rule: PASS only if every sampled complaint was resolved with a documented response AND an annual privacy review occurred

### PR-16 — Privacy training for personnel handling PII
- TSC: P8.1, P4.1 | Category: Privacy
- Applies when: Privacy is in scope
- Implement: annual privacy training for staff with PII access (support, engineering, marketing) covering notice commitments and DSAR handling
- Scan signals: none
- Type 1 test: training content and assignment exist
- Type 2 test: sample PII-access staff; confirm completion within 12 months
- Evidence: training content, completion report
- Pass rule: PASS only if every sampled PII-access staff member completed privacy training within 12 months
