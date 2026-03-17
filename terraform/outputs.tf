output "server_public_ip" {
  description = "Public IP of the web server"
  value       = aws_instance.web.public_ip
}

output "s3_bucket_name" {
  description = "S3 bucket for artifacts"
  value       = aws_s3_bucket.artifacts.id
}

output "vpc_id" {
  description = "VPC ID"
  value       = aws_vpc.main.id
}