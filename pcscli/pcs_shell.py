import os
import sys
import readline

from pcs_parse import parse_command

VERSION = "0.1"

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

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
                if user_input == "clear":
                    clear_screen()
                elif user_input == "exit": 
                    print("Exiting PCSCLI. Goodbye!") 
                    break
                else:
                    parsed_command = parse_command(user_input)
            else:
                continue 
        except (KeyboardInterrupt, EOFError):
            print("\nExiting Cluster CLI...")
            break

    # Save history to file
    readline.write_history_file(history_file)

if __name__ == "__main__":
    main()

