#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "hrmcli.h"
#include "cJSON.h"

// Load JSON config
cJSON* load_config(const char* filename) {
    FILE* file = fopen(filename, "r");
    if (!file) {
        fprintf(stderr, "Failed to open config file: %s\n", filename);
        return NULL;
    }

    fseek(file, 0, SEEK_END);
    long length = ftell(file);
    rewind(file);

    char* data = malloc(length + 1);
    fread(data, 1, length, file);
    data[length] = '\0';
    fclose(file);

    cJSON* json = cJSON_Parse(data);
    if (!json) {
        fprintf(stderr, "Error parsing JSON config\n");
        free(data);
        return NULL;
    }

    free(data);
    return json;
}

// basic commands (placeholders)
void cmd_help() {
    printf("HRMCLi commands:\n");
    printf("  help    Show this help\n");
    printf("  ping    Test connection (placeholder)\n");
}

void cmd_ping() {
    printf("Pinging server... (not implemented yet)\n");
}

int main(int argc, char* argv[]) {
    cJSON* config = load_config(CONFIG_FILE);
    if (!config) {
        printf("Warning: could not load config, using defaults.\n");
    }

    if (argc < 2) {
        cmd_help();
        return 0;
    }

    if (strcmp(argv[1], "help") == 0) {
        cmd_help();
    } else if (strcmp(argv[1], "ping") == 0) {
        cmd_ping();
    } else {
        printf("Unknown command: %s\n", argv[1]);
        cmd_help();
    }

    if (config) {
        cJSON_Delete(config);
    }

    return 0;
}
