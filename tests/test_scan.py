import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "skills" / "soc2" / "scripts" / "scan.py"
FIX = ROOT / "tests" / "fixtures"
sys.path.insert(0, str(SCRIPT.parent))
import scan  # noqa: E402


class ScanTest(unittest.TestCase):
    def test_empty_repo_matches_defaults(self):
        self.assertEqual(scan.scan(FIX / "empty"), scan.empty_signals())

    def test_tf_aws(self):
        s = scan.scan(FIX / "tf_aws")
        self.assertEqual(s["iac"], ["terraform"])
        self.assertEqual(s["ci"], ["github-actions"])
        self.assertEqual(s["cloud"], ["aws"])
        self.assertTrue(s["encryption"]["kms"])
        self.assertTrue(s["encryption"]["at_rest_hint"])
        self.assertTrue(s["logging"]["cloud_audit_trail"])
        self.assertEqual(s["logging"]["retention_days"], 400)
        self.assertTrue(s["backups"]["configured"])
        self.assertTrue(s["change_mgmt"]["codeowners"])
        self.assertTrue(s["secrets"]["scanning"])
        self.assertTrue(s["deps"]["sast"])

    def test_bare_app(self):
        s = scan.scan(FIX / "bare_app")
        self.assertEqual(s["secrets"]["hardcoded_hits"], 1)
        self.assertTrue(s["privacy"]["pii_fields"])
        self.assertFalse(s["auth"]["sso"])

    def test_schema_keys_stable(self):
        keys = scan.flatten_keys(scan.empty_signals())
        self.assertIn("auth.sso", keys)
        self.assertIn("auth.ci_oidc", keys)
        self.assertIn("logging.cloud_audit_trail", keys)
        self.assertNotIn("logging.cloudtrail", keys)
        self.assertEqual(len(keys), 29)

    def test_non_utf8_and_big_and_vendored_skipped(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            (p / "bad.py").write_bytes(b"\xff\xfe\x81 okta \x9d")
            (p / "big.tf").write_bytes(b'provider "aws" {}\n' + b"#" * 1_100_000)
            (p / "node_modules").mkdir()
            (p / "node_modules" / "x.tf").write_text('provider "google" {}', encoding="utf-8")
            s = scan.scan(p)
            self.assertEqual(s["auth"]["idp"], ["okta"])
            self.assertEqual(s["cloud"], [])
            self.assertEqual(s["iac"], [])

    def test_unreadable_file_does_not_crash(self):
        from unittest import mock
        real = Path.read_text

        def flaky(self, *a, **k):
            if self.name == "locked.py":
                raise PermissionError("denied")
            return real(self, *a, **k)

        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            (p / "locked.py").write_text("okta", encoding="utf-8")
            (p / "ok.py").write_text("keycloak", encoding="utf-8")
            with mock.patch.object(Path, "read_text", flaky):
                s = scan.scan(p)
            self.assertEqual(s["auth"]["idp"], ["keycloak"])

    def test_cli_bad_path_exit_2(self):
        r = subprocess.run([sys.executable, str(SCRIPT), str(FIX / "nope")],
                           capture_output=True, encoding="utf-8")
        self.assertEqual(r.returncode, 2)
        self.assertIn("error:", r.stderr)
        self.assertNotIn("Traceback", r.stderr)

    def test_cli_write_and_if_stale(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "main.tf").write_text('provider "aws" {}', encoding="utf-8")
            r = subprocess.run([sys.executable, str(SCRIPT), d, "--write"],
                               capture_output=True, encoding="utf-8")
            self.assertEqual(r.returncode, 0, r.stderr)
            cached = json.loads((Path(d) / ".soc2" / "scan.json").read_text(encoding="utf-8"))
            self.assertEqual(cached["cloud"], ["aws"])
            r2 = subprocess.run([sys.executable, str(SCRIPT), d, "--if-stale"],
                                capture_output=True, encoding="utf-8")
            self.assertEqual(json.loads(r2.stdout), cached)


def scan_files(files):
    """Scan a temp repo built from {relative path: text}."""
    with tempfile.TemporaryDirectory() as d:
        for rel, text in files.items():
            f = Path(d) / rel
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(text, encoding="utf-8")
        return scan.scan(d)


class FixtureCloudTest(unittest.TestCase):
    def test_gcp_fixture(self):
        s = scan.scan(FIX / "gcp")
        self.assertEqual(s["cloud"], ["gcp"])
        self.assertTrue(s["logging"]["cloud_audit_trail"])
        self.assertTrue(s["monitoring"]["alerts"])
        self.assertTrue(s["backups"]["configured"])
        self.assertEqual(s["logging"]["retention_days"], 365)
        self.assertIn("cloud-build", s["ci"])

    def test_azure_fixture(self):
        s = scan.scan(FIX / "azure")
        self.assertEqual(s["cloud"], ["azure"])
        self.assertIn("bicep", s["iac"])
        self.assertTrue(s["logging"]["cloud_audit_trail"])
        self.assertTrue(s["monitoring"]["alerts"])
        self.assertTrue(s["backups"]["configured"])
        self.assertEqual(s["secrets"]["hardcoded_hits"], 1)

    def test_docs_only_repo_reports_nothing(self):
        self.assertEqual(scan.scan(FIX / "docs_only"), scan.empty_signals())

    def test_cloud_from_deps_and_ci(self):
        self.assertEqual(scan_files({"package.json": '{"dependencies":{"@aws-sdk/client-s3":"1"}}'})["cloud"], ["aws"])
        self.assertEqual(scan_files({"package.json": '{"dependencies":{"@azure/cosmos":"1"}}'})["cloud"], ["azure"])
        self.assertEqual(scan_files({"app.yaml": "runtime: python312\n"})["cloud"], ["gcp"])
        self.assertEqual(scan_files({".github/workflows/d.yml": "steps:\n  - run: gcloud run deploy\n"})["cloud"], ["gcp"])
        self.assertEqual(scan_files({"cdk.json": "{}"})["iac"], ["cdk"])
        self.assertEqual(scan_files({"google_analytics.py": "google_analytics_id = 1"})["cloud"], [])


class SignalSemanticsTest(unittest.TestCase):
    def test_markdown_not_scanned_for_signals(self):
        s = scan_files({"README.md": "okta sso mfa tls datadog pagerduty restore test dsar ssn "
                                     "branch_protection_rules AKIAABCDEFGHIJKLMNOP"})
        self.assertEqual(s, scan.empty_signals())

    def test_markdown_filename_checks_still_work(self):
        s = scan_files({"docs/policies/access-control.md": "x", "PRIVACY.md": "x"})
        self.assertEqual(s["policies"], ["access-control"])
        self.assertTrue(s["privacy"]["privacy_notice"])

    def test_docs_soc2_dir_skipped_for_text(self):
        s = scan_files({"docs/soc2/notes.txt": "okta saml mfa"})
        self.assertEqual(s["auth"]["idp"], [])
        self.assertFalse(s["auth"]["mfa_hint"])

    def test_tls_ignores_bare_https_urls(self):
        self.assertFalse(scan_files({"a.py": 'u = "https://example.com"'})["encryption"]["tls"])
        self.assertTrue(scan_files({"a.tf": 'min_tls_version = "TLS1_2"'})["encryption"]["tls"])
        self.assertTrue(scan_files({"a.tf": 'ssl_policy = "ELBSecurityPolicy-TLS13-1-2-2021-06"'})["encryption"]["tls"])

    def test_sso_is_workforce_only(self):
        self.assertFalse(scan_files({"a.py": "client = Auth0()  # auth0 login"})["auth"]["sso"])
        s = scan_files({".github/workflows/d.yml": "permissions:\n  id-token: write\nsteps:\n"
                        "  - uses: aws-actions/configure-aws-credentials@v4\n    with:\n"
                        "      role-to-assume: arn\n      oidc: true\n"})
        self.assertFalse(s["auth"]["sso"])
        self.assertTrue(s["auth"]["ci_oidc"])
        self.assertTrue(scan_files({"a.tf": 'resource "aws_ssoadmin_permission_set" "p" {}'})["auth"]["sso"])
        self.assertTrue(scan_files({"idp.tf": "saml_metadata_url = 1"})["auth"]["sso"])

    def test_idp_list_extended(self):
        self.assertEqual(scan_files({"a.py": "import clerk"})["auth"]["idp"], ["clerk"])

    def test_centralized_needs_real_shipper(self):
        self.assertFalse(scan_files({"a.tf": 'resource "aws_cloudwatch_log_group" "g" {}'})["logging"]["centralized"])
        self.assertFalse(scan_files({"a.js": "const datadogApiKey = process.env.K"})["logging"]["centralized"])
        self.assertFalse(scan_files({"a.tf": 'resource "aws_elasticache_cluster" "c" {}\nresource "aws_eip" "elastic_ip" {}'})["logging"]["centralized"])
        self.assertTrue(scan_files({"x.yaml": "image: fluent/fluent-bit"})["logging"]["centralized"])
        self.assertTrue(scan_files({"a.tf": 'resource "google_logging_project_sink" "s" {}'})["logging"]["centralized"])
        self.assertTrue(scan_files({"filebeat.yml": "filebeat.inputs: []"})["logging"]["centralized"])

    def test_retention_is_min_and_zero_is_unlimited(self):
        s = scan_files({"a.tf": 'resource "aws_cloudwatch_log_group" "a" { retention_in_days = 400 }\n'
                                'resource "aws_cloudwatch_log_group" "b" { retention_in_days = 7 }\n'
                                'resource "aws_cloudwatch_log_group" "c" { retention_in_days = 0 }\n'})
        self.assertEqual(s["logging"]["retention_days"], 7)
        self.assertIsNone(scan_files({"a.tf": "retention_in_days = 0"})["logging"]["retention_days"])

    def test_branch_protection_rulesets(self):
        for rt in ("github_repository_ruleset", "github_organization_ruleset", "github_branch_protection"):
            s = scan_files({"a.tf": f'resource "{rt}" "r" {{}}'})
            self.assertEqual(s["change_mgmt"]["branch_protection"], "configured", rt)
        self.assertEqual(scan_files({"a.py": "x"})["change_mgmt"]["branch_protection"], "unknown")

    def test_renovaterc(self):
        for n in (".renovaterc", ".renovaterc.json", ".renovaterc.json5", "renovate.json5"):
            self.assertTrue(scan_files({n: "{}"})["deps"]["dependabot_or_renovate"], n)
        self.assertTrue(scan_files({"package.json": '{"renovate": {"extends": []}}'})["deps"]["dependabot_or_renovate"])

    def test_more_sast_tools(self):
        for tool in ("trivy", "checkov", "tfsec", "kics", "gosec", "brakeman", "njsscan",
                     "dependency-review-action", "osv-scanner", "grype"):
            self.assertTrue(scan_files({".github/workflows/s.yml": f"- uses: x/{tool}@v1"})["deps"]["sast"], tool)

    def test_alerts_and_backups_other_clouds(self):
        for rx in ("google_monitoring_alert_policy", "azurerm_monitor_metric_alert", "datadog_monitor"):
            self.assertTrue(scan_files({"a.tf": f'resource "{rx}" "x" {{}}'})["monitoring"]["alerts"], rx)
        for rx in ("azurerm_backup_policy_vm", "azurerm_recovery_services_vault", "aws_dlm_lifecycle_policy"):
            self.assertTrue(scan_files({"a.tf": f'resource "{rx}" "x" {{}}'})["backups"]["configured"], rx)

    def test_cloud_audit_trail_variants(self):
        for rx in ("aws_cloudtrail", "google_logging_organization_sink", "azurerm_monitor_log_profile"):
            self.assertTrue(scan_files({"a.tf": f'resource "{rx}" "x" {{}}'})["logging"]["cloud_audit_trail"], rx)

    def test_azure_audit_trail_needs_administrative_category(self):
        bare = 'resource "azurerm_monitor_diagnostic_setting" "x" { name = "d" }'
        self.assertFalse(scan_files({"a.tf": bare})["logging"]["cloud_audit_trail"])
        admin = bare[:-1] + ' enabled_log { category = "Administrative" } }'
        self.assertTrue(scan_files({"a.tf": admin})["logging"]["cloud_audit_trail"])
        bicep = "resource d 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = { name: 'a' }"
        self.assertFalse(scan_files({"m.bicep": bicep})["logging"]["cloud_audit_trail"])
        self.assertTrue(scan_files({"m.bicep": bicep + "\n// category: 'Administrative'"})["logging"]["cloud_audit_trail"])
        cli = "az monitor diagnostic-settings subscription create --name a --logs '[{\"category\":\"Administrative\"}]'"
        self.assertTrue(scan_files({"d.sh": cli})["logging"]["cloud_audit_trail"])

    def test_central_log_needs_setting_or_agent_not_workspace_alone(self):
        ws = 'resource "azurerm_log_analytics_workspace" "w" { name = "w" }'
        self.assertFalse(scan_files({"a.tf": ws})["logging"]["centralized"])
        self.assertFalse(scan_files({"m.bicep": "resource w 'Microsoft.OperationalInsights/workspaces@2022-10-01' = {}"})["logging"]["centralized"])
        self.assertTrue(scan_files({"a.tf": 'resource "azurerm_monitor_diagnostic_setting" "d" {}'})["logging"]["centralized"])
        self.assertTrue(scan_files({"m.bicep": "resource d 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = {}"})["logging"]["centralized"])
        self.assertTrue(scan_files({"a.tf": 'resource "azurerm_monitor_data_collection_rule" "r" {}'})["logging"]["centralized"])

    def test_cosmos_tls_and_continuous_backup(self):
        self.assertTrue(scan_files({"m.bicep": "properties: { minimalTlsVersion: 'Tls12' }"})["encryption"]["tls"])
        self.assertTrue(scan_files({"m.bicep": "backupPolicy: {\n type: 'Continuous'\n }"})["backups"]["configured"])
        self.assertTrue(scan_files({"a.tf": 'backup {\n type = "Continuous"\n }'})["backups"]["configured"])
        self.assertFalse(scan_files({"m.bicep": "properties: { x: 1 }"})["backups"]["configured"])

    def test_backup_dirs_skipped(self):
        s = scan_files({"docs/policies/_backup/old.md": "x", "docs/policies/a.md": "x"})
        self.assertEqual(s["policies"], ["a"])

    def test_runbook_placeholders(self):
        self.assertFalse(scan_files({"docs/incident-response-plan.md": "Owner: <name>\nPage {{oncall}}"})["incident"]["runbook"])
        self.assertFalse(scan_files({"docs/runbook.md": "Contact <Security Lead>"})["incident"]["runbook"])
        self.assertTrue(scan_files({"docs/incident-response-plan.md": "Page the on-call. See <https://x.example/y> and <br>"})["incident"]["runbook"])

    def test_runbook_only_for_runbook_files(self):
        def rb(path):
            return scan_files({path: "Page the on-call."})["incident"]["runbook"]
        self.assertTrue(rb("docs/runbooks/db-failover.md"))
        self.assertTrue(rb("ops/runbook-payments.md"))
        self.assertTrue(rb("playbook-ransomware.md"))
        self.assertTrue(rb("docs/incident-response-plan.md"))
        self.assertFalse(rb("docs/policies/incident-response.md"))
        self.assertFalse(rb("docs/policies/runbooks/x.md"))
        self.assertFalse(rb("docs/incident-response.md"))


class SecretsTest(unittest.TestCase):
    def hits(self, name, text):
        return scan_files({name: text})["secrets"]["hardcoded_hits"]

    def test_positive_patterns(self):
        cases = {
            "a.json": '{"c": "AccountEndpoint=https://x;AccountKey=abcDEF123456789xyz=="}',
            "b.txt": "DefaultEndpointsProtocol=https;SharedAccessSignature=sv=2020&sig=abc",
            "c.py": 'url = "https://host/blob?sv=1&sig=AbCdEf0123456789AbCdEf0123456789%3D"',
            "d.py": 'DB = "postgres://admin:hunter2@db.internal:5432/app"',
            "e.yml": 'password: "hunter2hunter2"',
            "f.json": '{"password": "p4ssw0rd"}',
            "g.tf": 'secret = "abc123abc123"',
            "h.pem": "-----BEGIN PRIVATE KEY-----\nabc\n-----END PRIVATE KEY-----",
            "i.py": 'k = "AKIAABCDEFGHIJKLMNOP"',
            "j.json": '{"type": "service_account", "private_key": "-----BEGIN PRIVATE KEY-----\\nMIIE"}',
            "k.py": 'api_key = "abcdef123456"',
            ".env.local": "DB_PASSWORD=hunter2hunter2",
            "l.py": 't = "ghp_' + "a" * 36 + '"',
        }
        for name, text in cases.items():
            self.assertGreaterEqual(self.hits(name, text), 1, name)

    def test_negative_patterns(self):
        cases = {
            "a.tf": "password = var.db_password",
            "b.tf": 'password = "${var.db_password}"',
            "c.yml": 'password: "${DB_PASSWORD}"',
            "d.py": 'password = os.environ["DB_PASSWORD"]',
            "e.py": 'password = ""',
            "f.yml": 'password: "<your-password>"',
            "g.py": 'u = "https://user@example.com/path"',
            "h.py": 'k = "AKIAIOSFODNN7EXAMPLE"',
            "i.yml": 'password: "{{ vault_pw }}"',
        }
        for name, text in cases.items():
            self.assertEqual(self.hits(name, text), 0, name)

    def test_counts_one_per_line(self):
        self.assertEqual(self.hits("a.py", 'x = "AKIAABCDEFGHIJKLMNOP"; password = "abc12345"\ny = 1\n'), 1)


class SecretsCliTest(unittest.TestCase):
    def test_secrets_flag_prints_only_locations(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "src").mkdir()
            (Path(d) / "src" / "a.py").write_text('x = 1\nk = "AKIAABCDEFGHIJKLMNOP"\n', encoding="utf-8")
            (Path(d) / "local.settings.json").write_text(
                '{"v": "AccountKey=Zm9vYmFyYmF6cXV4MTIzNDU2;"}', encoding="utf-8")
            r = subprocess.run([sys.executable, str(SCRIPT), d, "--secrets"],
                               capture_output=True, encoding="utf-8")
            self.assertEqual(r.returncode, 0, r.stderr)
            lines = r.stdout.strip().splitlines()
            self.assertIn("src/a.py:2 aws-key-id", lines)
            self.assertIn("local.settings.json:1 azure-key", lines)
            self.assertEqual(lines[-1], "total: 2")
            self.assertNotIn("AKIA", r.stdout)
            self.assertNotIn("Zm9v", r.stdout)
            self.assertFalse((Path(d) / ".soc2").exists())

    def test_secrets_flag_none(self):
        r = subprocess.run([sys.executable, str(SCRIPT), str(FIX / "empty"), "--secrets"],
                           capture_output=True, encoding="utf-8")
        self.assertEqual(r.stdout.strip(), "total: 0")


class SecretKindTest(unittest.TestCase):
    def kinds(self, text, is_env=False):
        return [k for _, k in scan.secret_hits(text, is_env=is_env)]

    def test_kind_labels(self):
        cases = [
            ('k = "AKIAABCDEFGHIJKLMNOP"', "aws-key-id"),
            ("-----BEGIN RSA PRIVATE KEY-----", "private-key"),
            ('u = "postgres://admin:hunter2@db:5432/app"', "url-credential"),
            ('password: "hunter2hunter2"', "db-password"),
            ('Server=x;Password=abcd1234efgh;', "db-password"),
            ('c = "AccountKey=abcDEF123456789xyz=="', "azure-key"),
            ('c = "Endpoint=sb://x/;SharedAccessKey=abcDEF123456789xyz0123="', "azure-key"),
            ('{"private_key": "-----BEGIN PRIVATE KEY-----\\nMIIE"}', "gcp-sa-key"),
            ('t = "ghp_' + "a" * 36 + '"', "token"),
            ('api_key = "abcdef123456"', "generic-secret"),
        ]
        for text, kind in cases:
            self.assertEqual(self.kinds(text), [kind], text)

    def test_kinds_are_the_allowed_set(self):
        self.assertEqual(scan.SECRET_KINDS, {"aws-key-id", "private-key", "url-credential", "db-password",
                                             "azure-key", "gcp-sa-key", "token", "generic-secret"})


class NameBasedSecretTest(unittest.TestCase):
    KEY = "Zm9vYmFyYmF6cXV4MTIzNDU2Nzg5MA=="

    def hits(self, name, text):
        return scan_files({name: text})["secrets"]["hardcoded_hits"]

    def test_json_settings_by_name(self):
        for fn in ("local.settings.json", "appsettings.json", "appsettings.Production.json"):
            self.assertEqual(self.hits(fn, '{"Values": {"COSMOS_KEY": "%s"}}' % self.KEY), 1, fn)
        self.assertEqual(self.hits("local.settings.json", '{"ServiceBusSecret": "%s"}' % self.KEY), 1)
        self.assertEqual(self.hits("prod.env", "COSMOS_KEY=%s" % self.KEY), 1)
        self.assertEqual(self.hits(".env", 'STORAGE_KEY="%s"' % self.KEY), 1)

    def test_sharedaccesskey(self):
        text = '{"c": "Endpoint=sb://x.servicebus.windows.net/;SharedAccessKeyName=r;SharedAccessKey=abcDEF123456789xyz0123="}'
        self.assertEqual(self.hits("a.json", text), 1)

    def test_name_rule_exclusions(self):
        for v in ("UseDevelopmentStorage=true", "@Microsoft.KeyVault(SecretUri=https://v.vault.azure.net/secrets/a)",
                  "%COSMOS_KEY%", "${COSMOS_KEY}", "short", "https://x.vault.azure.net/"):
            text = '{"Values": {"COSMOS_KEY": "%s", "AzureWebJobsStorage": "%s"}}' % (v, v)
            self.assertEqual(self.hits("local.settings.json", text), 0, v)
        self.assertEqual(self.hits("local.settings.json",
                                   '{"Values": {"FUNCTIONS_WORKER_RUNTIME": "node-abcdefghijklmnopqrstu1"}}'), 0)

    def test_name_rule_not_applied_to_other_files(self):
        self.assertEqual(self.hits("config.json", '{"COSMOS_KEY": "%s"}' % self.KEY), 0)


class ScopeCliTest(unittest.TestCase):
    def run_scope(self, arg):
        return subprocess.run([sys.executable, str(SCRIPT), str(FIX / "empty"), "--scope", arg],
                              capture_output=True, encoding="utf-8")

    def test_security_only(self):
        r = self.run_scope("security")
        self.assertEqual(r.returncode, 0, r.stderr)
        ids = r.stdout.split()
        self.assertIn("GOV-01", ids)
        self.assertIn("RSK-05", ids)  # cites CC9.1 as well as A1.2
        self.assertNotIn("AV-03", ids)

    def test_security_always_and_extra_category(self):
        avail = set(self.run_scope("availability").stdout.split())
        sec = set(self.run_scope("security").stdout.split())
        self.assertIn("GOV-01", avail)
        self.assertIn("AV-03", avail)
        self.assertGreater(len(avail), len(sec))

    def test_spaces_in_list(self):
        self.assertEqual(self.run_scope("security, privacy").stdout, self.run_scope("security,privacy").stdout)

    def test_unknown_key_errors(self):
        r = self.run_scope("security,bogus")
        self.assertEqual(r.returncode, 2)
        self.assertIn("bogus", r.stderr)
        self.assertNotIn("Traceback", r.stderr)


if __name__ == "__main__":
    unittest.main()
