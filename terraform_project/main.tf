provider "aws" {
  region = "us-east-1" # Replace with the desired region
}

# Security Groups
resource "aws_security_group" "bastion_sg" {
  name_prefix = "bastion-sg"
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "elb_sg" {
  name_prefix = "elb-sg"
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "webapp_sg" {
  name_prefix = "webapp-sg"
  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    security_groups = [aws_security_group.elb_sg.id]
  }
}

resource "aws_security_group" "nat_sg" {
  name_prefix = "nat-sg"
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Instances
resource "aws_instance" "bastion" {
  ami           = "ami-12345678" # Replace with a valid AMI ID
  instance_type = "t2.micro"
  security_groups = [aws_security_group.bastion_sg.name]
}

resource "aws_instance" "web_app" {
  ami           = "ami-12345678" # Replace with a valid AMI ID
  instance_type = "t2.micro"
  security_groups = [aws_security_group.webapp_sg.name]
}

resource "aws_instance" "nat" {
  ami           = "ami-12345678" # Replace with a valid AMI ID
  instance_type = "t2.micro"
  security_groups = [aws_security_group.nat_sg.name]
}

# Load Balancer
resource "aws_elb" "web_lb" {
  name               = "web-app-lb"
  security_groups    = [aws_security_group.elb_sg.id]
  availability_zones = ["us-east-1a"] # Replace with the desired AZs

  listener {
    instance_port     = 8080
    instance_protocol = "HTTP"
    lb_port           = 443
    lb_protocol       = "HTTPS"
  }

  health_check {
    target              = "HTTP:8080/"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 2
  }
}
