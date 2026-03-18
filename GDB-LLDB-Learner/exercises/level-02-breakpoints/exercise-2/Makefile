CC = gcc
CFLAGS = -g -Wall -Wextra

TARGET = prime_finder
SRC = prime_finder.c

all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) $(SRC) -o $(TARGET)

clean:
	rm -f $(TARGET)

.PHONY: all clean
