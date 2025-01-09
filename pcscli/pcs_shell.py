import os
import sys
import readline

from pcs_help import *

VERSION = "0.1"

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_version():
    """Displays the CLI version."""
    print("\nCluster CLI Version " + VERSION + "\n")

def execute_command(user_input):
    """Processes and executes a user command."""
    if user_input == "clear":
        os.system('cls' if os.name == 'nt' else 'clear')
    elif user_input.startswith("help"):
        # Parse the help command (e.g., 'help cluster')
        parts = user_input.split()
        topic = parts[1] if len(parts) > 1 else None
        show_help_message(topic)
    else:
        print(f"Unknown command: {user_input}")
        print("Type 'help' for a list of commands.")

def main():
    clear_screen()
    print("Welcome to the Cluster CLI!")

    # Enable history file (optional: make persistent across sessions)
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
                if user_input == "exit": 
                    print("Exiting PCSCLI. Goodbye!") 
                    break
                else:
                    execute_command(user_input)
            else:
                continue 
        except (KeyboardInterrupt, EOFError):
            print("\nExiting Cluster CLI...")
            break

    # Save history to file
    readline.write_history_file(history_file)

if __name__ == "__main__":
    main()

