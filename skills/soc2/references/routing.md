# Routing reference

The router classifies each turn by user intent first, then by scan signals. Intent beats signals when they conflict. Signal names refer to the JSON printed by `scripts/scan.py`.

## Routing table

| Condition | Route |
|---|---|
| Empty repo or docs/brainstorm only; design intent | `soc2-architect` |
| Code/IaC exists, in-scope controls incomplete | `soc2-type1-readiness` |
| Controls designed, no evidence automation | `soc2-type2-operations` |
| "audit", "gap", "are we compliant", "auditor" | `soc2-audit` |
| Policy request, or `policies` signal empty | `soc2-policies` |

## Intent keywords per route

Match case-insensitively; any one hit is enough. Keywords overlap (for example "audit" vs "audit period", "evidence" vs "evidence request list", "gap" vs "fix gaps"), so when several routes match, use this fixed precedence:

`soc2-audit` > `soc2-type2-operations` > `soc2-type1-readiness` > `soc2-policies` > `soc2-architect`

Exception: if the user names a phase or skill explicitly, that wins. Multi-word phrases beat single words (the phrase "audit period" counts for type2, not audit).

- `soc2-architect`: design, architect, architecture, brainstorm, greenfield, from scratch, new system, new service, add a new, new component, add a service, how should we build, ADR, architecture diagram, data flow, "SOC 2 compliant by design".
- `soc2-type1-readiness`: type 1, type I, point in time, readiness, "controls in place", check what we built, control matrix, what is missing, implement controls, fix gaps.
- `soc2-type2-operations`: type 2, type II, audit period, observation window, evidence, evidence automation, access review cadence, sampling, log retention, restore test, continuous compliance, collect evidence.
- `soc2-audit`: audit, gap, gap analysis, are we compliant, auditor, findings, severity, PBC, evidence request list, mock audit, pre-audit.
- `soc2-policies`: policy, policies, write the policy, acceptable use, incident response policy, vendor policy, HR security policy, templates.

## Signal tie-breakers

Use these only when intent is ambiguous or absent. Evaluate them in order; the first one that matches wins.

1. No `iac`, no code files, and `ci` empty: `soc2-architect`.
2. `policies` signal empty and the user asks for anything compliance-related with no phase named: `soc2-policies`, then continue the chain.
3. Code or IaC present and several core signals false (`auth.sso`, `logging.centralized`, `change_mgmt.codeowners`, `backups.configured`, `incident.runbook`): `soc2-type1-readiness`.
4. Core signals mostly true, `report_type` is `type2`, and `ci` is empty or evidence jobs are missing: `soc2-type2-operations`.
5. `state.completed` already contains the skill the signals suggest: suggest the next skill in the chain instead and say why.
6. Still tied: prefer the earlier phase (architect, policies, type1, type2). Audit is chosen by intent only, never by signals alone.
7. `secrets.hardcoded_hits > 0`: not a route on its own. Mention it in any route.

## Chain definitions

| Request | Chain |
|---|---|
| "make us SOC 2 ready", "end to end" (`report_type: type2`) | architect → policies → type1-readiness → type2-operations |
| Same, `report_type: type1` | architect → policies → type1-readiness |
| "we already have code, get us ready" | policies → type1-readiness → type2-operations |
| "audit us, then fix it" | audit → type1-readiness (or type2-operations when `report_type` is `type2` and controls are designed) |
| "policies and a gap check" | policies → audit |

Each step reads the previous step's output files and `.soc2/state.json`. Skip skills in `state.completed` unless asked to redo them.

## Worked examples

### 1. Greenfield design

Prompt: "We're starting a new B2B SaaS on AWS and want to design it so SOC 2 is easy later."
Scan excerpt: `iac: []`, `ci: []`, `cloud: []`, `policies: []`.
Route: `→ soc2-architect (empty repo, design intent)`.
Reason: no code or IaC and the user is designing. With no state file, ask only for `tsc_scope`, `report_type`, and `audit_period` if Type 2.

### 2. Existing code, MFA question

Prompt: "We have Terraform and GitHub Actions. Is MFA enforced everywhere? Sort out what's missing for Type 1."
Scan excerpt: `iac: ["terraform"]`, `ci: ["github-actions"]`, `auth: {"sso": false, "mfa_hint": false}`, `logging.cloudtrail: false`.
Route: `→ soc2-type1-readiness (code/IaC present, AC-02 and OPS-06 signals missing)`.
Reason: code exists and in-scope controls are incomplete; the user asked what is missing, which is a readiness question, not an auditor view. AC-02 (MFA) and OPS-06 (cloud audit trail) are the first gaps to check against the catalog pass rules.

### 3. Auditor question with a hardcoded secret

Prompt: "Are we compliant? Pretend you're the auditor."
Scan excerpt: `iac: ["terraform"]`, `change_mgmt: {"codeowners": true, "pr_template": true, "branch_protection": "unknown"}`, `secrets: {"hardcoded_hits": 2}`.
Route: `→ soc2-audit (auditor intent: "are we compliant")`.
Reason: intent keywords outweigh signals. Also mention in the reply that 2 hardcoded-secret hits were found (AC-17 → CC6.1, CC6.7; cite file and line, never the secret value), and that CHG-02 (peer review enforced by branch protection) cannot be confirmed from the repo alone because `branch_protection` is `unknown`.
