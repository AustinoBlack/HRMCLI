#ifndef LOADING_H
#define LOADING_H

#include <stddef.h>

// -------------------- Status Enum --------------------

typedef enum {
    STATUS_OK,
    STATUS_FAIL,
    STATUS_WARN
} status_t;

// -------------------- Function Type --------------------

typedef status_t (*check_func_t)(char *msg_out, size_t msg_len);

// -------------------- Boot Step Struct --------------------

typedef struct {
    const char *label;
    check_func_t check_function;
} boot_step_t;

// -------------------- Boot Sequence --------------------

void hrmcli_boot_sequence(void);

// -------------------- Check Function Prototypes --------------------

status_t check_config_files(char *msg, size_t len);
status_t check_server_database(char *msg, size_t len);
status_t check_network_stack(char *msg, size_t len);
status_t check_dependencies(char *msg, size_t len);
status_t check_USB_devices(char *msg, size_t len);
status_t check_serial_interface(char *msg, size_t len);
status_t check_BMC_interfaces(char *msg, size_t len);
status_t check_hardware_access(char *msg, size_t len);
status_t load_registry(char *msg, size_t len);
status_t set_logging(char *msg, size_t len);
status_t check_environment_variables(char *msg, size_t len);
status_t test_network_interfaces(char *msg, size_t len);
status_t check_hostname(char *msg, size_t len);
status_t load_server_cache(char *msg, size_t len);
status_t CLI_modules_init(char *msg, size_t len);
status_t check_firmware_versions(char *msg, size_t len);
status_t sync_time(char *msg, size_t len);
status_t final_checks(char *msg, size_t len);

status_t check_start_cli(char *msg, size_t len);

#endif

