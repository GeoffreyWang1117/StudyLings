CC = gcc
CFLAGS = -g -Wall
TARGET = breakpoint_commands
all: $(TARGET)
$(TARGET): breakpoint_commands.c
	$(CC) $(CFLAGS) breakpoint_commands.c -o $(TARGET)
clean:
	rm -f $(TARGET)
.PHONY: all clean
