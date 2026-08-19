output "data_lake_bucket_name" {
  description = "Name of the data lake S3 bucket."
  value       = aws_s3_bucket.data_lake.bucket
}

output "data_lake_bucket_arn" {
  description = "ARN of the data lake S3 bucket."
  value       = aws_s3_bucket.data_lake.arn
}