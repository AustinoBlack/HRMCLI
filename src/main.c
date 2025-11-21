#include "stdio.h"
#include "stdlib.h"
#include "cli.h"
#include "hrmcli.h"
#include "cjson/cJSON.h"

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

int main() {
    printf("Loading config: %s\n", CONFIG_FILE);
    cJSON* config = load_config(CONFIG_FILE);
    if (!config) {
        printf("Warning: could not load config, using defaults.\n");
    }

    start_cli();

    return 0;
}
