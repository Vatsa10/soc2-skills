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

Look up each ID in `../../soc2/references/control-catalog.md`; copy the TSC from its `TSC:` line.

| Control → TSC | How this decision satisfies it |
|---|---|
| <ID> → <criteria from catalog> | <one sentence> |

## Evidence produced (Type 2)

Every control above must name an automated evidence source. If none exists, say so and open a follow-up.

| Control | Evidence artifact | Source system | Frequency | Collection method |
|---|---|---|---|---|
| <ID> | <artifact> | <system/API> | <cadence> | <scheduled job, export, or API pull> |

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
- Record each ADR in `.soc2/state.json` under `decisions` as `{"control": "<ID>", "choice": "<short choice>", "date": "<YYYY-MM-DD>"}`, one entry per control the ADR satisfies.
