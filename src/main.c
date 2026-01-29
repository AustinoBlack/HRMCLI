#include "stdio.h"
#include "stdlib.h"
#include "cli.h"
#include "hrmcli.h"
#include "cjson/cJSON.h"
#include "banner.h"
#include "loading.h"
#include "servers.h"


int main() {
    system("clear");
    hrmcli_banner(0);
    sleep(1);
    
    hrmcli_boot_sequence();

    return 0;
}
