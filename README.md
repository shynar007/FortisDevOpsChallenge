# Fortis DevOps Challenge

This repository contains solutions for the Fortis DevOps Challenge. It includes:
1. A Python script to group EC2 instances by AMI.
2. A Terraform configuration to provision AWS resources.

## Project Structure
FortisDevOpsChallenge/
├── group_ec2_by_ami.py        # Python script for Question #1
├── terraform_project/         # Folder containing Terraform configuration
│   ├── main.tf                # Terraform main configuration file
│   ├── variables.tf           # Terraform variables file (It is optional for me)
│   ├── output.tf              # Terraform outputs file (this is optional too)
├── README.md                  # Project documentation

Question #1: Python Script
The group_ec2_by_ami.py script is designed to:

Gather information about all EC2 instances in the current AWS region.
Group the instances by the AMI (Amazon Machine Image) they use.
Output the data as a JSON object.
Mock Implementation
Since AWS access was not available, so i decided the script uses mock data to simulate AWS API responses. This is to ensure the script can run successfully without AWS credentials.

How to Run

Install Python 3.x on your system.

Install the required library:
pip install boto3

Run the script:
python3 group_ec2_by_ami.py

Example Output will be: 

{
    "ami-12345": {
        "ImageDescription": "Mock description for ami-12345",
        "ImageName": "Mock name for ami-12345",
        "ImageLocation": "mock_account/ami-12345",
        "OwnerId": "mock_owner_id",
        "InstanceIds": [
            "i-12345",
            "i-67890"
        ]
    },
    "ami-67890": {
        "ImageDescription": "Mock description for ami-67890",
        "ImageName": "Mock name for ami-67890",
        "ImageLocation": "mock_account/ami-67890",
        "OwnerId": "mock_owner_id",
        "InstanceIds": [
            "i-13579"
        ]
    }
}


Question #2: Terraform Configuration

The Terraform configuration in terraform_project/ provisions the following resources:

Bastion Host: For SSH access.
Web App Server: For hosting the application.
NAT Instance: To enable outbound traffic for the web app server.
Elastic Load Balancer (ELB): To distribute incoming traffic to the web app server.
Security Groups:
bastion_sg: Allows SSH (port 22) traffic.
elb_sg: Allows HTTPS (port 443) traffic.
webapp_sg: Allows traffic from the ELB to the web app server on port 8080.
nat_sg: Allows outbound traffic.

Why We Stopped at terraform validate

Due to the lack of AWS credentials, I stopped at validating the Terraform configuration. The configuration is correct and ready for deployment if credentials are provided.

How to Run

Navigate to the Terraform project folder:
cd terraform_project

Initialize Terraform:
terraform init

Validate the configuration:
terraform validate

(Optional) Plan and apply the configuration in an AWS account:
terraform plan
terraform apply


Testing Note

The Python script uses mock data, so no AWS credentials are required.
The Terraform configuration was validated but not applied due to the lack of AWS credentials.