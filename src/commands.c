#include <stdio.h>
#include <string.h>
#include "commands.h"

// placeholder command handler skeleton
void handle_command(const char* input) {
    if (strcmp(input, "help") == 0) {
        printf("Available commands:\n");
        printf("  help          Show this help\n");
        printf("  clear         Clears the screen\n");
        printf("  list          List servers\n");
        printf("  ping <name>   Ping server\n");
        printf("  exit / quit   Exit the CLI\n");
    }
    else if (strcmp(input, "clear") == 0 ){
        printf("\033[2J\033[H"); 
    }
    else if (strcmp(input, "list") == 0) {
        printf("Server list (placeholder): server1, server2\n");
    }
    else if (strncmp(input, "ping ", 5) == 0) {
        char* server_name = (char*)(input + 5);
        printf("Pinging server: %s (placeholder)\n", server_name);
    }
    else {
        printf("Unknown command: %s\n", input);
    }
}
