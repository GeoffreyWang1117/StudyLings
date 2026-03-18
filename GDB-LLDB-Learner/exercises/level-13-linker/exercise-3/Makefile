CC = gcc
CFLAGS = -g -Wall -Wextra -O0
LDFLAGS = -ldl

EXEC = pltgot
HOOK = hook.so

.PHONY: all clean analyze run-normal run-lazy run-hook

all: $(EXEC) $(HOOK)

$(EXEC): pltgot.c
	$(CC) $(CFLAGS) pltgot.c $(LDFLAGS) -o $(EXEC)
	@echo "可执行文件构建完成: $(EXEC)"

$(HOOK): hook.c
	$(CC) $(CFLAGS) -shared -fPIC hook.c $(LDFLAGS) -o $(HOOK)
	@echo "Hook 库构建完成: $(HOOK)"

# 正常运行
run-normal: $(EXEC)
	@echo "=== 正常运行 (延迟绑定) ==="
	./$(EXEC)

# 禁用延迟绑定
run-eager: $(EXEC)
	@echo "=== 禁用延迟绑定 ==="
	LD_BIND_NOW=1 ./$(EXEC) 1

# 使用 Hook
run-hook: $(EXEC) $(HOOK)
	@echo "=== 使用 LD_PRELOAD Hook ==="
	LD_PRELOAD=./$(HOOK) ./$(EXEC)

# 显示绑定过程
run-debug: $(EXEC)
	@echo "=== 显示绑定过程 ==="
	LD_DEBUG=bindings ./$(EXEC) 2>&1 | grep -E "(printf|malloc|free|binding)"

# 分析 PLT/GOT
analyze: $(EXEC)
	@echo "=== PLT 段 ==="
	@objdump -d -j .plt $(EXEC) | head -40
	@echo ""
	@echo "=== GOT.PLT 段 ==="
	@objdump -s -j .got.plt $(EXEC)
	@echo ""
	@echo "=== 重定位表 (.rela.plt) ==="
	@readelf -r $(EXEC) | grep "\.rela\.plt" -A 10

clean:
	rm -f $(EXEC) $(HOOK)
