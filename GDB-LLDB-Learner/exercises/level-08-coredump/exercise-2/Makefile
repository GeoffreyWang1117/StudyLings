CC = gcc
CFLAGS = -g -Wall
TARGET = segfault
all: $(TARGET)
$(TARGET): segfault.c
	$(CC) $(CFLAGS) segfault.c -o $(TARGET)
clean:
	rm -f $(TARGET) core*
.PHONY: all clean
