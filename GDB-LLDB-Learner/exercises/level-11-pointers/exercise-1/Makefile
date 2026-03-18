CC = gcc
CFLAGS = -g -Wall -Wextra -O0
TARGET = multilevel
all: $(TARGET)
$(TARGET): multilevel.c
	$(CC) $(CFLAGS) multilevel.c -o $(TARGET)
clean:
	rm -f $(TARGET)
.PHONY: all clean
