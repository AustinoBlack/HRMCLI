import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Moves up two levels
CONFIG_DIR = os.path.join(BASE_DIR, "configs")
commands_config = os.path.join(CONFIG_DIR, "commands.json")

def load_config(CONFIG_PATH):
    try:
        with open(CONFIG_PATH, "r") as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading config: {str(e)}")
        return {}

CONFIG_DATA = load_config(commands_config)

def show_help(prefix, command):
    try:
        command_data = CONFIG_DATA[prefix][command]
        print(f"\n{prefix} help: {command}".upper())
        print("-----------------------------------")
        print( str( command_data["help_msg"][0] ) )
        print("\nSyntax:")
        print(command_data["syntax"])

        print("\nDetails:")
        for detail in command_data["syntax_details"]:
            print(f"- {detail}")
        print()
        
        for message in command_data["help_msg"][1:]:
            print(message)
        print()

    except KeyError:
        print(f"Error: Command '{command}' not found under prefix '{prefix}'.")

def show_general_help(prefix):
    try:
        command_data = CONFIG_DATA[prefix]["general_help"]
        print(f"\n{prefix} General Help".upper())
        print("-----------------------------------")
        print( str( command_data["help_msg"][0] ) )
        print("\nSyntax:")
        print(command_data["syntax"])
        print()
        for message in command_data["help_msg"][1:]:
            print(message)
        print()
 
    except KeyError:
        print(f"Error: General help unavailable for {prefix}")    

