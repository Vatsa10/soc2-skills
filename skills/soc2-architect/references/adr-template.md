# ADR Template

> This skill prepares for a SOC 2 audit; it is not an attestation. Only a licensed CPA firm can issue a SOC 2 Type 1 or Type 2 report.

Write one ADR per significant design choice that satisfies or affects a SOC 2 control (identity provider, encryption approach, logging pipeline, tenancy model, backup strategy, CI/CD design, vendor selection). Save as `docs/soc2/adr/NNNN-<slug>.md` in the user's repo, where `NNNN` is the next zero-padded number (0001, 0002, ...) and `<slug>` is a short kebab-case title.

Auditors read ADRs as evidence of design (Type 1) and of change management (Type 2). Keep them factual and dated. Never edit an accepted ADR to change its decision; add a new ADR that supersedes it and update the old one's Status.

## Template

```markdown
# NNNN. <Title>

- Status: Proposed | Accepted | Superseded by NNNN | Deprecated
- Date: YYYY-MM-DD
- Deciders: <names or roles>

## Context

What problem or requirement forces this decision? Include system type, data classes involved,
cloud, scale, and the SOC 2 scope (TSC and report type) that constrains the choice.

## Decision

The choice made, in one or two sentences, with the concrete service or configuration
(for example "Okta as IdP with MFA enforced via sign-on policy; AWS IAM Identity Center via SAML").

## Controls satisfied

Look up each ID (index: `../../soc2/references/control-index.md`; full entry: search `### <ID>` in `../../soc2/references/control-catalog.md`); copy the TSC from its `TSC:` line.

| Control → TSC | How this decision satisfies it |
|---|---|
| <ID> → <criteria from catalog> | <one sentence> |

## Evidence produced (Type 2)

Every control above must name an automated evidence source. If none exists, say so and open a follow-up.

| Control | Evidence artifact | Source system | Frequency (catalog value) | Owner (role) | Collection method |
|---|---|---|---|---|---|
| <ID> | <artifact> | <system/API> | <Continuous/automated, Per event, Daily, Weekly, Monthly, Quarterly or Annual> | <role> | <scheduled job, export, or API pull> |

Type 1 pass (design and implementation, single instance as of a date): <what will be shown>
Type 2 pass (operated across the period): <what the sample will show>

Gaps (controls with no automated evidence): <list, or "none">

## Alternatives

| Option | Why not chosen |
|---|---|
| <option> | <reason: cost, control coverage, evidence gaps, operational burden> |

## Consequences

- Positive: <what gets easier or stronger>
- Negative: <cost, lock-in, operational burden>
- Follow-ups: <tasks, owners, dates>
- Revisit when: <trigger, such as a significant change that requires risk reassessment (RSK-04)>
```

## Rules

- Use real catalog IDs and the TSC from the catalog entry. Do not invent IDs or mappings.
- Fill `Evidence produced` for Type 1 projects too; it is cheap now and required once the Type 2 period starts.
- Record each ADR in `.soc2/state.json` under `decisions` as `{"control": "<ID>", "choice": "<short choice>", "date": "<YYYY-MM-DD>", "adr": "NNNN"}`, one entry per control the ADR satisfies. The `adr` value is the 4-digit ADR number as a string (for example "0003", never a path or "3"), so later skills can open `docs/soc2/adr/NNNN-*.md`.
