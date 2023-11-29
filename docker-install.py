import subprocess


# Docker installation steps
# Download the Docker installation script
subprocess.run(["curl", "-fsSL", "https://get.docker.com", "-o", "get-docker.sh"])

# Execute the Docker installation script
subprocess.run(["sudo", "sh", "get-docker.sh"])

# Install Docker Compose
subprocess.run(["sudo", "apt-get", "update"])
subprocess.run(["sudo", "apt", "install", "docker-compose"])