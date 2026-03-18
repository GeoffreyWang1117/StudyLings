CC = gcc
CFLAGS = -g -Wall -Wextra -O0
TARGET = hashtable
all: $(TARGET)
$(TARGET): hashtable.c
	$(CC) $(CFLAGS) hashtable.c -o $(TARGET)
clean:
	rm -f $(TARGET)
.PHONY: all clean
