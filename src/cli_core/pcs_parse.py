from pcs_help import show_help, show_general_help
from pcs_action import execute_command
from pcs_admin import change_password, add_node, edit_node, remove_node, list_nodes, pcscli_status, backup_config, restore_config, update

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
    
    elif prefix == "hrmcli":
        if args[0] == "cmd":
            node_index = args[-1]
            command = args[2:-2]
            execute_command(prefix, command, node_index)
        elif " ".join(args) == "update":
            update()            
        elif " ".join(args) == "change password":
            change_password()
        elif " ".join(args) == "add node":
            add_node()
        elif " ".join(args) == "edit node":
            edit_node()
        elif " ".join(args) == "remove node":
            remove_node()
        elif " ".join(args) == "list nodes":
            list_nodes()
        elif " ".join(args) == "status":
            pcscli_status()
        elif " ".join(args) == "backup config":
            backup_config()
        elif " ".join(args) == "restore config":
            restore_config()
        elif " ".join(args[0:-2]) == "test connection":
            node_index = args[-1]
            execute_command(prefix, "test connection", node_index)
        return

    else:
        print(f"Unknown prefix: {prefix}. Type 'help' for a list of commands.")

