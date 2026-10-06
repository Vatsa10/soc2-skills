provider "aws" { region = "us-east-1" }
resource "aws_kms_key" "k" {}
resource "aws_cloudtrail" "t" { name = "t" }
resource "aws_cloudwatch_log_group" "g" { retention_in_days = 400 }
resource "aws_db_instance" "db" {
  storage_encrypted       = true
  backup_retention_period = 7
}
