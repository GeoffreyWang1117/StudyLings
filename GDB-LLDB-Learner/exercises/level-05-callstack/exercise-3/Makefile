CC = gcc
CFLAGS = -g -Wall
TARGET = error
all: $(TARGET)
$(TARGET): error.c
	$(CC) $(CFLAGS) error.c -o $(TARGET)
clean:
	rm -f $(TARGET)
.PHONY: all clean
