"""
Exercise checker for Economlings.
"""

import ast
import importlib.util
import sys
import traceback
from io import StringIO
from pathlib import Path
from typing import Any, Callable, Optional

import numpy as np


class CheckResult:
    """Result of checking an exercise."""

    def __init__(self, success: bool, message: str = "", details: str = ""):
        self.success = success
        self.message = message
        self.details = details

    def __bool__(self):
        return self.success


class ExerciseChecker:
    """Check exercises for correctness."""

    def __init__(self, exercise_path: Path):
        self.exercise_path = exercise_path
        self.exercise_name = exercise_path.stem
        self.module = None
        self.errors = []

    def check_syntax(self) -> CheckResult:
        """Check if the file has valid Python syntax."""
        try:
            with open(self.exercise_path, "r", encoding="utf-8") as f:
                source = f.read()
            ast.parse(source)
            return CheckResult(True, "语法检查通过")
        except SyntaxError as e:
            return CheckResult(
                False,
                f"语法错误在第 {e.lineno} 行",
                f"{e.msg}: {e.text.strip() if e.text else ''}"
            )

    def check_no_pass(self) -> CheckResult:
        """Check that there are no unimplemented functions (just 'pass')."""
        try:
            with open(self.exercise_path, "r", encoding="utf-8") as f:
                source = f.read()

            tree = ast.parse(source)

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Check if function body is just 'pass'
                    if (len(node.body) == 1 and
                        isinstance(node.body[0], ast.Pass)):
                        return CheckResult(
                            False,
                            f"函数 '{node.name}' 尚未实现",
                            "请删除 'pass' 并实现函数逻辑"
                        )
                    # Check if function body is just 'pass' with docstring
                    if (len(node.body) == 2 and
                        isinstance(node.body[0], ast.Expr) and
                        isinstance(node.body[0].value, ast.Constant) and
                        isinstance(node.body[1], ast.Pass)):
                        return CheckResult(
                            False,
                            f"函数 '{node.name}' 尚未实现",
                            "请删除 'pass' 并实现函数逻辑"
                        )

            return CheckResult(True, "所有函数已实现")
        except Exception as e:
            return CheckResult(False, f"检查失败: {e}")

    def load_module(self) -> CheckResult:
        """Load the exercise as a module."""
        try:
            spec = importlib.util.spec_from_file_location(
                self.exercise_name,
                self.exercise_path
            )
            if spec is None or spec.loader is None:
                return CheckResult(False, "无法加载模块")

            module = importlib.util.module_from_spec(spec)
            sys.modules[self.exercise_name] = module

            # Capture stdout during module loading
            old_stdout = sys.stdout
            sys.stdout = StringIO()
            try:
                spec.loader.exec_module(module)
            finally:
                sys.stdout = old_stdout

            self.module = module
            return CheckResult(True, "模块加载成功")
        except Exception as e:
            return CheckResult(
                False,
                "模块加载失败",
                f"{type(e).__name__}: {e}"
            )

    def check_function_exists(self, func_name: str) -> CheckResult:
        """Check if a function exists in the module."""
        if self.module is None:
            return CheckResult(False, "模块未加载")

        if hasattr(self.module, func_name):
            return CheckResult(True, f"函数 '{func_name}' 存在")
        else:
            return CheckResult(False, f"函数 '{func_name}' 不存在")

    def check_function_output(
        self,
        func_name: str,
        args: tuple = (),
        kwargs: dict = None,
        expected: Any = None,
        tolerance: float = 1e-6,
        comparator: Optional[Callable] = None
    ) -> CheckResult:
        """Check if a function returns the expected output."""
        if self.module is None:
            return CheckResult(False, "模块未加载")

        kwargs = kwargs or {}

        if not hasattr(self.module, func_name):
            return CheckResult(False, f"函数 '{func_name}' 不存在")

        func = getattr(self.module, func_name)

        try:
            result = func(*args, **kwargs)
        except Exception as e:
            return CheckResult(
                False,
                f"函数 '{func_name}' 执行出错",
                f"{type(e).__name__}: {e}\n{traceback.format_exc()}"
            )

        # Use custom comparator if provided
        if comparator is not None:
            try:
                if comparator(result, expected):
                    return CheckResult(True, f"函数 '{func_name}' 输出正确")
                else:
                    return CheckResult(
                        False,
                        f"函数 '{func_name}' 输出不正确",
                        f"期望: {expected}\n实际: {result}"
                    )
            except Exception as e:
                return CheckResult(False, f"比较器错误: {e}")

        # Default comparison
        if isinstance(expected, (int, float)):
            if isinstance(result, (int, float)):
                if abs(result - expected) <= tolerance:
                    return CheckResult(True, f"函数 '{func_name}' 输出正确")
                else:
                    return CheckResult(
                        False,
                        f"函数 '{func_name}' 输出不正确",
                        f"期望: {expected}\n实际: {result}\n差异: {abs(result - expected)}"
                    )

        if isinstance(expected, np.ndarray):
            if isinstance(result, np.ndarray):
                if np.allclose(result, expected, atol=tolerance):
                    return CheckResult(True, f"函数 '{func_name}' 输出正确")
                else:
                    return CheckResult(
                        False,
                        f"函数 '{func_name}' 输出不正确",
                        f"期望形状: {expected.shape}, 实际形状: {result.shape}"
                    )

        if isinstance(expected, tuple):
            if isinstance(result, tuple) and len(result) == len(expected):
                all_match = True
                for r, e in zip(result, expected):
                    if isinstance(e, (int, float)) and isinstance(r, (int, float)):
                        if abs(r - e) > tolerance:
                            all_match = False
                            break
                    elif r != e:
                        all_match = False
                        break
                if all_match:
                    return CheckResult(True, f"函数 '{func_name}' 输出正确")

        if result == expected:
            return CheckResult(True, f"函数 '{func_name}' 输出正确")

        return CheckResult(
            False,
            f"函数 '{func_name}' 输出不正确",
            f"期望: {expected}\n实际: {result}"
        )

    def run_tests(self, tests: list[dict]) -> list[CheckResult]:
        """Run a list of tests."""
        results = []
        for test in tests:
            result = self.check_function_output(**test)
            results.append(result)
        return results


def get_exercise_tests(exercise_name: str) -> list[dict]:
    """Get tests for a specific exercise."""
    # Import tests dynamically based on exercise name
    tests_module_path = Path(__file__).parent.parent / "tests" / f"test_{exercise_name}.py"

    if tests_module_path.exists():
        try:
            spec = importlib.util.spec_from_file_location(
                f"test_{exercise_name}",
                tests_module_path
            )
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                if hasattr(module, "TESTS"):
                    return module.TESTS
        except Exception:
            pass

    return []


def check(filepath: str, verbose: bool = True) -> bool:
    """
    Check an exercise file.
    This is the main function called from exercise files.
    """
    from rich.console import Console
    from rich.panel import Panel

    console = Console()
    exercise_path = Path(filepath)
    exercise_name = exercise_path.stem

    checker = ExerciseChecker(exercise_path)
    all_passed = True

    # Step 1: Syntax check
    result = checker.check_syntax()
    if not result:
        console.print(Panel(
            f"[red]✗ {result.message}[/red]\n{result.details}",
            title="语法错误",
            border_style="red"
        ))
        return False

    # Step 2: Check for unimplemented functions
    result = checker.check_no_pass()
    if not result:
        console.print(Panel(
            f"[yellow]⚠ {result.message}[/yellow]\n{result.details}",
            title="未完成",
            border_style="yellow"
        ))
        return False

    # Step 3: Load module
    result = checker.load_module()
    if not result:
        console.print(Panel(
            f"[red]✗ {result.message}[/red]\n{result.details}",
            title="加载错误",
            border_style="red"
        ))
        return False

    # Step 4: Run tests
    tests = get_exercise_tests(exercise_name)
    if tests:
        results = checker.run_tests(tests)
        for i, result in enumerate(results):
            if not result:
                all_passed = False
                console.print(f"[red]✗ 测试 {i+1}: {result.message}[/red]")
                if verbose and result.details:
                    console.print(f"  [dim]{result.details}[/dim]")
            else:
                console.print(f"[green]✓ 测试 {i+1}: {result.message}[/green]")

    if all_passed:
        console.print(Panel(
            f"[green]恭喜！练习 '{exercise_name}' 完成！[/green]\n"
            "运行 [bold]python -m economlings[/bold] 继续下一个练习",
            title="成功",
            border_style="green"
        ))

        # Update progress
        try:
            import sys
            from pathlib import Path
            sys.path.insert(0, str(Path(__file__).parent.parent.parent))
            from studylings.progress import Progress as StudylingsProgress
            from .config import config
            progress = StudylingsProgress(config)
            progress.mark_complete(exercise_name)
        except Exception:
            # Fallback to legacy progress if studylings not available
            from .progress import Progress
            progress = Progress()
            progress.mark_complete(exercise_name)

    return all_passed
