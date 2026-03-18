CC = gcc
CFLAGS = -g -Wall -pthread
TARGET = race
all: $(TARGET)
$(TARGET): race.c
	$(CC) $(CFLAGS) race.c -o $(TARGET)
clean:
	rm -f $(TARGET)
.PHONY: all clean
