# Third-party notices

This pack contains original text. The projects below were read for structure and ideas; their MIT licenses and copyright notices are reproduced as required.

## claude-skills

- Source: https://github.com/alirezarezvani/claude-skills
- License: MIT, Copyright (c) 2025 Alireza Rezvani
- What was adapted (ideas and structure; all text rewritten, nothing copied verbatim):
  - SOC 2 reference material (`ra-qm-team/skills/soc2-compliance/references/`): per-criterion objective / typical control / evidence table structure, Type 1 vs Type 2 framing, evidence types per control family.
  - `compliance-os/skills/soc2-audit-prep/SKILL.md` and `compliance-os/agents/cs-soc2-auditor.md`: readiness and gap-assessment workflow ideas; observation-period discipline (skipped cycles, mid-period control changes, early-period evidence), sample-driven testing, and the rule that the assessor does not produce the report (a CPA firm does).
  - Not adopted: the source's "1-2 exceptions tolerated, 3+ is a finding" threshold; this pack uses catalog pass rules only.

```
MIT License

Copyright (c) 2025 Alireza Rezvani

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Claude-Skills-Governance-Risk-and-Compliance

- Source: https://github.com/Sushegaad/Claude-Skills-Governance-Risk-and-Compliance
- License: MIT, Copyright (c) 2026 Hemant Naik
- What was adapted (ideas and structure; all text rewritten, nothing copied verbatim):
  - `SOC 2 - Claude Skill/soc2.skill` (`references/controls.md`): the "what auditors look for / common gap" framing, control-statement fields (owner, frequency, test), and the idea of sampling individuals (e.g. 5 employees) for training tests.
  - `evidence.md` and `vendor.md`: complementary user entity control (CUEC) review and vendor SOC report review ideas (control VND-03).

```
MIT License

Copyright (c) 2026 Hemant Naik

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## claude-skills-soc2-policies

- Source: https://github.com/kurianoff/claude-skills-soc2-policies
- License: MIT, Copyright (c) 2026 Constantine Kurianoff
- What was adapted (ideas and structure; all text rewritten, nothing copied verbatim):
  - Read-only structural reference for `soc2-policies`: a manifest of policies with lazy, per-policy template reads; the placeholder-replacement concept (here `{{company}}` etc.); a policy-to-category list; the step-by-step review mode (walk statements one by one, report decisions); and the 17 template titles as a topic checklist, with the access control template read in full for section topics.
  - All 15 templates in this pack are original Markdown text, not copied. Source password rules (10 characters, 90-day expiry, 40-hour deprovisioning) were deliberately not carried over.
  - Not adapted: dashboard/widget UI, persistent storage keys, HTML pipeline, AI-rewrite roundtrip, Word export.

```
MIT License

Copyright (c) 2026 Constantine Kurianoff

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## skills-hub-registry

The `skills-hub-registry` project (tinh2, https://github.com/tinh2/skills-hub-registry) was an inspiration for the idea of a packaged skill collection. No content was copied from it.

## Own knowledge and verification

The sampling table and remediation defaults (15/30/90-day SLAs, 24-hour deprovisioning, 365-day log retention, TLS 1.2+) are common industry practice chosen for concreteness, not AICPA mandates. The criteria list (AICPA 2017 Trust Services Criteria with Revised Points of Focus, 2022; 61 criteria) was cross-checked against public summaries on 2026-10-06.
