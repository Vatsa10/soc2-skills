"""SOC 2 repo signal scanner. Stdlib only. Emits facts, never verdicts.

Usage: python scan.py <repo> [--write] [--if-stale]
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path

SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", "dist",
             "build", ".soc2", ".terraform", "vendor", "target"}
MAX_BYTES = 1_000_000
TEXT_EXT = {".tf", ".hcl", ".yml", ".yaml", ".json", ".py", ".js", ".ts", ".go",
            ".java", ".rb", ".cs", ".rs", ".php", ".kt", ".md", ".toml", ".ini",
            ".cfg", ".env", ".sh", ".txt", ".tsx", ".jsx", ""}

IDPS = ["okta", "auth0", "entra", "azuread", "keycloak", "cognito", "onelogin", "workos"]

# flag-name -> regex searched over every text file
PATTERNS = {
    "aws": r'provider\s+"aws"|\baws_[a-z_]+\b|AWSTemplateFormatVersion',
    "gcp": r'provider\s+"google"|\bgoogle_[a-z_]+\b',
    "azure": r'provider\s+"azurerm"|\bazurerm_[a-z_]+\b',
    "cfn": r"AWSTemplateFormatVersion",
    "k8s": r"^apiVersion:.*\n(?:.*\n)*?kind:",
    "sso": r"\b(saml|oidc|openid[-_ ]connect|sso)\b",
    "mfa": r"\b(mfa|totp|webauthn|two[-_ ]factor|2fa)\b",
    "kms": r"aws_kms_key|google_kms|azurerm_key_vault|kms_key_id",
    "tls": r"\btls\b|aws_acm_certificate|ssl_policy|cert-manager|https://",
    "at_rest": r"storage_encrypted\s*=\s*true|server_side_encryption|encrypted\s*=\s*true",
    "cloudtrail": r"aws_cloudtrail",
    "central_log": r"datadog|splunk|elastic|loki|cloudwatch_log_group|opentelemetry|sentry",
    "alerts": r"aws_cloudwatch_metric_alarm|alertmanager|pagerduty|opsgenie",
    "backups": r"aws_backup_plan|backup_retention_period|point_in_time_recovery|velero",
    "restore_test": r"restore[-_ ]test",
    "branch_prot": r"github_branch_protection|branch_protection_rules?",
    "secret_scan": r"gitleaks|trufflehog|detect-secrets|secret[-_ ]scanning",
    "sast": r"codeql|semgrep|snyk|bandit|sonar",
    "pii": r"\b(ssn|social_security|date_of_birth|dob|passport|phone_number)\b",
    "dsar": r"\bdsar\b|data[-_ ]subject|right[-_ ]to[-_ ](erasure|access)",
}
PATTERNS = {k: re.compile(v, re.I | re.M) for k, v in PATTERNS.items()}
HARDCODED = re.compile(r"AKIA[0-9A-Z]{16}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")
RETENTION = re.compile(r"retention_in_days\s*=\s*(\d+)")


def empty_signals():
    return {
        "iac": [], "ci": [], "cloud": [],
        "auth": {"sso": False, "mfa_hint": False, "idp": []},
        "encryption": {"kms": False, "tls": False, "at_rest_hint": False},
        "logging": {"cloudtrail": False, "centralized": False, "retention_days": None},
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
                if p.stat().st_size <= MAX_BYTES:
                    yield p
            except OSError:
                continue


def _add(lst, item):
    if item not in lst:
        lst.append(item)


def scan(root):
    root = Path(root)
    s = empty_signals()
    hits = set()
    for p in _files(root):
        rel = p.relative_to(root).as_posix().lower()
        name = p.name.lower()
        # path-based signals
        if p.suffix == ".tf":
            _add(s["iac"], "terraform")
        if name in ("pulumi.yaml", "pulumi.yml"):
            _add(s["iac"], "pulumi")
        if rel.startswith(".github/workflows/"):
            _add(s["ci"], "github-actions")
        if rel == ".gitlab-ci.yml":
            _add(s["ci"], "gitlab-ci")
        if rel == ".circleci/config.yml":
            _add(s["ci"], "circleci")
        if name == "codeowners":
            s["change_mgmt"]["codeowners"] = True
        if name.startswith("pull_request_template"):
            s["change_mgmt"]["pr_template"] = True
        if rel in (".github/dependabot.yml", ".github/dependabot.yaml") or name.startswith("renovate"):
            s["deps"]["dependabot_or_renovate"] = True
        if "/policies/" in f"/{rel}" and p.suffix == ".md":
            _add(s["policies"], p.stem.lower())
        if name.startswith("privacy") and p.suffix == ".md":
            s["privacy"]["privacy_notice"] = True
        if name.startswith(("vendors", "subprocessors")):
            s["vendors"]["list_present"] = True
        if "incident" in rel and ("runbook" in rel or "response" in rel):
            s["incident"]["runbook"] = True
        if p.suffix.lower() not in TEXT_EXT:
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        for k, rx in PATTERNS.items():
            if k not in hits and rx.search(text):
                hits.add(k)
        for idp in IDPS:
            if re.search(rf"\b{idp}\b", text, re.I):
                _add(s["auth"]["idp"], idp)
        s["secrets"]["hardcoded_hits"] += len(HARDCODED.findall(text))
        for m in RETENTION.findall(text):
            cur = s["logging"]["retention_days"] or 0
            s["logging"]["retention_days"] = max(cur, int(m))
    for cloud, k in (("aws", "aws"), ("gcp", "gcp"), ("azure", "azure")):
        if k in hits:
            _add(s["cloud"], cloud)
    if "cfn" in hits:
        _add(s["iac"], "cloudformation")
    if "k8s" in hits:
        _add(s["iac"], "k8s")
    s["auth"]["sso"] = "sso" in hits or bool(s["auth"]["idp"])
    s["auth"]["mfa_hint"] = "mfa" in hits
    s["encryption"]["kms"] = "kms" in hits
    s["encryption"]["tls"] = "tls" in hits
    s["encryption"]["at_rest_hint"] = "at_rest" in hits
    s["logging"]["cloudtrail"] = "cloudtrail" in hits
    s["logging"]["centralized"] = "central_log" in hits
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


def _stale(root, cache):
    if not cache.exists():
        return True
    t = cache.stat().st_mtime
    return any(p.stat().st_mtime > t for p in _files(root))


def main(argv=None):
    ap = argparse.ArgumentParser(description="SOC 2 repo signal scanner")
    ap.add_argument("path")
    ap.add_argument("--write", action="store_true", help="save to <path>/.soc2/scan.json")
    ap.add_argument("--if-stale", action="store_true", help="reuse cache unless files changed")
    a = ap.parse_args(argv)
    root = Path(a.path)
    if not root.is_dir():
        print(f"error: not a directory: {root}", file=sys.stderr)
        return 2
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
