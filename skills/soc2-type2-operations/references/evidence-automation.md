# Evidence automation snippets

> This skill prepares for a SOC 2 audit; it is not an attestation. Only a licensed CPA firm can issue a SOC 2 Type 1 or Type 2 report.

Ready-to-adapt snippets for `soc2-type2-operations`. Each is tagged with catalog control IDs (`../../soc2/references/control-catalog.md`). Adapt names, regions, and org/repo values; ask the user before writing any file into their repo. Snippets assume GitHub plus AWS; translate the same pattern for GitLab, GCP, or Azure.

Retention rule used throughout: keep evidence for the audit period plus one year. Log groups use 400 days (a full year of lookback plus slack for fieldwork, OPS-07 → CC7.2). The evidence bucket lock is a variable: audit period in days plus 365 (730 for a 12-month period).

## 1. Scheduled evidence export (GitHub Actions)

Controls: CHG-02 → CC8.1, CHG-03 → CC8.1, CHG-04 → CC8.1, CHG-05 → CC8.1, OPS-02 → CC7.1, MON-01 → CC4.1.

Facts that shape the design:
- GitHub Actions artifact `retention-days` accepts 1 to 90 days on public repositories and 1 to 400 days on private and internal repositories (repository, organization, or enterprise settings set the cap). Artifacts are still deletable by anyone with write access and a 400-day maximum falls short of audit period plus one year, so treat them as staging and copy every export to object-locked storage (section 2). The snippet below uses 90 days, which is valid everywhere.
- The default `GITHUB_TOKEN` cannot read branch protection or Dependabot alerts. Use a fine-grained PAT or GitHub App token stored as the secret `EVIDENCE_GH_TOKEN`, with read-only Administration (branch protection), Dependabot alerts, Actions, and Pull requests permissions. Record its rotation (AC-17 → CC6.1).
- Reach AWS through OIDC (`id-token: write`), not long-lived access keys.

`.github/workflows/soc2-evidence-export.yml`:

```yaml
name: soc2-evidence-export

on:
  schedule:
    - cron: "0 6 1 * *"   # monthly, 06:00 UTC on the 1st
  workflow_dispatch: {}

permissions:
  contents: read
  id-token: write          # OIDC to AWS

jobs:
  export:
    runs-on: ubuntu-latest
    env:
      GH_TOKEN: ${{ secrets.EVIDENCE_GH_TOKEN }}
      REPO: ${{ github.repository }}
      DEFAULT_BRANCH: ${{ github.event.repository.default_branch }}
    steps:
      - name: Set export date
        run: echo "EXPORT_DATE=$(date -u +%Y-%m-%d)" >> "$GITHUB_ENV"

      - name: Export branch protection (CHG-02 → CC8.1, CHG-03 → CC8.1, CHG-04 → CC8.1)
        run: |
          mkdir -p evidence
          gh api "repos/${REPO}/branches/${DEFAULT_BRANCH}/protection" \
            > "evidence/branch-protection-${EXPORT_DATE}.json"

      - name: Export open Dependabot alerts (OPS-02 → CC7.1)
        run: |
          gh api --paginate "repos/${REPO}/dependabot/alerts?state=open&per_page=100" \
            > "evidence/dependabot-open-${EXPORT_DATE}.json"

      - name: Export workflow run history (CHG-04 → CC8.1, MON-01 → CC4.1)
        run: |
          SINCE=$(date -u -d '31 days ago' +%Y-%m-%d)
          gh api --paginate "repos/${REPO}/actions/runs?per_page=100&status=completed&created=%3E%3D${SINCE}" \
            --jq '.workflow_runs[] | {id, name, head_branch, head_sha, event, conclusion, created_at, html_url}' \
            | jq -s '.' > "evidence/workflow-runs-${EXPORT_DATE}.json"

      - name: Export merged PRs with reviews, last 31 days (CHG-02 → CC8.1, CHG-05 → CC8.1)
        run: |
          SINCE=$(date -u -d '31 days ago' +%Y-%m-%d)
          # --limit 500 can truncate a very busy month; check the count and raise it if needed
          gh pr list --repo "${REPO}" --state merged --limit 500 \
            --search "merged:>=${SINCE}" \
            --json number,title,author,mergedAt,mergedBy,reviews,body,url \
            > "evidence/merged-prs-${EXPORT_DATE}.json"

      - name: Hash the export
        run: cd evidence && sha256sum ./*.json > "SHA256SUMS-${EXPORT_DATE}.txt"

      - name: Stage as artifact (staging only; the object-locked copy is the evidence)
        uses: actions/upload-artifact@v4
        with:
          name: soc2-evidence-${{ env.EXPORT_DATE }}
          path: evidence/
          retention-days: 90

      - name: Configure AWS credentials (OIDC)
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::111122223333:role/soc2-evidence-writer
          aws-region: us-east-1

      - name: Copy to the object-locked evidence bucket (lock = var.evidence_retention_days)
        run: |
          aws s3 cp evidence/ "s3://example-soc2-evidence/github/${EXPORT_DATE}/" --recursive
```

Notes for the user:
- The `soc2-evidence-writer` role needs `s3:PutObject` on the evidence bucket only, with no delete permission.
- A failed run is an exception the auditor can see; open a ticket per failure (MON-03 → CC4.2).
- Auditors sample the whole period, so the workflow must run on schedule from day one. Do not enable it halfway through a period without telling the auditor.

## 2. Terraform: log retention, evidence bucket, backups

Controls: OPS-05 → CC7.2, OPS-06 → CC7.2, OPS-07 → CC7.2, CF-03 → C1.1, AV-03 → A1.2, AV-04 → A1.3.

Targets the current AWS provider (v5 or later). S3 object lock is configured with the separate `aws_s3_bucket_object_lock_configuration` resource; the bucket must be created with `object_lock_enabled = true` and must have versioning enabled.

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
  }
}

# --- Log retention (OPS-07 → CC7.2, OPS-05 → CC7.2) ---------------------------------------
resource "aws_kms_key" "logs" {
  description         = "CloudWatch log encryption"
  enable_key_rotation = true
  # Add a key policy that lets logs.<region>.amazonaws.com use the key.
}

resource "aws_cloudwatch_log_group" "app" {
  name              = "/example/app"
  retention_in_days = 400 # valid CloudWatch value; covers a 12-month lookback
  kms_key_id        = aws_kms_key.logs.arn
}

variable "evidence_retention_days" {
  type        = number
  description = "Audit period length in days plus 365. Example: 12-month period gives 730."
  default     = 730
}

# --- Evidence bucket with object lock (OPS-07 → CC7.2, CF-03 → C1.1) ---------------------
resource "aws_s3_bucket" "evidence" {
  bucket              = "example-soc2-evidence"
  object_lock_enabled = true
}

resource "aws_s3_bucket_versioning" "evidence" {
  bucket = aws_s3_bucket.evidence.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_object_lock_configuration" "evidence" {
  bucket = aws_s3_bucket.evidence.id

  rule {
    default_retention {
      mode = "COMPLIANCE" # no one, including root, can shorten or delete
      days = var.evidence_retention_days # audit period in days + 365; compute it, do not hardcode
    }
  }

  depends_on = [aws_s3_bucket_versioning.evidence]
}

resource "aws_s3_bucket_server_side_encryption_configuration" "evidence" {
  bucket = aws_s3_bucket.evidence.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.logs.arn # or a dedicated evidence key; omit to use the AWS-managed key
    }
  }
}

resource "aws_s3_bucket_public_access_block" "evidence" {
  bucket                  = aws_s3_bucket.evidence.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# --- Backups (AV-03 → A1.2) ------------------------------------------------------
resource "aws_backup_vault" "main" {
  name = "example-backup-vault"
}

resource "aws_backup_plan" "daily" {
  name = "daily-35d"

  rule {
    rule_name         = "daily"
    target_vault_name = aws_backup_vault.main.name
    schedule          = "cron(0 5 * * ? *)"

    lifecycle {
      delete_after = 35
    }
  }
}

resource "aws_iam_role" "backup" {
  name = "example-backup-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Action    = "sts:AssumeRole"
      Principal = { Service = "backup.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "backup" {
  role       = aws_iam_role.backup.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSBackupServiceRolePolicy"
}

resource "aws_backup_selection" "tagged" {
  name         = "tagged-backup-true"
  plan_id      = aws_backup_plan.daily.id
  iam_role_arn = aws_iam_role.backup.arn

  selection_tag {
    type  = "STRINGEQUALS"
    key   = "backup"
    value = "true"
  }
}
```

Backup retention note: the 35-day backup lifecycle is an operational choice, separate from the evidence retention (`var.evidence_retention_days`: audit period in days plus 365). The evidence for AV-03 → A1.2 is the job success history (export it with section 1's pattern, for example `aws backup list-backup-jobs`), which belongs in the locked bucket.

Restore-test reminder (AV-04 → A1.3): a backup that was never restored is not evidence of recoverability. Pick one:
- AWS Backup restore testing (`aws_backup_restore_testing_plan` and `aws_backup_restore_testing_selection` in recent v5 provider releases), which restores on a schedule and records validation results (its role also needs the `AWSBackupServiceRolePolicyForRestores` managed policy); or
- a quarterly issue that a named engineer closes by attaching a restore report with date, data set, duration, and verification result. Opener workflow, `.github/workflows/soc2-evidence-restore-reminder.yml`:

```yaml
name: soc2-evidence-restore-reminder

on:
  schedule:
    - cron: "0 9 1 1,4,7,10 *"   # 09:00 UTC on the 1st of Jan, Apr, Jul, Oct
  workflow_dispatch: {}

permissions:
  issues: write

jobs:
  open-issue:
    runs-on: ubuntu-latest
    steps:
      - name: Open restore-test issue (AV-04 → A1.3)
        env:
          GH_TOKEN: ${{ github.token }}
        run: |
          gh issue create --repo "${{ github.repository }}" \
            --title "Backup restore test - $(date -u +%Y-%m)" \
            --label "soc2" \
            --body "Restore the latest production backup into an isolated environment. Attach: restore date, data set, duration, verification results, and who ran it. Close when done (AV-04 → A1.3)."
```

## 3. Quarterly access review (issue template and opener)

Controls: AC-05 → CC6.2, AC-04 → CC6.2, AC-06 → CC6.1, AC-07 → CC6.1.

The reviewer must not be the owner of the access being reviewed. `.github/ISSUE_TEMPLATE/access-review.md`:

```markdown
---
name: Quarterly access review
about: SOC 2 user access review (AC-05 → CC6.2)
title: "Access review - YYYY-QN"
labels: soc2
assignees: ""
---

## Scope

Systems in scope (check each; attach a user listing exported on the date below):

- [ ] Identity provider (users, groups, MFA status)
- [ ] Cloud console / IAM (AWS, GCP, Azure)
- [ ] Source control organization (members, owners, deploy keys)
- [ ] Production database access
- [ ] Other critical systems: ______

## Evidence

- Export date: ____-__-__
- Attach complete user listings (CSV, or screenshot with the date visible). Partial lists are not accepted by auditors.

## Review

- [ ] Every account maps to a current employee or approved contractor
- [ ] Terminated users compared against the HR roster; all disabled (AC-04 → CC6.2)
- [ ] Privileged and admin roles justified (AC-07 → CC6.1)
- [ ] Role assignments match job function (AC-06 → CC6.1)
- [ ] MFA enforced on every account

## Findings and remediation

| Account | Issue | Action | Ticket | Done date |
|---|---|---|---|---|
|  |  |  |  |  |

## Sign-off

Reviewer (not the access owner): ______  Date: ____-__-__
Approver: ______  Date: ____-__-__
```

Scheduled opener, `.github/workflows/soc2-evidence-access-review.yml`:

```yaml
name: soc2-evidence-access-review

on:
  schedule:
    - cron: "0 9 1 1,4,7,10 *"   # quarterly
  workflow_dispatch: {}

permissions:
  issues: write

jobs:
  open-issue:
    runs-on: ubuntu-latest
    steps:
      - name: Open quarterly access review issue (AC-05 → CC6.2)
        env:
          GH_TOKEN: ${{ github.token }}
        run: |
          gh issue create --repo "${{ github.repository }}" \
            --title "Access review - $(date -u +%Y-%m)" \
            --label "soc2" \
            ${{ vars.ACCESS_REVIEWER && format('--assignee {0}', vars.ACCESS_REVIEWER) || '' }} \
            --body "Run the quarterly access review. Follow the checklist in .github/ISSUE_TEMPLATE/access-review.md: export complete user listings, compare against the HR roster, remove or justify access, then record sign-off here (AC-05 → CC6.2)."
```

Close each issue only after every removal ticket is closed. The closed issue, attached listings, and removal tickets are the sampled evidence.

## 4. Change management: PR template and CODEOWNERS

Controls: CHG-02 → CC8.1, CHG-03 → CC8.1, CHG-05 → CC8.1, CTL-02 → CC5.1.

`.github/pull_request_template.md`:

```markdown
## What and why

<!-- Describe the change and the reason. -->

## Ticket

Ticket link (required): <!-- e.g. https://example.atlassian.net/browse/ABC-123 -->

## Risk and testing

- [ ] Tests added or updated; CI is green
- [ ] Rollback plan: <!-- how to revert -->
- [ ] Touches auth, encryption, logging, or infrastructure? Code owner review requested
- [ ] Emergency change? If yes, link the follow-up review ticket (CHG-07 → CC8.1)

## Approval

At least one approval from someone other than the author is required before merge.
```

`.github/CODEOWNERS` (adapt teams and paths):

```
# Sensitive paths require review from the named team (CHG-03 → CC8.1)
/infra/                 @example-org/platform-security
/terraform/             @example-org/platform-security
/.github/workflows/     @example-org/platform-security
/.github/CODEOWNERS     @example-org/platform-security
/src/auth/              @example-org/security
/migrations/            @example-org/data-owners
```

The template and CODEOWNERS do nothing unless branch protection enforces them. On the default branch enable: require a pull request with at least 1 approval, require review from code owners, dismiss stale approvals, require status checks, include administrators, and block force pushes. The monthly export in section 1 captures this setting as evidence (CHG-02 → CC8.1). A ticket link in the template is only a convention; add a CI check that fails when the PR body has no ticket URL if you want it system-enforced (CHG-05 → CC8.1).

## 5. Incident response: runbook skeleton and annual tabletop

Controls: OPS-09 → CC7.3, OPS-10 → CC7.4, OPS-11 → CC7.4, OPS-12 → CC7.5, OPS-13 → CC7.4.

`docs/runbooks/incident-response.md`:

```markdown
# Incident response runbook

Owner: <role>   Last reviewed: <date>   Review cadence: annual

## 1. Detect and declare
- Sources: alerts (OPS-08 → CC7.2), customer reports, employee reports.
- Anyone may declare. Open an incident ticket and record detection time.

## 2. Classify (OPS-09 → CC7.3)
| Severity | Definition | Response target |
|---|---|---|
| SEV1 | Confirmed data exposure or full outage | Immediate, 24x7 |
| SEV2 | Partial outage or suspected exposure | Within 1 hour |
| SEV3 | Minor impact, no data risk | Next business day |

## 3. Roles
Incident commander, communications lead, technical lead, scribe. Name a primary and a backup for each.

## 4. Contain, eradicate, recover
Steps per incident type: credential compromise, data exposure, ransomware, availability loss, vendor breach.

## 5. Communicate (OPS-13 → CC7.4)
- Internal updates every <interval> for SEV1.
- Customer and regulator notification triggers, owners, and contractual deadlines.
- Keep the timeline and decisions in the ticket.

## 6. Post-incident review (OPS-12 → CC7.5)
Blameless review within 5 business days for SEV1 and SEV2. Record root cause, what worked, and action items with owners and dates. Track to closure.

## 7. Evidence checklist per incident
Ticket with timeline, classification, communications sent, review notes, and action item closure.
```

Annual tabletop issue template, `.github/ISSUE_TEMPLATE/tabletop-exercise.md`:

```markdown
---
name: Annual incident response tabletop
about: SOC 2 IR tabletop exercise (OPS-11 → CC7.4)
title: "IR tabletop - YYYY"
labels: soc2
---

- Scenario: <!-- e.g. leaked cloud credential used to read customer data -->
- Date held: ____-__-__
- Facilitator: ______
- Attendees (names and roles): ______

## Walkthrough notes

- Detection and declaration:
- Classification:
- Containment and recovery:
- Customer and regulator communication:

## Gaps found and action items

| Gap | Action | Owner | Due | Ticket |
|---|---|---|---|---|
|  |  |  |  |  |

Close only when every action item is done or has an approved exception. Attach the attendee list and the final report.
```

Scheduled opener, `.github/workflows/soc2-evidence-tabletop.yml`. Schedule it early enough that the exercise falls inside the audit period; an annual control that fires after period end cannot be tested.

```yaml
name: soc2-evidence-tabletop

on:
  schedule:
    - cron: "0 9 1 3 *"   # 09:00 UTC, March 1st every year
  workflow_dispatch: {}

permissions:
  issues: write

jobs:
  open-issue:
    runs-on: ubuntu-latest
    steps:
      - name: Open annual tabletop issue (OPS-11 → CC7.4)
        env:
          GH_TOKEN: ${{ github.token }}
        run: |
          gh issue create --repo "${{ github.repository }}" \
            --title "IR tabletop - $(date -u +%Y)" \
            --label "soc2" \
            --body "Run the annual incident response tabletop. Use the structure in .github/ISSUE_TEMPLATE/tabletop-exercise.md: scenario, attendees, walkthrough notes, gaps, and action items tracked to closure (OPS-11 → CC7.4)."
```
