import os
import sys
import time
import readline
import subprocess

import json
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_DIR = os.path.join(BASE_DIR, "configs")

hrmcli_config = os.path.join(CONFIG_DIR, "hrmcli_config.json")
commands_config = os.path.join(CONFIG_DIR, "commands.json")

from pcs_parse import parse_command
from datetime import datetime

def load_config(CONFIG_PATH):
    try:
        with open(CONFIG_PATH, "r") as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading config: {str(e)}")
        return {}

CONFIG = load_config(hrmcli_config)
command_data = load_config(commands_config)

def display_logo():
    logo = CONFIG.get("logo", [])
    for line in logo:
        print(line)

def display_welcome():
    msg = CONFIG.get("welcome_msg", [])
    for line in msg:
        print(line)

def display_about():
    abt = CONFIG.get("about",[])
    for line in abt:
        print(line)

def display_help():
    hlp = CONFIG.get("help_msg",[])
    for line in hlp:
        print(line)

def clear_history():
    histfile = os.path.expanduser("~/.hrmcli_history")
    if os.path.exists(histfile):
        os.remove(histfile)

def complete(text, state):
    """Tab autocomplete function. Suggests commands based on user input."""
    options = []

    # Get prefixes
    if " " not in readline.get_line_buffer():
        options = list(command_data.keys())
    else:
        parts = readline.get_line_buffer().split()
        prefix = parts[0] if parts[0] in command_data else None

        if prefix and len(parts) == 2:
            options = list(command_data[prefix].keys())

    matches = [cmd for cmd in options if cmd.startswith(text)]
    return matches[state] if state < len(matches) else None   

def setup_readline():
    """Enable tab completion and command history."""
    readline.parse_and_bind("tab: complete") # Bind the tab key
    readline.set_completer(complete)
    readline.set_completer_delims(" ")

def get_last_login(username):
    try:
        # Run the 'last' command to get login history
        result = subprocess.check_output(["last", username], text=True)
        lines = [line for line in result.splitlines() if line.strip()]
        if lines:
            # Parse the line (example format: "username tty1 192.168.1.2 Fri Jan 20 10:00")
            parts = lines[0].split()
            ip = parts[2]
            date = " ".join(parts[3:7])
            return f"Last login: {date} from {ip}"
    except Exception as e:
        return "Unable to fetch last login information."

def clear_screen():
    """Clears the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    clear_screen()
    setup_readline()
   
    # Startup Sequence
    print("starting HRMCLI...")
    time.sleep(2)
    clear_screen()
    display_logo()
    
    # Display last login and welcome message [ascii graphic?]
    username = os.getenv("USER", "user")
    last_login_message = get_last_login(username)
    print(last_login_message)
    time.sleep(2)
    display_welcome()

    # Enable history file
    history_file = ".hrmcli_history"
    try:
        readline.read_history_file(history_file)
    except FileNotFoundError:
        pass

    while True:
        try:
            user_input = input("HrmCli# ").strip()
            if user_input:
                readline.add_history(user_input)
                if user_input == "clear":
                    clear_screen()
                    display_logo()
                elif user_input == "exit" or user_input == "quit": 
                    print("Exiting HRMCLI...") 
                    time.sleep(2)
                    clear_screen()
                    break
                elif user_input == "about":
                    display_about()
                elif user_input == "help":
                    display_help()
                else:
                    parse_command(user_input)
            else:
                print("HrmCli# ", end="", flush=True) 
        except (KeyboardInterrupt, EOFError):
            print("\nExiting HRMCLI...")
            time.sleep(2)
            clear_history()
            clear_screen()
            break

if __name__ == "__main__":
    main()

