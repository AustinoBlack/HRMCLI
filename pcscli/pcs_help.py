def show_help_message(topic=None):
    """
    Display help messages based on the topic.
    :param topic: The topic for which help is requested.
    """
    general_help = """
    PCSCLI General Commands:
    - help       : Show this help message or specific help (e.g., 'help cluster').
    - clear      : Clear the screen.
    - exit       : Exit the CLI.
    """
    
    cluster_help = """
    Cluster Commands:
    - cluster setpoweron -i <node_id>  : Power on a specific node in the cluster.
    - cluster setpoweroff -i <node_id> : Power off a specific node in the cluster.
    - cluster status                  : Show the current status of all nodes.
    """
    
    hardware_help = """
    Hardware Commands:
    - hw led on  -i <node_id> : Turn on the status LED for a node.
    - hw led off -i <node_id> : Turn off the status LED for a node.
    """
    
    # Determine which help message to display
    if topic is None or topic == "general":
        print(general_help)
    elif topic == "cluster":
        print(cluster_help)
    elif topic == "hardware":
        print(hardware_help)
    else:
        print(f"No help available for the topic '{topic}'. Type 'help' for general help.")

def list_available_topics():
    """
    List all topics for which help is available.
    """
    print("""
    Available Help Topics:
    - general  : General commands and usage.
    - cluster  : Cluster management commands.
    - hardware : Hardware-related commands.
    """)

