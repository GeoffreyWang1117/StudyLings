CC = gcc
CFLAGS = -g -Wall -Wextra -pthread

TARGET = threads
SRC = threads.c

all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) $(SRC) -o $(TARGET)

clean:
	rm -f $(TARGET)

.PHONY: all clean
