# SOC 2 Control Catalog

> This skill prepares for a SOC 2 audit; it is not an attestation. Only a licensed CPA firm can issue a SOC 2 Type 1 or Type 2 report.

## Purpose

A catalog of 106 auditor-realistic controls mapped to every one of the 61 AICPA Trust Services Criteria (see `tsc-criteria.md`). Skills use it to scope controls, map repository scan results to controls, plan evidence collection, and run readiness self-tests. The final control set, wording, and test procedures are agreed with your CPA firm; a control here is a strong starting point, not a guarantee that an auditor will accept it unchanged.

How to read it: start with `control-index.md` (one row per control with TSC, category, frequency, owner, and scan signals). Open a full entry here only for a control you are evaluating, by searching for `### <ID>`; do not load the whole catalog at once. For GCP or Azure service names, see `cloud-equivalents.md`.

## Field legend

Every entry has exactly these fields, in this order:

| Field | Meaning |
|---|---|
| TSC | Criteria IDs the control addresses, then ` \| Category: <name>` (one name per TSC series cited, for example `Security, Availability`) |
| Applies when | The scope trigger; if it does not apply, record the control as N/A with a reason in the system description |
| Implement | Concrete implementation, with example tooling |
| Scan signals | Dotted keys from the repository scanner (`scripts/scan.py`) that hint at the control, or `none` when only people/process evidence can show it |
| Frequency | How often the control operates: `Continuous/automated`, `Per event`, `Daily`, `Weekly`, `Monthly`, `Quarterly`, or `Annual` (a default; use your own cadence if it differs) |
| Owner | Default role that operates the control and holds its evidence |
| Type 1 test | What the auditor checks for design and implementation on the report date |
| Type 2 test | What the auditor checks for operating effectiveness across the observation period |
| Evidence | Artifacts to hand the auditor |
| Type 1 pass | Self-test rule for Type 1 readiness: the control is designed and implemented, shown by a single instance or configuration as of the report date |
| Type 2 pass | Self-test rule for Type 2 readiness: the control operated effectively across the whole period, judged on the sampled population |

A scan signal is a hint, never proof: the scanner sees the repository, not the cloud account, the IdP, or HR records. A control backed only by a scan signal is at best "likely implemented" until evidence is collected.

## ID prefixes

| Prefix | Area | Criteria |
|---|---|---|
| GOV | Governance, control environment, communication, system description, subservice organizations | CC1–CC2 (GOV-11 also CC9.2) |
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

## Scope selection rule

Every skill selects in-scope controls with this one rule. A control is in scope when **any** criterion on its `TSC:` line belongs to an in-scope category, judged by the criterion's series:

| Series | Category | `tsc_scope` key |
|---|---|---|
| CC1–CC9 | Security | `security` (always in scope) |
| A1.x | Availability | `availability` |
| PI1.x | Processing Integrity | `processing_integrity` |
| C1.x | Confidentiality | `confidentiality` |
| P1–P8 | Privacy | `privacy` |

Because Security is always in scope, every control citing a CC criterion is selected. The `Category:` label lists the same categories, one per series cited, so it always agrees with this rule. Then check `Applies when`; a control that does not apply is recorded as N/A with a reason.

## Type 1 vs Type 2

- Type 1 reports on whether the system description is fairly presented and controls are suitably designed and implemented as of a single date. The auditor typically tests one instance of each control (inquiry plus inspection or observation). Use the `Type 1 pass` field.
- Type 2 reports on whether controls operated effectively over an observation period (commonly 3 to 12 months; 6 or 12 is most common after a first report). The AICPA sets no minimum period; some report users do not accept periods shorter than 6 months. The auditor samples occurrences across the whole period and describes every deviation found in the test results. Management may add a response to a deviation; that response is optional, unaudited other information, but strongly advisable. Use the `Type 2 pass` field.
- A scheduled control that should have run inside the period but did not (for example a quarterly review that was skipped, or an annual review scheduled after period end) is a deviation; plan cadences so each control fires inside the window.
- An event-driven control with no triggering event in the period (no incidents, no terminations, no emergency changes) is reported as "no occurrence, not tested". That is not an exception. Keep evidence that nothing occurred, such as an empty population report from the system of record.

## Type 2 sampling guide

Sample sizes below are common auditor practice, not AICPA mandates; each CPA firm sets its own methodology.

| Control frequency | Typical sample |
|---|---|
| Annual | 1 |
| Quarterly | 2 |
| Monthly | 2–5 |
| Weekly | 5–15 |
| Daily | 20–40 |
| Many times/day | 25–60 |
| Per event (hires, terminations, changes, vendor onboarding) | about 25, or the full population if it is small (under about 20) |
| Continuous/automated | 1 (a test of one), see below |

- Automated controls: a system-enforced control is usually tested once (a test of one), provided the IT general controls over that system (logical access, AC-*, and change management, CHG-*) are effective for the whole period. An ITGC exception widens testing of the automated control.
- Population completeness (IPE): before sampling, auditors test that system-generated populations and reports are complete and accurate. For each population, record the source system and the query or report parameters so the auditor can re-run it.
- Plan for zero tolerance: one exception in a sample usually leads to expanded testing (for example from 25 to 40 or 60) or a reported deviation.
- Periods shorter than 12 months: sample sizes scale down with the number of occurrences (a 3-month period has one quarterly occurrence and fewer daily ones); agree sizes with your CPA firm.
- Evidence retention: keeping evidence for the audit period plus 1 year is common practice, not a standard; keep it longer if contracts or law require it.

## Security — Governance (CC1–CC2)

### GOV-01 — Code of conduct acknowledged by all personnel
- TSC: CC1.1, CC1.5 | Category: Security
- Applies when: always (every employee and contractor with system access)
- Implement: written code of conduct covering ethics, conflicts of interest, acceptable use, and sanctions; e-signature acknowledgement by employees and contractors at start and annually via HRIS (Rippling/BambooHR/Gusto) or contractor onboarding
- Scan signals: policies
- Frequency: Per event
- Owner: People ops
- Type 1 test: code of conduct exists, is approved by management, and the acknowledgement workflow is configured for new hires
- Type 2 test: sample new hires, new contractors, and existing staff (per-event and annual rows of the sampling table); each signed within 30 days of start and within the annual cycle
- Evidence: approved code of conduct with version date, acknowledgement report listing every person and signature date, new-hire roster for the period
- Type 1 pass: PASS if an approved code of conduct (approved within 12 months) exists AND the acknowledgement workflow is configured for new employees and contractors AND current staff have acknowledged it as of the report date
- Type 2 pass: PASS only if every sampled new hire or contractor acknowledged within 30 days of start AND every sampled existing person acknowledged within the annual cycle AND the document was approved within the period

### GOV-02 — Background checks before access is granted
- TSC: CC1.1, CC1.4 | Category: Security
- Applies when: hiring employees or long-term contractors who receive production or customer-data access (contractors through their agency's screening, confirmed in the contract)
- Implement: background screening (Checkr/Certn/HireRight) to the extent local law permits, completed before the start date or before production access is provisioned
- Scan signals: none
- Frequency: Per event
- Owner: People ops
- Type 1 test: screening policy defines who is screened and when; one completed check exists for a recent hire
- Type 2 test: sample new hires in the period; confirm a completed check dated on or before the access grant date
- Evidence: screening policy, vendor completion report (pass/fail only, no sensitive detail), hire roster with start and access dates
- Type 1 pass: PASS if a screening policy names who is screened and when AND at least one recent hire shows a completed check dated before production access
- Type 2 pass: PASS only if every sampled hire or long-term contractor in the period has a completed check dated before production access, or a documented legal exception approved by HR

### GOV-03 — Board or executive oversight of the security program
- TSC: CC1.2, CC4.2 | Category: Security
- Applies when: always; for startups without an independent board, a documented executive or advisory committee is the common substitute
- Implement: at least quarterly security briefing to the board or leadership committee covering risk register, incidents, audit status, and open deficiencies, with minutes
- Scan signals: none
- Frequency: Quarterly
- Owner: Leadership (CEO)
- Type 1 test: charter or written mandate for oversight exists; most recent meeting minutes show security agenda items
- Type 2 test: inspect minutes for each quarter in the period (sample 2 per frequency table); confirm security topics and action items
- Evidence: governance charter, dated meeting minutes or decks, attendee list
- Type 1 pass: PASS if a written oversight mandate exists AND the most recent meeting minutes show security agenda items and decisions
- Type 2 pass: PASS only if oversight meetings occurred every quarter of the period AND minutes record security review and decisions

### GOV-04 — Organizational chart and security roles defined
- TSC: CC1.3 | Category: Security
- Applies when: always
- Implement: current org chart from HRIS; named security owner (CISO/Head of Security or designated lead); RACI for key controls; written job descriptions for security-relevant roles
- Scan signals: none
- Frequency: Annual
- Owner: People ops
- Type 1 test: org chart is current as of the report date and the security owner's responsibilities are documented
- Type 2 test: org chart is maintained (reviewed at least annually or on reorganisation); role changes during the period are reflected
- Evidence: dated org chart, security role description, control-owner RACI
- Type 1 pass: PASS if the org chart matches HRIS headcount on the report date AND every in-scope control has a named owner
- Type 2 pass: PASS only if the org chart was reviewed at least once in the period AND role changes during the period are reflected AND control owners stayed assigned throughout

### GOV-05 — Security awareness training at hire and annually
- TSC: CC1.4, CC2.2 | Category: Security
- Applies when: always (all employees and contractors with system access)
- Implement: LMS-tracked training (KnowBe4/Curricula/Vanta/Drata training) within 30 days of hire and every 12 months; phishing simulations recommended; developers also take secure-coding training
- Scan signals: none
- Frequency: Per event
- Owner: People ops
- Type 1 test: training content and assignment rules exist; completion tracking is configured
- Type 2 test: sample new hires and existing staff; confirm completion dates within 30 days of hire and within 12 months of prior completion
- Evidence: training content or syllabus, LMS completion report with dates, escalation records for overdue users
- Type 1 pass: PASS if training content and assignment rules exist AND completion tracking is configured AND current staff show completion within the last 12 months
- Type 2 pass: PASS only if every sampled employee or contractor completed training within 30 days of hire and within 12 months of prior completion; overdue people have documented escalation and completion before period end

### GOV-06 — Performance reviews and disciplinary process cover security
- TSC: CC1.5 | Category: Security
- Applies when: always
- Implement: annual performance reviews that include adherence to policies; documented sanctions policy for violations applied consistently to employees and contractors (contractors through contract terms rather than reviews)
- Scan signals: none
- Frequency: Annual
- Owner: People ops
- Type 1 test: sanctions/disciplinary policy exists and review template references policy compliance
- Type 2 test: sample employees from the annual review population (annual control: the auditor samples people, typically about 25 or the whole population if small) for a completed review in the cycle; inspect every security-violation case in the period for documented action
- Evidence: disciplinary policy, review template, review completion report, anonymised violation case log
- Type 1 pass: PASS if a sanctions policy exists AND the review template references policy compliance
- Type 2 pass: PASS only if review completion is >= 95% for the annual cycle in the period (sampled from the full employee population) AND every recorded violation has a documented outcome

### GOV-07 — Information security policies approved, published, and acknowledged
- TSC: CC2.2, CC5.3 | Category: Security
- Applies when: always
- Implement: policy set (information security, access control, change management, incident response, BC/DR, data classification, vendor management, acceptable use) with owner, version, and approval date; published on intranet; reviewed at least annually
- Scan signals: policies
- Frequency: Annual
- Owner: Security owner
- Type 1 test: each policy exists, is approved, is accessible to staff, and has a named owner
- Type 2 test: confirm annual review/approval occurred in the period; sample personnel acknowledgements
- Evidence: policy documents with version history, approval records, acknowledgement report
- Type 1 pass: PASS if every required policy exists, is approved within the last 12 months, has a named owner, and is accessible to staff
- Type 2 pass: PASS only if the annual review and approval occurred within the period AND sampled personnel acknowledged the current versions

### GOV-08 — System component inventory and data-flow diagrams maintained
- TSC: CC2.1 | Category: Security
- Applies when: always (feeds the DC 200 system description in Section III of the SOC 2 report; see GOV-13)
- Implement: inventory of production components generated from IaC or cloud asset inventory; architecture and data-flow diagrams covering infrastructure, software, people, data, and processes; this feeds the DC 200 system description maintained under GOV-13
- Scan signals: iac, cloud
- Frequency: Annual
- Owner: Engineering lead
- Type 1 test: inventory and diagrams match the production environment on the report date
- Type 2 test: inventory and diagrams were updated for significant changes during the period (compare against change log)
- Evidence: architecture diagram, data-flow diagram, asset inventory export with extraction date
- Type 1 pass: PASS if every production component in the cloud inventory appears in the inventory or diagrams on the report date AND diagrams are dated within the last 12 months
- Type 2 pass: PASS only if the inventory and diagrams were updated for every significant change in the period (compared against the change log) AND reviewed at least annually

### GOV-09 — External communication of commitments and reporting channel
- TSC: CC2.3 | Category: Security
- Applies when: the system serves external customers
- Implement: published security page or trust center, terms/MSA and SLA stating security and availability commitments, public status page, security contact (security@ or security.txt) and responsible-disclosure policy
- Scan signals: incident.runbook
- Frequency: Per event
- Owner: Security owner
- Type 1 test: commitments are documented in customer agreements and a working external reporting channel exists
- Type 2 test: sample customer notifications sent in the period (incidents, material changes) and confirm they followed the communication procedure
- Evidence: MSA/terms excerpt, trust page URL capture, status-page history, security.txt, sample customer notices
- Type 1 pass: PASS if commitments are written in customer agreements AND an external reporting channel exists with a defined owner who monitors it
- Type 2 pass: PASS only if every sampled customer notification in the period followed the communication procedure AND the reporting channel was monitored throughout

### GOV-10 — Internal reporting channel for concerns (whistleblower)
- TSC: CC1.1, CC2.2 | Category: Security
- Applies when: always
- Implement: anonymous reporting option (EthicsPoint/Navex/a monitored form) plus a named escalation contact; non-retaliation statement in the code of conduct
- Scan signals: none
- Frequency: Per event
- Owner: People ops
- Type 1 test: channel exists, is communicated to staff, and reports route to someone independent of the reported party
- Type 2 test: inspect the report log for the period; confirm each report was triaged and closed with documentation
- Evidence: channel description in handbook, routing configuration, anonymised report log
- Type 1 pass: PASS if the channel exists, is communicated to staff, AND routes to someone independent of the reported party
- Type 2 pass: PASS only if the channel stayed available through the period AND every report in the period has a documented disposition (no reports: keep the empty log as evidence)

### GOV-11 — Subservice organizations and CSOCs identified (carve-out vs inclusive)
- TSC: CC9.2, CC2.3 | Category: Security
- Applies when: the system relies on a subservice organization (cloud provider, managed database, IdP, payment processor) for controls that support the criteria
- Implement: list each subservice organization in the system description with the method chosen (carve-out is the default; the inclusive method requires the subservice organization's own written assertion and auditor access); list the complementary subservice organization controls (CSOCs) your report assumes each one performs; obtain and review its SOC report under VND-03
- Scan signals: cloud, vendors.list_present
- Frequency: Annual
- Owner: Compliance owner
- Type 1 test: system description names each subservice organization, the method, and the CSOCs relied on; current SOC reports on file
- Type 2 test: subservice list and CSOCs reviewed within the period; changes in subservice organizations during the period reflected in the description
- Evidence: subservice organization list with method and CSOCs, system description excerpt, vendor SOC reports and review memos
- Type 1 pass: PASS if every subservice organization that performs controls relevant to the criteria is listed with its method and CSOCs AND a current SOC report is on file for each
- Type 2 pass: PASS only if the list and CSOCs were reviewed within the period AND every subservice organization change in the period is reflected AND reports (with bridge letters for gaps) cover the period

### GOV-12 — Complementary user entity controls (CUECs) communicated to customers
- TSC: CC2.3 | Category: Security
- Applies when: the system's controls depend on customers doing something themselves (managing their own users, protecting API keys, configuring SSO, reviewing their audit logs)
- Implement: written list of CUECs in the system description and in customer-facing documentation (trust center, security guide, or contract exhibit); updated when the product changes the customer's responsibilities
- Scan signals: none
- Frequency: Annual
- Owner: Compliance owner
- Type 1 test: CUEC list exists, appears in the system description, and is available to customers
- Type 2 test: CUEC list reviewed within the period and updated for product changes that shifted customer responsibilities
- Evidence: CUEC list, system description excerpt, customer documentation URL or contract exhibit
- Type 1 pass: PASS if every control that depends on customer action is listed as a CUEC AND the list is published to customers
- Type 2 pass: PASS only if the CUEC list was reviewed within the period AND matches the product's customer responsibilities at period end

### GOV-13 — System description (DC 200) and management assertion kept current
- TSC: CC2.2, CC2.3 | Category: Security
- Applies when: always (the description is Section III and the assertion Section II of the SOC 2 report)
- Implement: system description following AICPA DC 200: types of services, principal service commitments and system requirements, components (infrastructure, software, people, procedures, data), system boundaries, system incidents, applicable criteria and related controls, CUECs (GOV-12), subservice organizations and CSOCs (GOV-11), criteria that do not apply with reasons, and (Type 2) significant changes during the period; management's written assertion and representation letter drafted from the CPA firm's template; both reviewed and approved by management
- Scan signals: none
- Frequency: Annual
- Owner: Compliance owner
- Type 1 test: description covers every DC 200 element, matches the environment as of the report date, and management's assertion is drafted
- Type 2 test: description is accurate for the whole period, including significant changes and system incidents in the period; assertion signed for the period
- Evidence: approved system description with version history, management assertion, representation letter, change log used for significant changes
- Type 1 pass: PASS if the description covers every DC 200 element, matches the environment on the report date, AND is approved by management with a drafted assertion
- Type 2 pass: PASS only if the description is accurate for the whole period (significant changes and system incidents in the period included) AND the signed assertion covers the period

## Security — Risk Assessment (CC3, CC9.1)

### RSK-01 — Annual risk assessment against defined objectives
- TSC: CC3.1, CC3.2 | Category: Security
- Applies when: always
- Implement: documented methodology (likelihood × impact scale, risk appetite/tolerance statement); at least annual assessment covering threats to security, availability, and confidentiality objectives, including vendor risks; results approved by leadership
- Scan signals: none
- Frequency: Annual
- Owner: Security owner
- Type 1 test: methodology and a dated risk assessment with leadership approval exist
- Type 2 test: assessment was performed within the period and within 12 months of the prior one; outputs feed the risk register
- Evidence: risk methodology, risk assessment report with approval date, risk appetite statement
- Type 1 pass: PASS if a documented methodology AND an approved risk assessment dated within the last 12 months exist that state objectives and risk tolerance
- Type 2 pass: PASS only if an assessment was performed within the period, within 12 months of the prior one, AND its outputs fed the risk register

### RSK-02 — Risk register with owners and treatment plans
- TSC: CC3.2, CC5.1 | Category: Security
- Applies when: always
- Implement: register (spreadsheet or GRC tool) listing each risk, inherent and residual rating, owner, treatment decision (accept/mitigate/transfer/avoid), linked controls, and due dates; reviewed quarterly
- Scan signals: none
- Frequency: Quarterly
- Owner: Security owner
- Type 1 test: register exists, every risk has an owner and treatment, and high risks map to controls
- Type 2 test: sample quarterly reviews per frequency table; confirm updates and status changes recorded
- Evidence: risk register export with change history, quarterly review minutes, risk-acceptance sign-offs
- Type 1 pass: PASS if every high/critical risk has an owner, a treatment, and either mapped controls or a signed acceptance
- Type 2 pass: PASS only if the quarterly reviews in the period occurred AND recorded updates and status changes

### RSK-03 — Fraud risk assessment
- TSC: CC3.3 | Category: Security
- Applies when: always
- Implement: fraud scenarios (insider data theft, unauthorized privilege escalation, financial manipulation, fake vendor) assessed in the annual risk assessment with linked mitigations
- Scan signals: none
- Frequency: Annual
- Owner: Security owner
- Type 1 test: risk assessment explicitly includes fraud scenarios with incentive/opportunity analysis
- Type 2 test: fraud section updated in the period's assessment
- Evidence: fraud section of the risk assessment, linked controls list
- Type 1 pass: PASS if the risk assessment covers at least insider-misuse and unauthorized-access fraud scenarios with incentive/opportunity analysis and mitigating controls
- Type 2 pass: PASS only if the fraud section was updated in the assessment performed within the period

### RSK-04 — Significant change triggers risk reassessment
- TSC: CC3.4 | Category: Security
- Applies when: always
- Implement: defined triggers (new product line, acquisition, new critical vendor, cloud migration, leadership change, new regulation) that require a documented risk review before or soon after the change
- Scan signals: none
- Frequency: Per event
- Owner: Security owner
- Type 1 test: procedure lists triggers and the review responsible party
- Type 2 test: identify significant changes in the period (from change log, vendor list, org changes) and confirm each had a risk review
- Evidence: change-risk procedure, risk review records tied to each significant change
- Type 1 pass: PASS if a procedure lists the change triggers and who performs the risk review
- Type 2 pass: PASS only if every significant change identified in the period has a dated risk review

### RSK-05 — Business continuity plan with defined RTO/RPO
- TSC: CC9.1, A1.2 | Category: Security, Availability
- Applies when: always
- Implement: BCP covering critical services, roles, communication tree, RTO/RPO targets, alternate work arrangements; reviewed annually; cyber insurance considered as risk transfer
- Scan signals: backups.configured
- Frequency: Annual
- Owner: Leadership (CEO)
- Type 1 test: BCP exists, is approved, and defines RTO/RPO for in-scope services
- Type 2 test: annual review or exercise occurred in the period with documented results
- Evidence: approved BCP, business impact analysis, exercise report, insurance certificate if used
- Type 1 pass: PASS if the BCP is approved within 12 months AND defines RTO/RPO that match customer commitments
- Type 2 pass: PASS only if the annual review or exercise occurred within the period with documented results

## Security — Monitoring Activities (CC4)

### MON-01 — Continuous control monitoring
- TSC: CC4.1 | Category: Security
- Applies when: always
- Implement: automated compliance monitoring (Vanta/Drata/Secureframe or AWS Config/AWS Security Hub CSPM conformance packs and standards) with a named reviewer who checks failing tests at least weekly
- Scan signals: cloud, monitoring.alerts
- Frequency: Weekly
- Owner: Compliance owner
- Type 1 test: monitoring is configured against in-scope controls and failures notify an owner
- Type 2 test: sample weekly reviews per frequency table; confirm failing checks were triaged
- Evidence: tool configuration, failing-check history, review log or tickets
- Type 1 pass: PASS if monitoring covers all in-scope systems AND failures notify a named owner
- Type 2 pass: PASS only if sampled weekly reviews occurred AND sampled failing checks have a documented response

### MON-02 — Annual third-party penetration test
- TSC: CC4.1, CC7.1 | Category: Security
- Applies when: the system exposes applications or APIs to customers or the internet
- Implement: independent pentest of production-like application and external infrastructure at least annually and after major architecture changes; findings tracked to remediation by severity SLA
- Scan signals: none
- Frequency: Annual
- Owner: Security owner
- Type 1 test: most recent report exists, scope covers in-scope systems, and findings are tracked
- Type 2 test: pentest performed within the period; critical/high findings remediated within SLA or risk-accepted
- Evidence: pentest report (with tester independence statement), remediation tickets, retest letter
- Type 1 pass: PASS if a pentest report dated within 12 months covers the in-scope systems AND its findings are tracked
- Type 2 pass: PASS only if a pentest was performed within the period AND no critical/high finding stayed open past its SLA without signed risk acceptance

### MON-03 — Control deficiencies tracked to remediation
- TSC: CC4.2 | Category: Security
- Applies when: always
- Implement: deficiency log (Jira/Linear project) for findings from audits, pentests, monitoring, and incidents; each item has severity, owner, due date; overdue items escalated to leadership
- Scan signals: none
- Frequency: Per event
- Owner: Compliance owner
- Type 1 test: log exists with required fields and an escalation rule
- Type 2 test: sample deficiencies raised during the period; confirm remediation or escalation by due date
- Evidence: deficiency log export, escalation records, leadership reporting
- Type 1 pass: PASS if the deficiency log has severity, owner, due date, and an escalation rule
- Type 2 pass: PASS only if every sampled deficiency raised in the period has an owner and due date AND none passed its due date without escalation

### MON-04 — Periodic internal control assessment
- TSC: CC4.1 | Category: Security
- Applies when: always
- Implement: at least annual internal readiness review or internal audit by someone independent of the control operator (internal audit, compliance lead, or outside consultant), results reported to leadership
- Scan signals: none
- Frequency: Annual
- Owner: Compliance owner
- Type 1 test: assessment plan exists and assigns an independent assessor
- Type 2 test: assessment completed within the period with findings fed into MON-03
- Evidence: assessment plan, report, findings in deficiency log
- Type 1 pass: PASS if an assessment plan assigns an assessor independent of the control operators
- Type 2 pass: PASS only if an independent assessment was completed within the period AND its findings are tracked in MON-03

## Security — Control Activities (CC5)

### CTL-01 — Risk-to-control matrix
- TSC: CC5.1 | Category: Security
- Applies when: always
- Implement: matrix mapping each significant risk to preventive and detective controls and to TSC criteria; reviewed with the annual risk assessment
- Scan signals: none
- Frequency: Annual
- Owner: Compliance owner
- Type 1 test: matrix exists and every high risk maps to at least one control
- Type 2 test: matrix updated after the period's risk assessment
- Evidence: control matrix with version date
- Type 1 pass: PASS if every in-scope criterion and every high risk maps to at least one implemented control
- Type 2 pass: PASS only if the matrix was updated after the risk assessment performed in the period

### CTL-02 — Segregation of duties for production changes and access
- TSC: CC5.1, CC6.3 | Category: Security
- Applies when: always
- Implement: authors cannot approve or merge their own code; access requests approved by someone other than the requester; admins of the IdP are not the sole reviewers of their own access
- Scan signals: change_mgmt.branch_protection, change_mgmt.codeowners
- Frequency: Per event
- Owner: Engineering lead
- Type 1 test: technical settings and procedures enforce separation (branch protection requires non-author approval)
- Type 2 test: sample merged changes and access grants; confirm approver differs from requester
- Evidence: repository protection settings, sample PRs, access tickets
- Type 1 pass: PASS if technical settings enforce non-author approval AND access requests require an approver other than the requester
- Type 2 pass: PASS only if no sampled change or access grant in the period was self-approved; small-team exceptions require documented compensating detective review

### CTL-03 — Secure configuration baselines defined as code
- TSC: CC5.2, CC7.1 | Category: Security
- Applies when: the system runs on cloud infrastructure or managed hosts
- Implement: infrastructure defined in Terraform/CloudFormation/Pulumi with hardened modules; CIS benchmark-aligned baselines; policy-as-code checks (Trivy config, the successor to tfsec, or Checkov) in CI
- Scan signals: iac, ci
- Frequency: Continuous/automated
- Owner: Platform/DevOps lead
- Type 1 test: baseline standard exists and production resources are deployed from IaC
- Type 2 test: sample infrastructure changes; confirm they went through IaC and passed policy checks
- Evidence: baseline standard, IaC repository, CI policy-check logs
- Type 1 pass: PASS if a baseline standard exists AND production infrastructure is defined in IaC AND policy checks run in CI
- Type 2 pass: PASS only if sampled infrastructure changes went through IaC and passed policy checks AND drift from the baseline was detected or blocked throughout the period

### CTL-04 — Procedures documented with owners and timing
- TSC: CC5.3 | Category: Security
- Applies when: always
- Implement: runbooks for recurring controls (access review, backup test, vendor review) listing owner, frequency, steps, and evidence to retain; tracked in a compliance calendar
- Scan signals: policies, incident.runbook
- Frequency: Annual
- Owner: Compliance owner
- Type 1 test: procedures exist for each recurring control with owner and frequency
- Type 2 test: compliance calendar shows each recurring control executed on schedule
- Evidence: runbooks, compliance calendar, completion records
- Type 1 pass: PASS if every recurring in-scope control has a written procedure with owner and frequency
- Type 2 pass: PASS only if the compliance calendar shows each recurring control executed on schedule through the period

## Security — Logical and Physical Access (CC6)

### AC-01 — Centralized identity with SSO
- TSC: CC6.1 | Category: Security
- Applies when: any workforce access to production, admin tools, source control, or cloud console
- Implement: single IdP (Okta/Entra ID/Google Workspace) with SAML/OIDC SSO to cloud console, source control, and critical SaaS; local accounts disabled or inventoried as break-glass
- Scan signals: auth.sso, auth.idp
- Frequency: Continuous/automated
- Owner: IT admin
- Type 1 test: critical systems authenticate through the IdP on the report date
- Type 2 test: SSO configuration unchanged or changes approved; no unauthorized local accounts created during the period
- Evidence: IdP application list, SSO configuration screenshots, local account inventory
- Type 1 pass: PASS if every critical system authenticates through the IdP on the report date AND every local account is a documented break-glass account
- Type 2 pass: PASS only if SSO configuration stayed in place (changes approved) AND no unauthorized local accounts were created during the period

### AC-02 — MFA enforced for all workforce access
- TSC: CC6.1 | Category: Security
- Applies when: any human login to prod, admin tools, or cloud console
- Implement: IdP MFA policy (Okta/Entra/Google Workspace); cloud console via SSO only; no IAM users with console passwords
- Scan signals: auth.sso, auth.mfa_hint
- Frequency: Continuous/automated
- Owner: IT admin
- Type 1 test: MFA policy exists and is enforced (not optional) at the IdP on the report date
- Type 2 test: MFA is an automated control: test the IdP enforcement policy once, then inspect the IdP configuration-change log (policy-state history) for the whole period to show enforcement was never disabled or weakened, and test change management over the IdP; no login sampling is needed
- Evidence: IdP policy export, MFA enrollment report, IdP configuration-change log for the period
- Type 1 pass: PASS if MFA is enforced (not optional) for all users at the IdP on the report date AND no bypass/break-glass account lacks a compensating control
- Type 2 pass: PASS only if the IdP configuration-change log shows enforcement stayed on for the whole period AND change management over the IdP was effective

### AC-03 — Access provisioning requires documented approval
- TSC: CC6.2, CC6.3 | Category: Security
- Applies when: granting any user access to in-scope systems
- Implement: access requests via ticket or IdP workflow naming system, role, and justification; approved by manager or system owner before grant
- Scan signals: none
- Frequency: Per event
- Owner: IT admin
- Type 1 test: provisioning procedure exists and a sample grant shows approval before access
- Type 2 test: sample new hires and access changes; compare approval timestamp to grant timestamp from IdP or system logs
- Evidence: access request tickets, IdP provisioning logs, new-hire roster
- Type 1 pass: PASS if a provisioning procedure exists AND a sample grant shows approval dated before access
- Type 2 pass: PASS only if every sampled grant in the period has approval dated on or before the grant

### AC-04 — Timely access removal on termination
- TSC: CC6.2, CC6.3 | Category: Security
- Applies when: any employee or contractor departs or changes role
- Implement: HRIS-to-IdP deprovisioning (SCIM) disabling accounts within 24 hours of termination (immediately for involuntary); checklist for non-SSO systems and shared secrets
- Scan signals: auth.idp
- Frequency: Per event
- Owner: People ops
- Type 1 test: offboarding procedure defines the SLA and covers non-SSO systems
- Type 2 test: sample terminations; compare HR termination date to account disable timestamps in IdP and critical systems
- Evidence: termination roster from HRIS, IdP deactivation log, offboarding checklists
- Type 1 pass: PASS if the offboarding procedure defines the 24-hour SLA AND covers non-SSO systems and shared secrets
- Type 2 pass: PASS only if every sampled leaver in the period lost access within the stated SLA across the IdP and non-SSO systems

### AC-05 — Quarterly user access reviews
- TSC: CC6.2, CC6.3 | Category: Security
- Applies when: always (production, cloud console, databases, source control, critical SaaS)
- Implement: quarterly review by system owners of every account and role, using user lists exported from each system of record (record the export query or report parameters so the list can be shown complete); reviewers never approve their own access (a second person reviews the reviewer's accounts); inappropriate access removed and the removal ticketed
- Scan signals: none
- Frequency: Quarterly
- Owner: Security owner
- Type 1 test: review procedure exists and the most recent review is complete with sign-off
- Type 2 test: auditor typically samples 2 quarterly reviews (per frequency table) but may pick any quarter, so every quarter must be evidenced; confirm user lists were complete (IPE: source, extraction date, parameters), the reviewer was independent of the accounts reviewed, and flagged items were remediated
- Evidence: user listings with extraction date and query/parameters, reviewer sign-off, removal tickets
- Type 1 pass: PASS if the review procedure exists AND the most recent review is complete, signed off by a reviewer independent of the accounts reviewed, AND used a complete user list
- Type 2 pass: PASS only if every quarterly review in the period (not only the sampled ones) covered all in-scope systems from complete, system-generated user lists, was signed off by an independent reviewer, AND flagged access was removed within 30 days

### AC-06 — Least privilege and role-based access
- TSC: CC6.1, CC6.3 | Category: Security
- Applies when: always
- Implement: role definitions per system; production write access limited to an on-call/admin group; IAM policies without wildcard admin for workloads; just-in-time elevation for sensitive actions
- Scan signals: iac, cloud
- Frequency: Quarterly
- Owner: Platform/DevOps lead
- Type 1 test: role matrix exists and production admin membership is restricted to named roles
- Type 2 test: sample production admin accounts across the period and confirm membership matches role justification
- Evidence: role matrix, admin group membership exports, IAM policy documents
- Type 1 pass: PASS if a role matrix exists AND every production admin has a role-based justification AND no workload role grants unrestricted admin without approval
- Type 2 pass: PASS only if sampled production admin membership across the period matched documented justification

### AC-07 — Privileged and break-glass account controls
- TSC: CC6.1, CC6.3 | Category: Security
- Applies when: root/owner accounts or emergency accounts exist (cloud root, IdP super-admin, database superuser)
- Implement: root credentials vaulted with hardware MFA; break-glass use triggers an alert and a post-use review; privileged sessions logged
- Scan signals: logging.cloud_audit_trail, monitoring.alerts
- Frequency: Per event
- Owner: Security owner
- Type 1 test: privileged accounts inventoried, MFA-protected, and alerting configured on use
- Type 2 test: inspect all root/break-glass usage events in the period; confirm each has a ticket and review
- Evidence: privileged account inventory, alert rule, usage log and review tickets
- Type 1 pass: PASS if privileged accounts are inventoried, root has MFA, AND alerting on privileged/break-glass use is configured
- Type 2 pass: PASS only if every privileged/break-glass use in the period was alerted and reviewed AND root kept MFA throughout

### AC-08 — Password and authentication standards
- TSC: CC6.1 | Category: Security
- Applies when: any system that cannot use SSO, and the IdP itself
- Implement: baseline per NIST SP 800-63B-4: minimum 15 characters where a password is the only authenticator (minimum 8 when paired with MFA; 12 is a reasonable internal baseline), allow at least 64 characters, no composition rules, no periodic forced rotation (change only on evidence of compromise), screen against a blocklist of breached and common passwords, allow password managers and paste; lockout or throttling after repeated failures; password manager for shared credentials (1Password/Bitwarden)
- Scan signals: auth.idp
- Frequency: Continuous/automated
- Owner: IT admin
- Type 1 test: password standard documented and configured in IdP and non-SSO systems
- Type 2 test: configuration unchanged or changes approved during the period
- Evidence: password policy, IdP and system configuration screenshots
- Type 1 pass: PASS if configured settings meet the documented standard on every in-scope system on the report date
- Type 2 pass: PASS only if settings stayed compliant through the period (changes approved through change management)

### AC-09 — Encryption at rest
- TSC: CC6.1, C1.1 | Category: Security, Confidentiality
- Applies when: any datastore holding customer data (databases, object storage, volumes, backups)
- Implement: AES-256 encryption at rest for databases, object storage, volumes, and backups (RDS, S3, EBS or equivalents); provider-managed keys (for example SSE-S3 or default RDS/EBS keys) satisfy the control, customer-managed KMS keys (AWS KMS/Cloud KMS/Azure Key Vault) are recommended for sensitive data because they add key-policy control and key-use logging; default encryption enforced by IaC or organization policy
- Scan signals: encryption.kms, encryption.at_rest_hint
- Frequency: Continuous/automated
- Owner: Platform/DevOps lead
- Type 1 test: every in-scope datastore shows encryption enabled on the report date
- Type 2 test: new datastores created during the period are encrypted (inspect config rules or IaC changes)
- Evidence: datastore encryption configuration exports (for example aws s3api get-bucket-encryption, RDS StorageEncrypted), KMS key list where customer-managed keys are used, AWS Config/equivalent rule results
- Type 1 pass: PASS if 100% of in-scope datastores and backups are encrypted at rest on the report date (provider-managed keys such as SSE-S3 or default RDS keys satisfy this)
- Type 2 pass: PASS only if every datastore created or changed in the period was encrypted (config rules or IaC history) AND none was unencrypted at any point

### AC-10 — Encryption in transit
- TSC: CC6.1, CC6.7 | Category: Security
- Applies when: any network transmission of customer data, including internal service-to-service traffic crossing untrusted networks
- Implement: TLS 1.2 minimum on all public endpoints with TLS 1.3 enabled where supported, HSTS, HTTP redirected to HTTPS, managed certificates (ACM/Let's Encrypt) with expiry monitoring; database connections require TLS
- Scan signals: encryption.tls
- Frequency: Continuous/automated
- Owner: Platform/DevOps lead
- Type 1 test: external endpoints accept only TLS 1.2+ (SSL Labs or equivalent scan) and DB connections enforce TLS
- Type 2 test: certificate renewals and TLS configuration remained compliant through the period
- Evidence: TLS scan results, load-balancer listener configuration, certificate inventory
- Type 1 pass: PASS if no in-scope endpoint accepts plaintext or TLS below 1.2 on the report date AND database connections require TLS
- Type 2 pass: PASS only if TLS configuration stayed compliant and no certificate expired on an in-scope endpoint during the period

### AC-11 — Cryptographic key management
- TSC: CC6.1 | Category: Security
- Applies when: the entity manages encryption keys or signing keys
- Implement: keys held in KMS/HSM, not in code; automatic annual rotation for customer-managed keys; key administration separated from key use; key deletion requires approval
- Scan signals: encryption.kms
- Frequency: Annual
- Owner: Security owner
- Type 1 test: key management procedure exists; rotation enabled on KMS keys
- Type 2 test: rotation occurred as scheduled; key policy changes in the period were approved
- Evidence: KMS rotation status, key policies, key management procedure
- Type 1 pass: PASS if every customer-managed key has rotation enabled or a documented exception AND no keys are stored in source code
- Type 2 pass: PASS only if rotation occurred as scheduled AND key policy changes in the period were approved

### AC-12 — Network segmentation and least-access firewall rules
- TSC: CC6.1, CC6.6 | Category: Security
- Applies when: always for cloud or on-prem networks
- Implement: production in a separate VPC/account from non-production; databases in private subnets; security groups deny by default; no 0.0.0.0/0 on admin ports (22, 3389, DB ports)
- Scan signals: iac, cloud
- Frequency: Per event
- Owner: Platform/DevOps lead
- Type 1 test: network diagram matches configuration; no public admin ports on the report date
- Type 2 test: sample firewall/security group changes in the period; confirm approval and compliance with standard
- Evidence: network diagram, security group exports, change tickets
- Type 1 pass: PASS if no in-scope resource exposes admin or database ports to the internet AND prod is isolated from non-prod on the report date
- Type 2 pass: PASS only if every sampled firewall/security-group change in the period was approved and compliant AND no public admin port appeared

### AC-13 — Physical security via certified data centers and office controls
- TSC: CC6.4 | Category: Security
- Applies when: always; for cloud-only companies the data-center portion is carved out to the cloud provider (subservice organization)
- Implement: production hosted with a provider holding a current SOC 2 report covering physical security; offices use badge access and visitor logs if they store sensitive assets
- Scan signals: cloud
- Frequency: Annual
- Owner: Security owner
- Type 1 test: subservice provider's SOC 2 report is current and physical controls are identified as carved out; office controls exist where applicable
- Type 2 test: provider reports cover the period (a bridge letter from the provider's management covers any gap, typically 3 months or less, and is unaudited); office badge reviews performed
- Evidence: cloud provider SOC 2 report and bridge letter, office badge access list and reviews
- Type 1 pass: PASS if the cloud provider's current SOC 2 report is on file with physical controls identified as carved out AND office controls exist where sensitive assets are stored
- Type 2 pass: PASS only if the provider's reports (plus a bridge letter for any gap) cover the period with no relevant qualified opinion AND office badge reviews were performed where applicable

### AC-14 — Secure disposal of hardware and media
- TSC: CC6.5, C1.2 | Category: Security, Confidentiality
- Applies when: the entity retires laptops, drives, or other media that held company or customer data
- Implement: encrypted endpoints wiped (crypto-erase) before reuse; certified disposal vendor issues certificates of destruction; cloud media disposal relies on provider's SOC 2
- Scan signals: none
- Frequency: Per event
- Owner: IT admin
- Type 1 test: disposal procedure exists
- Type 2 test: sample disposed assets in the period from the asset inventory; confirm wipe or destruction certificate
- Evidence: disposal procedure, asset inventory with disposal status, certificates of destruction
- Type 1 pass: PASS if a disposal procedure exists covering wipe or certified destruction
- Type 2 pass: PASS only if every sampled asset retired in the period has a wipe record or destruction certificate

### AC-15 — Endpoint management and disk encryption
- TSC: CC6.7, CC6.8 | Category: Security
- Applies when: workforce laptops or desktops access production or customer data
- Implement: MDM (Jamf/Iru (formerly Kandji)/Intune) enforcing full-disk encryption, screen lock ≤ 15 minutes, OS auto-update, firewall; removable media restricted
- Scan signals: none
- Frequency: Continuous/automated
- Owner: IT admin
- Type 1 test: MDM policy enforces settings; device inventory matches headcount
- Type 2 test: sample devices across the period; confirm compliance status and encryption
- Evidence: MDM compliance report, device inventory, policy profiles
- Type 1 pass: PASS if the MDM policy enforces the settings AND the device inventory matches headcount AND devices show encryption on
- Type 2 pass: PASS only if every sampled in-scope device across the period was MDM-enrolled with disk encryption on

### AC-16 — Anti-malware / EDR on endpoints and servers
- TSC: CC6.8 | Category: Security
- Applies when: endpoints or servers that run general-purpose operating systems are in scope (immutable containers may rely on image scanning instead)
- Implement: EDR (CrowdStrike/SentinelOne/Microsoft Defender) with automatic signature updates and alerting to security; container images scanned before deploy
- Scan signals: none
- Frequency: Continuous/automated
- Owner: IT admin
- Type 1 test: EDR deployed and alerting configured on the report date
- Type 2 test: sample devices for agent presence and update status; inspect alerts in the period for triage
- Evidence: EDR console coverage report, alert triage tickets, image-scan logs
- Type 1 pass: PASS if EDR is deployed on >= 98% of in-scope devices AND alerting is configured on the report date
- Type 2 pass: PASS only if sampled devices had a current agent through the period AND every high alert in the period was triaged

### AC-17 — Secrets management and no hardcoded credentials
- TSC: CC6.1 | Category: Security
- Applies when: applications use API keys, database passwords, tokens, or certificates
- Implement: secrets stored in a manager (AWS Secrets Manager/Vault/Doppler); secret scanning (GitHub secret scanning/gitleaks/trufflehog) in CI and push protection; leaked secrets rotated immediately; service-account keys inventoried and rotated
- Scan signals: secrets.scanning, secrets.hardcoded_hits, auth.ci_oidc
- Frequency: Continuous/automated
- Owner: Engineering lead
- Type 1 test: secret manager in use, scanning enabled, and no live secrets in the repository on the report date
- Type 2 test: inspect secret-scanning alerts in the period; confirm each was rotated and closed
- Evidence: secret manager inventory, scanning configuration, alert history with rotation tickets
- Type 1 pass: PASS if a secret manager is in use AND secret scanning runs on every push AND secrets.hardcoded_hits is 0 (or every hit is confirmed revoked) on the report date
- Type 2 pass: PASS only if every secret-scanning alert in the period was rotated and closed AND scanning stayed enabled throughout

### AC-18 — External boundary protection
- TSC: CC6.6 | Category: Security
- Applies when: services are exposed to the internet
- Implement: WAF and DDoS protection (Cloudflare/AWS WAF + Shield), rate limiting, remote admin only through VPN or zero-trust proxy (Tailscale/Cloudflare Access/SSM Session Manager) with SSO and MFA
- Scan signals: iac, cloud
- Frequency: Continuous/automated
- Owner: Platform/DevOps lead
- Type 1 test: boundary controls configured on public endpoints; admin access path requires SSO/MFA
- Type 2 test: rule changes in the period approved; blocked-event logs show the control operated
- Evidence: WAF configuration, VPN/zero-trust access policy, change tickets
- Type 1 pass: PASS if every public endpoint sits behind boundary protection AND no direct internet admin access exists
- Type 2 pass: PASS only if rule changes in the period were approved AND blocked-event logs show the control operated through the period

## Security — System Operations (CC7)

### OPS-01 — Vulnerability scanning and patch SLAs
- TSC: CC7.1 | Category: Security
- Applies when: always
- Implement: authenticated infrastructure and container scanning at least monthly (Inspector/Wiz/Qualys/Trivy); remediation SLAs are the entity's own choice and the auditor tests against them (common practice: critical 15 days, high 30 days, medium 90 days; for CVEs on the CISA KEV list or actively exploited, 7 days or the KEV due date, whichever is sooner); OS patching automated
- Scan signals: ci, deps.sast
- Frequency: Monthly
- Owner: Security owner
- Type 1 test: scanning configured across in-scope assets and SLA policy documented
- Type 2 test: sample monthly scans; trace critical/high findings to remediation within SLA
- Evidence: scan schedules and reports, remediation tickets, SLA policy, exception approvals
- Type 1 pass: PASS if scanning is configured across in-scope assets AND the SLA policy is documented
- Type 2 pass: PASS only if scans ran at the stated cadence AND no critical/high finding exceeded its SLA without an approved exception

### OPS-02 — Dependency vulnerability management
- TSC: CC7.1 | Category: Security
- Applies when: the application uses third-party packages
- Implement: Dependabot or Renovate enabled on all production repositories; SCA results reviewed; critical dependency CVEs patched within the OPS-01 SLA
- Scan signals: deps.dependabot_or_renovate
- Frequency: Continuous/automated
- Owner: Engineering lead
- Type 1 test: automated dependency updates enabled on in-scope repositories
- Type 2 test: sample critical/high dependency alerts in the period; confirm fix or exception within SLA
- Evidence: Dependabot/Renovate configuration, alert history, merged update PRs
- Type 1 pass: PASS if every production repository has automated dependency alerts enabled
- Type 2 pass: PASS only if no sampled critical/high dependency alert in the period stayed open past SLA without an approved exception

### OPS-03 — Static application security testing in CI
- TSC: CC7.1, CC8.1 | Category: Security
- Applies when: the entity develops software that runs in production
- Implement: SAST (CodeQL/Semgrep/SonarQube) runs on every pull request; high-severity findings block merge or require documented triage
- Scan signals: deps.sast, ci
- Frequency: Per event
- Owner: Engineering lead
- Type 1 test: SAST job is configured and required in CI
- Type 2 test: sample merged PRs; confirm SAST ran and high findings were resolved or triaged
- Evidence: CI configuration, SAST results per PR, triage records
- Type 1 pass: PASS if a SAST job is configured and required in CI on the report date
- Type 2 pass: PASS only if SAST ran on every sampled merged PR AND no high finding merged without triage

### OPS-04 — Configuration drift and misconfiguration detection
- TSC: CC7.1 | Category: Security
- Applies when: cloud infrastructure is in scope
- Implement: CSPM or config rules (AWS Config/AWS Security Hub CSPM/GCP Security Command Center/Microsoft Defender for Cloud/Wiz) alerting on public buckets, unencrypted storage, open security groups, disabled logging
- Scan signals: cloud, monitoring.alerts
- Frequency: Continuous/automated
- Owner: Platform/DevOps lead
- Type 1 test: detection rules enabled on all in-scope accounts with alert routing
- Type 2 test: sample findings in the period; confirm triage and remediation
- Evidence: rule set, finding history, remediation tickets
- Type 1 pass: PASS if detection rules are enabled on all production accounts with alert routing
- Type 2 pass: PASS only if sampled high findings in the period were remediated or accepted AND coverage stayed on all production accounts

### OPS-05 — Centralized logging of security-relevant events
- TSC: CC7.2 | Category: Security
- Applies when: always
- Implement: application, IdP, cloud control-plane, database, and network logs shipped to a central store (Datadog/Splunk/ELK/CloudWatch/Panther) with restricted delete access
- Scan signals: logging.centralized
- Frequency: Continuous/automated
- Owner: Platform/DevOps lead
- Type 1 test: in-scope log sources are flowing to the central store on the report date
- Type 2 test: sample dates across the period and confirm logs exist for each source (no gaps)
- Evidence: log source inventory, sample log queries by date, access policy on log store
- Type 1 pass: PASS if every in-scope log source is flowing to the central store on the report date
- Type 2 pass: PASS only if sampled dates across the period show logs for each source with no unexplained gaps

### OPS-06 — Cloud audit trail enabled and protected
- TSC: CC7.2 | Category: Security
- Applies when: cloud infrastructure is in scope
- Implement: AWS CloudTrail (all regions, organization trail, log file validation), GCP Cloud Audit Logs with an aggregated log sink, or Azure Activity Log exported through diagnostic settings, delivered to a locked bucket or workspace in a separate account or project
- Scan signals: logging.cloud_audit_trail
- Frequency: Continuous/automated
- Owner: Platform/DevOps lead
- Type 1 test: audit trail enabled across all accounts and regions with integrity validation
- Type 2 test: confirm trail remained enabled throughout the period (no StopLogging events, or alerted and reviewed)
- Evidence: trail configuration, bucket policy, log-validation output, event history search
- Type 1 pass: PASS if the audit trail is enabled across all accounts and regions with integrity validation and a protected destination on the report date
- Type 2 pass: PASS only if audit logging covered all accounts/regions for the whole period (no unalerted StopLogging or equivalent events)

### OPS-07 — Log retention of at least one year
- TSC: CC7.2 | Category: Security
- Applies when: always
- Implement: security logs retained ≥ 365 days as the floor (400 days recommended so logs from the first day of a 12-month period survive until fieldwork; 400 is also a valid CloudWatch Logs value), 90 days hot and the remainder archived, immutable where feasible (S3 Object Lock or equivalent)
- Scan signals: logging.retention_days
- Frequency: Continuous/automated
- Owner: Platform/DevOps lead
- Type 1 test: retention setting configured at ≥ 365 days
- Type 2 test: retrieve logs from the start of the observation period to prove retention
- Evidence: retention configuration, query returning logs from the earliest period date
- Type 1 pass: PASS if logging.retention_days >= 365 on every security log store (or a longer contractual requirement is met)
- Type 2 pass: PASS only if logs from the first day of the period are retrievable at fieldwork AND retention was not shortened during the period

### OPS-08 — Security monitoring and alerting
- TSC: CC7.2, CC7.3 | Category: Security
- Applies when: always
- Implement: alerts for root login, IAM policy changes, disabled logging, impossible travel, mass data download, and threat detection findings (GuardDuty/Microsoft Defender for Cloud/Security Command Center) routed to on-call (PagerDuty/Jira Service Management; Opsgenie reaches end of support on 2027-04-05)
- Scan signals: monitoring.alerts, logging.centralized
- Frequency: Continuous/automated
- Owner: Security owner
- Type 1 test: alert rules exist for defined events and route to an on-call rotation
- Type 2 test: sample alerts in the period; confirm acknowledgement and triage within defined time
- Evidence: alert rule list, on-call schedule, alert history with triage notes
- Type 1 pass: PASS if alert rules exist for the defined events AND route to an on-call rotation
- Type 2 pass: PASS only if alert rules stayed active AND every sampled alert in the period was triaged with a documented outcome within the defined time

### OPS-09 — Security event triage and incident classification
- TSC: CC7.3 | Category: Security
- Applies when: always
- Implement: documented severity matrix (SEV1–SEV4) and criteria for declaring a security incident; triaged events recorded in a ticket system
- Scan signals: incident.runbook
- Frequency: Per event
- Owner: Security owner
- Type 1 test: classification criteria documented and a ticket workflow exists
- Type 2 test: sample security events in the period; confirm classification and escalation followed the matrix
- Evidence: severity matrix, event/incident tickets
- Type 1 pass: PASS if classification criteria are documented AND a ticket workflow exists
- Type 2 pass: PASS only if every sampled event in the period has a recorded classification consistent with the matrix

### OPS-10 — Incident response plan
- TSC: CC7.4 | Category: Security
- Applies when: always
- Implement: IR plan with roles (incident commander, comms, scribe), containment/eradication/recovery steps, evidence preservation, legal and customer notification paths; reviewed annually
- Scan signals: incident.runbook
- Frequency: Annual
- Owner: Security owner
- Type 1 test: plan exists, approved within 12 months, names responders and contact methods
- Type 2 test: sample incidents in the period; confirm the plan was followed (timeline, roles, communications)
- Evidence: IR plan, incident tickets and timelines, communication records
- Type 1 pass: PASS if the plan is approved within 12 months AND names responders and contact methods
- Type 2 pass: PASS only if the plan was reviewed within the period AND every sampled incident followed it (no incidents: not tested, keep the empty incident population as evidence)

### OPS-11 — Incident response tabletop exercise
- TSC: CC7.4, CC7.5 | Category: Security
- Applies when: always
- Implement: at least annual tabletop exercise with realistic scenario (ransomware, credential leak), attendance record, and action items tracked
- Scan signals: none
- Frequency: Annual
- Owner: Security owner
- Type 1 test: exercise plan exists or a recent exercise report is available
- Type 2 test: exercise held within the period; action items tracked to closure
- Evidence: exercise report, attendee list, action items
- Type 1 pass: PASS if an exercise plan or an exercise report dated within 12 months exists
- Type 2 pass: PASS only if an exercise was held within the period AND its action items are tracked to closure

### OPS-12 — Post-incident review and recovery
- TSC: CC7.5 | Category: Security
- Applies when: any security or availability incident occurs
- Implement: blameless postmortem within 10 business days for SEV1/SEV2 including root cause, recovery validation, and corrective actions entered in the deficiency log
- Scan signals: incident.runbook
- Frequency: Per event
- Owner: Engineering lead
- Type 1 test: postmortem template and requirement documented
- Type 2 test: inspect every SEV1/SEV2 incident in the period for a completed postmortem and tracked actions
- Evidence: postmortem documents, corrective action tickets
- Type 1 pass: PASS if the postmortem template and the 10-business-day requirement are documented
- Type 2 pass: PASS only if every SEV1/SEV2 incident in the period has a postmortem within 10 business days AND corrective actions are tracked

### OPS-13 — Incident notification to customers and authorities
- TSC: CC7.4, CC2.3 | Category: Security
- Applies when: customer contracts or laws require notification of security incidents
- Implement: notification matrix listing contractual and regulatory deadlines (e.g. GDPR 72 hours to regulator), approved templates, legal review step
- Scan signals: none
- Frequency: Per event
- Owner: Legal
- Type 1 test: matrix and templates exist and match contract terms
- Type 2 test: for incidents requiring notice in the period, confirm notices were sent within deadlines
- Evidence: notification matrix, templates, sent notices with timestamps
- Type 1 pass: PASS if the notification matrix and templates exist and match contract and legal terms
- Type 2 pass: PASS only if every notifiable incident in the period was notified within the contractual or legal deadline

### OPS-14 — On-call coverage for production
- TSC: CC7.2, CC7.4 | Category: Security
- Applies when: the system has availability or security commitments outside business hours
- Implement: 24×7 on-call rotation with escalation policy and paging (PagerDuty/Jira Service Management/incident.io; Opsgenie reaches end of support on 2027-04-05); acknowledgement SLA for critical pages
- Scan signals: monitoring.alerts
- Frequency: Weekly
- Owner: Engineering lead
- Type 1 test: rotation and escalation policy configured with no coverage gaps
- Type 2 test: sample weeks in the period; confirm continuous coverage and acknowledgement of critical pages within SLA
- Evidence: on-call schedule export, escalation policy, page acknowledgement report
- Type 1 pass: PASS if the rotation and escalation policy are configured with no coverage gaps
- Type 2 pass: PASS only if no sampled week had an uncovered shift AND critical pages met the acknowledgement SLA

## Security — Change Management (CC8)

### CHG-01 — Change management policy
- TSC: CC8.1 | Category: Security
- Applies when: always
- Implement: policy covering standard, normal, and emergency changes to code, infrastructure, configuration, and data; required approval, testing, and documentation for each type
- Scan signals: policies
- Frequency: Annual
- Owner: Engineering lead
- Type 1 test: policy approved and defines change types and approvals
- Type 2 test: policy reviewed in the period; changes sampled under CHG-02 follow it
- Evidence: approved policy with version history
- Type 1 pass: PASS if the policy is approved within 12 months AND covers code, infrastructure, configuration, data, and emergency changes
- Type 2 pass: PASS only if the policy was reviewed within the period AND changes sampled under CHG-02 followed it

### CHG-02 — Peer review enforced by branch protection or rulesets
- TSC: CC8.1, CC5.1 | Category: Security
- Applies when: any code or IaC deployed to production
- Implement: protected default branch via branch protection or a repository/organization ruleset requiring at least one approving review from someone other than the author, dismissal of stale approvals, no force pushes, and an empty bypass list (administrators included); production deploys reconciled to merged PRs; out-of-band console or CLI changes detected from cloud audit logs (CloudTrail/Cloud Audit Logs/Activity Log) and CD logs
- Scan signals: change_mgmt.branch_protection
- Frequency: Per event
- Owner: Engineering lead
- Type 1 test: branch protection or ruleset settings on production repositories on the report date; deploy pipeline is the only route to production
- Type 2 test: sample merged PRs (per-event row: about 25, or more for high volume); confirm non-author approval before merge; reconcile a sample of production deploys from CD logs to approved PRs; review the protection/ruleset change audit log and cloud audit logs for console changes to production outside the pipeline
- Evidence: branch protection and ruleset exports, sampled PR records, deploy log reconciled to PRs, organization audit log, cloud audit-log query for non-pipeline production changes
- Type 1 pass: PASS if branch protection or a ruleset on every production repository requires non-author approval with no bypass on the report date
- Type 2 pass: PASS only if every sampled production change had non-author approval before merge AND every sampled production deploy reconciles to an approved PR AND protection was never disabled and no out-of-band console change occurred without a recorded emergency change

### CHG-03 — Code ownership for sensitive paths
- TSC: CC8.1 | Category: Security
- Applies when: repositories contain security-sensitive code (auth, IaC, CI configuration)
- Implement: CODEOWNERS file requiring review from designated owners for sensitive directories, with "require review from code owners" enabled
- Scan signals: change_mgmt.codeowners
- Frequency: Per event
- Owner: Engineering lead
- Type 1 test: CODEOWNERS exists and code-owner review is required
- Type 2 test: sample changes to sensitive paths; confirm code-owner approval
- Evidence: CODEOWNERS file, branch protection setting, sampled PRs
- Type 1 pass: PASS if CODEOWNERS covers the sensitive paths AND code-owner review is required
- Type 2 pass: PASS only if every sampled change to a sensitive path in the period had code-owner approval

### CHG-04 — Automated tests and CI checks before merge
- TSC: CC8.1 | Category: Security
- Applies when: any code deployed to production
- Implement: CI (GitHub Actions/GitLab CI/CircleCI) runs unit/integration tests and security checks; status checks required to pass before merge
- Scan signals: ci, change_mgmt.branch_protection
- Frequency: Per event
- Owner: Engineering lead
- Type 1 test: CI pipeline exists and required status checks are configured
- Type 2 test: sample merged PRs; confirm checks passed before merge
- Evidence: CI configuration, required-check settings, sampled PR check results
- Type 1 pass: PASS if a CI pipeline exists AND required status checks are configured on production repositories
- Type 2 pass: PASS only if no sampled PR in the period merged with failing or skipped required checks

### CHG-05 — Change documentation and traceability
- TSC: CC8.1 | Category: Security
- Applies when: always
- Implement: PR template capturing description, risk, testing performed, and linked ticket; release notes for customer-impacting changes
- Scan signals: change_mgmt.pr_template
- Frequency: Per event
- Owner: Engineering lead
- Type 1 test: PR template or change record format exists
- Type 2 test: sample changes; confirm description, testing evidence, and ticket link are present
- Evidence: PR template, sampled PRs with linked tickets
- Type 1 pass: PASS if a PR template or change record format exists capturing purpose, risk, testing, and ticket
- Type 2 pass: PASS only if every sampled change documents purpose and testing

### CHG-06 — Separate environments and deployment only via pipeline
- TSC: CC8.1, CC5.2 | Category: Security
- Applies when: always
- Implement: dev/staging/prod separated (accounts or projects); production deploys only via CI/CD with restricted deploy credentials; no direct developer write access to prod infrastructure
- Scan signals: ci, iac
- Frequency: Continuous/automated
- Owner: Platform/DevOps lead
- Type 1 test: environments are separated and deploy permissions restricted to the pipeline
- Type 2 test: compare production deploy log to merged changes; investigate any deploy without a matching approved change
- Evidence: environment diagram, deploy role policy, deploy log reconciled to PRs
- Type 1 pass: PASS if environments are separated AND production deploy permissions are restricted to the pipeline
- Type 2 pass: PASS only if every sampled production deploy traces to an approved change AND no manual production change occurred outside the emergency process

### CHG-07 — Emergency change procedure
- TSC: CC8.1 | Category: Security
- Applies when: hotfixes or break-glass changes bypass normal review
- Implement: emergency changes allowed only with incident reference; retroactive review and approval within 2 business days
- Scan signals: none
- Frequency: Per event
- Owner: Engineering lead
- Type 1 test: emergency procedure documented including retroactive approval
- Type 2 test: identify all emergency changes in the period; confirm retroactive review within the window
- Evidence: emergency change log, retroactive approvals
- Type 1 pass: PASS if the emergency procedure is documented including retroactive approval within 2 business days
- Type 2 pass: PASS only if every emergency change in the period has retroactive approval within the defined window

## Security — Vendor Management (CC9.2)

### VND-01 — Vendor inventory with risk tiering
- TSC: CC9.2 | Category: Security
- Applies when: always
- Implement: inventory of vendors and subprocessors listing service, data accessed, criticality tier, contract owner, and review date
- Scan signals: vendors.list_present
- Frequency: Annual
- Owner: Compliance owner
- Type 1 test: inventory exists and is complete compared to accounts payable and SSO app list
- Type 2 test: new vendors added in the period appear in the inventory with a tier
- Evidence: vendor inventory, AP vendor list, IdP app list reconciliation
- Type 1 pass: PASS if every vendor with access to customer data appears in the inventory with a risk tier (reconciled to AP and the SSO app list)
- Type 2 pass: PASS only if every vendor added in the period appears in the inventory with a tier AND the inventory was reviewed within the period

### VND-02 — Vendor due diligence before onboarding
- TSC: CC9.2 | Category: Security
- Applies when: onboarding a vendor that will access customer data or support production
- Implement: security review (SOC 2 report or questionnaire) and approval by security before contract signature for high/medium-tier vendors
- Scan signals: none
- Frequency: Per event
- Owner: Security owner
- Type 1 test: due diligence procedure exists with tier-based requirements
- Type 2 test: sample vendors onboarded in the period; confirm review completed before contract or access
- Evidence: procedure, review records, contract signature dates
- Type 1 pass: PASS if a tier-based due diligence procedure exists
- Type 2 pass: PASS only if every sampled high/medium vendor onboarded in the period was reviewed before contract or access

### VND-03 — Annual vendor review including SOC reports and CUECs
- TSC: CC9.2 | Category: Security
- Applies when: high-tier vendors or subservice organizations exist (cloud provider, IdP, payment processor)
- Implement: annual review of each critical vendor's SOC 2/ISO report, exceptions, and complementary user entity controls (CUECs), with CUECs mapped to internal controls
- Scan signals: vendors.list_present
- Frequency: Annual
- Owner: Security owner
- Type 1 test: latest reports collected and CUEC mapping exists
- Type 2 test: for each critical vendor, confirm a review in the period that checked: the report period overlaps the user's period (a bridge letter covers any gap; bridge letters are signed by the vendor's management, are not audited, and typically cover 3 months or less), the opinion is unqualified, exceptions and their relevance, carve-outs of the vendor's own subservice organizations, and CUECs mapped to internal controls
- Evidence: vendor SOC reports, review memos, CUEC mapping
- Type 1 pass: PASS if the latest SOC reports for critical vendors are on file AND each vendor CUEC maps to an internal control
- Type 2 pass: PASS only if every critical vendor was reviewed within the period (report period overlap, opinion, exceptions, carve-outs, bridge letter for gaps) AND each CUEC maps to an operating internal control

### VND-04 — Contracts with security and confidentiality terms
- TSC: CC9.2, C1.1 | Category: Security, Confidentiality
- Applies when: vendors process or access confidential data
- Implement: contracts/DPAs include confidentiality, security requirements, breach notification, right to audit, subprocessor approval, and return/deletion at termination
- Scan signals: none
- Frequency: Per event
- Owner: Legal
- Type 1 test: template terms exist and are in critical vendor contracts
- Type 2 test: sample vendors onboarded or renewed in the period; confirm terms present
- Evidence: contract template, executed contracts/DPAs
- Type 1 pass: PASS if template terms exist AND are present in critical vendor contracts
- Type 2 pass: PASS only if every sampled data-processing vendor contract signed or renewed in the period contains confidentiality and breach-notification terms

### VND-05 — Vendor offboarding
- TSC: CC9.2 | Category: Security
- Applies when: a vendor relationship ends
- Implement: offboarding checklist revoking vendor access and API keys and obtaining data return or deletion confirmation
- Scan signals: none
- Frequency: Per event
- Owner: Security owner
- Type 1 test: offboarding procedure exists
- Type 2 test: sample terminated vendors; confirm access revoked and deletion confirmed
- Evidence: offboarding checklist, revocation records, deletion certificates
- Type 1 pass: PASS if an offboarding procedure exists covering access revocation and data return or deletion
- Type 2 pass: PASS only if every sampled vendor terminated in the period has access revocation AND a data deletion or return confirmation

## Availability (A1)

### AV-01 — Capacity monitoring and forecasting
- TSC: A1.1 | Category: Availability
- Applies when: Availability is in scope
- Implement: dashboards and alerts on CPU, memory, storage, DB connections, and queue depth with thresholds (e.g. 80%); autoscaling; quarterly capacity review
- Scan signals: monitoring.alerts
- Frequency: Quarterly
- Owner: Platform/DevOps lead
- Type 1 test: capacity alerts configured and autoscaling or headroom documented
- Type 2 test: sample quarterly capacity reviews; inspect capacity alerts in the period and their resolution
- Evidence: dashboard screenshots, alert rules, capacity review notes
- Type 1 pass: PASS if capacity alerts exist for every critical resource AND autoscaling or headroom is documented
- Type 2 pass: PASS only if the quarterly capacity reviews in the period occurred AND sampled capacity alerts were resolved

### AV-02 — Redundant infrastructure across failure domains
- TSC: A1.2 | Category: Availability
- Applies when: Availability is in scope
- Implement: multi-AZ databases and load-balanced stateless services across ≥ 2 availability zones; infrastructure defined in IaC for rebuild
- Scan signals: iac, cloud
- Frequency: Continuous/automated
- Owner: Platform/DevOps lead
- Type 1 test: production components deployed across multiple availability zones on the report date
- Type 2 test: configuration remained redundant throughout the period (config history)
- Evidence: architecture diagram, multi-AZ configuration exports
- Type 1 pass: PASS if every tier needed to meet the SLA spans multiple availability zones (or has a documented accepted risk) on the report date
- Type 2 pass: PASS only if configuration history shows redundancy stayed in place through the period

### AV-03 — Automated backups
- TSC: A1.2, PI1.5 | Category: Availability, Processing Integrity
- Applies when: the system stores customer data
- Implement: automated daily backups (point-in-time recovery where available), encrypted, retained per policy (e.g. 35 days), copied to a separate account or region
- Scan signals: backups.configured, encryption.kms
- Frequency: Daily
- Owner: Platform/DevOps lead
- Type 1 test: backup jobs configured for every production datastore
- Type 2 test: sample days per frequency table (20–40); confirm successful backup and investigate failures
- Evidence: backup configuration, job success history, failure tickets
- Type 1 pass: PASS if backup jobs are configured, encrypted, and retained per policy for every production datastore
- Type 2 pass: PASS only if sampled days in the period show successful backups or remediated failures

### AV-04 — Backup restore testing
- TSC: A1.3 | Category: Availability
- Applies when: backups exist for in-scope data
- Implement: restore test at least annually (quarterly recommended) to an isolated environment with data integrity verification and measured restore time vs RTO
- Scan signals: backups.restore_test
- Frequency: Quarterly
- Owner: Platform/DevOps lead
- Type 1 test: restore test procedure exists and a recent test record exists
- Type 2 test: restore tests performed at the stated cadence within the period
- Evidence: restore test reports with date, data set, duration, verification result
- Type 1 pass: PASS if a restore test procedure exists AND a successful restore test record exists with measured restore time
- Type 2 pass: PASS only if restore tests ran at the stated cadence within the period AND measured restore time met RTO

### AV-05 — Disaster recovery plan and test
- TSC: A1.2, A1.3 | Category: Availability
- Applies when: Availability is in scope
- Implement: DR plan for loss of a region or critical vendor with runbooks, RTO/RPO, roles; annual DR test (failover or simulation) with lessons learned
- Scan signals: incident.runbook, backups.configured
- Frequency: Annual
- Owner: Engineering lead
- Type 1 test: DR plan approved and consistent with BCP RTO/RPO
- Type 2 test: DR test executed within the period; results and remediation documented
- Evidence: DR plan, DR test report, remediation items
- Type 1 pass: PASS if the DR plan is approved AND consistent with BCP RTO/RPO
- Type 2 pass: PASS only if a DR test was executed within the period AND results met RTO/RPO or gaps are tracked

### AV-06 — Environmental protections via hosting provider
- TSC: A1.2 | Category: Availability
- Applies when: Availability is in scope and infrastructure is hosted by a third party
- Implement: rely on cloud/colo provider controls for power, cooling, fire suppression; obtain and review provider SOC 2 covering A1.2
- Scan signals: cloud
- Frequency: Annual
- Owner: Security owner
- Type 1 test: provider report obtained; environmental controls identified as carved out
- Type 2 test: provider reports cover the period, or a bridge letter (signed by the provider's management, unaudited, typically 3 months or less) covers the gap
- Evidence: provider SOC 2 report, review memo
- Type 1 pass: PASS if a current provider report covering environmental protections has been obtained and reviewed
- Type 2 pass: PASS only if the provider's reports (plus a bridge letter for any gap) cover the period AND were reviewed

## Processing Integrity (PI1)

### PI-01 — Processing specifications documented and communicated
- TSC: PI1.1 | Category: Processing Integrity
- Applies when: Processing Integrity is in scope (e.g. payments, payroll, data pipelines, calculations customers rely on)
- Implement: documented data definitions, processing rules, and output specifications; customer-facing API docs and changelogs
- Scan signals: none
- Frequency: Per event
- Owner: Engineering lead
- Type 1 test: specifications exist for in-scope processing and are available to users
- Type 2 test: specification updates in the period were communicated to customers
- Evidence: specification documents, API docs, changelog entries
- Type 1 pass: PASS if each in-scope process has documented inputs, processing rules, and outputs available to users
- Type 2 pass: PASS only if every specification change in the period was communicated to customers

### PI-02 — Input validation
- TSC: PI1.2 | Category: Processing Integrity
- Applies when: Processing Integrity is in scope
- Implement: schema validation on API and file inputs (type, range, required fields), rejection with error messages, and logging of rejected inputs
- Scan signals: none
- Frequency: Continuous/automated
- Owner: Engineering lead
- Type 1 test: validation rules implemented on in-scope inputs (code walkthrough or test cases)
- Type 2 test: sample rejected-input logs; confirm invalid data was blocked and errors returned
- Evidence: validation code or schemas, automated test results, rejection logs
- Type 1 pass: PASS if every in-scope input path validates data before processing (code walkthrough or test cases)
- Type 2 pass: PASS only if sampled rejection logs show invalid data was blocked and errors returned AND validation code changes went through change management

### PI-03 — Processing completeness monitoring and reconciliation
- TSC: PI1.3 | Category: Processing Integrity
- Applies when: Processing Integrity is in scope
- Implement: job-level monitoring (record counts in vs out, control totals), alerts on job failure or lag, daily reconciliation for financial or critical data
- Scan signals: monitoring.alerts
- Frequency: Daily
- Owner: Engineering lead
- Type 1 test: reconciliation and failure alerts configured
- Type 2 test: sample days (20–40); confirm reconciliations ran and discrepancies were resolved
- Evidence: reconciliation reports, job alert history, discrepancy tickets
- Type 1 pass: PASS if reconciliations and failure alerts are configured for in-scope processing
- Type 2 pass: PASS only if sampled reconciliations in the period completed AND every discrepancy has a documented resolution

### PI-04 — Output accuracy and controlled distribution
- TSC: PI1.4 | Category: Processing Integrity
- Applies when: Processing Integrity is in scope
- Implement: output validation checks before delivery, delivery only to authenticated recipients, delivery confirmation and timeliness monitoring
- Scan signals: none
- Frequency: Per event
- Owner: Engineering lead
- Type 1 test: output checks and access restrictions configured
- Type 2 test: sample outputs; confirm checks passed and delivery reached intended recipients on time
- Evidence: output check logs, delivery logs, access configuration
- Type 1 pass: PASS if output checks and recipient access restrictions are configured
- Type 2 pass: PASS only if sampled outputs in the period passed validation AND went only to authorized recipients

### PI-05 — Stored data integrity
- TSC: PI1.5 | Category: Processing Integrity
- Applies when: Processing Integrity is in scope
- Implement: database constraints, write-access restrictions, audit trails of data modifications, checksums or versioning on stored files (S3 versioning/Object Lock)
- Scan signals: backups.configured, logging.centralized
- Frequency: Continuous/automated
- Owner: Engineering lead
- Type 1 test: integrity mechanisms configured on in-scope stores
- Type 2 test: sample data-change audit records; confirm modifications were authorized
- Evidence: schema constraints, versioning configuration, data-change audit logs
- Type 1 pass: PASS if integrity mechanisms (constraints, versioning, write restrictions, audit trail) are configured on in-scope stores
- Type 2 pass: PASS only if sampled data-change audit records show modifications were authorized AND logging stayed on through the period

### PI-06 — Duplicate and replay protection (idempotency)
- TSC: PI1.3 | Category: Processing Integrity
- Applies when: Processing Integrity is in scope and inputs can be retried, replayed, or delivered more than once (payments, webhooks, queues, file drops)
- Implement: idempotency keys on write APIs and webhook handlers; unique constraints or dedupe tables on business keys; message-queue deduplication or exactly-once consumers; replay window on signed requests; duplicate attempts logged
- Scan signals: none
- Frequency: Continuous/automated
- Owner: Engineering lead
- Type 1 test: walkthrough or automated test shows a repeated request or message is processed once
- Type 2 test: automated control: test of one plus effective change management over the code for the period; inspect duplicate-detection logs in the period
- Evidence: idempotency design note, unique constraints or dedupe code, automated test results, duplicate-detection log
- Type 1 pass: PASS if every in-scope input path that can be retried rejects or collapses duplicates (shown by test or walkthrough)
- Type 2 pass: PASS only if duplicate-detection logs in the period show duplicates were caught AND changes to the dedupe logic went through change management

### PI-07 — Processing timeliness and completeness SLAs
- TSC: PI1.4 | Category: Processing Integrity
- Applies when: Processing Integrity is in scope and customers rely on outputs by a deadline (settlement files, reports, payouts, data deliveries)
- Implement: documented processing and delivery SLAs per output; monitoring of job completion and delivery time against the SLA; alerts on late or incomplete output; missed SLAs ticketed and communicated to affected customers
- Scan signals: monitoring.alerts
- Frequency: Daily
- Owner: Engineering lead
- Type 1 test: SLAs documented and timeliness alerts configured
- Type 2 test: sample days or delivery runs; compare completion time and record counts to the SLA; inspect every missed-SLA ticket in the period
- Evidence: SLA document, job completion and delivery logs, alert rules, missed-SLA tickets and customer notices
- Type 1 pass: PASS if every in-scope output has a documented SLA AND late or incomplete output raises an alert
- Type 2 pass: PASS only if sampled runs met the SLA or the miss was ticketed, resolved, and communicated

## Confidentiality (C1)

### CF-01 — Data classification policy and labeling
- TSC: C1.1, CC2.1 | Category: Confidentiality, Security
- Applies when: Confidentiality is in scope or the entity holds customer confidential data
- Implement: classification levels (Public, Internal, Confidential, Restricted) with handling rules; data stores tagged with classification
- Scan signals: policies, privacy.pii_fields
- Frequency: Per event
- Owner: Security owner
- Type 1 test: policy exists and in-scope data stores carry classification
- Type 2 test: new data stores in the period were classified
- Evidence: classification policy, data inventory with labels, resource tags
- Type 1 pass: PASS if the policy exists AND every data store holding confidential data is classified with handling rules applied
- Type 2 pass: PASS only if every data store created in the period was classified

### CF-02 — Restricted access to confidential data
- TSC: C1.1, CC6.3 | Category: Confidentiality, Security
- Applies when: Confidentiality is in scope
- Implement: production customer data accessible only to named roles; access logged; support access through audited tooling with customer consent where promised
- Scan signals: logging.centralized
- Frequency: Quarterly
- Owner: Security owner
- Type 1 test: access lists for confidential stores restricted to approved roles
- Type 2 test: sample access logs to confidential data; confirm each accessor was authorized
- Evidence: access control lists, data access logs, support-access tickets
- Type 1 pass: PASS if access to confidential stores is limited to approved roles on the report date
- Type 2 pass: PASS only if every sampled access to confidential data in the period was by an authorized role

### CF-03 — Retention schedule for confidential information
- TSC: C1.1, C1.2 | Category: Confidentiality
- Applies when: Confidentiality is in scope
- Implement: retention schedule per data type aligned with contracts; automated lifecycle rules (S3 lifecycle, DB TTL jobs)
- Scan signals: logging.retention_days
- Frequency: Continuous/automated
- Owner: Engineering lead
- Type 1 test: schedule exists and lifecycle rules are configured
- Type 2 test: sample data sets; confirm data older than retention was purged
- Evidence: retention schedule, lifecycle configuration, purge job logs
- Type 1 pass: PASS if a retention schedule exists AND lifecycle rules match it
- Type 2 pass: PASS only if sampled data sets show nothing retained beyond limits during the period

### CF-04 — Secure deletion at contract end or on request
- TSC: C1.2, P4.3 | Category: Confidentiality, Privacy
- Applies when: customers can terminate or request deletion
- Implement: documented deletion procedure within contractual timeframe (e.g. 30 days) covering primary stores, replicas, and noting backup expiry; deletion confirmation sent to customer
- Scan signals: privacy.dsar
- Frequency: Per event
- Owner: Engineering lead
- Type 1 test: procedure exists and matches contract terms
- Type 2 test: sample customer terminations and deletion requests; confirm deletion within timeframe
- Evidence: deletion procedure, deletion tickets, confirmation messages
- Type 1 pass: PASS if a deletion procedure exists that matches contract terms
- Type 2 pass: PASS only if every sampled deletion in the period completed within the committed timeframe with confirmation

### CF-05 — Confidentiality agreements for personnel
- TSC: C1.1, CC1.1 | Category: Confidentiality, Security
- Applies when: always
- Implement: NDA or confidentiality clause in employment and contractor agreements signed before access
- Scan signals: none
- Frequency: Per event
- Owner: People ops
- Type 1 test: template agreement includes confidentiality obligations
- Type 2 test: sample new hires and contractors; confirm signed agreements before access
- Evidence: agreement template, signed agreements, access grant dates
- Type 1 pass: PASS if the agreement template includes confidentiality obligations for employees and contractors
- Type 2 pass: PASS only if every sampled person onboarded in the period signed before receiving access

### CF-06 — No production confidential data in non-production
- TSC: C1.1 | Category: Confidentiality
- Applies when: development or test environments exist
- Implement: synthetic or masked data in dev/staging; any production data copy requires approval and masking
- Scan signals: privacy.pii_fields
- Frequency: Per event
- Owner: Engineering lead
- Type 1 test: policy prohibits unmasked prod data in non-prod; non-prod datastores inspected
- Type 2 test: sample prod-to-non-prod copy events in the period; confirm approval and masking
- Evidence: policy, masking scripts, approval tickets
- Type 1 pass: PASS if a policy prohibits unmasked prod data in non-prod AND inspected non-prod datastores hold none
- Type 2 pass: PASS only if every prod-to-non-prod copy in the period was approved and masked

## Privacy (P1–P8)

### PR-01 — Privacy notice published and maintained
- TSC: P1.1 | Category: Privacy
- Applies when: Privacy is in scope (the entity collects personal information directly from data subjects)
- Implement: public privacy notice describing purposes, categories collected, retention, sharing, rights, and contact; version history; updated when practices change
- Scan signals: privacy.privacy_notice
- Frequency: Per event
- Owner: Privacy owner
- Type 1 test: notice is published and matches actual collection practices
- Type 2 test: notice changes in the period were approved and communicated
- Evidence: notice URL with version date, approval records, change communications
- Type 1 pass: PASS if the notice is accessible at the point of collection AND matches documented processing
- Type 2 pass: PASS only if every notice change in the period was approved and communicated

### PR-02 — Consent capture and records
- TSC: P2.1 | Category: Privacy
- Applies when: processing relies on consent or opt-out choices (marketing, cookies, optional data)
- Implement: consent management (OneTrust/Cookiebot or in-app) recording who consented, to what, when, and the notice version; withdrawal honored
- Scan signals: privacy.privacy_notice
- Frequency: Per event
- Owner: Privacy owner
- Type 1 test: consent mechanism and consent records exist
- Type 2 test: sample data subjects; confirm consent record exists before processing and withdrawals were honored
- Evidence: consent logs, consent UI screenshots, withdrawal records
- Type 1 pass: PASS if a consent mechanism exists AND records who consented, to what, when, and which notice version
- Type 2 pass: PASS only if every sampled consent-based processing has a recorded consent before processing AND withdrawals were honored

### PR-03 — Collection limited to stated purposes
- TSC: P3.1 | Category: Privacy
- Applies when: Privacy is in scope
- Implement: data inventory of personal information fields with purpose; new fields require privacy review
- Scan signals: privacy.pii_fields
- Frequency: Per event
- Owner: Privacy owner
- Type 1 test: inventory maps each PII field to a purpose in the notice
- Type 2 test: sample schema changes adding PII in the period; confirm privacy review
- Evidence: personal data inventory, privacy review records
- Type 1 pass: PASS if every collected PII field maps to a stated purpose
- Type 2 pass: PASS only if every sampled schema change adding PII in the period had a privacy review

### PR-04 — Explicit consent for sensitive personal information
- TSC: P3.2 | Category: Privacy
- Applies when: the entity collects sensitive data (health, biometrics, government IDs, precise location) or law requires explicit consent
- Implement: separate affirmative opt-in for sensitive data with recorded consent
- Scan signals: privacy.pii_fields
- Frequency: Per event
- Owner: Privacy owner
- Type 1 test: explicit consent flow exists for each sensitive category
- Type 2 test: sample sensitive-data subjects; confirm explicit consent recorded before collection
- Evidence: consent flow, consent records
- Type 1 pass: PASS if an explicit consent flow exists for each sensitive category
- Type 2 pass: PASS only if every sampled sensitive-data collection in the period has explicit consent dated before collection

### PR-05 — Use limitation
- TSC: P4.1 | Category: Privacy
- Applies when: Privacy is in scope
- Implement: new uses of personal data (analytics, ML training, marketing) require privacy review against the notice; access to PII restricted by purpose
- Scan signals: none
- Frequency: Per event
- Owner: Privacy owner
- Type 1 test: privacy review procedure for new uses exists
- Type 2 test: sample new features or data uses in the period; confirm review and consistency with the notice
- Evidence: privacy review records, notice, feature tickets
- Type 1 pass: PASS if a privacy review procedure for new uses exists
- Type 2 pass: PASS only if every sampled new use of PII in the period was reviewed and is covered by the notice or consent

### PR-06 — Retention of personal information
- TSC: P4.2 | Category: Privacy
- Applies when: Privacy is in scope
- Implement: retention periods per PII category; automated purge jobs; protection against accidental deletion (backups, soft delete)
- Scan signals: logging.retention_days, backups.configured
- Frequency: Continuous/automated
- Owner: Engineering lead
- Type 1 test: retention periods defined and purge mechanisms configured
- Type 2 test: sample PII records; confirm none retained beyond period
- Evidence: retention schedule, purge job logs
- Type 1 pass: PASS if retention periods are defined AND purge mechanisms are configured
- Type 2 pass: PASS only if no sampled PII exceeded its defined retention period during the period

### PR-07 — Secure disposal of personal information
- TSC: P4.3 | Category: Privacy
- Applies when: Privacy is in scope
- Implement: deletion procedures for PII at end of retention or on request, including vendor copies; backups expire on schedule
- Scan signals: privacy.dsar
- Frequency: Per event
- Owner: Privacy owner
- Type 1 test: disposal procedure covers primary, backup, and vendor copies
- Type 2 test: sample disposal events; confirm deletion from all locations
- Evidence: disposal procedure, deletion logs, vendor deletion confirmations
- Type 1 pass: PASS if the disposal procedure covers primary, backup, and vendor copies
- Type 2 pass: PASS only if sampled disposals in the period cover primary stores and vendors AND backups expire within the stated period

### PR-08 — Data subject access requests
- TSC: P5.1, P6.7 | Category: Privacy
- Applies when: Privacy is in scope
- Implement: DSAR intake (form or email), identity verification, response within legal/committed deadline (e.g. 30 days GDPR, 45 days CCPA), including an accounting of disclosures when requested
- Scan signals: privacy.dsar
- Frequency: Per event
- Owner: Privacy owner
- Type 1 test: DSAR procedure with verification and deadlines exists
- Type 2 test: sample DSARs in the period; confirm verification and on-time response
- Evidence: DSAR log, verification records, responses with dates
- Type 1 pass: PASS if a DSAR procedure with identity verification and deadlines exists
- Type 2 pass: PASS only if every sampled DSAR in the period was identity-verified and answered within the deadline

### PR-09 — Correction requests
- TSC: P5.2 | Category: Privacy
- Applies when: Privacy is in scope
- Implement: self-service profile edits or support process to correct data; corrections propagated to vendors that received the data where required
- Scan signals: privacy.dsar
- Frequency: Per event
- Owner: Support lead
- Type 1 test: correction mechanism exists
- Type 2 test: sample correction requests; confirm timely correction and propagation
- Evidence: correction request log, propagation records
- Type 1 pass: PASS if a correction mechanism exists
- Type 2 pass: PASS only if every sampled correction in the period was completed and propagated within the committed timeframe

### PR-10 — Disclosure to third parties only for stated purposes
- TSC: P6.1, P6.4 | Category: Privacy
- Applies when: personal information is shared with vendors or partners
- Implement: subprocessor list published; DPAs with privacy commitments; new sharing requires privacy review and notice coverage
- Scan signals: vendors.list_present
- Frequency: Annual
- Owner: Privacy owner
- Type 1 test: subprocessor list and DPAs exist for vendors receiving PII
- Type 2 test: sample vendors receiving PII; confirm DPA and notice coverage; confirm periodic compliance review
- Evidence: subprocessor list, DPAs, vendor privacy reviews
- Type 1 pass: PASS if every vendor receiving PII has a DPA AND is disclosed in the notice or subprocessor list
- Type 2 pass: PASS only if sampled vendors receiving PII had DPA and notice coverage AND their privacy compliance was reviewed within the period

### PR-11 — Record of authorized disclosures
- TSC: P6.2 | Category: Privacy
- Applies when: personal information is disclosed to third parties, including law enforcement requests
- Implement: log of disclosures with date, recipient, data categories, legal basis; law-enforcement request procedure
- Scan signals: none
- Frequency: Per event
- Owner: Legal
- Type 1 test: disclosure log and procedure exist
- Type 2 test: sample disclosures in the period; confirm recorded completely
- Evidence: disclosure log, request procedure
- Type 1 pass: PASS if a disclosure log and request procedure exist
- Type 2 pass: PASS only if every known disclosure in the period is in the log with recipient and basis

### PR-12 — Breach records and notification
- TSC: P6.3, P6.6 | Category: Privacy
- Applies when: Privacy is in scope
- Implement: register of unauthorized disclosures/breaches; assessment of notification obligations; notices to data subjects and regulators within legal deadlines
- Scan signals: incident.runbook
- Frequency: Per event
- Owner: Privacy owner
- Type 1 test: breach register and notification procedure exist
- Type 2 test: inspect all breaches in the period; confirm recording and timely notification
- Evidence: breach register, notification records with timestamps
- Type 1 pass: PASS if a breach register and notification procedure exist
- Type 2 pass: PASS only if every breach in the period is recorded AND notifications met legal deadlines

### PR-13 — Vendor obligation to report privacy incidents
- TSC: P6.5 | Category: Privacy
- Applies when: vendors process personal information
- Implement: DPA clause requiring notification of suspected unauthorized disclosure within a fixed period (e.g. 72 hours or less); vendor notices routed into incident process
- Scan signals: none
- Frequency: Per event
- Owner: Legal
- Type 1 test: clause present in DPA template and executed DPAs
- Type 2 test: sample vendor DPAs; inspect any vendor incident notices in the period for handling
- Evidence: DPA template, executed DPAs, vendor incident notices
- Type 1 pass: PASS if the time-bound notification clause is in the DPA template and executed PII-vendor DPAs
- Type 2 pass: PASS only if every sampled PII vendor DPA includes the clause AND any vendor incident notice in the period entered the incident process

### PR-14 — Personal data quality
- TSC: P7.1 | Category: Privacy
- Applies when: Privacy is in scope
- Implement: validation at collection, periodic data quality checks, and user ability to update records
- Scan signals: none
- Frequency: Quarterly
- Owner: Privacy owner
- Type 1 test: validation and update mechanisms exist
- Type 2 test: sample data quality checks performed in the period
- Evidence: validation rules, data quality reports
- Type 1 pass: PASS if accuracy controls exist at collection AND users can update their data
- Type 2 pass: PASS only if the sampled data quality checks were performed in the period

### PR-15 — Privacy inquiries, complaints, and compliance monitoring
- TSC: P8.1 | Category: Privacy
- Applies when: Privacy is in scope
- Implement: privacy contact (privacy@ or DPO); complaint log with resolution; annual privacy compliance review reported to leadership
- Scan signals: privacy.privacy_notice
- Frequency: Per event
- Owner: Privacy owner
- Type 1 test: contact channel published and complaint procedure exists
- Type 2 test: sample complaints; confirm resolution and response; annual review performed
- Evidence: complaint log, responses, privacy review report
- Type 1 pass: PASS if a privacy contact is published AND a complaint procedure exists
- Type 2 pass: PASS only if every sampled complaint in the period was resolved with a documented response AND the annual privacy review occurred within the period

### PR-16 — Privacy training for personnel handling PII
- TSC: P8.1, P4.1 | Category: Privacy
- Applies when: Privacy is in scope
- Implement: annual privacy training for staff with PII access (support, engineering, marketing) covering notice commitments and DSAR handling
- Scan signals: none
- Frequency: Annual
- Owner: Privacy owner
- Type 1 test: training content and assignment exist
- Type 2 test: sample PII-access staff; confirm completion within 12 months
- Evidence: training content, completion report
- Type 1 pass: PASS if training content and assignment rules exist for PII-access staff
- Type 2 pass: PASS only if every sampled PII-access staff member completed privacy training within 12 months

### PR-17 — Personal information inventory and controller/processor role
- TSC: P1.1, P3.1 | Category: Privacy
- Applies when: Privacy is in scope (note: when the entity only processes personal information on customers' instructions as a processor, many notice and consent duties sit with the customer; record the role and scope privacy criteria accordingly)
- Implement: inventory of personal information categories, data subjects, sources, purposes, systems, recipients, and retention; documented role per processing activity (controller or processor); inventory reviewed when products or vendors change
- Scan signals: privacy.pii_fields
- Frequency: Annual
- Owner: Privacy owner
- Type 1 test: inventory exists, covers in-scope systems, and records the controller/processor role per activity
- Type 2 test: inventory reviewed within the period and updated for new PII fields, systems, or vendors added in the period
- Evidence: personal information inventory with review date, role determination, schema-change and vendor-change records
- Type 1 pass: PASS if every in-scope system holding PII appears in the inventory with purpose AND the controller/processor role is recorded
- Type 2 pass: PASS only if the inventory was reviewed within the period AND every PII-related change in the period is reflected
