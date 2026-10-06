# soc2-audit modes

This skill prepares for a SOC 2 audit; it is not an attestation. Only a licensed CPA firm can issue a SOC 2 Type 1 or Type 2 report.

## Full gap

Follow the procedure in `SKILL.md`. Omit the "Exceptions likely" section for Type 1.

## Type 2 gap

Full gap plus, per control:

- Evidence continuity: will evidence exist for the whole period, not just now? Look for a scheduled control that has not yet run (a deviation once its due date passes), a missed cycle, a gap in continuous logging, an annual item (training, pen test, policy review) that lapses mid-period, or a mid-period change.
- Event-driven controls with no triggering event (no incidents, no terminations) are reported by auditors as "no occurrence, not tested", not as exceptions. Keep evidence that nothing occurred (an empty population report).
- Sampling simulation: take the control's catalog `Frequency`, pick a sample size from the catalog sampling guide (common practice, not AICPA mandates; per-event controls about 25 or the full population if small), spread samples across the period including the first month, and test each against `Type 2 pass`. Plan for zero tolerance: one failing sample usually means expanded testing or a reported deviation. Put it in "Exceptions likely".
- Automated controls: a test of one stands only if the ITGCs (AC-*, CHG-*) are effective for the whole period.
- Periods shorter than 12 months use proportionally smaller samples; some report users do not accept periods under 6 months.

If the window has started or ended and most controls are `missing`: say plainly the elapsed part cannot be backfilled, and offer a later window or a Type 1.

## Pre-period readiness

Used when the Type 2 window starts after today. No sampling simulation. For each control give an "evidence live by" date: the window start for continuous and per-event controls; the first scheduled run inside the window for periodic controls (and it must actually run). Flag controls whose first run would fall after the window ends. Severity follows the rubric: not-yet-built is at most Medium unless there is live exposure.

## PBC-only

For "what will the auditor ask us for". Read existing `docs/soc2/*` and the control index; do not re-evaluate controls. Output only the PBC section of the report template (to `docs/soc2/pbc-list.md`), grouped by source system with merge keys, IPE parameters for populations, and the "Report deliverables you own" rows. For Type 2, request full populations for the whole period.

## Remediation plan

For "plan", "roadmap", "2 week plan". Use the latest `docs/soc2/audit-report.md`; run a full gap first only if it does not exist. Horizon: the one the user named (for example 2 weeks: day-by-day or per-day-block), else 30/60/90 days. Order: Do today (Blockers), then non-backfillable Type 2 controls, then High, Medium, Low. Each item: finding #, `ID → TSC`, owner role from the catalog, done-when (the `Type 1 pass` or `Type 2 pass` condition). Write it to section 7 of the report, or `docs/soc2/remediation-plan.md` when no report is being written. For Type 2, a fix that changes a control mid-period goes through change management with an effective date.
