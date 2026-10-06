"""SOC 2 repo signal scanner. Stdlib only. Emits facts, never verdicts.

Usage: python scan.py <repo> [--write] [--if-stale] [--secrets] [--scope KEYS]

--secrets prints `path:line kind` for each suspected hardcoded secret plus a
total count. kind is one of aws-key-id, private-key, url-credential,
db-password, azure-key, gcp-sa-key, token, generic-secret. It never prints
matched text.
--scope takes a comma list of tsc_scope keys (security, availability,
processing_integrity, confidentiality, privacy) and prints the in-scope
control IDs from references/control-index.md, one per line. Security is
always in scope; a control is in scope when any TSC it cites is in an
in-scope series.

Notes on semantics (all signals are hints, not verdicts):
- Markdown files are not scanned for control signals or secrets (documents
  describe controls, they do not implement them); only filename checks apply.
  Anything under docs/soc2/ is likewise skipped for text scanning.
- auth.sso is workforce SSO evidence only; CI OIDC is reported as auth.ci_oidc
  and an application-auth IdP alone never sets auth.sso.
- logging.centralized needs a real shipper, agent or sink configuration.
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path

SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", "dist",
             "build", ".soc2", ".terraform", "vendor", "target", "_backup"}
MAX_BYTES = 1_000_000
# .md is deliberately absent: docs are filename-checked only.
TEXT_EXT = {".tf", ".hcl", ".yml", ".yaml", ".json", ".py", ".js", ".ts", ".go",
            ".java", ".rb", ".cs", ".rs", ".php", ".kt", ".toml", ".ini",
            ".cfg", ".env", ".sh", ".txt", ".tsx", ".jsx", ".bicep", ".tfvars",
            ".jsonc", ".json5", ".properties", ".gradle", ".dockerfile",
            ".conf", ".config", ".mjs", ".cjs", ".pem", ".key", ""}
TEXT_SKIP_PREFIXES = ("docs/soc2/",)

IDPS = ["okta", "auth0", "entra", "azuread", "keycloak", "cognito", "onelogin",
        "workos", "jumpcloud", "clerk", "stytch", "supertokens", "zitadel",
        "authentik", "authelia", "ping identity", "firebase auth",
        "microsoft entra", "google workspace"]

# flag-name -> regex searched over every scanned text file
PATTERNS = {
    "aws": (r'provider\s+"aws"|\baws_[a-z_]+\b|AWSTemplateFormatVersion|\bAWS::[A-Za-z0-9]+::'
            r'|@aws-sdk/|\baws-sdk\b|aws-cdk|aws_cdk|aws-actions/|boto3'
            r'|\baws\s+(?:s3|ec2|sts|configure|iam|ecr|eks|lambda)\b'),
    "gcp": (r'provider\s+"google(?:-beta)?"'
            r'|\bgoogle_(?:compute|storage|sql|project|logging|monitoring|kms|container|cloud\w*'
            r'|bigquery|pubsub|secret_manager|service_account|folder|organization|dns'
            r'|artifact_registry|firestore|spanner|redis|backup_dr|binary_authorization|iam'
            r'|app_engine)\w*'
            r'|@google-cloud/|\bgcloud\s|google-github-actions/|\bgcr\.io/|google-cloud-[a-z]+'
            r'|cloud\.google\.com/go'),
    "azure": (r'provider\s+"azurerm"|\bazurerm_[a-z_]+\b|@azure/|\bazure-functions\b'
              r'|\bazure/(?:login|webapps-deploy|functions-action)'
              r'|\baz\s+(?:login|group|deployment|webapp|functionapp|keyvault|storage)\b'
              r'|Microsoft\.(?:Web|Storage|KeyVault|DocumentDB|Insights|RecoveryServices|Sql'
              r'|Network|Authorization|Compute|OperationalInsights|DataProtection)/'
              r'|AzureWebJobs|FUNCTIONS_WORKER_RUNTIME|\bazure-(?:storage|identity|cosmos|keyvault)[-\w]*'),
    "cfn": r"AWSTemplateFormatVersion",
    "arm": r"schema\.management\.azure\.com/schemas/[^\"'\s]*deploymentTemplate\.json",
    "k8s": r"^apiVersion:.*\n(?:.*\n)*?kind:",
    # workforce SSO only: no bare "oidc" (app auth / CI), skipped in CI files
    "sso": (r"(?<![A-Za-z0-9])(?:saml|sso)(?![A-Za-z0-9])|aws_ssoadmin|identity[-_ ]center"
            r"|\bscim\b|okta_app_saml|azuread_(?:saml|application)"),
    "ci_oidc": (r"id-token:\s*write|role-to-assume|workload_identity_provider"
                r"|token\.actions\.githubusercontent\.com|id_tokens:|azure/login"),
    "mfa": r"\b(mfa|totp|webauthn|two[-_ ]factor|2fa)\b",
    "kms": r"aws_kms_key|google_kms|azurerm_key_vault|kms_key_id|AWS::KMS::Key|Microsoft\.KeyVault/",
    # no bare https:// URLs: they say nothing about TLS configuration
    "tls": (r"\btls\b|aws_acm_certificate|ssl_policy|cert-manager|min_tls_version|minimum_tls_version"
            r"|minimumTlsVersion|minimalTlsVersion|minimal_tls_version|tls_policy|ELBSecurityPolicy|google_compute_ssl_policy"
            r"|redirect_http_to_https|\bhsts\b|AWS::CertificateManager"),
    "at_rest": r"storage_encrypted\s*=\s*true|server_side_encryption|encrypted\s*=\s*true",
    "cloud_audit_trail": (r"aws_cloudtrail|AWS::CloudTrail::Trail|cloudtrail\.Trail"
                          r"|google_logging_(?:project|folder|organization|billing_account)_sink"
                          r"|google_project_iam_audit_config"
                          r"|azurerm_monitor_log_profile|gcloud\s+logging\s+sinks"
                          r"|az\s+monitor\s+log-profiles"),
    # a real shipper / agent / sink config, not a bare log group or an API-key string
    "central_log": (r"fluentd|fluent[-_ ]?bit|filebeat|logstash|promtail|otel[-_ ]?collector"
                    r"|opentelemetry[-_ ]collector|elastic[-_ ]agent|grafana[-_ ]agent|grafana/alloy"
                    r"|grafana/loki|vector\.dev|vector\.toml|datadog[-_ ]agent|datadog/agent"
                    r"|DD_LOGS_ENABLED|datadog_logs\w*|splunk[-_](?:otel|forwarder|connect|hec)"
                    r"|splunk/universalforwarder|aws_cloudwatch_log_subscription_filter"
                    r"|aws_cloudwatch_log_destination|aws_kinesis_firehose_delivery_stream"
                    r"|google_logging_(?:project|folder|organization|billing_account)_sink"
                    r"|azurerm_monitor_(?:diagnostic_setting|data_collection_rule\w*)"
                    r"|Microsoft\.Insights/(?:diagnosticSettings|dataCollectionRules)"
                    r"|az\s+monitor\s+diagnostic-settings\s+(?:subscription\s+)?create"
                    r"|AzureMonitor(?:Linux|Windows)Agent|newrelic-infra|\bnri-"),
    "alerts": (r"aws_cloudwatch_metric_alarm|AWS::CloudWatch::Alarm|alertmanager|prometheusrule"
               r"|pagerduty|opsgenie|jira_service_management|incident\.io|grafana[-_ ]oncall"
               r"|google_monitoring_alert_policy"
               r"|azurerm_monitor_(?:metric_alert|activity_log_alert|scheduled_query_rules_alert\w*)"
               r"|Microsoft\.Insights/(?:metricAlerts|scheduledQueryRules|activityLogAlerts)"
               r"|datadog_monitor|grafana_(?:rule_group|alert\w*)"),
    "backups": (r"aws_backup_(?:plan|vault)|aws_dlm_lifecycle_policy|backup_retention_period"
                r"|point_in_time_recovery|velero|backup_configuration|google_backup_dr"
                r"|snapshot_schedule_policy|azurerm_backup_policy\w*"
                r"|azurerm_recovery_services_vault|azurerm_data_protection_backup\w*"
                r"|Microsoft\.RecoveryServices|Microsoft\.DataProtection|AWS::Backup::"
                r"|BackupRetentionPeriod|backupPolicy[\s\S]{0,200}?Continuous"
                r"|\btype\s*[=:]\s*['\"]Continuous(?:7Days|30Days)?['\"]"),
    "restore_test": r"restore[-_ ]test",
    "branch_prot": (r"github_(?:branch_protection(?:_v3)?|repository_ruleset|organization_ruleset)"
                    r"|branch_protection_rules?|\"enforcement\"\s*:\s*\"active\""),
    "secret_scan": r"gitleaks|trufflehog|detect-secrets|secret[-_ ]scanning",
    "sast": (r"codeql|semgrep|snyk|bandit|sonar|\btrivy\b|checkov|tfsec|\bkics\b|gosec|brakeman"
             r"|njsscan|dependency-review-action|osv-scanner|\bgrype\b|\bwiz(?:cli)?\b"),
    "pii": r"\b(ssn|social_security|date_of_birth|dob|passport|phone_number)\b",
    "dsar": r"\bdsar\b|data[-_ ]subject|right[-_ ]to[-_ ](erasure|access)",
}
PATTERNS = {k: re.compile(v, re.I | re.M) for k, v in PATTERNS.items()}
# Azure diagnostic setting is audit-trail evidence only for the Activity Log
# (subscription scope, Administrative category); a resource-level one is not.
AZURE_DIAG = re.compile(r"azurerm_monitor_diagnostic_setting|azurerm_monitor_aad_diagnostic_setting"
                        r"|Microsoft\.Insights/diagnosticSettings|az\s+monitor\s+diagnostic-settings", re.I)
AZURE_ADMIN = re.compile(r"\bAdministrative\b")
RETENTION = re.compile(r'(?:retention_in_days|retentionInDays|retention_days)"?\s*[=:]\s*(\d+)')
RENOVATE_PKG = re.compile(r'"renovate"\s*:')
HOST_JSON = re.compile(r'"version"\s*:')
APP_YAML = re.compile(r"^\s*runtime\s*:", re.M)

# --- secrets -------------------------------------------------------------
SECRET_KINDS = {"aws-key-id", "private-key", "url-credential", "db-password", "azure-key",
                "gcp-sa-key", "token", "generic-secret"}
# (kind, regex); the first matching rule on a line decides the kind
SECRET_RULES = [
    ("gcp-sa-key", re.compile(r"[\"']private_key[\"']?\s*[:=]\s*[\"']?-----BEGIN")),
    ("aws-key-id", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("private-key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA |PGP |ENCRYPTED )?PRIVATE KEY(?: BLOCK)?-----")),
    ("token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{20,}|xox[bapors]-[A-Za-z0-9-]{10,}"
                         r"|sk_live_[A-Za-z0-9]{10,}|AIza[0-9A-Za-z_\-]{35}")),
    ("azure-key", re.compile(r"AccountKey=[^;\s\"']{10,}|SharedAccessKey=[^;\s\"']{10,}"
                             r"|SharedAccessSignature=[^;\s\"']{10,}|[?&;]sig=[A-Za-z0-9%+/=]{20,}")),
    # scheme://user:password@host (env refs like ${X} / <x> / {{x}} are excluded)
    ("url-credential", re.compile(r"\b[a-z][a-z0-9+.\-]*://[^\s:/@\"'<>{}$]+:[^\s@/\"'<>{}$]+@", re.I)),
    # connection-string style Password=... / Pwd=...
    ("db-password", re.compile(r"(?<![A-Za-z0-9_])(?:Password|Pwd)=(?![\s$<{%;])[^;\s\"']{4,}", re.I)),
    # password = "literal" / "secret": "literal" (non-empty, not an env or template ref)
    ("db-password", re.compile(r"(?:password|passwd|pwd)[\"']?\s*[:=]\s*([\"'])(?![\s$<{%])[^\"'\s]+\1", re.I)),
    ("generic-secret", re.compile(r"(?:secret|api[_-]?key|access[_-]?key|private[_-]?key|auth[_-]?token"
                                  r"|client[_-]?secret)[\"']?\s*[:=]\s*([\"'])(?![\s$<{%])[^\"'\s]+\1", re.I)),
]
ENV_SECRET_RX = re.compile(
    r"^\s*(?:export\s+)?[A-Za-z0-9_]*(?:PASSWORD|SECRET|API_KEY|ACCESS_KEY|TOKEN|PRIVATE_KEY)"
    r"\s*=\s*(?![\s$<{#\"'])\S+", re.I)
PLACEHOLDER_VALUE = re.compile(r"EXAMPLE|YOUR[_-]|^[x*]{3,}$|REPLACE[_-]?ME|PLACEHOLDER", re.I)
TEMPLATE_SUFFIXES = (".example", ".sample", ".template", ".dist")

# name-based rule for settings files: NAME matches KEY|SECRET|TOKEN|PASSWORD|PWD|CONNECTION
NAME_WORDS = re.compile(r"KEY|SECRET|TOKEN|PASSWORD|PWD|CONNECTION", re.I)
_JSON_PAIR = re.compile(r"[\"']([A-Za-z0-9_.:\-]+)[\"']\s*:\s*[\"']([^\"']*)[\"']")
_ENV_PAIR = re.compile(r"^\s*(?:export\s+)?([A-Za-z0-9_.\-]+)\s*=\s*[\"']?([^\"'\r\n]*?)[\"']?\s*$")
_KEYISH = re.compile(r"[A-Za-z0-9+/=_\-]{20,}")
_CONN_CRED = re.compile(r"(?:Key|Password|Pwd|Secret|Sig)\w*=[^;\s]{8,}", re.I)
_NAME_EXCLUDE = re.compile(r"UseDevelopmentStorage=true|@Microsoft\.KeyVault\(|%[^%\s]+%|\$\{[^}]*\}"
                           r"|\{\{|<[^>]*>", re.I)


def _name_kind(name):
    n = name.upper()
    if re.search(r"COSMOS|STORAGE|SERVICEBUS|EVENTHUB|SHAREDACCESS|ACCOUNT|CONNECTION", n):
        return "azure-key"
    if re.search(r"PASSWORD|PWD", n):
        return "db-password"
    if "TOKEN" in n:
        return "token"
    return "generic-secret"


def is_settings_file(name):
    n = name.lower()
    return (n == "local.settings.json" or (n.startswith("appsettings") and n.endswith(".json"))
            or n.startswith(".env") or n.endswith(".env"))


def _name_rule(line):
    pairs = _JSON_PAIR.findall(line)
    m = _ENV_PAIR.match(line)
    if m:
        pairs.append((m.group(1), m.group(2)))
    for name, value in pairs:
        if not NAME_WORDS.search(name) or _NAME_EXCLUDE.search(value) or PLACEHOLDER_VALUE.search(value):
            continue
        if "CONNECTION" in name.upper():
            if _CONN_CRED.search(value):
                return _name_kind(name)
        elif _KEYISH.fullmatch(value) and (re.search(r"\d", value) or (value.lower() != value and value.upper() != value)):
            return _name_kind(name)
    return None


def secret_hits(text, is_env=False, settings=False):
    """Return [(1-based line, kind)] for suspected secrets. Never returns text."""
    out = []
    for i, line in enumerate(text.splitlines(), 1):
        if len(line) > 20000:
            line = line[:20000]
        kind = None
        for k, rx in SECRET_RULES:
            if any(not PLACEHOLDER_VALUE.search(m.group(0)) for m in rx.finditer(line)):
                kind = k
                break
        if kind is None and is_env and any(not PLACEHOLDER_VALUE.search(m.group(0))
                                           for m in ENV_SECRET_RX.finditer(line)):
            kind = "generic-secret"
        if kind is None and (settings or is_env):
            kind = _name_rule(line)
        if kind:
            out.append((i, kind))
    return out


def secret_lines(text, is_env=False, settings=False):
    return [ln for ln, _ in secret_hits(text, is_env, settings)]


# --- unresolved template placeholders (runbook skeletons) -----------------
_HTML_TAGS = {"br", "p", "b", "i", "em", "strong", "code", "pre", "ul", "ol", "li", "a", "img",
              "div", "span", "table", "tr", "td", "th", "details", "summary", "hr", "sup", "sub",
              "kbd", "h1", "h2", "h3", "h4", "h5", "h6", "blockquote", "thead", "tbody"}
_BRACES = re.compile(r"\{\{[^{}]*\}\}")
_ANGLE = re.compile(r"<([^<>\n]{1,60})>")


def has_placeholders(text):
    if _BRACES.search(text):
        return True
    for m in _ANGLE.finditer(text):
        inner = m.group(1).strip()
        if not inner or inner[0] in "/!?" or any(c in inner for c in "=:/@"):
            continue
        if inner.lower() in _HTML_TAGS:
            continue
        return True
    return False


def empty_signals():
    return {
        "iac": [], "ci": [], "cloud": [],
        "auth": {"sso": False, "ci_oidc": False, "mfa_hint": False, "idp": []},
        "encryption": {"kms": False, "tls": False, "at_rest_hint": False},
        "logging": {"cloud_audit_trail": False, "centralized": False, "retention_days": None},
        "monitoring": {"alerts": False},
        "backups": {"configured": False, "restore_test": False},
        "change_mgmt": {"codeowners": False, "pr_template": False, "branch_protection": "unknown"},
        "secrets": {"scanning": False, "hardcoded_hits": 0},
        "deps": {"dependabot_or_renovate": False, "sast": False},
        "policies": [],
        "privacy": {"pii_fields": False, "dsar": False, "privacy_notice": False},
        "vendors": {"list_present": False},
        "incident": {"runbook": False},
    }


def flatten_keys(d, prefix=""):
    out = []
    for k, v in d.items():
        key = f"{prefix}{k}"
        out.extend(flatten_keys(v, key + ".") if isinstance(v, dict) else [key])
    return out


def _files(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            p = Path(dirpath) / name
            try:
                if p.is_file() and p.stat().st_size <= MAX_BYTES:
                    yield p
            except OSError:
                continue


def _add(lst, item):
    if item not in lst:
        lst.append(item)


def _is_text_candidate(p, rel):
    if rel.startswith(TEXT_SKIP_PREFIXES):
        return False
    name = p.name.lower()
    if name.startswith(".env") or name == "local.settings.json":
        return True
    return p.suffix.lower() in TEXT_EXT


def _is_runbook_path(rel, name):
    """Runbook/playbook/IR-plan files only, never policies (a policy is not a runbook)."""
    parts = rel.split("/")
    if "policies" in parts[:-1]:
        return False
    return ("runbook" in name or "playbook" in name or name.startswith("incident-response-plan")
            or "runbooks" in parts[:-1])


def _is_ci_file(rel):
    return (rel.startswith((".github/workflows/", ".circleci/", ".buildkite/"))
            or rel in (".gitlab-ci.yml", "azure-pipelines.yml", "bitbucket-pipelines.yml",
                       "jenkinsfile", "cloudbuild.yaml", "cloudbuild.yml"))


def _read(p):
    try:
        return p.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return None


def scan_secrets(root):
    """List of (relative posix path, line, kind) for suspected hardcoded secrets."""
    root = Path(root)
    out = []
    for p in _files(root):
        rel = p.relative_to(root).as_posix()
        low = rel.lower()
        name = p.name.lower()
        if not _is_text_candidate(p, low) or name.endswith(TEMPLATE_SUFFIXES):
            continue
        text = _read(p)
        if text is None:
            continue
        for ln, kind in secret_hits(text, is_env=name.startswith(".env") or p.suffix.lower() == ".env",
                                    settings=is_settings_file(name)):
            out.append((rel, ln, kind))
    return sorted(out)


def scan(root):
    root = Path(root)
    s = empty_signals()
    hits = set()
    retentions = []
    for p in _files(root):
        rel = p.relative_to(root).as_posix().lower()
        name = p.name.lower()
        # path-based signals
        if p.suffix == ".tf" or rel.endswith((".tf.json", ".tfvars")):
            _add(s["iac"], "terraform")
        if p.suffix == ".bicep":
            _add(s["iac"], "bicep")
        if name == "cdk.json":
            _add(s["iac"], "cdk")
        if name in ("pulumi.yaml", "pulumi.yml"):
            _add(s["iac"], "pulumi")
        if rel.startswith(".github/workflows/"):
            _add(s["ci"], "github-actions")
        if rel == ".gitlab-ci.yml":
            _add(s["ci"], "gitlab-ci")
        if rel == ".circleci/config.yml":
            _add(s["ci"], "circleci")
        if rel in ("azure-pipelines.yml", "azure-pipelines.yaml"):
            _add(s["ci"], "azure-pipelines")
        if rel == "jenkinsfile":
            _add(s["ci"], "jenkins")
        if rel == "bitbucket-pipelines.yml":
            _add(s["ci"], "bitbucket-pipelines")
        if rel.startswith(".buildkite/"):
            _add(s["ci"], "buildkite")
        if rel in ("cloudbuild.yaml", "cloudbuild.yml"):
            _add(s["ci"], "cloud-build")
            hits.add("gcp")
        if name == "codeowners":
            s["change_mgmt"]["codeowners"] = True
        if name.startswith("pull_request_template"):
            s["change_mgmt"]["pr_template"] = True
        if (rel in (".github/dependabot.yml", ".github/dependabot.yaml")
                or name.startswith(("renovate", ".renovaterc"))):
            s["deps"]["dependabot_or_renovate"] = True
        if "/policies/" in f"/{rel}" and p.suffix == ".md":
            _add(s["policies"], p.stem.lower())
        if name.startswith("privacy") and p.suffix == ".md":
            s["privacy"]["privacy_notice"] = True
        if name.startswith(("vendors", "subprocessors")):
            s["vendors"]["list_present"] = True
        if _is_runbook_path(rel, name):
            body = _read(p)
            if body is None or not has_placeholders(body):
                s["incident"]["runbook"] = True
        if not _is_text_candidate(p, rel):
            continue
        text = _read(p)
        if text is None:
            continue
        is_ci = _is_ci_file(rel)
        for k, rx in PATTERNS.items():
            if k in hits or (k == "sso" and is_ci):
                continue
            if rx.search(text):
                hits.add(k)
        if "cloud_audit_trail" not in hits and AZURE_DIAG.search(text) and AZURE_ADMIN.search(text):
            hits.add("cloud_audit_trail")
        if name == "host.json" and HOST_JSON.search(text):
            hits.add("azure")
        if name == "app.yaml" and APP_YAML.search(text):
            hits.add("gcp")
        if name == "package.json" and RENOVATE_PKG.search(text):
            s["deps"]["dependabot_or_renovate"] = True
        for idp in IDPS:
            if re.search(rf"\b{idp}\b", text, re.I):
                _add(s["auth"]["idp"], idp)
        if not name.endswith(TEMPLATE_SUFFIXES):
            s["secrets"]["hardcoded_hits"] += len(
                secret_lines(text, is_env=name.startswith(".env") or p.suffix.lower() == ".env",
                             settings=is_settings_file(name)))
        retentions.extend(int(m) for m in RETENTION.findall(text))
    for cloud in ("aws", "gcp", "azure"):
        if cloud in hits:
            _add(s["cloud"], cloud)
    if "cfn" in hits:
        _add(s["iac"], "cloudformation")
    if "arm" in hits:
        _add(s["iac"], "arm")
    if "k8s" in hits:
        _add(s["iac"], "k8s")
    s["auth"]["sso"] = "sso" in hits
    s["auth"]["ci_oidc"] = "ci_oidc" in hits
    s["auth"]["mfa_hint"] = "mfa" in hits
    s["encryption"]["kms"] = "kms" in hits
    s["encryption"]["tls"] = "tls" in hits
    s["encryption"]["at_rest_hint"] = "at_rest" in hits
    s["logging"]["cloud_audit_trail"] = "cloud_audit_trail" in hits
    s["logging"]["centralized"] = "central_log" in hits
    # MIN across all log groups (the weakest one decides); 0 means never expire
    finite = [r for r in retentions if r > 0]
    s["logging"]["retention_days"] = min(finite) if finite else None
    s["monitoring"]["alerts"] = "alerts" in hits
    s["backups"]["configured"] = "backups" in hits
    s["backups"]["restore_test"] = "restore_test" in hits
    if "branch_prot" in hits:
        s["change_mgmt"]["branch_protection"] = "configured"
    s["secrets"]["scanning"] = "secret_scan" in hits
    s["deps"]["sast"] = "sast" in hits
    s["privacy"]["pii_fields"] = "pii" in hits
    s["privacy"]["dsar"] = "dsar" in hits
    return s


SCOPE_KEYS = {"security": "CC", "availability": "A", "processing_integrity": "PI",
              "confidentiality": "C", "privacy": "P"}
_SERIES = re.compile(r"^(CC|PI|A|C|P)\d")


def scope_ids(keys):
    """Control IDs in scope for the given tsc_scope keys (security always in scope)."""
    want = {"CC"} | {SCOPE_KEYS[k] for k in keys}
    index = Path(__file__).resolve().parent.parent / "references" / "control-index.md"
    ids = []
    for line in index.read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3 or not re.fullmatch(r"[A-Z]+-\d+", cells[0]):
            continue
        series = {m.group(1) for c in cells[2].split(",") if (m := _SERIES.match(c.strip()))}
        if series & want:
            ids.append(cells[0])
    return ids


def _stale(root, cache):
    if not cache.exists():
        return True
    t = cache.stat().st_mtime
    for p in _files(root):
        try:
            if p.stat().st_mtime > t:
                return True
        except OSError:
            continue
    return False


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    ap = argparse.ArgumentParser(description="SOC 2 repo signal scanner")
    ap.add_argument("path", nargs="?")
    ap.add_argument("--write", action="store_true", help="save to <path>/.soc2/scan.json")
    ap.add_argument("--if-stale", action="store_true", help="reuse cache unless files changed")
    ap.add_argument("--secrets", action="store_true",
                    help="print only path:line of suspected secrets and a total; never the text")
    ap.add_argument("--scope", metavar="KEYS",
                    help="comma list of tsc_scope keys; print in-scope control IDs, one per line")
    a = ap.parse_args(argv)
    if a.scope is not None:
        keys = [k.strip().lower() for k in a.scope.split(",") if k.strip()]
        bad = [k for k in keys if k not in SCOPE_KEYS]
        if bad:
            print(f"error: unknown scope key(s): {', '.join(bad)} "
                  f"(valid: {', '.join(SCOPE_KEYS)})", file=sys.stderr)
            return 2
        for cid in scope_ids(keys):
            print(cid)
        return 0
    if a.path is None:
        ap.error("path is required unless --scope is given")
    root = Path(a.path)
    if not root.is_dir():
        print(f"error: not a directory: {root}", file=sys.stderr)
        return 2
    if a.secrets:
        found = scan_secrets(root)
        for rel, ln, kind in found:
            print(f"{rel}:{ln} {kind}")
        print(f"total: {len(found)}")
        return 0
    cache = root / ".soc2" / "scan.json"
    if a.if_stale and not _stale(root, cache):
        print(cache.read_text(encoding="utf-8"))
        return 0
    out = json.dumps(scan(root), indent=2)
    if a.write or a.if_stale:
        cache.parent.mkdir(exist_ok=True)
        cache.write_text(out, encoding="utf-8")
    print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
