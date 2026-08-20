variable "aws_region" {
  description = "AWS region where the data lake is hosted."
  type        = string
  default     = "eu-west-2"
}

variable "bucket_name" {
  description = "S3 bucket used by the data engineering platform."
  type        = string
  default     = "tom-data-engineering-platform"
}

variable "github_repository" {
  description = "GitHub repository allowed to assume the deployment role."
  type        = string
  default     = "thomasrawnson/aws-data-engineering-platform"
}