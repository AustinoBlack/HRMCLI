#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "cli.h"
#include "commands.h"

#define MAX_INPUT 256

void start_cli() {
    char input[MAX_INPUT];

    printf("Welcome to HRMCLi interactive shell.\n");
    printf("Type 'help' for a list of commands.\n");

    while (1) {
        printf("HRMCLi> ");
        if (!fgets(input, sizeof(input), stdin)) {
            break; // Ctrl+D
        }

        // remove newline
        input[strcspn(input, "\n")] = 0;

        // skip empty input
        if (strlen(input) == 0) continue;

        // exit commands
        if (strcmp(input, "exit") == 0 || strcmp(input, "quit") == 0) {
            break;
        }

        // call command handler
        handle_command(input);
    }

    printf("Exiting HRMCLi.\n");
}
