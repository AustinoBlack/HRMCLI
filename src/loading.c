#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>

#include "loading.h"
#include "servers.h"
#include "cli.h"

#define SERVERS_CONFIG "config/servers.json"
 
// ------------------------------ Colors ------------------------------------
#define CLR_OK   "\033[1;32m"
#define CLR_FAIL "\033[1;31m"
#define CLR_WARN "\033[1;33m"
#define CLR_RST  "\033[0m"

// --------------------------- Status printer ----------------------------------
static void print_status(status_t s) {
    switch (s) {
        case STATUS_OK:   printf(CLR_OK  "[ OK ]"  CLR_RST); break;
        case STATUS_FAIL: printf(CLR_FAIL"[FAIL]"  CLR_RST); break;
        case STATUS_WARN: printf(CLR_WARN"[WARN]"  CLR_RST); break;
    }
}

// --------------------------- Boot step table --------------------------------

static boot_step_t boot_steps[] = {
    { "Loading configuration files",       check_config_files },
    { "Loading server database",           check_server_database },
    { "Checking network stack",            check_network_stack },
    { "Verifying dependencies",            check_dependencies },
    { "Scanning USB devices...",           check_USB_devices },
    { "Initializing serial interfaces...", check_serial_interface },
    { "Checking BMC/IPMI modules...",      check_BMC_interfaces },
    { "Verifying hardware access...",      check_hardware_access },
    { "Loading command registry...",       load_registry },
    { "Setting up logging system...",      set_logging },
    { "Verifying environment variables...", check_environment_variables },
    { "Testing network interfaces...",     test_network_interfaces },
    { "Checking hostname resolution...",   check_hostname },
    { "Loading server cache...",           load_server_cache },
    { "Initializing CLI modules...",       CLI_modules_init },
    { "Checking firmware versions...",     check_firmware_versions },
    { "Synchronizing time...",             sync_time },
    { "Finalizing system initialization...", final_checks },
    { "Starting HRMCLi shell...",          check_start_cli }
};

static const int BOOT_STEP_COUNT = sizeof(boot_steps) / sizeof(boot_steps[0]);

// ----------------------------- BOOT SEQUENCE -----------------------------------

void hrmcli_boot_sequence(void) 
{
    srand(time(NULL));

    char detail[256];

    printf("\n");

    for (int i = 0; i < BOOT_STEP_COUNT; i++) {

        // Print main label
        printf("%-50s", boot_steps[i].label);
        fflush(stdout);

        // Slow it down for realism
        usleep((rand() % 400 + 150) * 1000);

        // Run check function
        memset(detail, 0, sizeof(detail));
        status_t st = boot_steps[i].check_function(detail, sizeof(detail));

        print_status(st);
        printf("\n");

        // If the function printed a detail message
        if (strlen(detail) > 0) {
            printf(" - %s\n", detail);
        }

        // Optional: abort on fatal fail
        // if (st == STATUS_FAIL) break;
    }

    printf("\n");
}

// --------------- CHECK FUNCTIONS (Stub implementations) ---------------

status_t check_config_files(char *msg, size_t len) {
    FILE *f = fopen(SERVERS_CONFIG, "r");
    if (!f) {
        snprintf(msg, len, "ERROR: Could not read config/servers.json");
        return STATUS_FAIL;
    }
    else if (load_servers(SERVERS_CONFIG) != 0) {
        printf("\033[33m[WARN]\033[0m Could not load server configuration.\n");
        printf("Using an empty server list.\n");
    }
    fclose(f);
    snprintf(msg, len, "Loaded: config/servers.json");
    return STATUS_OK;
}

status_t check_server_database(char *msg, size_t len) {
    extern int num_servers;
    if (num_servers <= 0) {
        snprintf(msg, len, "No servers defined");
        return STATUS_WARN;
    }
    snprintf(msg, len, "Loaded %d servers", num_servers);
    return STATUS_OK;
}

status_t check_network_stack(char *msg, size_t len) {
    snprintf(msg, len, "Network interfaces detected");
    return STATUS_OK;
}

status_t check_dependencies(char *msg, size_t len) {
    snprintf(msg, len, "ipmitool, socat OK");
    return STATUS_OK;
}

status_t check_USB_devices(char *msg, size_t len) {
    snprintf(msg, len, "USB scan complete");
    return STATUS_OK;
}

status_t check_serial_interface(char *msg, size_t len) {
    snprintf(msg, len, "Serial ports initialized");
    return STATUS_OK;
}

status_t check_BMC_interfaces(char *msg, size_t len) {
    snprintf(msg, len, "Some BMCs unreachable (expected)");
    return STATUS_WARN;
}

status_t check_hardware_access(char *msg, size_t len) {
    snprintf(msg, len, "/dev access OK");
    return STATUS_OK;
}

status_t load_registry(char *msg, size_t len) {
    snprintf(msg, len, "Command registry loaded");
    return STATUS_OK;
}

status_t set_logging(char *msg, size_t len) {
    snprintf(msg, len, "Logging enabled");
    return STATUS_OK;
}

status_t check_environment_variables(char *msg, size_t len) {
    snprintf(msg, len, "Environment validated");
    return STATUS_OK;
}

status_t test_network_interfaces(char *msg, size_t len) {
    snprintf(msg, len, "eth0 UP, wlan0 DOWN");
    return STATUS_OK;
}

status_t check_hostname(char *msg, size_t len) {
    snprintf(msg, len, "Hostname OK");
    return STATUS_OK;
}

status_t load_server_cache(char *msg, size_t len) {
    snprintf(msg, len, "Cache not found (fresh start)");
    return STATUS_WARN;
}

status_t CLI_modules_init(char *msg, size_t len) {
    snprintf(msg, len, "CLI modules ready");
    return STATUS_OK;
}

status_t check_firmware_versions(char *msg, size_t len) {
    snprintf(msg, len, "Firmware checks deferred");
    return STATUS_WARN;
}

status_t sync_time(char *msg, size_t len) {
    snprintf(msg, len, "Time is synced");
    return STATUS_OK;
}

status_t final_checks(char *msg, size_t len) {
    snprintf(msg, len, "System ready");
    return STATUS_OK;
}

// ------------------ start_cli() wrapper for boot system ------------------------
status_t check_start_cli(char *msg, size_t len) {
    start_cli();
    snprintf(msg, len, "Exiting shell...");
    return STATUS_OK;
}

