CC = gcc
CFLAGS = -g -Wall -Wextra
TARGET = callstack
all: $(TARGET)
$(TARGET): callstack.c
	$(CC) $(CFLAGS) callstack.c -o $(TARGET)
clean:
	rm -f $(TARGET)
.PHONY: all clean
