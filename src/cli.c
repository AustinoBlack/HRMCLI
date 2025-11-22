#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <readline/readline.h>
#include <readline/history.h>

#include "cli.h"
#include "commands.h"

#define MAX_INPUT 256

// ***AutoTab complete code***
static const char* commands[] = {
    "help",
    "list",
    "ping",
    "clear",
    "exit",
    "quit",
    NULL
};

char* command_generator(const char* text, int state) {
    static int list_index;
    static int len;

    if (!state) {
        list_index = 0;
        len = strlen(text);
    }

    while (commands[list_index]) {
        const char* cmd = commands[list_index];
        list_index++;

        if (strncmp(cmd, text, len) == 0) {
            return strdup(cmd);  // readline frees this later
        }
    }

    return NULL;
}

char** cli_completion(const char* text, int start, int end) {
    (void)start;
    (void)end;

    return rl_completion_matches(text, command_generator);
}

// *** Run CLI ***
void start_cli() {
    rl_attempted_completion_function = cli_completion;

    printf("Welcome to HRMCLi interactive shell.\n");
    printf("Type 'help' for a list of commands.\n");

    while (1) {
        char* input = readline("HRMCLi> ");

        if (!input) {
            break;
        }

        // skip empty input
        if (strlen(input) == 0) {
            free(input);
            continue;
        }

        // add to history
        add_history(input);

        // exit conditions
        if (strcmp(input, "exit") == 0 || strcmp(input, "quit") == 0) {
            free(input);
            break;
        }

        // pass the input to command handler
        handle_command(input);

        free(input);
    }

    printf("Exiting HRMCLi.\n");
}
