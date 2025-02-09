# PCSCLI (Proxmox Control Server Command Line Interface)
 A simple command line interface for managing my home proxmox cluster

- inspiration taken from Microsoft cloud server Chassis Manager.

Progress updates:
[02-08] - first successful pcscli command (pcscli setpoweron -i 2) powered on node 2 of my proxmox cluster.

Revised file structure:

pcscli/
│── src/
│   │── cli_core/                # Main PCSCLI source code
│   │   ├── pcs_shell.py         # Main CLI interface
│   │   ├── pcscli.sh            # Auto-execution script for login
│   │   ├── pcs_help.py          # Help message functions
│   │   ├── pcs_action.py        # IPMI & hardware-related functions
│   │   ├── pcs_parse.py         # Command parsing logic
│   │── configs/                 # Configuration files
│   │   ├── ipmi_config.json     # Stores IPMI credentials & node mappings
│   │   ├── pcscli_config.json   # Other PCSCLI settings
│── README.md                    # Project documentation
│── .gitignore                   # Git ignore file
│── setup.sh                     # Installation/setup script (optional)
