#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>
#include "loading.h"

// ANSI color codes
#define COLOR_RESET  "\033[0m"
#define COLOR_GREEN  "\033[32m"
#define COLOR_YELLOW "\033[33m"

// Grow bar animation with randomized speed
static void grow_bar(int width, int min_delay_ms, int max_delay_ms) {
    printf("\nInitializing HRMCLi...\n\n");

    for (int i = 0; i <= width; i++) {
        printf("\r[");
        for (int j = 0; j < width; j++) {
            if (j < i) printf("█");
            else       printf(" ");
        }
        printf("]");
        fflush(stdout);

        // random delay between min_delay_ms and max_delay_ms
        int delay = min_delay_ms + rand() % (max_delay_ms - min_delay_ms + 1);
        usleep(delay * 1000);
    }

    printf("\n\n");
}

// Status check helper with randomized delay
static void status_line(const char *msg, int min_delay_ms, int max_delay_ms) {
    // print in-progress indicator in yellow
    printf("[%s..%s] %s", COLOR_YELLOW, COLOR_RESET, msg);
    fflush(stdout);

    int delay = min_delay_ms + rand() % (max_delay_ms - min_delay_ms + 1);
    usleep(delay * 1000);

    // replace with OK in green
    printf("\r[%sOK%s] %s\n", COLOR_GREEN, COLOR_RESET, msg);
    fflush(stdout);
}

void hrmcli_boot_sequence(void) {
    // seed random generator
    srand((unsigned int)time(NULL));

    int bar_width = 30;

    // grow bar with randomized speed 20–60ms per step
    grow_bar(bar_width, 20, 250);

     // Long status list
    const char *status_steps[] = {
        "Loading configuration files...",
        "Initializing serial interfaces...",
        "Scanning USB devices...",
        "Checking BMC/IPMI modules...",
        "Verifying hardware access...",
        "Loading command registry...",
        "Setting up logging system...",
        "Verifying environment variables...",
        "Testing network interfaces...",
        "Checking hostname resolution...",
        "Loading server cache...",
        "Initializing CLI modules...",
        "Checking firmware versions...",
        "Synchronizing time...",
        "Finalizing system initialization...",
        "Starting HRMCLi shell..."
    };

    int num_steps = sizeof(status_steps) / sizeof(status_steps[0]);

    for (int i = 0; i < num_steps; i++) {
        status_line(status_steps[i], 100, 1000); // randomized 100–500ms
    }

    printf("\n");
}

