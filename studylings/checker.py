"""
Pluggable validation strategies for studylings projects.
"""

import ast
import importlib.util
import os
import subprocess
import sys
import traceback
from io import StringIO
from pathlib import Path
from typing import Any, Callable, Optional

from .exercise import Exercise, ProjectConfig, ValidationMode


class CheckResult:
    """Result of checking an exercise."""

    def __init__(self, success: bool, message: str = "", details: str = ""):
        self.success = success
        self.message = message
        self.details = details

    def __bool__(self):
        return self.success


class CheckerBase:
    """Base class for exercise checkers."""

    def __init__(self, exercise: Exercise, config: ProjectConfig):
        self.exercise = exercise
        self.config = config

    def check(self, verbose: bool = True) -> CheckResult:
        raise NotImplementedError


class TestFileChecker(CheckerBase):
    """Validates exercises using external test files (study-Economy style)."""

    def __init__(self, exercise: Exercise, config: ProjectConfig):
        super().__init__(exercise, config)
        self.module = None

    def check_syntax(self) -> CheckResult:
        """Check if the file has valid Python syntax."""
        try:
            source = self.exercise.path.read_text(encoding="utf-8")
            ast.parse(source)
            return CheckResult(True, "语法检查通过")
        except SyntaxError as e:
            return CheckResult(
                False,
                f"语法错误在第 {e.lineno} 行",
                f"{e.msg}: {e.text.strip() if e.text else ''}",
            )

    def check_no_pass(self) -> CheckResult:
        """Check that there are no unimplemented functions (just 'pass')."""
        try:
            source = self.exercise.path.read_text(encoding="utf-8")
            tree = ast.parse(source)

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
                        return CheckResult(
                            False,
                            f"函数 '{node.name}' 尚未实现",
                            "请删除 'pass' 并实现函数逻辑",
                        )
                    if (
                        len(node.body) == 2
                        and isinstance(node.body[0], ast.Expr)
                        and isinstance(node.body[0].value, ast.Constant)
                        and isinstance(node.body[1], ast.Pass)
                    ):
                        return CheckResult(
                            False,
                            f"函数 '{node.name}' 尚未实现",
                            "请删除 'pass' 并实现函数逻辑",
                        )

            return CheckResult(True, "所有函数已实现")
        except Exception as e:
            return CheckResult(False, f"检查失败: {e}")

    def load_module(self) -> CheckResult:
        """Load the exercise as a module."""
        try:
            spec = importlib.util.spec_from_file_location(
                self.exercise.name, self.exercise.path
            )
            if spec is None or spec.loader is None:
                return CheckResult(False, "无法加载模块")

            module = importlib.util.module_from_spec(spec)
            sys.modules[self.exercise.name] = module

            old_stdout = sys.stdout
            sys.stdout = StringIO()
            try:
                spec.loader.exec_module(module)
            finally:
                sys.stdout = old_stdout

            self.module = module
            return CheckResult(True, "模块加载成功")
        except Exception as e:
            return CheckResult(False, "模块加载失败", f"{type(e).__name__}: {e}")

    def check_function_output(
        self,
        func_name: str,
        args: tuple = (),
        kwargs: dict = None,
        expected: Any = None,
        tolerance: float = 1e-6,
        comparator: Optional[Callable] = None,
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
                f"{type(e).__name__}: {e}\n{traceback.format_exc()}",
            )

        if comparator is not None:
            try:
                if comparator(result, expected):
                    return CheckResult(True, f"函数 '{func_name}' 输出正确")
                else:
                    return CheckResult(
                        False,
                        f"函数 '{func_name}' 输出不正确",
                        f"期望: {expected}\n实际: {result}",
                    )
            except Exception as e:
                return CheckResult(False, f"比较器错误: {e}")

        # Default comparison
        if isinstance(expected, (int, float)) and isinstance(result, (int, float)):
            if abs(result - expected) <= tolerance:
                return CheckResult(True, f"函数 '{func_name}' 输出正确")
            else:
                return CheckResult(
                    False,
                    f"函数 '{func_name}' 输出不正确",
                    f"期望: {expected}\n实际: {result}\n差异: {abs(result - expected)}",
                )

        # numpy array comparison
        try:
            import numpy as np

            if isinstance(expected, np.ndarray) and isinstance(result, np.ndarray):
                if np.allclose(result, expected, atol=tolerance):
                    return CheckResult(True, f"函数 '{func_name}' 输出正确")
                else:
                    return CheckResult(
                        False,
                        f"函数 '{func_name}' 输出不正确",
                        f"期望形状: {expected.shape}, 实际形状: {result.shape}",
                    )
        except ImportError:
            pass

        if isinstance(expected, tuple) and isinstance(result, tuple) and len(result) == len(expected):
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
            f"期望: {expected}\n实际: {result}",
        )

    def get_exercise_tests(self) -> list:
        """Get tests for the exercise from external test files."""
        tests_path = self.config.get_tests_path()
        if tests_path is None:
            return []

        test_file = tests_path / f"test_{self.exercise.name}.py"
        if not test_file.exists():
            return []

        try:
            spec = importlib.util.spec_from_file_location(
                f"test_{self.exercise.name}", test_file
            )
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                if hasattr(module, "TESTS"):
                    return module.TESTS
        except Exception:
            pass

        return []

    def check(self, verbose: bool = True) -> CheckResult:
        """Run full validation pipeline."""
        # Step 1: Syntax check
        result = self.check_syntax()
        if not result:
            return result

        # Step 2: Check for unimplemented functions
        result = self.check_no_pass()
        if not result:
            return result

        # Step 3: Load module
        result = self.load_module()
        if not result:
            return result

        # Step 4: Run tests
        tests = self.get_exercise_tests()
        if tests:
            all_passed = True
            messages = []
            for i, test in enumerate(tests):
                result = self.check_function_output(**test)
                if not result:
                    all_passed = False
                    msg = f"✗ 测试 {i+1}: {result.message}"
                    if verbose and result.details:
                        msg += f"\n  {result.details}"
                    messages.append(msg)
                else:
                    messages.append(f"✓ 测试 {i+1}: {result.message}")

            detail_text = "\n".join(messages)
            if not all_passed:
                return CheckResult(False, "部分测试未通过", detail_text)
            return CheckResult(True, "所有测试通过", detail_text)

        return CheckResult(True, "练习完成")


class VerifyFuncChecker(CheckerBase):
    """Validates exercises using embedded verify() functions (TodayPhysics style)."""

    def check(self, verbose: bool = True) -> CheckResult:
        """Run the exercise and call verify()."""
        try:
            spec = importlib.util.spec_from_file_location(
                self.exercise.name, self.exercise.path
            )
            module = importlib.util.module_from_spec(spec)

            stdout_capture = StringIO()
            stderr_capture = StringIO()

            from contextlib import redirect_stdout, redirect_stderr

            with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                spec.loader.exec_module(module)

                if hasattr(module, "verify"):
                    result = module.verify()
                    if result is False:
                        output = stdout_capture.getvalue()
                        return CheckResult(False, "验证失败 Verification failed", output)

            output = stdout_capture.getvalue()
            return CheckResult(True, "验证通过", output)

        except Exception as e:
            return CheckResult(
                False,
                "执行出错",
                f"{type(e).__name__}: {e}\n{traceback.format_exc()}",
            )


class CompileAndRunChecker(CheckerBase):
    """Validates exercises by checking markers, compiling, and running (Vulkan-Study style)."""

    def check(self, verbose: bool = True) -> CheckResult:
        """Check markers, compile, and run."""
        try:
            content = self.exercise.path.read_text(encoding="utf-8")
        except Exception as e:
            return CheckResult(False, f"无法读取文件: {e}")

        # Check for placeholder markers
        for marker in self.config.placeholder_markers:
            if marker in content:
                count = content.count(marker)
                return CheckResult(
                    False,
                    f"还有 {count} 个占位符需要填写",
                    f"占位符: {marker}",
                )

        # Check TODO markers (warning, not failure)
        todo_warnings = []
        for marker in self.config.todo_markers:
            prefix = self.config.comment_prefix
            full_marker = f"{prefix} {marker}"
            if full_marker in content:
                count = content.count(full_marker)
                todo_warnings.append(f"还有 {count} 个 {marker} 未完成")

        # Compile
        build_dir = self.config.build_dir
        if not build_dir:
            return CheckResult(False, "未配置构建目录")

        try:
            compile_result = subprocess.run(
                ["make", self.exercise.name],
                cwd=build_dir,
                capture_output=True,
                text=True,
                timeout=60,
            )
            if compile_result.returncode != 0:
                error_lines = compile_result.stderr.split("\n")[-20:]
                return CheckResult(
                    False,
                    "编译失败",
                    "\n".join(error_lines),
                )
        except subprocess.TimeoutExpired:
            return CheckResult(False, "编译超时")
        except FileNotFoundError:
            return CheckResult(False, "找不到 make 命令，请先运行 cmake")

        # Run
        executable = Path(build_dir) / self.exercise.name
        if not executable.exists():
            return CheckResult(False, f"找不到可执行文件: {executable}")

        try:
            run_result = subprocess.run(
                [str(executable)],
                capture_output=True,
                text=True,
                timeout=self.config.run_timeout,
            )
            if run_result.returncode != 0:
                return CheckResult(
                    False,
                    "运行失败",
                    run_result.stderr or run_result.stdout,
                )
        except subprocess.TimeoutExpired:
            return CheckResult(False, "运行超时")

        # Mark as completed
        completed_file = self.exercise.path.parent / ".completed"
        completed_file.touch()

        detail = ""
        if todo_warnings:
            detail = "警告: " + "; ".join(todo_warnings)

        return CheckResult(True, "验证通过", detail)


class BuildAndProbeChecker(CheckerBase):
    """Builds one CMake target, then probes the binary from outside with pytest.

    Used by Unixlings/Netlings: systems behaviour (signals, fds, zombies, sockets)
    cannot be judged by comparing stdout, so each exercise has a probe at
    tests/<chapter>/test_<name>.py that drives the program like a real user would.
    """

    def __init__(self, exercise: Exercise, config: ProjectConfig, preset: Optional[str] = None):
        super().__init__(exercise, config)
        self.preset = preset or os.environ.get("STUDYLINGS_PRESET") or config.cmake_preset
        root = config.project_root
        self.build_dir = root / "build" / self.preset

    def _cmake(self, args: list, timeout: int) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["cmake", *args], cwd=self.config.project_root,
            capture_output=True, text=True, timeout=timeout,
        )

    def build(self) -> CheckResult:
        try:
            if not (self.build_dir / "CMakeCache.txt").exists():
                r = self._cmake(["--preset", self.preset], timeout=120)
                if r.returncode != 0:
                    return CheckResult(False, "CMake 配置失败", (r.stdout + r.stderr)[-3000:])
            r = self._cmake(["--build", "--preset", self.preset, "--target", self.exercise.name], timeout=180)
        except FileNotFoundError:
            return CheckResult(False, "找不到 cmake，请先安装工具链（见项目 README 或 .devcontainer/systems）")
        except subprocess.TimeoutExpired:
            return CheckResult(False, "编译超时")
        if r.returncode != 0:
            lines = [l for l in (r.stdout + r.stderr).splitlines() if not l.startswith("[")]
            return CheckResult(False, "编译失败", "\n".join(lines[-40:]))
        return CheckResult(True, "编译通过")

    def binary(self) -> Path:
        return self.build_dir / "bin" / self.exercise.name

    def probe_file(self) -> Path:
        tests = self.config.project_root / (self.config.tests_dir or "tests")
        return tests / self.exercise.chapter / f"test_{self.exercise.name}.py"

    def probe(self) -> CheckResult:
        probe = self.probe_file()
        env = dict(os.environ)
        suite_root = str(Path(__file__).resolve().parent.parent)
        env["PYTHONPATH"] = os.pathsep.join(filter(None, [suite_root, env.get("PYTHONPATH")]))
        env["SL_BIN"] = str(self.binary())
        env["SL_BUILD_DIR"] = str(self.build_dir)

        if not probe.exists():
            r = subprocess.run([str(self.binary())], capture_output=True, text=True,
                               timeout=self.config.run_timeout, env=env)
            if r.returncode != 0:
                return CheckResult(False, f"运行失败 (exit {r.returncode})", (r.stdout + r.stderr)[-3000:])
            return CheckResult(True, "运行通过", r.stdout[-2000:])

        cmd = [sys.executable, "-m", "pytest", "-q", "-x", "--no-header", "-rs", "--tb=short",
               "-p", "no:cacheprovider", str(probe)]
        try:
            r = subprocess.run(cmd, cwd=self.config.project_root, capture_output=True,
                               text=True, timeout=max(120, self.config.run_timeout * 6), env=env)
        except subprocess.TimeoutExpired:
            return CheckResult(False, "测试超时（程序可能卡死：死锁、忘记关闭管道写端、阻塞在 accept/read？）")
        out = (r.stdout + r.stderr).strip()
        summary = out.splitlines()[-1] if out else ""
        if r.returncode == 0 and "passed" not in summary and "skipped" in summary:
            return CheckResult(False, "环境不满足，测试被跳过（见下方原因）", out[-3000:])
        if r.returncode != 0:
            return CheckResult(False, "行为测试未通过", out[-4000:])
        return CheckResult(True, "行为测试通过", summary)

    def check(self, verbose: bool = True) -> CheckResult:
        result = self.build()
        if not result:
            return result
        result = self.probe()
        if not result:
            return result

        # Rustlings semantics: passing is not enough, the learner removes the marker to move on
        content = self.exercise.path.read_text(encoding="utf-8")
        for marker in self.config.incomplete_markers:
            if f"{self.config.comment_prefix} {marker}" in content:
                return CheckResult(
                    False,
                    f"编译和测试都通过了！删除 '{self.config.comment_prefix} {marker}' 这一行以进入下一题",
                    result.details,
                )
        return result


def get_checker(exercise: Exercise, config: ProjectConfig) -> CheckerBase:
    """Factory function to get the appropriate checker."""
    if config.validation_mode == ValidationMode.TEST_FILE:
        return TestFileChecker(exercise, config)
    elif config.validation_mode == ValidationMode.VERIFY_FUNC:
        return VerifyFuncChecker(exercise, config)
    elif config.validation_mode == ValidationMode.COMPILE_AND_RUN:
        return CompileAndRunChecker(exercise, config)
    elif config.validation_mode == ValidationMode.BUILD_AND_PROBE:
        return BuildAndProbeChecker(exercise, config)
    else:
        raise ValueError(f"Unknown validation mode: {config.validation_mode}")
