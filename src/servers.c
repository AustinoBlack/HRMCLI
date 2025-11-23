#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <cjson/cJSON.h>
#include "servers.h"

server_t servers[32];
int num_servers = 0;

int load_servers(const char* file_path) {
    printf("DEBUG: Trying to open file '%s'\n", file_path);
    FILE* f = fopen(file_path, "r");
    if (!f) {
        perror("DEBUG: fopen failed");
        return -1;
    }   
    fseek(f, 0, SEEK_END);
    long size = ftell(f);
    fseek(f, 0, SEEK_SET);

    char* buffer = malloc(size + 1);
    size_t read = fread(buffer, 1, size, f);
    buffer[size] = '\0';
    fclose(f);

    if (read == 0) {
        printf("DEBUG: fread read 0 bytes\n");
        free(buffer);
        return -1;
    }

    cJSON* json = cJSON_Parse(buffer);
    if (!json) {
        printf("DEBUG: cJSON_Parse failed\n");
        free(buffer);
        return -1;
    }
    free(buffer);

    num_servers = 0;
    cJSON* item = NULL;
    cJSON_ArrayForEach(item, json) {
        if (num_servers >= 32) break;

        cJSON* name = cJSON_GetObjectItem(item, "name");
        cJSON* ip = cJSON_GetObjectItem(item, "ip");
        cJSON* user = cJSON_GetObjectItem(item, "bmc_user");
        cJSON* pass = cJSON_GetObjectItem(item, "bmc_pass");

        if (name && ip && user && pass) {
            strncpy(servers[num_servers].name, name->valuestring, 31);
            strncpy(servers[num_servers].ip, ip->valuestring, 31);
            strncpy(servers[num_servers].bmc_user, user->valuestring, 31);
            strncpy(servers[num_servers].bmc_pass, pass->valuestring, 31);
            num_servers++;
        }
    }

    cJSON_Delete(json);
    return 0;
}

void list_servers() {
    printf("Loaded servers (%d):\n", num_servers);
    for (int i = 0; i < num_servers; i++) {
        printf("%d: %s (%s)\n", i + 1, servers[i].name, servers[i].ip);
    }
}
