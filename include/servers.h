#ifndef SERVERS_H
#define SERVERS_H

typedef struct {
    char name[32];
    char ip[32];
    char bmc_user[32];
    char bmc_pass[32];
} server_t;

int load_servers (const char* file_path);
void list_servers();

extern server_t servers[32]; // *** supports up to 32 servers ***
extern int num_servers;

#endif
