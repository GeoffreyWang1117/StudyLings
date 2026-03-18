CC = gcc
CFLAGS = -g -Wall -Wextra -O0
TARGET = alignment
all: $(TARGET)
$(TARGET): alignment.c
	$(CC) $(CFLAGS) alignment.c -o $(TARGET)
clean:
	rm -f $(TARGET)
.PHONY: all clean
