import subprocess
import json

def load_config():
    """
    Load ipmi_configs.json - stores ipmi ip addresses and login credentials mapped to a particullar node id
    """
    with open("../configs/ipmi_config.json", "r") as file:
        return json.load( file )

CONFIG = load_config()

def execute_command(prefix, command, node_index):
    """
    Executes a command based on the provided prefix, command, and arguments.

    Args:
        prefix (str): The prefix of the command (e.g., pcscli, sh, set).
        args (list): List of arguments for the command.
    """
    print(f"Executing: Prefix='{prefix}', Command='{command}', Index='{node_index}'")

    if prefix == "pcscli":
        if command == "setpoweron":
            setpoweron(node_index)
        elif command == "setpoweroff":
            setpoweroff(node_index)
        else:
            print(f"*** Unknown command: {prefix} {command}. Type 'pcscli -help' for a list of pcscli commands.")
    
    elif prefix == "sh":
        if command == "sysinfo":
            sys_info(node_index)
        elif command == "sysfru":
            sys_fru(node_index)
        else:
            print(f"*** Unknown command: {prefix} {command}. Type 'sh -help' for a list of sh commands.")

    elif prefix == "set":
        if command == "sysledon":
            sys_led_on(node_index)
        elif command == "sysledoff":
            sys_led_off(node_index)
        elif command == "sysselclear":
            sys_sel_clear(node_index)
        else:
            print(f"*** Unknown command: {prefix} {command}. Type 'set -help' for a list of set commands.")

def setpoweron(node_index):
    """ 
    Turns on a specified node by a given node index
    """
    print(f"Executing setpoweron on node {node_index}") #DEBUG
    
    # setup ipmi command
    node_data = CONFIG["nodes"].get(str(node_index))
    if not node_data:
        print(f"Error: No data found for node {node_index}")
        return

    ipmi_command = [
        "ipmitool", "-I", "lanplus", "-H", node_data["ip"], "-U", node_data["user"], "-P", node_data["password"], "power", "on"
    ]
    
    # try running the created ipmitool command
    try:
        result = subprocess.run(ipmi_command, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Node {node_index} powered on successfully.")
        else:
            print(f"Error powering on node {node_index}: {result.stderr}")
    except Exception as e:
        print(f"Exception occurred: {str(e)}")

def setpoweroff(node_index):
    """ 
    Turns off a specified node by a given node index
    """
    print(f"Executing setpoweroff on node {node_index}") #DEBUG
    
    # setup ipmi command
    node_data = CONFIG["nodes"].get(str(node_index))
    if not node_data:
        print(f"Error: No data found for node {node_index}")
        return

    ipmi_command = [
        "ipmitool", "-I", "lanplus", "-H", node_data["ip"], "-U", node_data["user"], "-P", node_data["password"], "power", "off"
    ]
    
    # try running the created ipmitool command
    try:
        result = subprocess.run(ipmi_command, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Node {node_index} powered off successfully.")
        else:
            print(f"Error powering off node {node_index}: {result.stderr}")
    except Exception as e:
        print(f"Exception occurred: {str(e)}")

def sys_info(node_index):
    print(f"Retrieving system info for node {node_index}")

def sys_fru(node_index):
    print(f"Retrieving FRU data for node {node_index}")

def sys_led_on(node_index):
    print(f"Turning LED on for node {node_index}")

def sys_led_off(node_index):
    print(f"Turning LED off for node {node_index}")

def sys_sel_clear(node_index):
    print(f"Clearing SEL log for node {node_index}")
