# SOC 2 Skills Pack — Design Spec

Date: 2026-10-06
Status: Draft for review

## 1. Purpose

A skill pack for Claude Code and Codex that helps developers:

1. **Architect** systems from the ground up to SOC 2 (Type 1 and Type 2), during brainstorming and design.
2. **Operate** controls continuously so Type 2 evidence accumulates over the audit period.
3. **Audit** an existing repo/system and produce an auditor-style gap report.
4. **Generate policies** tailored to the system.

Scope: all five Trust Services Criteria (TSC) — Security (CC1–CC9), Availability (A1), Processing Integrity (PI1), Confidentiality (C1), Privacy (P1–P8) — per AICPA TSC 2017 with revised points of focus (2022).

**Disclaimer (in README and every skill):** this pack prepares for an audit; it is not an attestation. Only a licensed CPA firm issues SOC 2 reports.

## 2. Source material and licensing

The workspace currently holds four cloned repos. Content is extracted from them, then the folders are deleted.

| Repo | License | Use |
|---|---|---|
| `claude-skills` (alirezarezvani) — `soc2-compliance`, `soc2-audit-prep`, `cs-soc2-auditor` | MIT | Copy/adapt with attribution |
| `Claude-Skills-Governance-Risk-and-Compliance` (Sushegaad) — `SOC 2 - Claude Skill/soc2.skill` | MIT | Copy/adapt with attribution |
| `claude-skills-soc2-policies` (kurianoff) — `soc2-policies`, `policy-review`, `policy-export` | MIT | Policy template base, with attribution |
| `skills-hub-registry` (tinh2) | None (all rights reserved) | Ideas only; all text written fresh |

Attributions live in `THIRD_PARTY_NOTICES.md` (full MIT notices).

Web research verifies criterion numbering against the official AICPA TSC, Type 2 sampling norms, and typical auditor evidence requests. Where repo content conflicts with the official criteria, the official criteria win.

## 3. Repository layout

The workspace root becomes the repo: https://github.com/Vatsa10/soc2-skills

```
SOC2-Skills/
├── .claude-plugin/plugin.json    # Claude Code plugin manifest
├── AGENTS.md                     # Codex entry: points to skills/, router-first rule
├── CLAUDE.md                     # same rule for Claude Code
├── skills/
│   ├── soc2/                     # router + shared core
│   │   ├── SKILL.md
│   │   ├── scripts/scan.py       # shared stdlib scanner
│   │   └── references/
│   │       ├── routing.md
│   │       ├── tsc-criteria.md   # all TSC criteria + points of focus
│   │       └── control-catalog.md # single source of truth for controls
│   ├── soc2-architect/
│   ├── soc2-type1-readiness/
│   ├── soc2-type2-operations/
│   ├── soc2-audit/
│   └── soc2-policies/            # each: SKILL.md + references/*.md (+ templates/ for policies)
├── tests/
│   ├── fixtures/                 # small fixture repos for scanner
│   ├── test_scan.py
│   ├── test_catalog.py
│   └── router-evals.md           # manual routing eval cases
├── scripts/install.py            # installs whole pack to ~/.claude/skills or ~/.codex/skills
├── THIRD_PARTY_NOTICES.md
├── README.md
└── LICENSE                       # MIT
```

Decisions:
- One `skills/` tree serves both tools; no per-tool duplicated copies.
- Shared files live inside the router skill (`skills/soc2/references/`, `skills/soc2/scripts/`). Sub-skills reference them as `../soc2/...`. This holds both in the repo and when installed, because skills install as sibling folders (`~/.claude/skills/<name>`, `~/.codex/skills/<name>`, or the plugin's `skills/`). `install.py` copies all six skill folders together.
- Language: Markdown for skills; Python 3 stdlib only for scripts (no third-party dependencies).

## 4. Router (`skills/soc2`)

**Trigger:** the frontmatter description covers SOC 2, TSC, trust services, compliance audit, compliant architecture, and design/brainstorm requests in repos containing a `.soc2/` directory.

**Dynamic behavior, three combined modes:**

- **A. Re-route each turn.** Re-classify the phase every turn from conversation intent; switch sub-skill when the phase changes.
- **B. Repo-state detection.** Run `scan.py`, cache the result to `.soc2/scan.json`, and re-scan when tracked files' mtimes are newer than the cache or the user asks.
- **C. Chaining.** Multi-phase requests run sub-skills in sequence, each consuming the previous output (e.g. architect → policies → type1 → type2 plan).

**Routing table** (intent first, signals second):

| Condition | Route |
|---|---|
| Empty repo or docs/brainstorm only; design intent | `soc2-architect` |
| Code/IaC exists, in-scope controls incomplete | `soc2-type1-readiness` |
| Controls designed, no evidence automation | `soc2-type2-operations` |
| "audit", "gap", "are we compliant", "auditor" | `soc2-audit` |
| Policy request, or `policies` signal empty | `soc2-policies` |

The router announces each route in one line, e.g. `→ soc2-architect (empty repo, design intent)`, so the user can override it.

**Project state `.soc2/state.json`** (written in the user's project):

```json
{
  "tsc_scope": ["security","availability","processing_integrity","confidentiality","privacy"],
  "report_type": "type2",
  "audit_period": {"start": "2027-01-01", "end": "2027-06-30"},
  "system": {"name": "", "cloud": [], "data_classes": []},
  "decisions": [{"control": "AC-03", "choice": "Okta MFA", "date": "2026-10-06"}],
  "completed": ["soc2-architect"]
}
```

The router reads state before asking questions; anything already answered is never asked again.

## 5. Scanner (`scan.py`)

- Usage: `python scan.py <repo_path> [--json]`. Runs on Python 3.9+ with stdlib only and explicit UTF-8 file reads.
- Output: **signals only, no verdicts.** Verdicts come from the catalog's pass rules, applied by the skills.
- Detection uses file presence plus regex over text files. No YAML/HCL parser is used; pattern matching is sufficient for signals.

Signal schema (keys stable; tests enforce them):

```json
{
  "iac": ["terraform","cloudformation","pulumi","k8s"],
  "ci": ["github-actions","gitlab-ci","circleci"],
  "cloud": ["aws","gcp","azure"],
  "auth": {"sso": false, "mfa_hint": false, "idp": []},
  "encryption": {"kms": false, "tls": false, "at_rest_hint": false},
  "logging": {"cloudtrail": false, "centralized": false, "retention_days": null},
  "monitoring": {"alerts": false},
  "backups": {"configured": false, "restore_test": false},
  "change_mgmt": {"codeowners": false, "pr_template": false, "branch_protection": "unknown"},
  "secrets": {"scanning": false, "hardcoded_hits": 0},
  "deps": {"dependabot_or_renovate": false, "sast": false},
  "policies": ["access-control"],
  "privacy": {"pii_fields": false, "dsar": false, "privacy_notice": false},
  "vendors": {"list_present": false},
  "incident": {"runbook": false}
}
```

## 6. Sub-skills

| Skill | Behavior | Output in user repo |
|---|---|---|
| `soc2-architect` | Asks for system type, data classes, cloud, and TSC scope (skipping anything in state), then maps each component to required controls | `docs/soc2/architecture.md` (Mermaid + component→control table), `docs/soc2/adr/NNNN-*.md`, `.soc2/state.json` |
| `soc2-type1-readiness` | For each in-scope control: designed? implemented? Uses scan signals plus code reading | `docs/soc2/type1-readiness.md`: control matrix (designed/partial/missing), gaps, fixes |
| `soc2-type2-operations` | Builds continuous evidence: CI evidence jobs, access-review cadence, log retention ≥ 1 year, PR-linked change records, IR runbooks, restore tests | `docs/soc2/type2-operations.md` (control→frequency→owner→evidence source→sample size), generated CI/IaC snippets |
| `soc2-audit` | Auditor view: full gap scan against the catalog, severity rating, Type 2 sampling simulation | `docs/soc2/audit-report.md`: findings by TSC, PBC (evidence request) list, remediation plan |
| `soc2-policies` | Generates ~15 core policies from templates, tailored to state (InfoSec, Access Control, Change Mgmt, Incident Response, BCP/DR, Vendor Mgmt, Data Classification, Retention & Disposal, Privacy, Risk Assessment, Acceptable Use, Encryption, Logging & Monitoring, HR Security, Asset Mgmt) | `docs/policies/*.md` |

Shared rules:
- Every recommendation or finding cites a control ID and TSC criterion (e.g. `AC-03 → CC6.1`).
- Pass/fail uses the catalog's `Pass rule`; the model does not invent criteria.
- Type 1 vs Type 2 differ only by which catalog test column applies.

## 7. Control catalog

`skills/soc2/references/control-catalog.md`, roughly 80–100 controls, all five TSC. Entry format:

```markdown
### AC-03 — MFA enforced for all workforce access
- TSC: CC6.1, CC6.2 | Category: Security
- Applies when: any human login to prod/admin/cloud console
- Implement: IdP MFA policy; cloud SSO only; no IAM users with console passwords
- Scan signals: auth.sso, auth.mfa_hint
- Type 1 test: MFA policy exists and is enforced at IdP
- Type 2 test: enforced whole period; sample per frequency table
- Evidence: IdP policy export, MFA enrollment report, quarterly access review
- Pass rule: PASS only if enforced (not optional) AND no bypass accounts
```

`skills/soc2/references/tsc-criteria.md` lists every official criterion ID with title and summarized points of focus.

## 8. Testing

Run with `python -m unittest discover tests`.

- `test_scan.py`: three fixtures (empty repo, Terraform+AWS+GitHub Actions, app without controls) → expected signal JSON.
- `test_catalog.py`: every entry parses; every TSC ID exists in `tsc-criteria.md`; every criterion is covered by at least one control; every `Scan signals` key exists in the scanner schema.
- Every sub-skill's `../soc2/...` references resolve (asserted in `test_catalog.py`).
- `router-evals.md`: about 10 prompt + repo-state cases with expected routes, checked manually in Claude Code and Codex.

## 9. Build order

1. `git init` at root; `.gitignore` the four source folders.
2. Extract source content + web research → `tsc-criteria.md`, `control-catalog.md`, `test_catalog.py`.
3. `scan.py` + fixtures + `test_scan.py`.
4. Router, then the five sub-skills.
5. `install.py`, `AGENTS.md`, `CLAUDE.md`, `plugin.json`, README, `THIRD_PARTY_NOTICES.md`, LICENSE.
6. Smoke test: install into Claude Code and Codex; run router evals.
7. Delete the four source folders — only after tests pass, with explicit user confirmation.

## 10. Out of scope

Live cloud API checks (AWS Config/Security Hub), MCP server, GRC platform integrations (Vanta, Drata), automated router eval harness. Add when needed.
