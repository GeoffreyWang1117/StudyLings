CC = gcc
CFLAGS = -g -Wall -Wextra

TARGET = calculator
SRC = calculator.c

all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) $(SRC) -o $(TARGET)

clean:
	rm -f $(TARGET)

.PHONY: all clean
