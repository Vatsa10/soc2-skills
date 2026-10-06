# Router Eval Cases

## Test Matrix

| # | Prompt | Repo State | Expected Route/Chain | Scan Signals | Result (Claude) | Result (Codex) |
|---|--------|-----------|----------------------|-----------------|---|---|
| 1 | "Let's design a multi-tenant SaaS for HR data" | empty | `soc2-architect` | iac=[], ci=[], no code | pending (manual) | pending (manual) |
| 2 | "We need SOC 2, where do we start?" | empty | `soc2-architect` | iac=[], ci=[], no code | pending (manual) | pending (manual) |
| 3 | "Are our controls in place for Type 1?" | tf_aws | `soc2-type1-readiness` | iac=[terraform], ci=[github-actions], auth.sso=false, auth.mfa_hint=false, monitoring.alerts=false, incident.runbook=false | pending (manual) | pending (manual) |
| 4 | "Our Type 2 audit period starts in March, set up evidence collection" | tf_aws | `soc2-type2-operations` | iac=[terraform], ci=[github-actions], logging.centralized=true, backups.configured=true, but evidence automation needed | pending (manual) | pending (manual) |
| 5 | "Audit this repo for SOC 2" | bare_app | `soc2-audit` | code present, secrets.hardcoded_hits=1 (AWS_KEY on app.py:1), privacy.pii_fields=true (email, date_of_birth on app.py:3) | pending (manual) | pending (manual) |
| 6 | "Write our access control policy" | any | `soc2-policies` | policies=[], explicit policy request | pending (manual) | pending (manual) |
| 7 | "Make us SOC 2 ready end to end" | empty | `architect → policies → type1-readiness → type2-operations` | iac=[], ci=[], no code, full chain request (assumes `report_type: type2`; with `type1` the chain stops at type1-readiness) | pending (manual) | pending (manual) |
| 8 | Mid-conversation: architect session, then the team writes the Terraform, then "now check what we built" | tf_aws (after architect phase) | `soc2-type1-readiness` | type1 intent keyword "check what we built" (routing.md); intent beats tie-breaker 5 | pending (manual) | pending (manual) |
| 9 | "Add a new payments service" | repo with `.soc2/state.json` | `soc2-architect` | design intent + .soc2 marker present | pending (manual) | pending (manual) |
| 10 | "Use soc2-audit" (intent: audit skill) | empty or any | `soc2-audit` | explicit skill name override | pending (manual) | pending (manual) |

---

## Scan Signal References

### empty fixture
```json
{
  "iac": [],
  "ci": [],
  "cloud": [],
  "auth": {"sso": false, "mfa_hint": false, "idp": []},
  "policies": [],
  "incident": {"runbook": false}
}
```
**Routing signal:** Design phase (no code/IaC); precedence: architect.

### tf_aws fixture
```json
{
  "iac": ["terraform"],
  "ci": ["github-actions"],
  "cloud": ["aws"],
  "auth": {"sso": false, "mfa_hint": false},
  "logging": {"cloudtrail": true, "centralized": true, "retention_days": 400},
  "backups": {"configured": true, "restore_test": false},
  "monitoring": {"alerts": false},
  "incident": {"runbook": false},
  "policies": []
}
```
**Routing signal:** Code/IaC present with partial controls; missing auth (`AC-02 → CC6.1, CC6.2`), alerting (`OPS-08 → CC7.2, CC7.3`), incident response (`OPS-10 → CC7.4`). Precedence: type1-readiness.

### bare_app fixture
```json
{
  "iac": [],
  "ci": [],
  "cloud": ["aws"],
  "secrets": {"hardcoded_hits": 1},
  "privacy": {"pii_fields": true}
}
```
**Files:**
- `app.py:1` — AWS_KEY = "AKIAABCDEFGHIJKLMNOP" (hardcoded secret, `AC-17 → CC6.1, CC6.7`)
- `app.py:3` — PII fields: email, date_of_birth (`PR-03 → P3.1`, `CF-01 → C1.1, CC2.1`)

**Routing signal:** Audit scope (hardcoded secret, PII without controls). Precedence: audit.

---

## How to Run

### Install SOC 2 skills

#### Claude Code
1. Run: `python scripts/install.py --target claude --dest <scratchpad>/claude-skills-test`
   - Should create 6 folders in the destination
2. Confirm exit code 0 and presence of: `soc2-architect`, `soc2-policies`, `soc2-type1-readiness`, `soc2-type2-operations`, `soc2-audit`, `soc2`
3. In Claude Code, load the skill manually or via:
   - `/plugin marketplace add Vatsa10/soc2-skills` (if available)
   - `/plugin install soc2-skills@soc2-skills`
   - Or import via the installed destination folder

#### Codex
1. Run: `python scripts/install.py --target codex --dest <scratchpad>/codex-skills-test`
   - Should create 6 folders in the destination
2. Confirm exit code 0 and presence of: `soc2`, `soc2-architect`, `soc2-policies`, `soc2-type1-readiness`, `soc2-type2-operations`, `soc2-audit`
3. In Codex, point to the skill destination or import via the installed folder

### Run eval cases

For each case:
1. Create a fresh session (Claude Code or Codex)
2. Copy the prompt from the table
3. Point to the repo state (empty, tf_aws, or bare_app from tests/fixtures/)
4. Run the prompt and observe which route the router chooses
5. Record the result in the table (which skill/phase was invoked)

---

## Notes

- Results columns show "pending (manual)" because routing output depends on interactive LLM sessions; the human runner fills these after testing.
- Hardcoded secret in bare_app (app.py:1) matches AWS access key pattern `AKIA[0-9A-Z]{16}`.
- Case 8 assumes the architect phase has already run and `.soc2/state.json` exists with `"completed": ["soc2-architect"]`, and that code/IaC (the tf_aws fixture) now exists.
- Case 9 requires a `.soc2/state.json` marker in the repo (router checks for it as a signal).
- Case 10 tests explicit skill override: even if signals point elsewhere, naming a skill wins.
