CC = gcc
CFLAGS = -g -Wall
TARGET = assert_fail
all: $(TARGET)
$(TARGET): assert_fail.c
	$(CC) $(CFLAGS) assert_fail.c -o $(TARGET)
clean:
	rm -f $(TARGET) core*
.PHONY: all clean
