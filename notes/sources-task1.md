# Sources for Task 1 (attribution notes; delete in Task 9)

## Mined sources (all text rewritten; no verbatim copying)

- claude-skills (MIT, Copyright (c) 2025 Alireza Rezvani)
  - `ra-qm-team/skills/soc2-compliance/references/trust_service_criteria.md`: per-criterion objective/typical-control/evidence table structure; informed CC1–CC9 typical controls (code of conduct, background checks, access reviews).
  - `ra-qm-team/skills/soc2-compliance/references/type1_vs_type2.md`: Type 1 vs Type 2 framing (design at a point in time vs operating effectiveness over a period; exceptions reported with management response).
  - `ra-qm-team/skills/soc2-compliance/references/evidence_collection_guide.md`, `soc2_audit_playbook.md`: evidence types per control family.
  - `compliance-os/skills/soc2-audit-prep/SKILL.md`, `compliance-os/agents/cs-soc2-auditor.md`: readiness/gap-assessment workflow ideas.
- Claude-Skills-Governance-Risk-and-Compliance (MIT, Copyright (c) 2026 Hemant Naik)
  - `SOC 2 - Claude Skill/soc2.skill` (zip): `references/controls.md` — "what auditors look for / common gap" framing and control-statement fields (owner, frequency, test); idea of sampling individuals (e.g. 5 employees) for training tests. `evidence.md`, `vendor.md` — CUEC review and vendor SOC report review ideas (VND-03).
- skills-hub-registry: not used (no license; ideas only).

## Criteria verification

- Web search (2026-10-06) confirmed AICPA 2017 TSC with Revised Points of Focus (2022), TSP Section 100, has 61 criteria; privacy series P1–P8 (notice; choice/consent; collection; use/retention/disposal; access; disclosure/notification; quality; monitoring/enforcement). Sources: https://blog.rsisecurity.com/what-are-the-aicpa-trust-services-criteria/, https://www.tcsa.in/frameworks/soc-2/trust-service-criteria, https://myctrl.tools/frameworks/soc2-tsc
- The brief's ID list (61 IDs) matched; no contradictions found.

## Own knowledge / practice (not from mined sources)

- Sampling table is common auditor practice as given in the brief, not AICPA mandate.
- Remediation SLAs (15/30/90 days), 24h deprovisioning, 365-day log retention, TLS 1.2+ are common industry baselines chosen for concreteness; auditors accept the entity's documented values if consistently met.
