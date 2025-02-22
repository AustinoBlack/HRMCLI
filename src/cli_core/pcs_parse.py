from pcs_help import show_help, show_general_help
from pcs_action import execute_command

def parse_command(user_input):
    """
    Parses the user input and determines the command to execute.

    Args:
        user_input (str): The command input by the user.
    """
    tokens = user_input.split()
    if not tokens:
        return

    command = tokens[0]
    args = tokens[1:]
    prefix = command

    if len(args) == 1 and args[-1] == "-help":
        show_general_help(prefix)
        return

    elif len(args) > 1 and args[-1] == "-help":
        specific_command = " ".join(args[:-1])
        show_help(prefix, specific_command)
        return

    elif args[-1] == "1" or args[-1] == "2":  # TODO needs attention
        command = " ".join(args[:-2])
        execute_command(prefix, command, args[-1])
        return
    
    else:
        print(f"Unknown command: {command}. Type 'help' for a list of commands.")

