# SOC 2 Trust Services Criteria (TSC) — Reference

> This skill prepares for a SOC 2 audit; it is not an attestation. Only a licensed CPA firm can issue a SOC 2 Type 1 or Type 2 report.

Source framework: AICPA *2017 Trust Services Criteria for Security, Availability, Processing Integrity, Confidentiality, and Privacy (With Revised Points of Focus – 2022)*, TSP Section 100. There are 61 criteria. Titles and focus summaries below are paraphrased in our own words; consult the AICPA publication for the authoritative text. Points of focus are illustrative aids, not individually required checklist items — the auditor evaluates whether each criterion is met.

Scoping: Security (Common Criteria, CC1–CC9) is required in every SOC 2 report. Availability, Processing Integrity, Confidentiality, and Privacy are optional and are included only when they are in the system description's scope.

## Security — Common Criteria (required)

### CC1 — Control Environment
- **CC1.1** — Commitment to integrity and ethical values: documented code of conduct; leadership sets the tone; workforce and contractors acknowledge standards; deviations are identified and addressed promptly.
- **CC1.2** — Board independence and oversight: the board (or equivalent governing body) is independent of management where applicable, has relevant expertise, and oversees the design and operation of internal control.
- **CC1.3** — Structure, reporting lines, and authority: management defines org structure, reporting lines, roles, and responsibilities, including for security and for third parties.
- **CC1.4** — Commitment to competence: policies define required competence; hiring includes background screening; personnel are trained; succession planning exists for key roles.
- **CC1.5** — Accountability for internal control: individuals are held accountable through performance measures, incentives, and disciplinary action; pressures on staff are considered.

### CC2 — Communication and Information
- **CC2.1** — Relevant, quality information: the entity identifies information requirements, captures internal and external data, and maintains an inventory of system components and data flows so controls can function.
- **CC2.2** — Internal communication: objectives, responsibilities, and policies are communicated to personnel; a channel exists for reporting concerns (including anonymously); security commitments are communicated to staff.
- **CC2.3** — External communication: commitments, system boundaries, and changes are communicated to customers, vendors, and regulators; external parties have a channel to report incidents or complaints.

### CC3 — Risk Assessment
- **CC3.1** — Clear objectives: operational, reporting, and compliance objectives are specified with enough clarity (including risk tolerance) to identify and assess risks.
- **CC3.2** — Risk identification and analysis: risks across the entity, including from vendors and business partners, are identified, analyzed for likelihood and impact, and given a response (accept, mitigate, transfer, avoid).
- **CC3.3** — Fraud risk: the assessment considers incentives, opportunities, and rationalizations for fraud, including unauthorized access and manipulation of data.
- **CC3.4** — Significant change: changes in the external environment, business model, leadership, vendors, and technology are identified and assessed for impact on internal control.

### CC4 — Monitoring Activities
- **CC4.1** — Ongoing and separate evaluations: a mix of continuous monitoring and periodic independent evaluations (internal audit, penetration tests, readiness reviews) confirms controls are present and functioning.
- **CC4.2** — Evaluating and communicating deficiencies: deficiencies are evaluated, communicated to those responsible for corrective action (and to senior management or the board as appropriate), and remediation is tracked.

### CC5 — Control Activities
- **CC5.1** — Selecting and developing controls: control activities are selected to mitigate assessed risks to acceptable levels, considering a mix of preventive/detective and manual/automated controls and segregation of duties.
- **CC5.2** — Technology general controls: general controls over technology infrastructure, security management, and technology acquisition, development, and maintenance are selected and developed.
- **CC5.3** — Policies and procedures: control activities are deployed through policies stating expectations and procedures putting them into action, with assigned responsibility, timely performance, and periodic reassessment.

### CC6 — Logical and Physical Access Controls
- **CC6.1** — Logical access security: asset inventory; restricted access to information assets; identification and authentication (including MFA); network segmentation; encryption and key management protect data.
- **CC6.2** — User registration and authorization: new internal and external users are authorized before credentials are issued; credentials are removed when access is no longer authorized.
- **CC6.3** — Role-based access and changes: access is granted, modified, and removed based on roles, least privilege, and segregation of duties; access is periodically reviewed.
- **CC6.4** — Physical access: physical access to facilities and protected assets (data centers, backup media, offices) is restricted to authorized personnel and reviewed.
- **CC6.5** — Asset disposal: protections are discontinued only after data is removed or rendered unreadable when physical assets are retired or reused.
- **CC6.6** — Boundary protection: logical access controls protect against threats from sources outside system boundaries (firewalls, restricted remote access, intrusion detection).
- **CC6.7** — Data transmission and movement: transmission, movement, and removal of information is restricted to authorized users and processes and protected (encryption in transit, removable media controls, endpoint protection).
- **CC6.8** — Malicious software prevention: controls prevent or detect the introduction of unauthorized or malicious software (anti-malware, restricted software installation, integrity checks).

### CC7 — System Operations
- **CC7.1** — Detecting configuration and vulnerability issues: configuration standards are defined; changes introducing vulnerabilities are detected; vulnerability scans are conducted and remediated.
- **CC7.2** — Monitoring for anomalies: system components are monitored for anomalies indicative of malicious acts, natural disasters, and errors; logging and alerting are in place.
- **CC7.3** — Evaluating security events: detected events are analyzed to determine whether they are security incidents requiring response.
- **CC7.4** — Incident response: a defined incident response program contains, remediates, and communicates incidents with assigned roles.
- **CC7.5** — Incident recovery: activities restore operations after an incident, including root-cause analysis, lessons learned, and periodic testing of the response plan.

### CC8 — Change Management
- **CC8.1** — Change management: changes to infrastructure, data, software, and procedures are authorized, designed, documented, tested, approved, and implemented; emergency changes and configuration baselines are controlled.

### CC9 — Risk Mitigation
- **CC9.1** — Business disruption risk: activities to mitigate risks from potential business disruptions are identified and developed (business continuity planning, insurance).
- **CC9.2** — Vendor and business partner risk: risks from vendors and business partners are assessed and managed (due diligence, contractual commitments, periodic monitoring, termination procedures).

## Availability (optional)
- **A1.1** — Capacity management: current processing capacity and usage are monitored and evaluated, and capacity is forecast to meet availability commitments.
- **A1.2** — Environmental protections, backup, and recovery infrastructure: environmental protections, software, data backup processes, and recovery infrastructure are designed, implemented, operated, and monitored.
- **A1.3** — Recovery plan testing: business continuity and disaster recovery procedures, including backup restoration, are tested periodically and results are used to improve the plan.

## Processing Integrity (optional)
- **PI1.1** — Processing specifications: information about processing objectives, including definitions of data and product/service specifications, is obtained or generated and communicated.
- **PI1.2** — System inputs: inputs are complete and accurate, validated, and errors are identified and corrected.
- **PI1.3** — System processing: processing is complete, accurate, and timely; processing errors are detected, logged, and corrected.
- **PI1.4** — System outputs: outputs are complete, accurate, distributed only to intended parties, and delivered on time.
- **PI1.5** — Stored data: inputs, items in processing, and outputs are stored completely and accurately and protected from unauthorized modification, with retention per specifications.

## Confidentiality (optional)
- **C1.1** — Identifying and maintaining confidential information: confidential information is identified, classified, and protected from unauthorized access during its retention period.
- **C1.2** — Disposing of confidential information: confidential information is identified for destruction and securely disposed of when the retention period ends or upon request.

## Privacy (optional)
- **P1.1** — Notice: data subjects receive timely notice of the entity's privacy practices (purposes, collection, use, retention, disclosure, access, and how to contact the entity), updated when practices change.
- **P2.1** — Choice and consent: choices about collection, use, retention, disclosure, and disposal are communicated; implicit or explicit consent is obtained and documented; consequences of declining are explained.
- **P3.1** — Collection limited to objectives: personal information is collected only as needed for identified privacy objectives, by fair and lawful means, including from third parties.
- **P3.2** — Explicit consent: explicit consent is obtained and documented where required (e.g., sensitive personal information) before collection.
- **P4.1** — Use limitation: personal information is used only for the purposes identified in the notice and consented to.
- **P4.2** — Retention: personal information is retained only as long as needed for its objectives and protected from erroneous or unauthorized deletion.
- **P4.3** — Disposal: personal information is securely disposed of when no longer needed, including copies held in backups and by vendors where applicable.
- **P5.1** — Access: authenticated data subjects can access their personal information; requests are handled within committed timelines, and denials are explained.
- **P5.2** — Correction: data subjects can request correction or amendment; corrections are communicated to third parties that received the data where required.
- **P6.1** — Disclosure to third parties: personal information is disclosed only for identified purposes and with consent where required.
- **P6.2** — Record of authorized disclosures: complete, accurate, and timely records of authorized disclosures are created and retained.
- **P6.3** — Record of unauthorized disclosures: detected or reported unauthorized disclosures, including breaches, are recorded completely and accurately.
- **P6.4** — Third-party commitments: vendors with access to personal information have privacy commitments consistent with the entity's, and their compliance is assessed.
- **P6.5** — Third-party notification: vendors are required to notify the entity of actual or suspected unauthorized disclosures.
- **P6.6** — Breach notification: affected data subjects, regulators, and others are notified of breaches as required by law and commitments.
- **P6.7** — Accounting of disclosures: data subjects can obtain an accounting of the personal information held and disclosures made about them, on request.
- **P7.1** — Data quality: personal information is collected and maintained accurately, completely, and relevantly for its purposes.
- **P8.1** — Monitoring and enforcement: a process exists to receive, address, resolve, and communicate privacy inquiries, complaints, and disputes; compliance with privacy commitments is monitored and deficiencies remediated.
