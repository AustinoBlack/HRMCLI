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

# Add auto-launch to bashrc for the default user
BASHRC_FILE="/home/$PCSCLI_USER/.bashrc"
cat <<EOL >> "$BASHRC_FILE"
# Auto-launch pcs_shell for the pcscli user and exit on exit
if [ -t 0 ]; then
    USER=\$PCSCLI_USER
    LAST_LOGIN=\$(last -i \$USER | head -1 | awk '{print \$6, \$7, \$8, \$9 " from " \$3}')
    echo "Last login: \$LAST_LOGIN"
    python3 \$INSTALL_DIR/src/cli_core/pcs_shell.py
    exit
fi

EOL

# Configure Static IP
read -p "Enter a new static IP and subnet (or press Enter to keep default: $DEFAULT_IP): " CUSTOM_IP
if [ -z "$CUSTOM_IP" ]; then
    CUSTOM_IP="$DEFAULT_IP"
fi

get_interface() {
    nmcli device status | grep ethernet | awk '{print $1}'
}

INTERFACE=$(get_interface)
nmcli connection modify "$INTERFACE" ipv4.addresses "$DEFAULT_IP" ipv4.method manual
nmcli connection up "$INTERFACE"

# Script complete
echo "PCSCLI setup complete! Log in as '$PCSCLI_USER' with password '$DEFAULT_PASSWORD' to start using PCSCLI."
echo "Static IP set to $CUSTOM_IP."
echo "System will reboot in 10 seconds."
sleep 10
reboot
