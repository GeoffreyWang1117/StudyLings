CC = gcc
CFLAGS = -g -Wall -Wextra -O0

TARGET = linkedlist
SRC = linkedlist.c

all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) $(SRC) -o $(TARGET)

clean:
	rm -f $(TARGET)

# 辅助目标
debug-gdb: $(TARGET)
	gdb -ex "break main" -ex "run" ./$(TARGET)

debug-lldb: $(TARGET)
	lldb -o "b main" -o "run" ./$(TARGET)

.PHONY: all clean debug-gdb debug-lldb
