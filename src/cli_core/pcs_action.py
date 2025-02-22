import subprocess
import json
import os

def load_config(CONFIG_PATH):
    try:
        with open(CONFIG_PATH, "r") as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading config: {str(e)}")
        return {}

COMMANDS_FILE = "../configs/commands.json"
IPMI_FILE = "../configs/ipmi_config.json"
command_data = load_config(COMMANDS_FILE)
ipmi_data = load_config(IPMI_FILE)

def execute_command(prefix, command, node_index):
    """
    Executes a command based on the provided prefix, command, and arguments.

    Args:
        prefix (str): The prefix of the command (e.g., pcscli, sh, set).
        args (list): List of arguments for the command.
    """
    # print(f"Executing: Prefix='{prefix}', Command='{command}', Index='{node_index}'")  # DEBUG
 
    try:
        ipmi_cmd = command_data[prefix][command]["ipmi_cmd"]
        ipmi_cred = ipmi_data["nodes"].get(str(node_index))
        print( "ipmi cmd is: >" + str(ipmi_cmd) )

        ipmi_command = [
            "ipmitool", "-I", "lanplus", "-H", ipmi_cred["ip"], "-U", ipmi_cred["user"], "-P", ipmi_cred["password"], str(ipmi_cmd)
        ]

        print("Built cmd: ")
        print(" ".join(ipmi_command))

    except KeyError:
        print(f"Error: Command '{command}' not found under prefix '{prefix}'.")    
