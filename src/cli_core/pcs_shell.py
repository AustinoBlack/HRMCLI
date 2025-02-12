import os
import sys
import time
import readline
import subprocess

from pcs_parse import parse_command
from datetime import datetime

LOGO = """

██████╗  ██████╗███████╗ ██████╗██╗     ██╗
██╔══██╗██╔════╝██╔════╝██╔════╝██║     ██║
██████╔╝██║     ███████╗██║     ██║     ██║
██╔═══╝ ██║     ╚════██║██║     ██║     ██║
██║     ╚██████╗███████║╚██████╗███████╗██║
╚═╝      ╚═════╝╚══════╝ ╚═════╝╚══════╝╚═╝
                                           
Proxmox Control Server Command Line Interface
----------------------------------------------
"""

VERSION = "0.5"

COMMANDS = {
    "pcscli": ["setpoweron", "setpoweroff", "reset", "status"],
    "sh": ["sys", "bios", "code"],
    "set": ["sys", "boot", "led", "fru"],
    "help": [],
    "clear": [],
    "exit": []
}

def complete(text, state):
    """Tab autocomplete function. Suggests commands based on user input."""
    buffer = readline.get_line_buffer().split()
    if len(buffer) == 1:
        options = [cmd for cmd in COMMANDS.keys() if cmd.startswith(text)]
    elif len(buffer) > 1 and buffer[0] in COMMANDS:
        options = [sub for sub in COMMANDS[buffer[0]] if sub.startswith(text)]
    else:
        options = []

    return options[state] if state < len(options) else None

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
    print("starting PCSCLI...")
    time.sleep(2)
    clear_screen()
    print(LOGO) 
    
    # Display last login and welcome message [ascii graphic?]
    username = os.getenv("USER", "user")
    last_login_message = get_last_login(username)
    print(last_login_message)
    time.sleep(2)
    print("Enter 'help' to get started\n")

    # Enable history file
    history_file = ".pcscli_history"
    try:
        readline.read_history_file(history_file)
    except FileNotFoundError:
        pass

    while True:
        try:
            user_input = input("PcsCli# ").strip()
            if user_input:
                readline.add_history(user_input)
                if user_input == "clear":
                    clear_screen()
                    print(LOGO)
                elif user_input == "exit" or user_input == "quit": 
                    print("Exiting PCSCLI...") 
                    time.sleep(2)
                    clear_screen()
                    break
                else:
                    parsed_command = parse_command(user_input)
            else:
                print("PcsCli# ", end="", flush=True) 
        except (KeyboardInterrupt, EOFError):
            print("\nExiting PCSCLI...")
            time.sleep(2)
            clear_screen()
            break

    # Save history to file
    readline.write_history_file(history_file)

if __name__ == "__main__":
    main()

