CC = gcc
CFLAGS = -g -Wall -Wextra

TARGET = help_demo
SRC = help_demo.c

all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) $(SRC) -o $(TARGET)

clean:
	rm -f $(TARGET)

.PHONY: all clean
