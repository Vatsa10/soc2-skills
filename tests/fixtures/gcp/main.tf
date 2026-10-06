provider "google" { project = "p" }
resource "google_logging_project_sink" "audit" { name = "audit" }
resource "google_monitoring_alert_policy" "cpu" { display_name = "cpu" }
resource "google_sql_database_instance" "db" {
  settings {
    backup_configuration { enabled = true }
  }
}
resource "google_logging_project_bucket_config" "b" { retention_days = 365 }
