CC = gcc
CFLAGS = -g -Wall
TARGET = params
all: $(TARGET)
$(TARGET): params.c
	$(CC) $(CFLAGS) params.c -o $(TARGET)
clean:
	rm -f $(TARGET)
.PHONY: all clean
