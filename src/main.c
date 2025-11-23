#include "stdio.h"
#include "stdlib.h"
#include "cli.h"
#include "hrmcli.h"
#include "cjson/cJSON.h"
#include "banner.h"
#include "loading.h"
#include "servers.h"

#define SERVER_CONFIG "config/servers.json"

int main() {
    system("clear");
    hrmcli_banner(0);
    sleep(1);
    printf("Loading server config: %s\n", SERVER_CONFIG);

    // Load server list
    if (load_servers(SERVER_CONFIG) != 0) {
        printf("\033[33m[WARN]\033[0m Could not load server configuration.\n");
        printf("Using an empty server list.\n");
    } else {
        printf("\033[32m[OK]\033[0m Loaded %d servers.\n", num_servers);
    } 

    hrmcli_boot_sequence();
    start_cli();

    return 0;
}
