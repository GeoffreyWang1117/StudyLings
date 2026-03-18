CC = gcc
CFLAGS = -g -Wall
TARGET = python_pretty
all: $(TARGET)
$(TARGET): python_pretty.c
	$(CC) $(CFLAGS) python_pretty.c -o $(TARGET)
clean:
	rm -f $(TARGET)
.PHONY: all clean
