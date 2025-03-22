#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

# Default username and password
HRMCLI_USER="hrmcli"
DEFAULT_PASSWORD="hrmcli"
INSTALL_DIR="/opt/HRMCLI"
REPO_URL="https://github.com/AustinoBlack/HRMCLI.git"
DEFAULT_IP="172.16.0.1/29"

# Create the HrmCli user if it does not exist
if ! id "$HRMCLI_USER" &>/dev/null; then
    echo "Creating user: $HRMCLI_USER"
    useradd -m -s /bin/bash "$HRMCLI_USER"
    echo "$HRMCLI_USER:$DEFAULT_PASSWORD" | chpasswd
fi

# Install required dependencies
apt update
apt install -y ipmitool python3 python3-pip git

# Clone HRMCLI repository
if [ ! -d "$INSTALL_DIR" ]; then
    echo "Cloning HRMCLI repository into $INSTALL_DIR"
    git clone "$REPO_URL" "$INSTALL_DIR"
    chown -R "$HRMCLI_USER":"$HRMCLI_USER" "$INSTALL_DIR"
fi

# Add auto-launch to bashrc for the default user
BASHRC_FILE="/home/$HRMCLI_USER/.bashrc"
cat <<EOL >> "$BASHRC_FILE"

# Auto-launch pcs_shell for the pcscli user and exit on exit
if [ -t 0 ]; then
    USER="user"
    LAST_LOGIN=\$(last -i \$USER | head -1 | awk '{print \$6, \$7, \$8, \$9 " from " \$3}')
    echo "Last login: \$LAST_LOGIN"
    python3 /opt/HRMCLI/src/cli_core/pcs_shell.py
    exit
fi

EOL

# Configure Static IP
echo "Attention!"
read -p "Enter a new static IP and subnet (or press Enter to keep default: $DEFAULT_IP): " CUSTOM_IP
if [ -z "$CUSTOM_IP" ]; then
    CUSTOM_IP="$DEFAULT_IP"
fi

# Function to get the active Ethernet interface
get_interface() {
    nmcli device status | awk '$2 == "ethernet" {print $1; exit}'
}

# Function to get the correct connection profile name
get_connection_name() {
    nmcli -g NAME,DEVICE connection show | grep "$1" | cut -d ':' -f1
}

INTERFACE=$(get_interface)

if [ -z "$INTERFACE" ]; then
    echo "No Ethernet interface found. Exiting."
    exit 1
fi

CONNECTION_NAME=$(get_connection_name "$INTERFACE")

if [ -z "$CONNECTION_NAME" ]; then
    echo "No connection profile found for $INTERFACE. Exiting."
    exit 1
fi

echo "Setting IP for $INTERFACE using connection profile: $CONNECTION_NAME"

# Set IP address
nmcli connection modify "$CONNECTION_NAME" ipv4.addresses "$CUSTOM_IP" ipv4.method manual
nmcli connection up "$CONNECTION_NAME"

# Configure Serial Console
sudo raspi-config nonint do_serial 0
stty -F /dev/USB0 115200

# Script complete
echo "HRMCLI setup complete! Log in as '$HRMCLI_USER' with password '$DEFAULT_PASSWORD' to start using HRMCLI."
echo "Static IP set to $CUSTOM_IP."
echo "System will reboot in 10 seconds."
sleep 10
reboot
