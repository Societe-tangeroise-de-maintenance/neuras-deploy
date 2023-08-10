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
    eth0:
      dhcp4: no
      addresses: [{desired_ip}/24]
      gateway4: {gateway}
"""

# Write the modified configuration to the Netplan file
with open(netplan_config_path, "w") as f:
    f.write(netplan_config)

# Apply the Netplan configuration changes
subprocess.run(["sudo", "netplan", "apply"])
