import subprocess
import json
import os
from datetime import datetime
import shutil

# ANSI color codes
RESET = "\033[0m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"

#---------------------- File Handlers ----------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_DIR = os.path.join(BASE_DIR, "configs")
BACKUP_DIR = os.path.join(BASE_DIR, "backups")

ipmi_config = os.path.join(CONFIG_DIR, "ipmi_config.json")
hrmcli_config = os.path.join(CONFIG_DIR, "hrmcli_config.json")

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

hrmcli_data = load_config(hrmcli_config)
VERSION = hrmcli_data["version"]

ipmi_data = load_config(ipmi_config)

#---------------------- Helper Functions ----------------------

def get_node_count():
    """Returns the number of configured nodes from ipmi_config.json."""
    return len(ipmi_data.get("nodes", {}))

def get_serial_status():
    """Checks if the serial console is enabled."""
    try:
        result = subprocess.run(["systemctl", "is-enabled", "serial-getty@ttyS0.service"],
                                capture_output=True, text=True)
        return "Enabled" if "enabled" in result.stdout else "Disabled"
    except Exception:
        return "Unknown"

def get_network_info():
    """Gets the network IP and subnet for the primary interface."""
    try:
        result = subprocess.run(["ip", "-4", "addr", "show", "eth0"], capture_output=True, text=True)
        for line in result.stdout.split("\n"):
            if "inet" in line:
                return line.split()[1]  # Should extract ip. ie - '172.16.0.1/29'
    except Exception:
        return "Unknown"
    return "Unknown"

def get_system_uptime():
    """Gets system uptime in a readable format."""
    try:
        result = subprocess.run(["uptime"], capture_output=True, text=True)
        return result.stdout.strip().replace("up ", "")
    except Exception:
        return "Unknown"

def get_usage_bar(usage_percent, bar_length=20):
    """Generate an ASCII progress bar with color based on usage percentage."""
    filled_blocks = int((usage_percent / 100) * bar_length)

    # Set color based on usage level
    if usage_percent < 50:
        color = GREEN
    elif usage_percent < 80:
        color = YELLOW
    else:
        color = RED

    return f"{color}[{'█' * filled_blocks}{'-' * (bar_length - filled_blocks)}] {usage_percent}%{RESET}"

def get_disk_usage():
    """Get disk usage and represent it as a colored bar."""
    total, used, free = shutil.disk_usage("/")
    used_percent = (used / total) * 100
    return f"Disk: {get_usage_bar(used_percent)}, {free // (1024 ** 3)}GB free"


def get_last_backup():
    """Finds the most recent backup timestamp."""
    try:
        backups = [f for f in os.listdir(BACKUP_DIR) if f.endswith(".json")]
        if backups:
            latest_backup = max(backups, key=lambda x: os.path.getctime(os.path.join(BACKUP_DIR, x)))
            timestamp = datetime.fromtimestamp(os.path.getctime(os.path.join(BACKUP_DIR, latest_backup)))
            return timestamp.strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return "Never"
    return "Never"

def ensure_backup_dir():
    """Ensure the backup directory exists."""
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

def list_backups():
    """List available backup files."""
    backups = sorted([f for f in os.listdir(BACKUP_DIR) if f.startswith("ipmi_config_backup_")])
    if not backups:
        print("No backups available.")
        return None
    print("\nAvailable backups:")
    for i, backup in enumerate(backups, start=1):
        print(f"{i}. {backup}")
    return backups

#---------------------- ADMIN Functions ----------------------

def update():
    """Updates HRMCLI by pulling the latest changes from the repository."""
    repo_path = "/opt/HRMCLI/"
    try:
        print("Updating HRMCLI...")
        output = subprocess.run(["git", "-C", repo_path, "pull"], capture_output=True, text=True)
        print(output.stdout)
        print("HRMCLI has been updated successfully.")
    except Exception as e:
        print(f"Error updating HRMCLI: {e}")

def change_password():
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
    print(f"  BMC Password: {bmc_pass}")
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

def edit_node():
    # Get node index to edit
    node_index = input("Enter node index to edit: ").strip()

    # Check if the node exists
    if node_index not in ipmi_data["nodes"]:
        print(f"Error: Node {node_index} does not exist!")
        return

    # Display current values
    current_node = ipmi_data["nodes"][node_index]
    print(f"\nEditing Node {node_index} (Press Enter to keep current values)\n")
    
    # Get new values (keep existing if Enter is pressed)
    new_ip = input(f"Enter new IP (Current: {current_node['ip']}): ").strip() or current_node["ip"]
    new_user = input(f"Enter new BMC username (Current: {current_node['user']}): ").strip() or current_node["user"]
    new_password = input(f"Enter new BMC password (Current: {current_node['password']}): ").strip() or current_node["password"]

    # Update node details
    ipmi_data["nodes"][node_index] = {
        "ip": new_ip,
        "user": new_user,
        "password": new_password
    }

    # Save changes
    save_config(ipmi_data)

    print(f"Node {node_index} successfully updated!")

def remove_node():
    # Get node index to remove
    node_index = input("Enter node index to remove: ").strip()

    # Check if the node exists
    if node_index not in ipmi_data["nodes"]:
        print(f"Error: Node {node_index} does not exist!")
        return

    # Ask for confirmation
    confirm = input(f"Are you sure you want to remove Node {node_index}? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("Operation canceled.")
        return

    # Remove the node
    del ipmi_data["nodes"][node_index]

    # Save changes
    save_config(ipmi_data)

    print(f"Node {node_index} successfully removed!")

def list_nodes(): 
    if not ipmi_data:
        print("No nodes found in configuration.")
        return
    
    # Print header
    print("Node Index  | IP Address   | Username")
    print("------------------------------------")
    
    # Print node details
    for index, details in sorted(ipmi_data["nodes"].items(), key=lambda x: int(x[0])):
        print(f"{index:<11} | {details['ip']:<12} | {details['user']}")

def pcscli_status():
    """Displays PCSCLI system status."""
    print(" ")
    print(f"{VERSION} - Status")
    print("-" * 22)
    print(get_disk_usage())
    print(f"Nodes Configured: {get_node_count()}")
    print(f"Serial Console: {get_serial_status()}")
    print(f"Network: {get_network_info()} (eth0)")
    print(f"System Uptime: {get_system_uptime()}")
    print(f"Last Backup: {get_last_backup()}")
    print(" ")

def backup_config():
    """Creates a timestamped backup of ipmi_config.json."""
    ensure_backup_dir()
    
    # Generate timestamped backup filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"ipmi_config_backup_{timestamp}.json"
    backup_path = os.path.join(BACKUP_DIR, backup_filename)

    try:
        shutil.copy(ipmi_config, backup_path)
        print(f"Backup successful: {backup_filename}")
    except Exception as e:
        print(f"Error creating backup: {e}")

def restore_config():
    """Restore a selected backup file."""
    backups = list_backups()
    if not backups:
        return

    # Ask user to select a backup
    try:
        choice = int(input("\nEnter the number of the backup to restore: "))
        if choice < 1 or choice > len(backups):
            print("Invalid selection.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return

    # Restore selected backup
    backup_file = backups[choice - 1]
    backup_path = os.path.join(BACKUP_DIR, backup_file)
    print(f"\nRestoring {backup_file}...")

    try:
        shutil.copy(backup_path, ipmi_config)
        global ipmi_data
        ipmi_data = load_config(ipmi_config)
        print("Configuration restored successfully!")
    except Exception as e:
        print(f"Error restoring backup: {e}")
