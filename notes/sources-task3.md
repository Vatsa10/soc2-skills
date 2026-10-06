# Sources for Task 3 (soc2-policies)

Source repo: `claude-skills-soc2-policies` (MIT, Constantine Kurianoff 2026), read-only, mined for structure and topic coverage.

## Read
- `skills/soc2-policies/SKILL.md`: dashboard skill. Adapted: the idea of a manifest of policies with lazy, per-policy template reads (one template read per policy at generation time), the `[COMPANY NAME]` replacement concept (here `{{company}}` etc.), and the notion of keeping a policy-to-category list. Not adapted: widget/dashboard UI, persistent storage keys, HTML-only pipeline.
- `skills/soc2-policies/references/templates/*.html` (17 templates): `access_control_policy.html` read in full; section topics (access control requirements, user provisioning, privileged access, access reviews, password rules) informed the Access Control template. The rest were used only as a topic checklist (titles).
- `skills/policy-review/SKILL.md`: adapted into Review mode (walk statements one by one; report decisions). Not adapted: carousel widget, AI-rewrite roundtrip, audit-trail storage.
- `skills/policy-export/SKILL.md`: head read only. Not adapted (Word export is out of scope; policies are markdown).

## Differences
- All 15 templates here are original text written for this pack, in Markdown, with numbered statements tagged by control ID and TSC criterion. No template text was copied from the source.
- The source has 17 policies (adds code of conduct, roles and responsibilities, physical security, removable media, secure development, operations security); this pack has 15 with different slugs. Mapping: cryptography -> `encryption`; data management -> `data-classification` + `data-retention-disposal`; risk management -> `risk-assessment`; third-party management -> `vendor-management`; secure development and operations security -> `change-management` and `logging-monitoring`; code of conduct -> HR security; physical security and removable media -> covered by access control, acceptable use and asset management statements; no standalone `privacy` or `logging-monitoring` source exist (new).
- Source password rules (10 chars, 90-day expiry, 40-hour deprovisioning) were deliberately not carried over; templates use 14 characters, no scheduled rotation, 24-hour removal.
