CC = gcc
CFLAGS = -g -Wall -Wextra

TARGET = factorial
SRC = factorial.c

all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) $(SRC) -o $(TARGET)

clean:
	rm -f $(TARGET)

.PHONY: all clean
