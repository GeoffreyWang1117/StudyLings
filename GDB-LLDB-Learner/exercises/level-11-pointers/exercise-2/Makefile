CC = gcc
CFLAGS = -g -Wall -Wextra -O0
TARGET = arrays
all: $(TARGET)
$(TARGET): arrays.c
	$(CC) $(CFLAGS) arrays.c -o $(TARGET)
clean:
	rm -f $(TARGET)
.PHONY: all clean
