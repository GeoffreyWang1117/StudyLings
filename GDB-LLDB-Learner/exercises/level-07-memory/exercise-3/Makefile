CC = gcc
CFLAGS = -g -Wall -Wno-stringop-overflow
TARGET = buffer
all: $(TARGET)
$(TARGET): buffer.c
	$(CC) $(CFLAGS) buffer.c -o $(TARGET)
clean:
	rm -f $(TARGET)
.PHONY: all clean
