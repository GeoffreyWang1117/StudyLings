CC = gcc
CFLAGS = -g -Wall -Wextra -O0

# 可执行文件
EXEC = symbols
EXEC_WITH_OVERRIDE = symbols_override

.PHONY: all clean analyze

all: $(EXEC) $(EXEC_WITH_OVERRIDE)

# 基本版本（包含弱符号的默认实现）
$(EXEC): symbols.c
	$(CC) $(CFLAGS) symbols.c -o $(EXEC)
	@echo "基本版本构建完成: $(EXEC)"

# 覆盖版本（强符号覆盖弱符号）
$(EXEC_WITH_OVERRIDE): symbols.c external.c
	$(CC) $(CFLAGS) symbols.c external.c -o $(EXEC_WITH_OVERRIDE)
	@echo "覆盖版本构建完成: $(EXEC_WITH_OVERRIDE)"

# 分析符号
analyze: all
	@echo ""
	@echo "=== 基本版本符号分析 ==="
	@echo "所有全局符号:"
	@nm $(EXEC) | grep " [TDB] " | head -20
	@echo ""
	@echo "弱符号:"
	@nm $(EXEC) | grep " [Ww] "
	@echo ""
	@echo "静态符号:"
	@nm $(EXEC) | grep " [tdb] " | head -10
	@echo ""
	@echo "=== 覆盖版本符号分析 ==="
	@echo "弱符号状态:"
	@nm $(EXEC_WITH_OVERRIDE) | grep -E "(weak_var|weak_function)"
	@echo ""
	@echo "=== 符号表详情 (readelf) ==="
	@readelf -s $(EXEC) | grep -E "(weak_|hidden_|static_)" | head -10

clean:
	rm -f $(EXEC) $(EXEC_WITH_OVERRIDE) *.o

.PHONY: symbols
symbols: all
	@echo ""
	@echo "=== 符号类型统计 ==="
	@echo "T (全局函数):      $$(nm $(EXEC) | grep -c ' T ')"
	@echo "t (局部函数):      $$(nm $(EXEC) | grep -c ' t ')"
	@echo "D (全局数据):      $$(nm $(EXEC) | grep -c ' D ')"
	@echo "d (局部数据):      $$(nm $(EXEC) | grep -c ' d ')"
	@echo "B (全局 BSS):      $$(nm $(EXEC) | grep -c ' B ')"
	@echo "b (局部 BSS):      $$(nm $(EXEC) | grep -c ' b ')"
	@echo "R (只读数据):      $$(nm $(EXEC) | grep -c ' R ')"
	@echo "W (弱符号):        $$(nm $(EXEC) | grep -c ' W ')"
	@echo "U (未定义):        $$(nm $(EXEC) | grep -c ' U ')"
