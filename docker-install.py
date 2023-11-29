import subprocess

# Apply the Netplan configuration changes
subprocess.run(["sudo", "netplan", "apply"])

# Docker installation steps
# Download the Docker installation script
subprocess.run(["curl", "-fsSL", "https://get.docker.com", "-o", "get-docker.sh"])

# Execute the Docker installation script
subprocess.run(["sudo", "sh", "get-docker.sh"])

# Install Docker Compose
subprocess.run(["sudo", "apt-get", "update"])
subprocess.run(["sudo", "apt-get", "install", "docker-compose-plugin"])