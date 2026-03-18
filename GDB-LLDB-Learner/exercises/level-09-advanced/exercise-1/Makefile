CC = gcc
CFLAGS_DEBUG = -Og -g
CFLAGS_OPT = -O2 -g
TARGET = optimized
all: $(TARGET)_debug $(TARGET)_opt
$(TARGET)_debug: optimized.c
	$(CC) $(CFLAGS_DEBUG) optimized.c -o $(TARGET)_debug
$(TARGET)_opt: optimized.c
	$(CC) $(CFLAGS_OPT) optimized.c -o $(TARGET)_opt
clean:
	rm -f $(TARGET)_debug $(TARGET)_opt
.PHONY: all clean
