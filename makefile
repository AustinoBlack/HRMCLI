CC = gcc
CFLAGS = -Wall -Wextra -Iinclude
LIBS = -lcjson
SRC = $(wildcard src/*.c)
OBJ = $(SRC:.c=.o)
TARGET = hrmcli

all: $(TARGET)

$(TARGET): $(OBJ)
	$(CC) $(CFLAGS) -o $@ $^ $(LIBS)

clean:
	rm -f $(OBJ) $(TARGET)
