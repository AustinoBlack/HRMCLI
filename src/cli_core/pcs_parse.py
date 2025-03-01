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

    prefix = tokens[0]
    args = tokens[1:]

    if len(args) == 1 and args[-1] == "-help":
        show_general_help(prefix)
        return

    elif len(args) > 1 and args[-1] == "-help":
        command = " ".join(args[:-1])
        show_help(prefix, command)
        return

    elif prefix == "set" or prefix == "sh":
        node_index = args[-1]
        command = " ".join(args[:-2])
        execute_command(prefix, command, node_index)
        return
    
    elif prefix == "pcscli":
        if args[0] == "cmd":
            node_index = args[-1]
            command = args[2:-2]
            execute_command(prefix, command, node_index)            
        else:
            print("placeholder")
        return

    else:
        print(f"Unknown prefix: {prefix}. Type 'help' for a list of commands.")

