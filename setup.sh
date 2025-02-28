#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

# Default username and password
PCSCLI_USER="pcscli"
DEFAULT_PASSWORD="pcscli"
INSTALL_DIR="/opt/PCSCLI"
REPO_URL="https://github.com/AustinoBlack/PCSCLI.git"
DEFAULT_IP="172.16.0.1/29"

# Create the pcscli user if it does not exist
if ! id "$PCSCLI_USER" &>/dev/null; then
    echo "Creating user: $PCSCLI_USER"
    useradd -m -s /bin/bash "$PCSCLI_USER"
    echo "$PCSCLI_USER:$DEFAULT_PASSWORD" | chpasswd
fi

# Install required dependencies
apt update
apt install -y ipmitool python3 python3-pip git

# Clone PCSCLI repository
if [ ! -d "$INSTALL_DIR" ]; then
    echo "Cloning PCSCLI repository into $INSTALL_DIR"
    git clone "$REPO_URL" "$INSTALL_DIR"
    chown -R "$PCSCLI_USER":"$PCSCLI_USER" "$INSTALL_DIR"
fi

# Ensure pcs_shell.py runs on login for pcscli user
BASHRC_FILE="/home/$PCSCLI_USER/.bashrc"
if ! grep -q "python3 $INSTALL_DIR/src/cli_core/pcs_shell.py" "$BASHRC_FILE"; then
    echo "python3 $INSTALL_DIR/src/cli_core/pcs_shell.py" >> "$BASHRC_FILE"
fi

# Configure Static IP
read -p "Enter a new static IP and subnet (or press Enter to keep default: $DEFAULT_IP): " CUSTOM_IP
if [ -z "$CUSTOM_IP" ]; then
    CUSTOM_IP="$DEFAULT_IP"
fi

nmcli connection modify eth0 ipv4.addresses "$CUSTOM_IP" ipv4.method manual
nmcli connection up eth0

# Script complete
echo "PCSCLI setup complete! Log in as '$PCSCLI_USER' with password '$DEFAULT_PASSWORD' to start using PCSCLI."
echo "Static IP set to $CUSTOM_IP."

