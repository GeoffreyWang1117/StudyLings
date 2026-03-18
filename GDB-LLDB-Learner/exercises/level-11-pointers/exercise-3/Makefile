CC = gcc
CFLAGS = -g -Wall -Wextra -O0
TARGET = funcptr
all: $(TARGET)
$(TARGET): funcptr.c
	$(CC) $(CFLAGS) funcptr.c -o $(TARGET)
clean:
	rm -f $(TARGET)
.PHONY: all clean
