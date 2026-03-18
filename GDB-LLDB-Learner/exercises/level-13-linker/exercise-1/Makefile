CC = gcc
CFLAGS = -g -Wall -Wextra -O0
AR = ar

# 目标文件
OBJS = mathlib.o

# 静态库
STATIC_LIB = libmath.a

# 动态库
SHARED_LIB = libmath.so

# 可执行文件
STATIC_EXEC = main_static
DYNAMIC_EXEC = main_dynamic

.PHONY: all clean static dynamic both

all: both

# 编译目标文件
mathlib.o: mathlib.c mathlib.h
	$(CC) $(CFLAGS) -c mathlib.c -o mathlib.o

# 编译目标文件（位置无关代码，用于动态库）
mathlib_pic.o: mathlib.c mathlib.h
	$(CC) $(CFLAGS) -fPIC -c mathlib.c -o mathlib_pic.o

# 创建静态库
$(STATIC_LIB): mathlib.o
	$(AR) rcs $(STATIC_LIB) mathlib.o
	@echo "静态库创建完成: $(STATIC_LIB)"

# 创建动态库
$(SHARED_LIB): mathlib_pic.o
	$(CC) -shared -o $(SHARED_LIB) mathlib_pic.o
	@echo "动态库创建完成: $(SHARED_LIB)"

# 静态链接的可执行文件
static: $(STATIC_LIB)
	$(CC) $(CFLAGS) main.c -L. -lmath -o $(STATIC_EXEC)
	@echo "静态链接可执行文件: $(STATIC_EXEC)"
	@size $(STATIC_EXEC)

# 动态链接的可执行文件
dynamic: $(SHARED_LIB)
	$(CC) $(CFLAGS) main.c -L. -lmath -o $(DYNAMIC_EXEC)
	@echo "动态链接可执行文件: $(DYNAMIC_EXEC)"
	@size $(DYNAMIC_EXEC)

# 构建两种版本
both: static dynamic
	@echo ""
	@echo "=== 文件大小对比 ==="
	@ls -lh $(STATIC_EXEC) $(DYNAMIC_EXEC) $(STATIC_LIB) $(SHARED_LIB)
	@echo ""
	@echo "=== 符号对比 ==="
	@echo "静态链接符号数:"
	@nm $(STATIC_EXEC) | wc -l
	@echo "动态链接符号数:"
	@nm $(DYNAMIC_EXEC) | wc -l

# 分析工具
analyze: both
	@echo "=== 静态链接分析 ==="
	@echo "符号表:"
	@nm -C $(STATIC_EXEC) | grep -E "(add|multiply|factorial)"
	@echo ""
	@echo "=== 动态链接分析 ==="
	@echo "符号表:"
	@nm -D $(DYNAMIC_EXEC) | grep -E "(add|multiply|factorial)"
	@echo ""
	@echo "动态库依赖:"
	@ldd $(DYNAMIC_EXEC)
	@echo ""
	@echo "库中的符号:"
	@nm -D $(SHARED_LIB)

clean:
	rm -f *.o $(STATIC_LIB) $(SHARED_LIB) $(STATIC_EXEC) $(DYNAMIC_EXEC)

.PHONY: analyze
