#!/bin/bash 

# Update system packages
dnf update -y

# Install Java 21 (Amazon Corretto)
dnf install -y java-21-amazon-corretto

# Install Docker
dnf install -y docker
systemctl enable docker
systemctl start docker

# Add default user to Docker group
usermod -aG docker ec2-user

# Install Docker Compose v2 (as a CLI plugin)
mkdir -p /usr/local/lib/docker/cli-plugins

curl -SL https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64 \
    -o /usr/local/lib/docker/cli-plugins/docker-compose

chmod +x /usr/local/lib/docker/cli-plugins/docker-compose

# Ensure Docker Compose has correct permissions
chown root:root /usr/local/lib/docker/cli-plugins/docker-compose

# Install Python 3.12 and venv support
dnf install -y python3.12 python3.12-venv

# Add Google Chrome repository
cat <<EOF > /etc/yum.repos.d/google-chrome.repo
[google-chrome]
name=Google Chrome
baseurl=https://dl.google.com/linux/chrome/rpm/stable/x86_64
enabled=1
gpgcheck=1
gpgkey=https://dl.google.com/linux/linux_signing_key.pub
EOF

# Install Google Chrome
dnf install -y google-chrome-stable

