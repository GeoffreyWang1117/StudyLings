# I AM NOT DONE

"""
comp04_constant_folding.py

Constant folding is a compiler optimization that evaluates constant
expressions at compile time rather than runtime. For example, "2 + 3"
can be replaced with "5" before the program runs.

Your task: Implement constant folding for a simple expression language.

Optimizations to implement:
- Arithmetic: 2 + 3 → 5, 10 * 0 → 0
- Boolean: True and False → False, not True → False
- Algebraic identities: x + 0 → x, x * 1 → x, x * 0 → 0
"""

from enum import Enum, auto
from typing import Union
import unittest


class BinaryOp(Enum):
    """Binary operators."""
    ADD = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()
    EQ = auto()
    LT = auto()
    AND = auto()
    OR = auto()


class UnaryOp(Enum):
    """Unary operators."""
    NEG = auto()
    NOT = auto()


class Expr:
    """Base class for expressions."""
    pass


class Int(Expr):
    """Integer literal."""

    def __init__(self, value: int):
        self.value = value

    def __eq__(self, other):
        return isinstance(other, Int) and self.value == other.value

    def __repr__(self):
        return f"Int({self.value})"


class Bool(Expr):
    """Boolean literal."""

    def __init__(self, value: bool):
        self.value = value

    def __eq__(self, other):
        return isinstance(other, Bool) and self.value == other.value

    def __repr__(self):
        return f"Bool({self.value})"


class Var(Expr):
    """Variable reference."""

    def __init__(self, name: str):
        self.name = name

    def __eq__(self, other):
        return isinstance(other, Var) and self.name == other.name

    def __repr__(self):
        return f"Var({self.name})"


class Binary(Expr):
    """Binary operation."""

    def __init__(self, op: BinaryOp, left: Expr, right: Expr):
        self.op = op
        self.left = left
        self.right = right

    def __eq__(self, other):
        return (isinstance(other, Binary) and
                self.op == other.op and
                self.left == other.left and
                self.right == other.right)

    def __repr__(self):
        return f"Binary({self.op}, {self.left}, {self.right})"


class Unary(Expr):
    """Unary operation."""

    def __init__(self, op: UnaryOp, operand: Expr):
        self.op = op
        self.operand = operand

    def __eq__(self, other):
        return (isinstance(other, Unary) and
                self.op == other.op and
                self.operand == other.operand)

    def __repr__(self):
        return f"Unary({self.op}, {self.operand})"


class If(Expr):
    """If expression."""

    def __init__(self, condition: Expr, then_branch: Expr, else_branch: Expr):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def __eq__(self, other):
        return (isinstance(other, If) and
                self.condition == other.condition and
                self.then_branch == other.then_branch and
                self.else_branch == other.else_branch)

    def __repr__(self):
        return f"If({self.condition}, {self.then_branch}, {self.else_branch})"


class ConstantFolder:
    """Performs constant folding optimization."""

    def fold(self, expr: Expr) -> Expr:
        """
        TODO: Recursively fold constants in the expression.

        Process children first (bottom-up), then try to fold this node.

        Handle:
        - Int, Bool, Var: return as-is
        - Binary: call fold_binary
        - Unary: call fold_unary
        - If: call fold_if
        """
        pass  # TODO: Implement this

    def fold_binary(self, op: BinaryOp, left: Expr, right: Expr) -> Expr:
        """
        TODO: Fold binary operations.

        1. Recursively fold left and right
        2. Try to apply algebraic identities (x + 0, x * 1, etc.)
        3. If both are constants, evaluate
        4. Otherwise, return Binary with folded children
        """
        pass  # TODO: Implement this

    def fold_unary(self, op: UnaryOp, operand: Expr) -> Expr:
        """
        TODO: Fold unary operations.

        1. Recursively fold operand
        2. If operand is constant, evaluate
        3. Otherwise, return Unary with folded operand
        """
        pass  # TODO: Implement this

    def fold_if(self, condition: Expr, then_branch: Expr, else_branch: Expr) -> Expr:
        """
        TODO: Fold if expressions.

        1. Recursively fold all branches
        2. If condition is constant Bool, return the appropriate branch
        3. Otherwise, return If with folded branches
        """
        pass  # TODO: Implement this

    def eval_binary_int(self, op: BinaryOp, left: int, right: int) -> Union[Expr, None]:
        """
        TODO: Evaluate binary operation on two integers.

        Handle: ADD, SUB, MUL, DIV, EQ, LT
        Return Int or Bool result, or None if invalid
        """
        pass  # TODO: Implement this

    def eval_binary_bool(self, op: BinaryOp, left: bool, right: bool) -> Union[Expr, None]:
        """
        TODO: Evaluate binary operation on two booleans.

        Handle: AND, OR, EQ
        Return Bool result, or None if invalid
        """
        pass  # TODO: Implement this

    def eval_unary(self, op: UnaryOp, operand: Expr) -> Union[Expr, None]:
        """
        TODO: Evaluate unary operation.

        Handle: NEG (for Int), NOT (for Bool)
        Return result, or None if invalid
        """
        pass  # TODO: Implement this

    def apply_algebraic_identity(self, op: BinaryOp, left: Expr, right: Expr) -> Union[Expr, None]:
        """
        TODO: Apply algebraic identities.

        Examples:
        - x + 0 → x, 0 + x → x
        - x * 0 → 0, 0 * x → 0
        - x * 1 → x, 1 * x → x
        - x - 0 → x
        - x and True → x, True and x → x
        - x and False → False, False and x → False
        - x or True → True, True or x → True
        - x or False → x, False or x → x

        Return simplified expression or None if no identity applies
        """
        pass  # TODO: Implement this


# Unit Tests
class TestConstantFolding(unittest.TestCase):

    def test_constant_arithmetic(self):
        folder = ConstantFolder()

        # 2 + 3 → 5
        expr = Binary(BinaryOp.ADD, Int(2), Int(3))
        self.assertEqual(folder.fold(expr), Int(5))

        # 10 * 5 → 50
        expr = Binary(BinaryOp.MUL, Int(10), Int(5))
        self.assertEqual(folder.fold(expr), Int(50))

        # 20 - 7 → 13
        expr = Binary(BinaryOp.SUB, Int(20), Int(7))
        self.assertEqual(folder.fold(expr), Int(13))

        # 100 / 4 → 25
        expr = Binary(BinaryOp.DIV, Int(100), Int(4))
        self.assertEqual(folder.fold(expr), Int(25))

    def test_nested_constants(self):
        folder = ConstantFolder()

        # (2 + 3) * 4 → 20
        expr = Binary(BinaryOp.MUL, Binary(BinaryOp.ADD, Int(2), Int(3)), Int(4))
        self.assertEqual(folder.fold(expr), Int(20))

    def test_identity_add_zero(self):
        folder = ConstantFolder()

        # x + 0 → x
        expr = Binary(BinaryOp.ADD, Var("x"), Int(0))
        self.assertEqual(folder.fold(expr), Var("x"))

        # 0 + x → x
        expr = Binary(BinaryOp.ADD, Int(0), Var("x"))
        self.assertEqual(folder.fold(expr), Var("x"))

    def test_identity_mul_zero(self):
        folder = ConstantFolder()

        # x * 0 → 0
        expr = Binary(BinaryOp.MUL, Var("x"), Int(0))
        self.assertEqual(folder.fold(expr), Int(0))

        # 0 * x → 0
        expr = Binary(BinaryOp.MUL, Int(0), Var("x"))
        self.assertEqual(folder.fold(expr), Int(0))

    def test_identity_mul_one(self):
        folder = ConstantFolder()

        # x * 1 → x
        expr = Binary(BinaryOp.MUL, Var("x"), Int(1))
        self.assertEqual(folder.fold(expr), Var("x"))

        # 1 * x → x
        expr = Binary(BinaryOp.MUL, Int(1), Var("x"))
        self.assertEqual(folder.fold(expr), Var("x"))

    def test_identity_sub_zero(self):
        folder = ConstantFolder()

        # x - 0 → x
        expr = Binary(BinaryOp.SUB, Var("x"), Int(0))
        self.assertEqual(folder.fold(expr), Var("x"))

    def test_boolean_constants(self):
        folder = ConstantFolder()

        # True and False → False
        expr = Binary(BinaryOp.AND, Bool(True), Bool(False))
        self.assertEqual(folder.fold(expr), Bool(False))

        # True or False → True
        expr = Binary(BinaryOp.OR, Bool(True), Bool(False))
        self.assertEqual(folder.fold(expr), Bool(True))

    def test_boolean_identities(self):
        folder = ConstantFolder()

        # x and True → x
        expr = Binary(BinaryOp.AND, Var("x"), Bool(True))
        self.assertEqual(folder.fold(expr), Var("x"))

        # x and False → False
        expr = Binary(BinaryOp.AND, Var("x"), Bool(False))
        self.assertEqual(folder.fold(expr), Bool(False))

        # x or True → True
        expr = Binary(BinaryOp.OR, Var("x"), Bool(True))
        self.assertEqual(folder.fold(expr), Bool(True))

        # x or False → x
        expr = Binary(BinaryOp.OR, Var("x"), Bool(False))
        self.assertEqual(folder.fold(expr), Var("x"))

    def test_unary_negation(self):
        folder = ConstantFolder()

        # -5 → -5
        expr = Unary(UnaryOp.NEG, Int(5))
        self.assertEqual(folder.fold(expr), Int(-5))

        # not True → False
        expr = Unary(UnaryOp.NOT, Bool(True))
        self.assertEqual(folder.fold(expr), Bool(False))

        # not False → True
        expr = Unary(UnaryOp.NOT, Bool(False))
        self.assertEqual(folder.fold(expr), Bool(True))

    def test_if_constant_condition(self):
        folder = ConstantFolder()

        # if True then 1 else 2 → 1
        expr = If(Bool(True), Int(1), Int(2))
        self.assertEqual(folder.fold(expr), Int(1))

        # if False then 1 else 2 → 2
        expr = If(Bool(False), Int(1), Int(2))
        self.assertEqual(folder.fold(expr), Int(2))

    def test_partial_folding(self):
        folder = ConstantFolder()

        # (2 + 3) + x → 5 + x
        expr = Binary(BinaryOp.ADD, Binary(BinaryOp.ADD, Int(2), Int(3)), Var("x"))
        expected = Binary(BinaryOp.ADD, Int(5), Var("x"))
        self.assertEqual(folder.fold(expr), expected)

    def test_comparison_folding(self):
        folder = ConstantFolder()

        # 5 == 5 → True
        expr = Binary(BinaryOp.EQ, Int(5), Int(5))
        self.assertEqual(folder.fold(expr), Bool(True))

        # 5 == 6 → False
        expr = Binary(BinaryOp.EQ, Int(5), Int(6))
        self.assertEqual(folder.fold(expr), Bool(False))

        # 3 < 5 → True
        expr = Binary(BinaryOp.LT, Int(3), Int(5))
        self.assertEqual(folder.fold(expr), Bool(True))


if __name__ == '__main__':
    unittest.main()
