import os
import sys
import readline

VERSION = "0.1"

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_help():
    """Displays a list of available commands."""
    help_text = """
    Cluster CLI Commands:
    - clear      : Clears the screen
    - exit       : Exits the CLI
    - help       : Displays this help message
    - version    : Displays the CLI version
    - cluster setpoweron -i <node_id> : Power on a specific node
    - cluster setpoweroff -i <node_id> : Power off a specific node
    """
    print(help_text)

def show_version():
    """Displays the CLI version."""
    print("\nCluster CLI Version " + VERSION + "\n")

def execute_command(command):
    """Processes and executes a user command."""
    if command == "clear":
        clear_screen()
    elif command == "help":
        show_help()
    elif command == "exit":
        print("Exiting Cluster CLI...")
        sys.exit(0)
    elif command == "version":
        show_version()
    elif command.startswith("cluster"):
        # Placeholder
        print(f"Executing cluster command: {command}")
    else:
        print(f"Unknown command: {command}. Type 'help' for a list of commands.")

def main():
    clear_screen()
    print("Welcome to the Cluster CLI!")

    # Enable history file (optional: make persistent across sessions)
    history_file = "/home/user/.pcscli_history"
    try:
        readline.read_history_file(history_file)
    except FileNotFoundError:
        pass

    while True:
        try:
            command = input("PcsCli# ").strip()
            if command:
                readline.add_history(command)
                execute_command(command)
            else:
                continue 
        except (KeyboardInterrupt, EOFError):
            print("\nExiting Cluster CLI...")
            break

    # Save history to file
    readline.write_history_file(history_file)

if __name__ == "__main__":
    main()

