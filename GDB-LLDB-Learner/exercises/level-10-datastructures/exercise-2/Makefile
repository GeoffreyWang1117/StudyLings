CC = gcc
CFLAGS = -g -Wall -Wextra -O0
TARGET = binarytree
all: $(TARGET)
$(TARGET): binarytree.c
	$(CC) $(CFLAGS) binarytree.c -o $(TARGET)
clean:
	rm -f $(TARGET)
.PHONY: all clean
