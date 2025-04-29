#!/bin/bash

# Update and install prerequisites
dnf update -y
dnf install -y java-21-openjdk git curl ca-certificates gnupg2 lsb-core shadow-utils wget dnf-plugins-core

# Install Docker
dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
dnf install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Enable and start Docker
systemctl enable --now docker

# Add 'ec2-user' to the docker group
usermod -aG docker ec2-user

# Install Python 3.12 and venv (from source, since DNF doesn’t have it yet)
dnf groupinstall -y "Development Tools"
dnf install -y gcc openssl-devel bzip2-devel libffi-devel zlib-devel wget make

cd /usr/src
wget https://www.python.org/ftp/python/3.12.3/Python-3.12.3.tgz
tar xvf Python-3.12.3.tgz
cd Python-3.12.3
./configure --enable-optimizations
make altinstall

# Ensure Python 3.12 is linked
ln -s /usr/local/bin/python3.12 /usr/bin/python3.12
python3.12 -m ensurepip
python3.12 -m pip install virtualenv

# Install Google Chrome (via RPM)
cat << EOF > /etc/yum.repos.d/google-chrome.repo
[google-chrome]
name=google-chrome
baseurl=https://dl.google.com/linux/chrome/rpm/stable/x86_64
enabled=1
gpgcheck=1
gpgkey=https://dl-ssl.google.com/linux/linux_signing_key.pub
EOF

dnf install -y google-chrome-stable
