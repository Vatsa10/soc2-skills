# Secure Development Lifecycle Policy

| Field | Value |
|---|---|
| Company | {{company}} |
| Policy owner | {{owner}} |
| Approver | {{approver}} |
| Approval date | {{approval_date}} |
| Version | {{version}} |
| Effective date | {{effective_date}} |
| Review cadence | {{review_cadence}} |
| Next review due | {{next_review}} |

## Purpose

This policy ensures software built by {{company}} is designed, written, tested and released securely. It complements the Change Management Policy, which governs how changes reach production.

## Scope

All application code, infrastructure-as-code, build pipelines and third-party libraries that are part of the in-scope services.

## Policy statements

_Numbers and timeframes in these statements are defaults. {{owner}} must confirm {{company}} can meet each one before approving this policy, because an auditor tests against the policy as written. Statements that start with "(if ... in scope)" apply only when that category is in the audit scope._

1. A new service, or a change that adds an external interface, a new data class or a new authentication path, receives a written design review (data flows, trust boundaries, abuse cases and mitigations) recorded in the design document or ADR before implementation starts. [CHG-05 → CC8.1] [RSK-04 → CC3.4]
2. {{company}} follows a written secure coding standard that covers input validation, output encoding, authentication and session handling, authorization checks, error handling without data leakage, and use of parameterized queries. Engineers are trained on it annually. [CTL-03 → CC5.2] [GOV-05 → CC1.4]
3. Every merge to the production branch passes automated static analysis (SAST), dependency vulnerability scanning and secret scanning in CI; findings at or above the blocking severity ({{sast_block_severity}}) stop the merge until fixed or risk-accepted in writing. [OPS-03 → CC7.1] [OPS-02 → CC7.1] [CHG-04 → CC8.1]
4. Dynamic testing (DAST or an equivalent authenticated scan) of internet-facing applications runs at least {{dast_cadence}}, and an external penetration test is performed at least annually and after major architecture changes. [MON-02 → CC7.1]
5. Secrets, keys and credentials are never committed to source control; secret scanning runs on every push, and any exposed secret is revoked and rotated within 24 hours. [AC-17 → CC6.1]
6. A software bill of materials or dependency inventory is generated for each release; direct and transitive dependencies are pinned through lockfiles and updated automatically or at least monthly. [OPS-02 → CC7.1]
7. Vulnerable dependencies and code findings are remediated within the deadlines in Logging and Monitoring Policy statement 9. [OPS-02 → CC7.1]
8. New open-source dependencies are checked for licence compatibility and maintenance health (active maintainer, no unresolved critical advisories) before adoption. [OPS-02 → CC7.1]
9. Build artifacts are produced only by the CI/CD pipeline, stored in an access-controlled registry, and deployed from there; where the platform supports it, artifacts are signed and the signature is verified at deploy time. [CHG-06 → CC8.1]
10. Production secrets and customer data are not available in development or test environments; test data is synthetic or masked. [CF-06 → C1.1] [CHG-06 → CC5.2]
11. Before each release that changes authentication, authorization, encryption or data handling, a named reviewer other than the author confirms the security checks passed and records the sign-off in the pull request or release ticket. [CHG-02 → CC8.1] [CHG-05 → CC8.1]
12. Code that implements authentication, authorization, payments or encryption is listed in a code-owners file so that changes require review by a designated owner. [CHG-03 → CC8.1]
13. (if processing_integrity in scope) Code that accepts external input has automated tests for validation (type, range, required fields) and rejected inputs are logged. [PI-02 → PI1.2]

## Roles

| Role | Responsibility |
|---|---|
| Engineering lead | Owns the secure coding standard, CI security gates and release sign-off. |
| Engineers | Follow the standard, fix findings and complete annual training. |
| {{owner}} | Owns this policy and reviews exceptions and risk acceptances. |

## Exceptions

Exceptions to this policy must be requested in writing, state the business reason and compensating controls, and be approved by {{owner}} (and by the most senior executive for exceptions affecting Restricted data). Each exception expires after at most 12 months and is recorded in the exceptions register, a dated list kept by {{owner}} with requester, reason, compensating controls, approver and expiry.

## Enforcement

Violations are investigated by {{owner}} and People Operations (or whoever handles HR). Confirmed violations may result in access removal, retraining, disciplinary action up to termination, and termination of contractor agreements. Violations that expose customer data are handled under the Incident Response Policy.

## Review and approval

This policy is reviewed on the cadence in the header ({{review_cadence}}), and also after any major incident or material change to systems or scope. Approval (approver name and date) is recorded in the header and in the revision history below; version-control history alone is not evidence of approval. After a material change, all personnel re-acknowledge the policy set within 30 days (Information Security Policy, statement 5). Next review is due by the date in the header.

| Version | Date | Change | Approved by |
|---|---|---|---|
| {{version}} | {{effective_date}} | Initial issue | {{approver}} |
