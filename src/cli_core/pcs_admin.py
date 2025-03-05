import subprocess
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_DIR = os.path.join(BASE_DIR, "configs")

ipmi_config = os.path.join(CONFIG_DIR, "ipmi_config.json")

def load_config(CONFIG_PATH):
    try:
        with open(CONFIG_PATH, "r") as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading config: {str(e)}")
        return {}

def save_config(config):
    """Save IPMI config to JSON file."""
    with open(ipmi_config, "w") as f:
        json.dump(config, f, indent=4)

ipmi_data = load_config(ipmi_config)

def change_pcscli_password():
    """Allows the user to change the password for the pcscli user."""
        
    print("WARNING: You are about to change the password for the 'pcscli' user.")
    confirmation = input("Do you want to continue? (y/n): ").strip().lower()

    if confirmation != 'y':
        print("Password change canceled.")
        return

    # Execute password change command
    try:
        subprocess.run(["passwd"], stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr, check=True)
        print("Password changed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to change password: {e}")

def add_node():
    """Add a new node to the IPMI config."""

    node_index = input("Enter node index: ").strip()
    if node_index in ipmi_data["nodes"]:
        print(f"Node {node_index} already exists! Use 'pcscli edit node -i {node_index}' to modify it.")
        return

    bmc_user = input("Enter BMC username: ").strip()
    bmc_pass = input("Enter BMC password: ").strip()
    ipmi_ip = input("Enter IPMI interface IP: ").strip()

    print("\nSummary of entered data:")
    print(f"  Node Index: {node_index}")
    print(f"  BMC Username: {bmc_user}")
    print(f"  BMC Password: {'*' * len(bmc_pass)} (hidden)")
    print(f"  IPMI IP: {ipmi_ip}")
    
    confirm = input("Confirm? (y/n): ").strip().lower()
    if confirm != "y":
        print("Operation canceled.")
        return

    ipmi_data["nodes"][node_index] = {
        "ip": ipmi_ip,
        "user": bmc_user,
        "password": bmc_pass
    }
    
    save_config(ipmi_data)
    print(f"New node {node_index} successfully added!")
