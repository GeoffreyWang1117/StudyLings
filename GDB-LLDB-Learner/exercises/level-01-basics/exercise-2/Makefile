CC = gcc
CFLAGS = -g -Wall -Wextra

TARGET = args_demo
SRC = args_demo.c

all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) $(SRC) -o $(TARGET)

clean:
	rm -f $(TARGET)

.PHONY: all clean
