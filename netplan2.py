import subprocess
import os
import shutil
from glob import glob

def get_active_interface():
    try:
        result = subprocess.run(
            ["ip", "-o", "link", "show", "up"],
            stdout=subprocess.PIPE,
            check=True,
            text=True
        )
        for line in result.stdout.strip().split("\n"):
            iface = line.split(":")[1].strip()
            if iface != "lo":
                return iface
    except Exception as e:
        print(f"Error detecting interface: {e}")
        exit(1)

def detect_netplan_config():
    netplan_files = glob("/etc/netplan/*.yaml")
    if not netplan_files:
        print("❌ No Netplan config found in /etc/netplan/")
        exit(1)
    return netplan_files[0]

def backup_config(path):
    backup_path = path + ".bak"
    shutil.copy(path, backup_path)
    print(f"✅ Backup created at: {backup_path}")
    return backup_path

def write_new_config(path, iface, ip, gateway):
    config = f"""
network:
  version: 2
  renderer: networkd
  ethernets:
    {iface}:
      dhcp4: no
      addresses: [{ip}/24]
      gateway4: {gateway}
      nameservers:
        addresses: [8.8.8.8, 8.8.4.4]
"""
    with open(path, "w") as f:
        f.write(config)
    print("✅ New configuration written.")

def apply_netplan():
    print("⏳ Applying Netplan configuration...")
    result = subprocess.run(["sudo", "netplan", "apply"])
    if result.returncode == 0:
        print("✅ Netplan applied successfully.")
    else:
        print("❌ Netplan failed to apply.")

def restore_backup(path):
    backup_path = path + ".bak"
    if os.path.exists(backup_path):
        shutil.copy(backup_path, path)
        print("🔁 Original configuration restored.")
        subprocess.run(["sudo", "netplan", "apply"])
    else:
        print("❌ No backup file found to restore.")

def main():
    iface = get_active_interface()
    print(f"🧠 Detected interface: {iface}")

    config_path = detect_netplan_config()
    print(f"🧾 Using config file: {config_path}")
    backup_config(config_path)

    ip = input("📥 Enter the new static IP address (e.g., 192.168.1.100): ").strip()
    gateway = input("📥 Enter the gateway address (e.g., 192.168.1.1): ").strip()

    write_new_config(config_path, iface, ip, gateway)

    confirm = input("❓ Apply changes now? [y/N]: ").strip().lower()
    if confirm == "y":
        apply_netplan()
    else:
        print("⚠️ Skipped applying Netplan.")

    revert = input("🔄 Do you want to restore the original configuration? [y/N]: ").strip().lower()
    if revert == "y":
        restore_backup(config_path)
    else:
        print("✅ Done. Original config is backed up if needed.")

if __name__ == "__main__":
    main()
