#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

# Default username and password
PCSCLI_USER="pcscli"
DEFAULT_PASSWORD="pcscli"
INSTALL_DIR="/opt/PCSCLI"
REPO_URL="https://github.com/AustinoBlack/PCSCLI.git"

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
if ! grep -q "python3 $INSTALL_DIR/pcs_shell.py" "$BASHRC_FILE"; then
    echo "python3 $INSTALL_DIR/pcs_shell.py" >> "$BASHRC_FILE"
fi

# Allow user to configure IPMI nodes
echo "Configuring IPMI nodes..."
IPMI_CONFIG="$INSTALL_DIR/configs/ipmi_config.json"
mkdir -p "$INSTALL_DIR/configs"

cat > "$IPMI_CONFIG" <<EOL
{
    "nodes": {}
}
EOL

while true; do
    read -p "Add a Proxmox node? (y/n): " yn
    case $yn in
        [Yy]* )
            read -p "Enter node index: " node_index
            read -p "Enter IP address: " node_ip
            read -p "Enter username: " node_user
            read -s -p "Enter password: " node_pass
            echo
            jq --argjson index "$node_index" --arg ip "$node_ip" --arg user "$node_user" --arg pass "$node_pass" \
                '.nodes[$index] = {"ip": $ip, "user": $user, "password": $pass}' "$IPMI_CONFIG" > temp.json && mv temp.json "$IPMI_CONFIG"
            ;;
        [Nn]* )
            break;;
        * ) echo "Please answer yes or no.";;
    esac
done

chown "$PCSCLI_USER":"$PCSCLI_USER" "$IPMI_CONFIG"

# Script complete
echo "PCSCLI setup complete! Log in as '$PCSCLI_USER' with password '$DEFAULT_PASSWORD' to start using PCSCLI."

