# Encryption and Key Management Policy

| Field | Value |
|---|---|
| Company | {{company}} |
| Policy owner | {{owner}} |
| Effective date | {{effective_date}} |
| Review cadence | {{review_cadence}} |

## Purpose

This policy sets cryptographic standards for protecting data in transit and at rest and for managing keys over their lifecycle.

## Scope

All {{company}} systems, networks, endpoints, backups and third-party services that handle {{company}} or customer data.

## Policy statements

1. All data in transit over public or untrusted networks uses TLS 1.2 or higher; SSL, TLS 1.0 and TLS 1.1 are disabled. [AC-01 → CC6.1]
2. Data at rest in databases, object storage, volumes and backups is encrypted with AES-256 or the cloud provider's equivalent managed encryption. [AC-02 → CC6.2]
3. Laptops and mobile devices use full-disk encryption (FileVault, BitLocker or equivalent), verified by device management. [AC-03 → CC6.1]
4. Encryption keys are created and stored in a managed key service (such as AWS KMS, Google Cloud KMS or Azure Key Vault) and never stored in source code or in plaintext config. [AC-04 → CC6.7]
5. Customer-managed keys are rotated at least annually, and automatic rotation is enabled where supported. [AC-05 → CC6.6]
6. Access to administer keys is limited to named key custodians, requires MFA, and is logged. [AC-03 → CC6.1]
7. Only industry-standard algorithms are used: AES-256, RSA 2048-bit or larger, ECDSA P-256 or larger, SHA-256 or stronger; MD5 and SHA-1 are prohibited for security purposes. [CTL-01 → CC5.1]
8. Passwords are stored using a salted adaptive hash (argon2id, bcrypt or scrypt). [AC-05 → CC6.6]
9. TLS certificates are issued by a trusted CA, renewed automatically, and monitored for expiry with an alert 30 days before expiration. [MON-01 → CC4.1]
10. A compromised key is revoked and replaced within 24 hours and handled under the Incident Response Policy. [OPS-01 → CC7.2]
11. Encryption configuration is reviewed at least annually and exceptions are recorded with an expiry date. [CTL-02 → CC5.3]

## Roles

| Role | Responsibility |
|---|---|
| {{owner}} | Owns the standards and approves algorithm exceptions. |
| Engineering lead | Implements and verifies encryption and key rotation. |
| Key custodians | Named individuals with access to administer keys. |

## Exceptions

Exceptions to this policy must be requested in writing, state the business reason and compensating controls, and be approved by {{owner}} (and by the CEO for exceptions affecting Restricted data). Each exception expires after at most 12 months and is recorded in the exceptions register.

## Enforcement

Violations are investigated by {{owner}} and People Operations. Confirmed violations may result in access removal, retraining, disciplinary action up to termination, and termination of contractor agreements. Violations that expose customer data are handled under the Incident Response Policy.

## Review

This policy is reviewed on the cadence in the header ({{review_cadence}}), and also after any major incident or material change to systems or scope. The effective date and approver are recorded in version control history. Next review is due before the end of the cadence period following {{effective_date}}.
