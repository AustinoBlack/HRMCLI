# HRMCLI (HomeLab Rack Manager Command Line Interface)

## About
HRMCLI is a data-driven command-line interface designed for homelab environments, providing seamless management of IPMI-compatible hardware via `ipmitool`. It simplifies power management, system monitoring, and administrative tasks for servers and networked devices.

## Features
- **IPMI Management** – Power on/off, reset, and monitor system status.
- **Chassis & Sensor Control** – Manage chassis attention LED, view sensor data records (SDR), and system event logs (SEL).
- **Data-Driven Configuration** – Nodes and credentials are managed through JSON-based configuration files.
- **Flexible Command Structure** – Supports direct `ipmitool` commands while providing intuitive command prefixes for ease of use.

## Getting Started
### Prerequisites
#### For the Rack Manager:
- A Raspberry pi with at least one USB port, one Ethernet port, and running raspberry pi OS

#### For the HomeLab:
- Hardware with an IPMI LAN interface or any other BMC compatible with `ipmitool`.

#### For the Network:
- ...

### Installation
```
wget -O - https://raw.githubusercontent.com/yourrepo/hrmcli/main/setup.sh | bash
```

### Basic Usage
Once installed, use the following command structure:
```
[prefix] [command] {options} <-i ID>
```
Example commands:
```
hrmcli set power on -i 1            # Power on node 1
hrmcli sh sys info -i 2             # Display system info for node 2
hrmcli hrmcli cmd user list -i 1    # Execute direct ipmitool command
```

## Future Plans
- **Support for other Operating Systems**
- **Extended Hardware Support** – Compatibility for additional BMC implementations.
- **Automated Alerts** – Notifications for system events and failures.

