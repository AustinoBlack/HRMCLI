def show_general_help():
    """
    Displays a general help message for the CLI.
    """
    print("""
Cluster CLI - General Help
========================================================
This command-line interface allows you to manage your Proxmox cluster via serial commands.

Basic Commands:
    help        Display this general help message.
    clear       Clears the screen.
    exit        Exits the Cluster CLI.

Using the -help Flag:
    Add the -help flag to any valid command to see detailed usage instructions.

Command Prefixes:
    pcscli      Manage power, reset, and basic node operations.
    sh          Retrieve system information for nodes.
    set         Configure system settings, including boot options, LEDs, and FRU.

For specific help on a command, use:
    PcsCli# <prefix> <command> -help
Example:
    PcsCli# pcscli setpoweron -help

Version Information:
    PCSCLI Version: 0.1.0
    Author: Austin Black
    License: MIT
    """)


def show_help(prefix, command):
    """
    Displays the help message for a given prefix and command.

    Args:
        prefix (str): The command prefix (e.g., pcscli, sh, set).
        command (str): The specific command to show help for.
    """
    help_messages = {
        "pcscli": {
            "setpoweron": """
PcsCli Command: (SetPowerOn)
========================================================
This command turns the AC outlet ON for the specified node.

Syntax:
    pcscli setpoweron <-i ID> [-help]

Flags:
    -i      Node ID [1-4] (Required)
    -help   Show this help message.

Example Usage:
    pcscli setpoweron -i 1
            """,
        },
        "sh": {
            "sys": """
Sh Command: (System Info)
========================================================
Displays system information for the specified node.

Syntax:
    sh sys [options] <-i ID> [-help]

Flags:
    -i      Node ID [1-4] (Required)
    -help   Show this help message.

Example Usage:
    sh sys -i 2
            """,
        },
        "set": {
            "sys": """
Set Command: (System Configuration)
========================================================
Configures system settings for the specified node.

Syntax:
    set sys <option> <-i ID> [-help]

Options:
    -boot  Sets the boot configuration (-bios, -usb, -pxe).
    -led   Turns the status LED ON or OFF.
    -fru   Updates the Field Replaceable Unit (FRU).

Flags:
    -i      Node ID [1-4] (Required)
    -help   Show this help message.

Example Usage:
    set sys -boot -bios -i 3
            """,
        },
    }

    prefix_help = help_messages.get(prefix)
    if not prefix_help:
        print(f"No help available for prefix '{prefix}'.")
        return

    command_help = prefix_help.get(command)
    if not command_help:
        print(f"No help available for command '{command}' under prefix '{prefix}'.")
        return

    print(command_help)

