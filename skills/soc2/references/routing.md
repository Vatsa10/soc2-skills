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

Exception: if the user names a phase or skill explicitly, that wins. Multi-word phrases beat single words (the phrase "audit period" counts for type2, not audit). The special phrases in the next section beat the plain keyword lists.

- `soc2-architect`: design, architect, architecture, brainstorm, greenfield, from scratch, new system, new service, add a new, new component, add a service, how should we build, ADR, architecture diagram, data flow, "SOC 2 compliant by design", invoices, billing, payments, data pipeline (when designing or building).
- `soc2-type1-readiness`: type 1, type I, point in time, readiness, "controls in place", check what we built, control matrix, what is missing, implement controls, fix gaps.
- `soc2-type2-operations`: type 2, type II, audit period, observation window, evidence, evidence automation, access review cadence, sampling, log retention, restore test, continuous compliance, collect evidence.
- `soc2-audit`: audit, gap, gap analysis, are we compliant, auditor, findings, severity, PBC, evidence request list, mock audit, pre-audit, security questionnaire, enterprise security review.
- `soc2-policies`: policy, policies, write the policy, acceptable use, incident response policy, vendor policy, HR security policy, templates.

## Special phrases (checked first)

These beat the keyword lists and the precedence order.

| User says | Route |
|---|---|
| "type 1 first", "type 1 then type 2", "are we ready", a readiness question, even if "type 2" is also mentioned | `soc2-type1-readiness` |
| "type 2 readiness", "type 2 gap", "where are we for type 2" | `soc2-audit` in Type 2 gap mode |
| "what will the auditor ask", "PBC", "evidence request list" | `soc2-audit` in PBC-only mode |
| "plan", "roadmap", "2 week plan", "30-60-90", "what do we fix first" | `soc2-audit` in remediation plan mode |
| "add a service/component", "we're adding X" | `soc2-architect` in "Adding a component" mode, even if `soc2-architect` is in `completed` |
| "a customer asked for SOC 2", "enterprise security review", "security questionnaire" with no phase named | First run questions if state is missing, then by scan signals |

## Signal tie-breakers

Use these only when intent is ambiguous or absent. Evaluate them in order; the first one that matches wins.

1. No `iac`, no code files, and `ci` empty: `soc2-architect`.
2. `policies` signal empty and the user asks for anything compliance-related with no phase named: `soc2-policies`, then continue the chain.
3. Code or IaC present and several core signals false (`auth.sso`, `logging.centralized`, `change_mgmt.codeowners`, `backups.configured`, `incident.runbook`): `soc2-type1-readiness`.
4. Core signals mostly true, `report_type` is `type2`, and `ci` is empty or evidence jobs are missing: `soc2-type2-operations`. If `report_type` is `type1`, never pick type2-operations here: stay on `soc2-type1-readiness`, or `soc2-audit` if the user wants a final check.
5. `state.completed` already contains the skill the signals suggest and the user is not asking for something new: suggest the next skill in the chain (for `report_type: type1`, the chain stops at type1-readiness) and say why. A new component or a redo request is never blocked by `completed`.
6. Still tied: prefer the earlier phase (architect, policies, type1, type2). Audit is chosen by intent only, never by signals alone.
7. `secrets.hardcoded_hits > 0`: not a route on its own. Mention it in any route.

## Period mode (Type 2)

Check `audit_period` against today before routing a Type 2 request.

- `audit_period.start` is in the future: pre-period readiness. Report the date each control's evidence must be live by. No sampling simulation.
- The window has started or ended and most controls fail: say so plainly (the gaps cannot be backfilled), and offer a later window or a Type 1 first.

## Chain definitions

| Request | Chain |
|---|---|
| "make us SOC 2 ready", "end to end" (`report_type: type2`) | architect → policies → type1-readiness → type2-operations |
| Same, `report_type: type1` | architect → policies → type1-readiness |
| "we already have code, get us ready" | policies → type1-readiness → type2-operations |
| "audit us, then fix it" | audit → type1-readiness (or type2-operations when `report_type` is `type2` and controls are designed) |
| "policies and a gap check" | policies → audit |

Each step reads the previous step's output files and `.soc2/state.json`. Skip skills in `state.completed` unless asked to redo them, and print what was skipped and why. At the end of the chain, list what was not produced (policies, IaC, CI evidence jobs) and offer to scaffold it.

## Worked examples

### 1. Greenfield design

Prompt: "We're starting a new B2B SaaS on AWS and want to design it so SOC 2 is easy later."
Scan excerpt: `iac: []`, `ci: []`, `cloud: []`, `policies: []`.
Route: `→ soc2-architect (empty repo, design intent)`.
Reason: no code or IaC and the user is designing. With no state file, send the single first-run message (report type, date, cloud, company/owner/team size); do not ask for `audit_period` unless Type 2 was chosen.

### 2. Existing code, MFA question

Prompt: "We have Terraform and GitHub Actions. Is MFA enforced everywhere? Sort out what's missing for Type 1."
Scan excerpt: `iac: ["terraform"]`, `ci: ["github-actions"]`, `auth: {"sso": false, "mfa_hint": false}`, `logging.cloud_audit_trail: false`.
Route: `→ soc2-type1-readiness (code/IaC present, AC-02 and OPS-06 signals missing)`.
Reason: code exists and in-scope controls are incomplete; the user asked what is missing, which is a readiness question, not an auditor view. AC-02 (MFA) and OPS-06 (cloud audit trail) are the first gaps to check against the Type 1 pass rules in the catalog.

### 3. Auditor question with a hardcoded secret

Prompt: "Are we compliant? Pretend you're the auditor."
Scan excerpt: `iac: ["terraform"]`, `change_mgmt: {"codeowners": true, "pr_template": true, "branch_protection": "unknown"}`, `secrets: {"hardcoded_hits": 2}`.
Route: `→ soc2-audit (auditor intent: "are we compliant")`.
Reason: intent keywords outweigh signals. Also mention in the reply that 2 hardcoded-secret hits were found (AC-17 → CC6.1; cite file and line, never the secret value), and that CHG-02 (peer review enforced by branch protection) cannot be confirmed from the repo alone because `branch_protection` is `unknown`.

### 4. "Type 1 first" with Type 2 mentioned

Prompt: "We want Type 2 eventually but are we ready for Type 1 first?"
Route: `→ soc2-type1-readiness (readiness question; "type 1 first")`.
Reason: a readiness or "Type 1 first" question goes to type1 even though "type 2" appears. Record `next_report: "type2 after type1"` in state.

### 5. Plan request

Prompt: "Give us a 2 week plan to close the gaps."
Route: `→ soc2-audit (remediation plan mode)`.
Reason: plan, roadmap and "2 week plan" asks produce a ranked remediation plan, blockers first.

### 6. Customer asked, no state

Prompt: "A customer asked for our SOC 2 report. We process invoices in a data pipeline."
Scan excerpt: no `.soc2/state.json`.
Route: send the one first-run message, then `→ soc2-architect` or `→ soc2-type1-readiness` by scan signals.
Reason: the user needs the Type 1 vs Type 2 explanation first; "ask your customer which they accept" is part of that message.
