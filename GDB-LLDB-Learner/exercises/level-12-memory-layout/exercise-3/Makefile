CC = gcc
CFLAGS = -g -Wall -Wextra -O0
TARGET = segments

all: $(TARGET)

$(TARGET): segments.c
	$(CC) $(CFLAGS) segments.c -o $(TARGET)

clean:
	rm -f $(TARGET)

.PHONY: all clean
