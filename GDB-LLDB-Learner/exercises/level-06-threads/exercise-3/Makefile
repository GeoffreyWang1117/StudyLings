CC = gcc
CFLAGS = -g -Wall -pthread
TARGET = deadlock
all: $(TARGET)
$(TARGET): deadlock.c
	$(CC) $(CFLAGS) deadlock.c -o $(TARGET)
clean:
	rm -f $(TARGET)
.PHONY: all clean
