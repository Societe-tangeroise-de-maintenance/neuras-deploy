import subprocess

desired_ip = input("Enter the desired IP address: ")
gateway = input("Enter the gateway address: ")
netplan_config_path = "/etc/netplan/01-netcfg.yaml"  # Path to your Netplan config file

# Modify the Netplan configuration file with the user-provided IP address and gateway
netplan_config = f"""
network:
  version: 2
  renderer: networkd
  ethernets:
    eno1:
      dhcp4: no
      addresses: [{desired_ip}/24]
      gateway4: {gateway}
      nameservers:
        addresses: [8.8.8.8, 8.8.4.4]
"""

# Write the modified configuration to the Netplan file
with open(netplan_config_path, "w") as f:
    f.write(netplan_config)

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
