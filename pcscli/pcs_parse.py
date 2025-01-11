from pcs_help import show_help

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
        if len(args) >= 1 and args[-1] == "-help":
            from pcs_help import show_help
            specific_command = args[0] if len(args) > 0 else None
            show_help(prefix, specific_command)
            return

        # Pass to command execution
        from pcs_action import execute_command
        execute_command(prefix, args)
        return

    print(f"Unknown command: {command}. Type 'help' for a list of commands.")

