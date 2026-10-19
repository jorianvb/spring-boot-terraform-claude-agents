output "vpc_id" {
  description = "Identifiant du VPC"
  value       = aws_vpc.this.id
}

output "public_subnet_ids" {
  description = "Identifiants des sous-reseaux publics"
  value       = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  description = "Identifiants des sous-reseaux prives"
  value       = aws_subnet.private[*].id
}
