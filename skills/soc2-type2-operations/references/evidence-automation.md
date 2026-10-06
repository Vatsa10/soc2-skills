# Evidence automation snippets

> This skill prepares for a SOC 2 audit; it is not an attestation. Only a licensed CPA firm can issue a SOC 2 Type 1 or Type 2 report.

Ready-to-adapt snippets for `soc2-type2-operations`. Each is tagged with catalog control IDs (`../../soc2/references/control-catalog.md`; cite `<ID> → <TSC>` from that control's `TSC:` line). Adapt names, regions, and org/repo values. Ask the user before writing any file into their repo, and check for name collisions first (see "Collision rules" below).

Sections:
- 0. Prerequisites checklist and evidence-writer role
- 1. Scheduled evidence export: GitHub Actions (1) and GitLab CI (1b)
- 2. Log retention, evidence store, backups: AWS Terraform (2), GCP (2b), Azure (2c)
- 3. Quarterly access review
- 4. Change management: PR template and CODEOWNERS
- 5. Incident response runbook and annual tabletop
- 6. Processing Integrity evidence
- 7. Generating a snippet when none matches the stack

Cloud service names per control family are in `../../soc2/references/cloud-equivalents.md`.

Retention rule used throughout: keep evidence for the audit period plus one year (a common practice, not an AICPA requirement). The floor for logs is 365 days (OPS-07 → CC7.2); the snippets set 400 days as a recommended value that adds slack for fieldwork. The evidence store lock is a variable: audit period in days plus 365 (730 for a 12-month period).

Collision rules (apply before writing anything):
- Every Terraform resource and cloud resource in these snippets is prefixed `soc2_` / `soc2-`. Before writing, search the user's IaC for the same resource addresses and the cloud for the same names (log group, bucket, vault, role). On a clash, rename the snippet's resource; never edit the user's resource.
- The snippets contain no `terraform {}` or `provider` block. Use the user's existing ones (AWS provider v5 or v6; `aws_s3_bucket_object_lock_configuration` works on new and existing buckets and needs versioning).
- CODEOWNERS may live at the repo root, `.github/`, or `docs/`. GitHub uses the first found in that order: `.github/`, then root, then `docs/`. If any exists, merge the new rules into that file; never write a second one (a new `.github/CODEOWNERS` would silently shadow a root file). The same applies to `pull_request_template.md` and issue templates.

## 0. Prerequisites checklist and evidence-writer role

Tell the user these must exist before the export workflows can succeed. Mark each done or open in `docs/soc2/type2-operations.md`.

- [ ] Evidence store exists with a lock or retention policy sized to audit period plus 1 year (section 2, 2b, or 2c).
- [ ] CI-to-cloud trust exists (OIDC federation; no long-lived keys) and the role/identity can only write to the evidence store.
- [ ] GitHub: secret `EVIDENCE_GH_TOKEN` (fine-grained PAT or GitHub App token) with read-only Administration, Dependabot alerts, Actions, and Pull requests permissions (Metadata read is implicit). The default `GITHUB_TOKEN` cannot read branch protection or rulesets (needs Administration read) but can read Dependabot alerts with `permissions: vulnerability-alerts: read`. Record the token's owner and rotation date (AC-17 → CC6.1).
- [ ] GitLab: masked CI/CD variable `EVIDENCE_GL_TOKEN` (project or group access token, `read_api` scope, Reporter role or higher) and a pipeline schedule.
- [ ] Label `soc2` exists (workflows below create it with `gh label create ... --force`).
- [ ] Role ARN / account ID / bucket name placeholders replaced.
- [ ] Production data stores carry the backup tag (`backup = "true"`) used by the backup selection, or the selection is changed to match the user's tags.
- [ ] Someone is named owner for each scheduled workflow, and failures notify them.

Evidence-writer role for GitHub OIDC to AWS (no `terraform {}` or `provider` block; add to the user's existing configuration; the evidence bucket and key are defined in section 2):

```hcl
variable "soc2_github_repo" {
  type        = string
  description = "owner/repo allowed to assume the evidence writer role, for example example-org/app"
}

# If the account already has the GitHub OIDC provider, use a data source instead of this resource.
resource "aws_iam_openid_connect_provider" "soc2_github" {
  url             = "https://token.actions.githubusercontent.com"
  client_id_list  = ["sts.amazonaws.com"]
  thumbprint_list = ["6938fd4d98bab03faadb97b34396831e3780aea1"] # still required by some provider versions; AWS validates GitHub's chain itself
}

resource "aws_iam_role" "soc2_evidence_writer" {
  name = "soc2-evidence-writer"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Action    = "sts:AssumeRoleWithWebIdentity"
      Principal = { Federated = aws_iam_openid_connect_provider.soc2_github.arn }
      Condition = {
        StringEquals = {
          "token.actions.githubusercontent.com:aud" = "sts.amazonaws.com"
        }
        StringLike = {
          # scheduled runs execute on the default branch
          "token.actions.githubusercontent.com:sub" = "repo:${var.soc2_github_repo}:ref:refs/heads/main"
        }
      }
    }]
  })
}

resource "aws_iam_role_policy" "soc2_evidence_writer" {
  name = "soc2-evidence-write-only"
  role = aws_iam_role.soc2_evidence_writer.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["s3:PutObject"]
        Resource = "${aws_s3_bucket.soc2_evidence.arn}/*"
      },
      {
        Effect   = "Allow"
        Action   = ["kms:GenerateDataKey"]
        Resource = aws_kms_key.soc2_evidence.arn
      }
    ]
  })
}
```

The role has no delete, no `s3:BypassGovernanceRetention`, and no read permission. If the default branch is not `main`, change the `sub` condition. The thumbprint line may be dropped on recent provider versions that accept an empty list; keep it if `terraform validate` or apply asks for it.

## 1. Scheduled evidence export (GitHub Actions)

Controls: CHG-02 → CC8.1 (CC5.1), CHG-03 → CC8.1, CHG-04 → CC8.1, CHG-05 → CC8.1, OPS-02 → CC7.1, MON-01 → CC4.1.

Facts that shape the design:
- Artifact `retention-days` accepts 1 to 90 days on public repositories and 1 to 400 days on private and internal repositories (cap set in repository, organization, or enterprise settings). Artifacts are deletable by anyone with write access and 400 days falls short of audit period plus one year, so treat them as staging and copy every export to locked storage. The snippet uses 90 days, valid everywhere.
- The default `GITHUB_TOKEN` cannot read branch protection or rulesets. Use `EVIDENCE_GH_TOKEN` (section 0).
- Branch rules can be classic branch protection, repository rulesets, or organization rulesets. The classic endpoint returns 404 for a branch governed only by rulesets, and `gh api` exits non-zero on a 404, which would abort every later step. The export therefore captures rulesets and effective rules unconditionally and tolerates a 404 on classic protection.
- `gh api --paginate` without `--slurp` prints one JSON array per page, which is not a valid single document. Use `--paginate --slurp` and flatten with `jq`.
- Reach AWS through OIDC (`id-token: write`), not access keys. Actions are pinned to major versions here (`upload-artifact@v7`, `configure-aws-credentials@v6`, verified current); pin to a commit SHA for audit-relevant workflows if the user wants supply-chain hardening (CHG-06 → CC8.1).

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
    steps:
      - name: Set export date and default branch
        run: |
          echo "EXPORT_DATE=$(date -u +%Y-%m-%d)" >> "$GITHUB_ENV"
          echo "DEFAULT_BRANCH=$(gh repo view "${REPO}" --json defaultBranchRef --jq .defaultBranchRef.name)" >> "$GITHUB_ENV"

      - name: Export branch rules (CHG-02 → CC8.1, CHG-03 → CC8.1)
        run: |
          mkdir -p evidence
          gh api "repos/${REPO}/rulesets?includes_parents=true" > "evidence/rulesets-${EXPORT_DATE}.json"
          gh api "repos/${REPO}/rules/branches/${DEFAULT_BRANCH}" > "evidence/branch-rules-${EXPORT_DATE}.json"
          # classic protection returns 404 when only rulesets apply; record that instead of failing
          gh api "repos/${REPO}/branches/${DEFAULT_BRANCH}/protection" > "evidence/branch-protection-${EXPORT_DATE}.json" \
            || echo '{"note":"no classic branch protection (404); see rulesets"}' > "evidence/branch-protection-${EXPORT_DATE}.json"
          # per-ruleset detail (bypass_actors, rules)
          for id in $(jq -r '.[].id' "evidence/rulesets-${EXPORT_DATE}.json"); do
            gh api "repos/${REPO}/rulesets/${id}" > "evidence/ruleset-${id}-${EXPORT_DATE}.json"
          done

      - name: Export open Dependabot alerts (OPS-02 → CC7.1)
        run: |
          gh api --paginate --slurp "repos/${REPO}/dependabot/alerts?state=open&per_page=100" \
            | jq 'add // []' > "evidence/dependabot-open-${EXPORT_DATE}.json"

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
          jq 'length' "evidence/merged-prs-${EXPORT_DATE}.json"

      - name: Hash the export
        run: cd evidence && sha256sum ./*.json > "SHA256SUMS-${EXPORT_DATE}.txt"

      - name: Stage as artifact (staging only; the locked copy is the evidence)
        uses: actions/upload-artifact@v7
        with:
          name: soc2-evidence-${{ env.EXPORT_DATE }}
          path: evidence/
          retention-days: 90

      - name: Configure AWS credentials (OIDC)
        uses: aws-actions/configure-aws-credentials@v6
        with:
          role-to-assume: arn:aws:iam::111122223333:role/soc2-evidence-writer
          aws-region: us-east-1

      - name: Copy to the object-locked evidence bucket (lock = var.soc2_evidence_retention_days)
        run: |
          aws s3 cp evidence/ "s3://example-soc2-evidence/github/${EXPORT_DATE}/" --recursive
```

Notes for the user:
- Organization-level rulesets are included by `includes_parents=true`; listing `orgs/{org}/rulesets` directly needs organization Administration read.
- Reconcile deployments to PRs (CHG-02 → CC8.1): the export of merged PRs plus workflow runs lets the auditor map each production deploy to an approved PR. Changes made in the cloud console bypass this; enable the cloud audit trail (OPS-06 → CC7.2) and alert on console changes to production.
- A failed run is an exception the auditor can see; open a ticket per failure (MON-03 → CC4.2).
- Auditors sample the whole period, so the workflow must run on schedule from day one. Do not enable it halfway through a period without telling the auditor.
- Population: the monthly run produces 12 occurrences in a 12-month period but only 3 to 6 in a short one. State the count in the type2 output.

### 1b. Scheduled evidence export (GitLab CI)

Same controls as section 1. Create a pipeline schedule (CI/CD, Schedules) set to `0 6 1 * *` and the masked variable `EVIDENCE_GL_TOKEN` (`read_api`). Merge-request approval rules and protected branches are readable by the token; approval-rule endpoints require a tier that supports them (Premium or higher), so the step tolerates a failure the same way as the GitHub classic endpoint. Dependency vulnerability export requires Ultimate; on lower tiers use the Dependabot or Renovate evidence from the user's chosen tool instead. Copy the output to the object-locked store using that cloud's OIDC job token (`id_tokens:`) with the same write-only role as section 0.

`.gitlab-ci.yml` job (merge into the user's file; keep the job name unique):

```yaml
soc2-evidence-export:
  image: alpine:3.20
  rules:
    - if: $CI_PIPELINE_SOURCE == "schedule"
  before_script:
    - apk add --no-cache curl jq coreutils
  script:
    - export EXPORT_DATE=$(date -u +%Y-%m-%d)
    - SINCE=$(date -u -d '31 days ago' +%Y-%m-%dT00:00:00Z)
    - mkdir -p evidence
    - |
      api() { curl --fail --silent --show-error --header "PRIVATE-TOKEN: ${EVIDENCE_GL_TOKEN}" "${CI_API_V4_URL}/projects/${CI_PROJECT_ID}/$1"; }
    - api "protected_branches" > "evidence/protected-branches-${EXPORT_DATE}.json"
    - api "approval_rules" > "evidence/approval-rules-${EXPORT_DATE}.json" || echo '{"note":"approval rules unavailable on this tier"}' > "evidence/approval-rules-${EXPORT_DATE}.json"
    - |
      page=1; : > mr-pages.ndjson
      while :; do
        out=$(api "merge_requests?state=merged&updated_after=${SINCE}&per_page=100&page=${page}")
        [ "$(echo "$out" | jq 'length')" -eq 0 ] && break
        echo "$out" >> mr-pages.ndjson; page=$((page+1))
      done
      jq -s 'add // []' mr-pages.ndjson > "evidence/merged-mrs-${EXPORT_DATE}.json"
    - |
      for iid in $(jq -r '.[].iid' "evidence/merged-mrs-${EXPORT_DATE}.json"); do
        api "merge_requests/${iid}/approvals" > "evidence/mr-${iid}-approvals-${EXPORT_DATE}.json"
      done
    - cd evidence && sha256sum ./*.json > "SHA256SUMS-${EXPORT_DATE}.txt"
  artifacts:
    paths: [evidence/]
    expire_in: 90 days
```

GitLab job artifacts are staging only for the same reason as GitHub's; add a final upload step to the locked store.

## 2. Terraform (AWS): log retention, evidence bucket, backups

Controls: OPS-05 → CC7.2, OPS-06 → CC7.2, OPS-07 → CC7.2, CF-03 → C1.1, AV-03 → A1.2, AV-04 → A1.3.

Targets AWS provider v5 or v6. Object Lock can be enabled at bucket creation (`object_lock_enabled = true`) or later with `aws_s3_bucket_object_lock_configuration` (versioning required). Resource names are `soc2_*`; there is no `terraform {}` block, so rename on collision and reuse the user's provider configuration. If the user already has a CloudWatch log group for the app, set its `retention_in_days` and `kms_key_id` in place (do not create a duplicate) and keep the `soc2_` resources for everything else.

```hcl
data "aws_caller_identity" "soc2" {}
data "aws_region" "soc2" {}

# --- Log retention (OPS-07 → CC7.2, OPS-05 → CC7.2) -------------------------------------
# CloudWatch Logs can only use a customer key whose policy allows the logs service; without
# the second statement the log group creation or association fails.
resource "aws_kms_key" "soc2_logs" {
  description         = "CloudWatch log encryption"
  enable_key_rotation = true
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "EnableAccountAdministration"
        Effect    = "Allow"
        Principal = { AWS = "arn:aws:iam::${data.aws_caller_identity.soc2.account_id}:root" }
        Action    = "kms:*"
        Resource  = "*"
      },
      {
        Sid       = "AllowCloudWatchLogs"
        Effect    = "Allow"
        Principal = { Service = "logs.${data.aws_region.soc2.name}.amazonaws.com" }
        Action = [
          "kms:Encrypt*",
          "kms:Decrypt*",
          "kms:ReEncrypt*",
          "kms:GenerateDataKey*",
          "kms:Describe*"
        ]
        Resource = "*"
        Condition = {
          ArnLike = {
            "kms:EncryptionContext:aws:logs:arn" = "arn:aws:logs:${data.aws_region.soc2.name}:${data.aws_caller_identity.soc2.account_id}:log-group:*"
          }
        }
      }
    ]
  })
}

resource "aws_cloudwatch_log_group" "soc2_app" {
  name              = "/soc2/app" # rename to the app's real log group, or set retention in place on the existing one
  retention_in_days = 400         # valid CloudWatch value; 365 is the OPS-07 floor, 400 adds slack for fieldwork
  kms_key_id        = aws_kms_key.soc2_logs.arn
}

variable "soc2_evidence_retention_days" {
  type        = number
  description = "Audit period length in days plus 365. Example: 12-month period gives 730."
  default     = 730
}

# --- Evidence bucket with object lock (OPS-07 → CC7.2, CF-03 → C1.1) -----------------------
resource "aws_kms_key" "soc2_evidence" {
  description         = "Evidence bucket encryption"
  enable_key_rotation = true
  # Default key policy (account root delegates to IAM). Grant the evidence writer role kms:GenerateDataKey in IAM (section 0).
}

resource "aws_s3_bucket" "soc2_evidence" {
  bucket              = "example-soc2-evidence" # globally unique; replace
  object_lock_enabled = true
}

resource "aws_s3_bucket_versioning" "soc2_evidence" {
  bucket = aws_s3_bucket.soc2_evidence.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_object_lock_configuration" "soc2_evidence" {
  bucket = aws_s3_bucket.soc2_evidence.id

  rule {
    default_retention {
      mode = "COMPLIANCE"                           # no one, including root, can shorten or delete
      days = var.soc2_evidence_retention_days       # audit period in days + 365; compute it
    }
  }

  depends_on = [aws_s3_bucket_versioning.soc2_evidence]
}

resource "aws_s3_bucket_server_side_encryption_configuration" "soc2_evidence" {
  bucket = aws_s3_bucket.soc2_evidence.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.soc2_evidence.arn
    }
    bucket_key_enabled = true
  }
}

resource "aws_s3_bucket_public_access_block" "soc2_evidence" {
  bucket                  = aws_s3_bucket.soc2_evidence.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# --- Backups (AV-03 → A1.2) -----------------------------------------------------------
resource "aws_backup_vault" "soc2_main" {
  name = "soc2-backup-vault"
}

resource "aws_backup_plan" "soc2_daily" {
  name = "soc2-daily-35d"

  rule {
    rule_name         = "daily"
    target_vault_name = aws_backup_vault.soc2_main.name
    schedule          = "cron(0 5 * * ? *)"

    lifecycle {
      delete_after = 35
    }
  }
}

resource "aws_iam_role" "soc2_backup" {
  name = "soc2-backup-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Action    = "sts:AssumeRole"
      Principal = { Service = "backup.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "soc2_backup" {
  role       = aws_iam_role.soc2_backup.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSBackupServiceRolePolicyForBackup"
}

# Add this too if S3 buckets are backed up:
# arn:aws:iam::aws:policy/AWSBackupServiceRolePolicyForS3Backup

resource "aws_backup_selection" "soc2_tagged" {
  name         = "soc2-tagged-backup-true"
  plan_id      = aws_backup_plan.soc2_daily.id
  iam_role_arn = aws_iam_role.soc2_backup.arn

  selection_tag {
    type  = "STRINGEQUALS"
    key   = "backup"
    value = "true"
  }
}
```

Required follow-up, or the plan backs up nothing: add the tag `backup = "true"` to every production data store in the user's IaC (for example `tags = { backup = "true" }` on the `aws_db_instance`, DynamoDB table, EFS file system, EBS volumes). Alternatively change the `selection_tag` to the tag the user already uses, or select by resource ARN with `resources = [...]`. List the tagged resources in the output and confirm each production datastore appears in the first backup job. If the user already runs AWS Backup or RDS automated backups, adapt instead of duplicating.

Backup retention note: the 35-day backup lifecycle is an operational choice, separate from evidence retention (`var.soc2_evidence_retention_days`). The evidence for AV-03 → A1.2 is the job success history (export it with section 1's pattern, for example `aws backup list-backup-jobs`), which belongs in the locked bucket.

Restore-test reminder (AV-04 → A1.3): a backup that was never restored is not evidence of recoverability. Pick one:
- AWS Backup restore testing (`aws_backup_restore_testing_plan` and `aws_backup_restore_testing_selection`, provider v5.3x and later and v6; the selection's role needs `AWSBackupServiceRolePolicyForRestores`). Minimal plan:

```hcl
resource "aws_backup_restore_testing_plan" "soc2_weekly" {
  name                = "soc2_weekly_restore_test"
  schedule_expression = "cron(0 12 ? * 1 *)"

  recovery_point_selection {
    algorithm             = "LATEST_WITHIN_WINDOW"
    include_vaults        = [aws_backup_vault.soc2_main.arn]
    recovery_point_types  = ["SNAPSHOT"]
    selection_window_days = 7
  }
}
```

  The plan needs a matching `aws_backup_restore_testing_selection` (name, `restore_testing_plan_name`, `protected_resource_type`, `iam_role_arn`, and `protected_resource_arns` or conditions); or
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
          gh label create soc2 --repo "${{ github.repository }}" --color 0E8A16 --force || true
          gh issue create --repo "${{ github.repository }}" \
            --title "Backup restore test - $(date -u +%Y-%m)" \
            --label "soc2" \
            --body "Restore the latest production backup into an isolated environment. Attach: restore date, data set, duration, verification results, and who ran it. Close when done (AV-04 → A1.3)."
```

### 2b. GCP variant

Controls: OPS-05 → CC7.2, OPS-06 → CC7.2, OPS-07 → CC7.2, AV-03 → A1.2.

Cloud Audit Logs: Admin Activity logs are always on; Data Access logs for most services must be enabled per project in IAM and Admin, Audit Logs. Route audit logs to a Cloud Storage bucket with a locked retention policy so the evidence cannot be shortened. Locking is irreversible; confirm the period with the user first (audit period in days plus 365 equals 730 days for 12 months, which is 63072000 seconds).

```bash
PROJECT=example-project
BUCKET=example-soc2-audit-logs
RETENTION=730d    # audit period + 365 days; adapt

# 1. Evidence bucket with a retention policy (uniform bucket-level access, no public access)
gcloud storage buckets create "gs://${BUCKET}" --project="${PROJECT}" --location=us \
  --uniform-bucket-level-access --public-access-prevention --retention-period="${RETENTION}"

# 2. Lock the retention policy (irreversible: it can no longer be removed or reduced)
gcloud storage buckets update "gs://${BUCKET}" --lock-retention-period

# 3. Log sink for audit logs to the bucket
gcloud logging sinks create soc2-audit-sink "storage.googleapis.com/${BUCKET}" \
  --project="${PROJECT}" \
  --log-filter='logName:"cloudaudit.googleapis.com"'
# For an organization-wide sink use --organization=ORG_ID --include-children instead of --project.

# 4. Grant the sink's writer identity permission to write objects
WRITER=$(gcloud logging sinks describe soc2-audit-sink --project="${PROJECT}" --format='value(writerIdentity)')
gcloud storage buckets add-iam-policy-binding "gs://${BUCKET}" \
  --member="${WRITER}" --role=roles/storage.objectCreator
```

Retention for operational logs: set the `_Default` log bucket retention to at least 365 days with `gcloud logging buckets update _Default --location=global --retention-days=400` (OPS-07 → CC7.2). Backups (AV-03 → A1.2): Cloud SQL automated backups with point-in-time recovery, or Backup and DR Service plans; export the backup job history monthly with the section 1 pattern. GitHub Actions or GitLab CI reach GCP with Workload Identity Federation (`google-github-actions/auth@v3` with `workload_identity_provider` and `service_account`; permissions `id-token: write`), granting only `roles/storage.objectCreator` on the evidence bucket.

### 2c. Azure variant

Controls: OPS-05 → CC7.2, OPS-06 → CC7.2, OPS-07 → CC7.2, AV-03 → A1.2.

Activity log: send it with a subscription diagnostic setting to a Log Analytics workspace (query and alert) and to a storage account (long retention). Immutable storage: a time-based retention policy on the container, then lock it (irreversible; confirm the period first).

```bash
SUB=00000000-0000-0000-0000-000000000000
RG=soc2-evidence-rg
SA=examplesoc2evidence
CONTAINER=activity-logs
WS_ID=$(az monitor log-analytics workspace show -g "$RG" -n soc2-law --query id -o tsv)
SA_ID=$(az storage account show -g "$RG" -n "$SA" --query id -o tsv)

# 1. Subscription activity log to workspace and storage (OPS-06 → CC7.2)
az monitor diagnostic-settings subscription create --name soc2-activity-log \
  --location eastus --workspace "$WS_ID" --storage-account "$SA_ID" \
  --logs '[{"category":"Administrative","enabled":true},{"category":"Security","enabled":true},{"category":"Policy","enabled":true},{"category":"Alert","enabled":true}]'

# 2. Immutable container: create an unlocked time-based policy, then lock it with its ETag
az storage container create --account-name "$SA" --name "$CONTAINER" --auth-mode login
az storage container immutability-policy create --account-name "$SA" -g "$RG" \
  --container-name "$CONTAINER" --period 730
ETAG=$(az storage container immutability-policy show --account-name "$SA" -g "$RG" \
  --container-name "$CONTAINER" --query etag -o tsv)
az storage container immutability-policy lock --account-name "$SA" -g "$RG" \
  --container-name "$CONTAINER" --if-match "$ETAG"

# 3. Workspace retention of at least 365 days (OPS-07 → CC7.2)
az monitor log-analytics workspace update -g "$RG" -n soc2-law --retention-time 400

# 4. Azure Policy compliance export as periodic evidence (OPS-04 → CC7.1)
az policy state list --subscription "$SUB" --filter "complianceState eq 'NonCompliant'" -o json > "policy-noncompliant-$(date -u +%F).json"
az policy state summarize --subscription "$SUB" -o json > "policy-summary-$(date -u +%F).json"
```

Note that `--period` is in days and the lock can only be extended afterwards, never shortened. Also use the Azure Backup vault job history for AV-03 → A1.2 (`az backup job list`), exported monthly. GitHub Actions reach Azure with OIDC federation (`azure/login@v3` with `client-id`, `tenant-id`, `subscription-id` and `permissions: id-token: write`); grant only Storage Blob Data Contributor scoped to the evidence container. If the login identity needs the same write-only property as the AWS role, avoid delete rights on the container.

## 3. Quarterly access review (issue template and opener)

Controls: AC-05 → CC6.2 (CC6.3), AC-04 → CC6.2, AC-06 → CC6.1, AC-07 → CC6.1.

The reviewer must not be the owner of the access being reviewed. The review is only evidence if the user listings are complete (every account in every in-scope system, exported by system, with the export date) and the reviewer is independent. `.github/ISSUE_TEMPLATE/access-review.md`:

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
- Attach complete user listings (CSV, or screenshot with the date visible). State the total account count per system; partial lists are not accepted by auditors.

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
          ACCESS_REVIEWER: ${{ vars.ACCESS_REVIEWER }}
        run: |
          gh label create soc2 --repo "${{ github.repository }}" --color 0E8A16 --force || true
          gh issue create --repo "${{ github.repository }}" \
            --title "Access review - $(date -u +%Y-%m)" \
            --label "soc2" \
            ${ACCESS_REVIEWER:+--assignee "$ACCESS_REVIEWER"} \
            --body "Run the quarterly access review. Follow the checklist in .github/ISSUE_TEMPLATE/access-review.md: export complete user listings, compare against the HR roster, remove or justify access, then record sign-off here (AC-05 → CC6.2)."
```

Close each issue only after every removal ticket is closed. The closed issue, attached listings, and removal tickets are the sampled evidence. If a quarter has no leavers, record "no terminations in the period" in the issue; that is the no-occurrence evidence for AC-04.

## 4. Change management: PR template and CODEOWNERS

Controls: CHG-02 → CC8.1 (CC5.1), CHG-03 → CC8.1, CHG-05 → CC8.1, CTL-02 → CC5.1 (CC6.3).

`.github/pull_request_template.md` (merge into an existing template if one exists):

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

CODEOWNERS (adapt teams and paths). First look for an existing file at `CODEOWNERS`, `.github/CODEOWNERS`, or `docs/CODEOWNERS`. If one exists, append only the missing rules to that file (keep the user's rules and order; later patterns win). Write a new `.github/CODEOWNERS` only when none exists:

```
# Sensitive paths require review from the named team (CHG-03 → CC8.1)
/infra/                 @example-org/platform-security
/terraform/             @example-org/platform-security
/.github/workflows/     @example-org/platform-security
/.github/CODEOWNERS     @example-org/platform-security
/src/auth/              @example-org/security
/migrations/            @example-org/data-owners
```

The template and CODEOWNERS do nothing unless enforcement is on. On the default branch enable, through branch protection or a repository or organization ruleset: require a pull request with at least 1 approval, require review from code owners, dismiss stale approvals, require status checks, block force pushes, and no bypass (an empty ruleset bypass list or "include administrators" in classic protection). The monthly export in section 1 captures this setting as evidence (CHG-02 → CC8.1). A ticket link in the template is only a convention; add a CI check that fails when the PR body has no ticket URL if you want it system-enforced (CHG-05 → CC8.1).

## 5. Incident response: runbook skeleton and annual tabletop

Controls: OPS-09 → CC7.3, OPS-10 → CC7.4, OPS-11 → CC7.4 (CC7.5), OPS-12 → CC7.5, OPS-13 → CC7.4 (CC2.3).

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
Blameless review within 10 business days for SEV1 and SEV2. Record root cause, what worked, and action items with owners and dates. Track to closure.

## 7. Evidence checklist per incident
Ticket with timeline, classification, communications sent, review notes, and action item closure.
```

Adjust the response targets to what the team can actually staff; a 24x7 target the team cannot meet becomes an exception. Replace the `<...>` placeholders before the file is treated as evidence.

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

Scheduled opener, `.github/workflows/soc2-evidence-tabletop.yml`. Schedule it early enough that the exercise falls inside the audit period; an annual control that fires after period end, or before it starts, cannot be tested. Set the month from `audit_period` (the cron below is March; change it).

```yaml
name: soc2-evidence-tabletop

on:
  schedule:
    - cron: "0 9 1 3 *"   # 09:00 UTC, March 1st every year; set the month inside the audit period
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
          gh label create soc2 --repo "${{ github.repository }}" --color 0E8A16 --force || true
          gh issue create --repo "${{ github.repository }}" \
            --title "IR tabletop - $(date -u +%Y)" \
            --label "soc2" \
            --body "Run the annual incident response tabletop. Use the structure in .github/ISSUE_TEMPLATE/tabletop-exercise.md: scenario, attendees, walkthrough notes, gaps, and action items tracked to closure (OPS-11 → CC7.4)."
```

## 6. Processing Integrity evidence

Controls: PI-01 → PI1.1, PI-02 → PI1.2, PI-03 → PI1.3, PI-04 → PI1.4, PI-05 → PI1.5, PI-06 → PI1.3, PI-07 → PI1.4 (take each TSC from the control's catalog entry). Only for systems in scope for processing_integrity. These controls fire per record or per batch, so the auditor samples from a population you must be able to list in full. Keep every artifact below dated, append-only, and copied to the locked store.

Population and completeness: for each control keep a count of items processed per period (records, files, batches). An auditor will ask that the listing they sample from is complete; produce it from the system, not by hand.

1. Rejection log (PI-02 → PI1.2). Every input rejected by validation is written as a structured event with timestamp, source, rule that failed, and a correlation ID; the payload itself is not logged if it holds personal data. Export monthly the count by rule and the full list. Example Log Analytics (Azure) query, adapt table and field names:

```kusto
AppTraces
| where TimeGenerated > ago(31d) and Message startswith "input_rejected"
| extend rule = tostring(Properties.rule), source = tostring(Properties.source)
| summarize rejected = count() by rule, source, bin(TimeGenerated, 1d)
```

2. Reconciliation report (PI-03 → PI1.3). A scheduled job compares what entered a stage with what left it and records the difference. Minimum report schema, one row per run per stage:

```json
{
  "run_id": "2026-10-01T06:00Z-intake-to-ledger",
  "period_start": "2026-09-30T00:00:00Z",
  "period_end": "2026-09-30T23:59:59Z",
  "records_in": 10432,
  "records_out": 10430,
  "records_rejected": 2,
  "amount_in": "1830211.45",
  "amount_out": "1830011.45",
  "unreconciled": 0,
  "status": "balanced",
  "reviewed_by": "Operations lead",
  "reviewed_at": "2026-10-01T09:12:00Z"
}
```

   A run where `records_in != records_out + records_rejected` or amounts differ must open a ticket (MON-03 → CC4.2). Keep both the automated report and the human review sign-off.

3. Duplicate and replay detection (PI-06 → PI1.3). Evidence: the idempotency-key store or unique constraint (schema or migration file) and a monthly count of suppressed duplicates. Example SQL, adapt names:

```sql
SELECT date_trunc('day', received_at) AS day, count(*) AS duplicates_suppressed
FROM ingest_events
WHERE outcome = 'duplicate_ignored' AND received_at >= now() - interval '31 days'
GROUP BY 1 ORDER BY 1;
```

4. Timeliness and completeness SLAs (PI-07 → PI1.4). Record for each run the start, end, SLA target, and met or missed. Alert on a missed SLA and keep the alert history; export the monthly percentage on time.

5. Output checks (PI-04 → PI1.4). For each delivered output (report, invoice, export file, API response batch) keep: output ID, recipient, generation time, row count and checksum, and the check that compared the output with the source (count or control total). Keep the delivery access list so only authorised recipients receive it.

6. Stored data integrity (PI-05 → PI1.5). Keep the backup and restore evidence from section 2 and any periodic checksum or row-count verification of critical tables.

Low-occurrence warning: if a Processing Integrity control fires only monthly, a short period yields very few occurrences and an exception leaves little room; say so in the output.

## 7. Generating a snippet when none matches the stack

When the user's stack is not covered above (another CI, another cloud service, a different issue tracker), do not skip the control. Generate the artifact from these patterns, tell the user it is generated rather than tested, and validate it before writing (`python -c "import yaml,sys; yaml.safe_load(open(sys.argv[1]))" file.yml` for YAML, `terraform fmt -check` and `terraform validate` when Terraform is installed, `bash -n` for shell):

- Scheduled export: a job triggered by a schedule that (1) pulls configuration state and event history from the system's API with a read-only identity, (2) writes dated JSON files, (3) hashes them, (4) copies them to write-only locked storage, and (5) fails loudly and opens a ticket on error.
- Recurring human control: a scheduled job or calendar series that opens a ticket from a template with a checklist, an owner, a due date, and a sign-off block; the closed ticket plus attachments is the evidence.
- Retention or immutability: a retention policy on the evidence store covering the audit period plus one year, locked where the platform offers it.
- Name every created resource with a `soc2` prefix, check for existing resources and files of the same name first, and merge rather than overwrite.
