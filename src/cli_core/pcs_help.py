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

Advanced Commands:
    pcscli      Manage power, reset, and basic node operations.
    sh          Retrieve system information for nodes.
    set         Configure system settings, including boot options, LEDs, and FRU.

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
    #print(f"Entered: Prefix: {prefix}, command: {command}" )
    
    if prefix == "pcscli":
        if command == "-help":
            pcscli_general_help()
        elif command == "setpoweron":
            setpoweron_help()
        elif command == "setpoweroff":
            setpoweroff_help()
        else:
            print(f"*** Unknown command: {prefix} {command}. Type 'pcscli -help' for a list of pcscli commands.")
    
    elif prefix == "sh":
        if command == "-help":
            sh_general_help()
        elif command == "sys info":
            sysinfo_help()
        elif command == "sys fru":
            sysfru_help()
        elif command == "sys sel":
            syssel_help()
        elif comand == "sys sdr":
            syssdr_help()
        else:
            print(f"*** Unknown command: {prefix} {command}. Type 'sh -help' for a list of sh commands.")

    elif prefix == "set":
        if command == "-help":
            set_general_help()
        elif command == "sys led on":
            ledon_help()
        elif command == "sys led off":
            ledoff_help()
        elif command == "sys sel clear":
            selclear_help()
        else:
            print(f"*** Unknown command: {prefix} {command}. Type 'set -help' for a list of set commands.")

def pcscli_general_help():
    print("""
'pcscli' General Help:
========================================================
This command will provide a list of operation commands
available under the the "pcscli prefix"

Syntax: pcscli [operation] {-help}

-help  Displays the help message for the given operation 
       command.

List of avaiable operations:
- setpoweron
- setpoweroff
""")

def setpoweron_help():
    print("""
PcsCli Command: setpoweron
========================================================
This command sends an ipmi signal to turn the blade on.

Syntax: pcscli setpoweron {-help} <-i ID>

-i     Blade ID [1 - n]
-help  Displays this help message.

Sample Usage:
pcscli setpoweron -i 1
""")

def setpoweroff_help():
    print("""
PcsCli Command: setpoweroff
========================================================
This command sends an ipmi signal to turn the blade on.

Syntax: pcscli setpoweroff {-help} <-i ID>

-i     Blade ID [1 - n]
-help  Displays this help message.

Sample Usage:
pcscli setpoweroff -i 1
""")

def sh_general_help():
    print("""
'show' General Help:
========================================================
This command will provide a list of operation commands
available under the the "sh prefix"

Syntax: sh [operation] {-help}

-help  Displays the help message for the given operation 
       command.

List of avaiable operations:
- sys info
- sys fru
""")

def sysinfo_help():
    print("""
'Show' Command: sys info 
========================================================
This command prints the systems information by given node index

Syntax: sh sys info {-help} <-i ID>

-i     Blade ID [1 - n]
-help  Displays this help message.

Sample Usage:
sh sys info -i 1
""")

def sysfru_help():
    print("""
'Show' Command: sys fru 
========================================================
This command prints the systems fru information by given node index

Syntax: sh sys fru {-help} <-i ID>

-i     Blade ID [1 - n]
-help  Displays this help message.

Sample Usage:
sh sys fru -i 1
""")
    
def syssel_help():
    print("""
'Show' Command: sys sel
========================================================
This command prints the nodes SEL log by given node index

Syntax: sh sys sel {-help} <-i ID>

-i     Blade ID [1 - n]
-help  Displays this help message.

Sample Usage:
sh sys sel -i 1
""")

def syssdr_help():
    print("""
'Show' Command: sys sdr
========================================================
This command prints the nodes SDR by given node index

Syntax: sh sys sdr {-help} <-i ID>

-i     Blade ID [1 - n]
-help  Displays this help message.

Sample Usage:
sh sys sdr -i 1    
""")

def set_general_help():
    print("""
'set' General Help:
========================================================
This command will provide a list of operation commands
available under the the "set prefix"

Syntax: set [operation] {-help}

-help  Displays the help message for the given operation 
       command.

List of avaiable operations:
- sys led on
- sys led off
- sys sel clear
""")

def ledon_help():
    print("""
'Set' Command: sys led on
========================================================
This command turns on the chassis attention led by given node index

Syntax: sh sys led on {-help} <-i ID>

-i     Blade ID [1 - n]
-help  Displays this help message.

Sample Usage:
sh sys led on -i 1
""")

def ledoff_help():
    print("""
'Set' Command: sys led off
========================================================
This command turns off the chassis attention led by given node index

Syntax: sh sys led on {-help} <-i ID>

-i     Blade ID [1 - n]
-help  Displays this help message.

Sample Usage:
sh sys led off -i 1
""")

def selclear_help():
    print("""
'Set' Command: sys sel clear
========================================================
This command clears the nodes SEL log by given node index

Syntax: sh sys sel clear {-help} <-i ID>

-i     Blade ID [1 - n]
-help  Displays this help message.

Sample Usage:
sh sys sel clear -i 1
""")
