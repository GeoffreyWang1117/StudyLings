CC = gcc
CFLAGS = -g -Wall
TARGET = crash
all: $(TARGET)
$(TARGET): crash.c
	$(CC) $(CFLAGS) crash.c -o $(TARGET)
clean:
	rm -f $(TARGET) core
.PHONY: all clean
