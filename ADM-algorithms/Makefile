# ADM Judge Makefile
# 简化常用命令

.PHONY: all build clean install run watch list progress help test verify-all

# 默认目标
all: build

# 构建判题系统
build:
	@echo "🔨 构建 ADM Judge..."
	@mkdir -p build
	@cd build && cmake .. && make
	@echo "✅ 构建完成！"
	@echo ""
	@echo "运行: make run 或 cd build && ./adm-judge"

# 清理构建文件
clean:
	@echo "🧹 清理构建文件..."
	@rm -rf build
	@echo "✅ 清理完成！"

# 安装（使用安装脚本）
install:
	@bash tools/install.sh

# 运行判题系统
run: build
	@cd build && ./adm-judge

# 启动监视模式
watch: build
	@cd build && ./adm-judge watch

# 列出所有练习
list: build
	@cd build && ./adm-judge list

# 查看进度
progress: build
	@cd build && ./adm-judge progress

# 验证所有练习文件能否编译
verify-all:
	@bash tools/verify_all.sh

# 测试特定练习
# 用法: make test EXERCISE=intro01
test: build
	@if [ -z "$(EXERCISE)" ]; then \
		echo "❌ 错误: 请指定练习名称"; \
		echo "用法: make test EXERCISE=intro01"; \
		exit 1; \
	fi
	@cd build && ./adm-judge verify $(EXERCISE)

# 显示帮助
help:
	@echo "ADM Judge - Makefile 命令"
	@echo ""
	@echo "可用命令:"
	@echo "  make              - 构建项目（等同于 make build）"
	@echo "  make build        - 构建判题系统"
	@echo "  make clean        - 清理构建文件"
	@echo "  make install      - 运行安装脚本"
	@echo "  make run          - 运行判题系统"
	@echo "  make watch        - 启动监视模式"
	@echo "  make list         - 列出所有练习"
	@echo "  make progress     - 查看学习进度"
	@echo "  make test EXERCISE=<name>  - 测试特定练习"
	@echo "  make verify-all   - 验证所有练习文件"
	@echo "  make help         - 显示此帮助信息"
	@echo ""
	@echo "示例:"
	@echo "  make              # 构建项目"
	@echo "  make run          # 运行判题系统"
	@echo "  make test EXERCISE=intro01  # 测试 intro01"
	@echo "  make progress     # 查看进度"

# 快速开始（构建并运行）
quickstart: build
	@echo ""
	@echo "🎉 欢迎使用 ADM Judge!"
	@echo ""
	@echo "📖 快速开始指南: QUICKSTART.md"
	@echo "📚 完整教程: docs/TUTORIAL.md"
	@echo ""
	@cd build && ./adm-judge
