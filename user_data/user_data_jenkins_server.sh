#!/bin/bash

# This script sets up a Jenkins server on an Ubuntu machine.
# It installs Java, Jenkins, Docker (so Jenkins can run Docker containers),
# Python venv, and Google Chrome (for testing tools like Selenium).
# It also ensures Jenkins starts on boot and has the needed permissions to use Docker.

# Redirect all output (stdout and stderr) to a log file and the system logger
exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1

# Update the system package list
sudo apt update

# Install required dependencies for Jenkins and Java
sudo apt install -y fontconfig openjdk-17-jre wget gnupg2 software-properties-common

# Verify Java installation
java -version

# Download Jenkins GPG key and save it in a secure location
wget -O /usr/share/keyrings/jenkins-keyring.asc https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key

# Add Jenkins repository to apt sources
echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/" > /etc/apt/sources.list.d/jenkins.list

# Update the package list again with the new Jenkins repository
sudo apt update

# Try to install Jenkins, allow failures to avoid breaking the script
sudo apt install -y jenkins || true

# Fix any broken dependencies
sudo apt install -f -y

# Ensure Jenkins is installed
sudo apt install -y jenkins

# Enable Jenkins service to start on boot
sudo systemctl enable jenkins

# Start Jenkins service
sudo systemctl start jenkins

# Print the current status of Jenkins service
sudo systemctl status jenkins

# Update package list before installing Docker
apt-get update

# Install Docker dependencies
apt-get install -y ca-certificates curl

# Create directory for storing Docker's GPG key
install -m 0755 -d /etc/apt/keyrings

# Download Docker's GPG key and store it
curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc

# Set correct permissions on the GPG key
chmod a+r /etc/apt/keyrings/docker.asc

# Add Docker's repository to apt sources
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  tee /etc/apt/sources.list.d/docker.list > /dev/null

# Update package list again to include Docker packages
apt-get update

# Install Docker and related components
apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y

# Add Jenkins user to the Docker group
usermod -aG docker jenkins

# Add Ubuntu user to the Docker group
usermod -aG docker ubuntu

# Restart Jenkins to apply Docker permissions
systemctl restart jenkins

# Install Python 3.12 virtual environment package
apt install python3.12-venv -y

# Add Google Chrome repository key
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -

# Add Google Chrome repository to apt sources
sh -c 'echo "deb https://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'

# Update package list to include Google Chrome
apt-get update

# Install Google Chrome
apt-get install google-chrome-stable -y

reboot
