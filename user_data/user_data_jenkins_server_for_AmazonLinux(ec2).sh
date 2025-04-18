#!/bin/bash

# This script sets up a Jenkins server on an Amazon Linux 2 machine.
# It installs Java, Jenkins, Docker (so Jenkins can run Docker containers),
# Python venv, and Google Chrome (for testing tools like Selenium).
# It also ensures Jenkins starts on boot and has the needed permissions to use Docker.

exec > >(tee /var/log/user-data.log | logger -t user-data -s 2>/dev/console) 2>&1

# Update the system
yum update -y

# Install Java 17 (Amazon Corretto)
amazon-linux-extras enable corretto17
yum install -y java-17-amazon-corretto

# Verify Java
java -version

# Add Jenkins repo
wget -O /etc/yum.repos.d/jenkins.repo https://pkg.jenkins.io/redhat-stable/jenkins.repo
rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io-2023.key

# Install Jenkins
yum install -y jenkins

# Enable and start Jenkins
systemctl enable jenkins
systemctl start jenkins
systemctl status jenkins

# Install Docker
yum install -y docker
systemctl enable docker
systemctl start docker

# Add Jenkins and EC2 default user to docker group
usermod -aG docker jenkins
usermod -aG docker ec2-user

# Restart Jenkins to apply group changes
systemctl restart jenkins

# Install Python 3.12 (via source or custom repo if needed)
# Amazon Linux 2 comes with Python 3.7; to install Python 3.12 you need IUS or build manually
# For simplicity, we'll install Python 3 and venv
yum install -y python3 python3-venv

# Install Chrome dependencies
yum install -y wget curl unzip

# Download and install Google Chrome
cat <<EOF > /etc/yum.repos.d/google-chrome.repo
[google-chrome]
name=google-chrome
baseurl=http://dl.google.com/linux/chrome/rpm/stable/x86_64
enabled=1
gpgcheck=1
gpgkey=https://dl-ssl.google.com/linux/linux_signing_key.pub
EOF

yum install -y google-chrome-stable
