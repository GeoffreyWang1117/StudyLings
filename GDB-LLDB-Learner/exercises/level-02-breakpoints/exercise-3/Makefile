CC = gcc
CFLAGS = -g -Wall -Wextra

TARGET = multi_break
SRC = multi_break.c

all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) $(SRC) -o $(TARGET)

clean:
	rm -f $(TARGET)

.PHONY: all clean
