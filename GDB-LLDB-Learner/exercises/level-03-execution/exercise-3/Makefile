CC = gcc
CFLAGS = -g -Wall -Wextra
TARGET = recursion
SRC = recursion.c

all: $(TARGET)
$(TARGET): $(SRC)
	$(CC) $(CFLAGS) $(SRC) -o $(TARGET)
clean:
	rm -f $(TARGET)
.PHONY: all clean
