CC = gcc
CFLAGS = -g -Wall -Wextra -O0
TARGET = union_bits
all: $(TARGET)
$(TARGET): union_bits.c
	$(CC) $(CFLAGS) union_bits.c -o $(TARGET)
clean:
	rm -f $(TARGET)
.PHONY: all clean
