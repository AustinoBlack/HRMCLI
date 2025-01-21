from pcs_help import show_help
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

    if command == "help":
        from pcs_help import show_general_help
        show_general_help()
        return

    # Handle prefix commands like pcscli, sh, set
    if command in ("pcscli", "sh", "set"):
        prefix = command
        if len(args) > 1 and args[-1] == "-help":
            specific_command = " ".join(args[:-1])
            show_help(prefix, specific_command)
            return
        elif len(args) == 1 and args[-1] == "-help":
            show_help(prefix, "-help")
            return

        # Pass to command execution
        execute_command(prefix, args)
        return

    print(f"Unknown command: {command}. Type 'help' for a list of commands.")

