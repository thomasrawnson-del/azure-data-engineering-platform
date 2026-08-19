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