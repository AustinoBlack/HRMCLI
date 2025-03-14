# HCSCLI (Homelab Control Server Command Line Interface)

## About
HCSCLI is a data-driven command-line interface designed for homelab environments, providing seamless management of IPMI-compatible hardware via `ipmitool`. It simplifies power management, system monitoring, and administrative tasks for servers and networked devices.

## Features
- **IPMI Management** – Power on/off, reset, and monitor system status.
- **Chassis & Sensor Control** – Manage chassis attention LED, view sensor data records (SDR), and system event logs (SEL).
- **Data-Driven Configuration** – Nodes and credentials are managed through JSON-based configuration files.
- **Flexible Command Structure** – Supports direct `ipmitool` commands while providing intuitive command prefixes for ease of use.

## Getting Started
### Prerequisites
- Hardware with an IPMI LAN interface or any other BMC compatible with `ipmitool`.

### Installation
```
wget -O - https://raw.githubusercontent.com/yourrepo/hcscli/main/setup.sh | bash
```

### Basic Usage
Once installed, use the following command structure:
```
[prefix] [command] {options} <-i ID>
```
Example commands:
```
hcscli set power on -i 1      # Power on node 1
hcscli sh sys info -i 2      # Display system info for node 2
hcscli pcscli cmd user list -i 1  # Execute direct ipmitool command
```

## Future Plans
- **Extended Hardware Support** – Compatibility for additional BMC implementations.
- **Web Interface** – A GUI for easier management.
- **Automated Alerts** – Notifications for system events and failures.

