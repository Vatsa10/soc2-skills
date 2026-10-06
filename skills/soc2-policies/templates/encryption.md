# Encryption and Key Management Policy

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

This policy sets cryptographic standards for protecting data in transit and at rest and for managing keys over their lifecycle.

## Scope

All {{company}} systems, networks, endpoints, backups and third-party services that handle {{company}} or customer data.

## Policy statements

_Numbers and timeframes in these statements are defaults. {{owner}} must confirm {{company}} can meet each one before approving this policy, because an auditor tests against the policy as written. Statements that start with "(if ... in scope)" apply only when that category is in the audit scope._

1. All data in transit over public or untrusted networks uses TLS 1.2 or higher, with TLS 1.3 enabled and preferred on internet-facing endpoints; SSL, TLS 1.0 and TLS 1.1 are disabled. [AC-10 → CC6.7]
2. Data at rest in databases, object storage, volumes and backups is encrypted with AES-256 or the cloud provider's equivalent managed encryption. [AC-09 → CC6.1]
3. Laptops and mobile devices use full-disk encryption (FileVault, BitLocker or equivalent), verified by device management. [AC-15 → CC6.7]
4. Encryption keys are created and stored in a managed key service ({{cloud_kms}}) and never stored in source code or in plaintext config. [AC-11 → CC6.1]
5. Customer-managed keys are rotated at least annually, and automatic rotation is enabled where supported. [AC-11 → CC6.1]
6. Access to administer keys is limited to named key custodians, requires MFA, and is logged. [AC-11 → CC6.1]
7. Only industry-standard algorithms are used: AES-256, RSA 2048-bit or larger, ECDSA P-256 or larger, SHA-256 or stronger; MD5 and SHA-1 are prohibited for security purposes. [CTL-03 → CC5.2]
8. Passwords are stored using a salted adaptive hash (argon2id, bcrypt or scrypt). [AC-08 → CC6.1]
9. TLS certificates are issued by a trusted CA, renewed automatically, and monitored for expiry with an alert 30 days before expiration. [AC-10 → CC6.7]
10. A compromised key is revoked and replaced within 24 hours and handled under the Incident Response Policy. [OPS-10 → CC7.4]
11. Encryption configuration is reviewed at least annually and exceptions are recorded with an expiry date. [CTL-04 → CC5.3]
12. Keys are generated inside the managed key service and never exported in plaintext; a key is scheduled for deletion only after the data it protects is deleted or re-encrypted, with the approval recorded in a ticket. [AC-11 → CC6.1]

## Roles

| Role | Responsibility |
|---|---|
| {{owner}} | Owns the standards and approves algorithm exceptions. |
| Engineering lead | Implements and verifies encryption and key rotation. |
| Key custodians | Named individuals with access to administer keys. |

## Exceptions

Exceptions to this policy must be requested in writing, state the business reason and compensating controls, and be approved by {{owner}} (and by the most senior executive for exceptions affecting Restricted data). Each exception expires after at most 12 months and is recorded in the exceptions register, a dated list kept by {{owner}} with requester, reason, compensating controls, approver and expiry.

## Enforcement

Violations are investigated by {{owner}} and People Operations (or whoever handles HR). Confirmed violations may result in access removal, retraining, disciplinary action up to termination, and termination of contractor agreements. Violations that expose customer data are handled under the Incident Response Policy.

## Review and approval

This policy is reviewed on the cadence in the header ({{review_cadence}}), and also after any major incident or material change to systems or scope. Approval (approver name and date) is recorded in the header and in the revision history below; version-control history alone is not evidence of approval. After a material change, all personnel re-acknowledge the policy set within 30 days (Information Security Policy, statement 5). Next review is due by the date in the header.

| Version | Date | Change | Approved by |
|---|---|---|---|
| {{version}} | {{effective_date}} | Initial issue | {{approver}} |
