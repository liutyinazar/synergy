# AWS EC2 Deployment

This directory contains Terraform configuration for deploying the application to AWS EC2.

## Prerequisites

1. AWS CLI installed and configured
2. Terraform installed
3. SSH key pair in AWS

## Deployment Steps

1. Copy `terraform.tfvars.example` to `terraform.tfvars`:
   ```bash
   cp terraform.tfvars.example terraform.tfvars
   ```

2. Edit `terraform.tfvars` and set your values:
   ```hcl
   aws_region    = "us-east-1"
   instance_type = "t2.micro"
   key_name      = "your-key-name"
   ```

3. Initialize Terraform:
   ```bash
   terraform init
   ```

4. Apply the configuration:
   ```bash
   terraform apply
   ```

5. After deployment, SSH into the instance:
   ```bash
   ssh -i /path/to/your-key.pem ubuntu@<instance-public-ip>
   ```

6. Clone your repository and start the application:
   ```bash
   git clone <your-repo-url>
   cd <your-repo>
   docker-compose up -d
   ```

## Cleanup

To destroy the infrastructure:
```bash
terraform destroy
``` 