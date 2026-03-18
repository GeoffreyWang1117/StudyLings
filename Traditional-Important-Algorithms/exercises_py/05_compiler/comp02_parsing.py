# I AM NOT DONE

"""
comp02_parsing.py

Parsing is the process of analyzing a sequence of tokens to determine
their grammatical structure according to a formal grammar. A recursive
descent parser is a top-down parser built from mutually recursive functions.

Your task: Implement a recursive descent parser for simple arithmetic expressions.

Grammar:
  expression → term (('+' | '-') term)*
  term       → factor (('*' | '/') factor)*
  factor     → NUMBER | '(' expression ')'
"""

from enum import Enum, auto
from typing import List, Optional
import unittest


class TokenType(Enum):
    """Token types for the parser."""
    NUMBER = auto()
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    EOF = auto()


class Token:
    """Represents a token."""

    def __init__(self, token_type: TokenType, value=None):
        self.type = token_type
        self.value = value

    def __eq__(self, other):
        if not isinstance(other, Token):
            return False
        return self.type == other.type and self.value == other.value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"


class BinaryOp(Enum):
    """Binary operators."""
    ADD = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()


class Expr:
    """Base class for expression nodes."""
    pass


class Number(Expr):
    """Number literal expression."""

    def __init__(self, value: float):
        self.value = value

    def __eq__(self, other):
        return isinstance(other, Number) and self.value == other.value

    def __repr__(self):
        return f"Number({self.value})"


class Binary(Expr):
    """Binary operation expression."""

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


class Parser:
    """Recursive descent parser for arithmetic expressions."""

    def __init__(self, tokens: List[Token]):
        """Initialize parser with list of tokens."""
        self.tokens = tokens
        self.position = 0

    def current_token(self) -> Token:
        """Get the current token."""
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return Token(TokenType.EOF)

    def advance(self):
        """Move to the next token."""
        if self.position < len(self.tokens):
            self.position += 1

    def expect(self, expected: TokenType) -> None:
        """
        TODO: Check if current token matches expected token.

        If yes, advance and return.
        If no, raise ValueError with an error message.
        """
        pass  # TODO: Implement this

    def parse(self) -> Expr:
        """
        TODO: Parse the token stream and return an AST.

        Steps:
        1. Call parse_expression() to get the result
        2. Verify we reached EOF (current token should be EOF)
        3. If not EOF, raise an error
        4. Return the expression
        """
        pass  # TODO: Implement this

    def parse_expression(self) -> Expr:
        """
        TODO: Parse expression → term (('+' | '-') term)*

        Algorithm:
        1. Parse the first term
        2. While current token is + or -:
           a. Save the operator
           b. Advance past the operator
           c. Parse another term
           d. Create a Binary node with saved operator and both terms
           e. Use this Binary node as the left side for any subsequent operations
        3. Return the resulting expression
        """
        pass  # TODO: Implement this

    def parse_term(self) -> Expr:
        """
        TODO: Parse term → factor (('*' | '/') factor)*

        Similar structure to parse_expression but for * and /.
        """
        pass  # TODO: Implement this

    def parse_factor(self) -> Expr:
        """
        TODO: Parse factor → NUMBER | '(' expression ')'

        Algorithm:
        1. If current token is NUMBER:
           - Create Number node with the value
           - Advance past the number
           - Return the Number node
        2. If current token is LEFT_PAREN:
           - Advance past '('
           - Recursively call parse_expression()
           - Expect and consume ')'
           - Return the expression
        3. Otherwise: raise an error
        """
        pass  # TODO: Implement this


def eval_expr(expr: Expr) -> float:
    """Helper function to evaluate the AST."""
    if isinstance(expr, Number):
        return expr.value
    elif isinstance(expr, Binary):
        left = eval_expr(expr.left)
        right = eval_expr(expr.right)
        if expr.op == BinaryOp.ADD:
            return left + right
        elif expr.op == BinaryOp.SUB:
            return left - right
        elif expr.op == BinaryOp.MUL:
            return left * right
        elif expr.op == BinaryOp.DIV:
            return left / right
    raise ValueError(f"Unknown expression type: {type(expr)}")


# Unit Tests
class TestParser(unittest.TestCase):

    def test_simple_number(self):
        tokens = [Token(TokenType.NUMBER, 42.0), Token(TokenType.EOF)]
        parser = Parser(tokens)
        ast = parser.parse()

        self.assertEqual(ast, Number(42.0))
        self.assertEqual(eval_expr(ast), 42.0)

    def test_addition(self):
        tokens = [
            Token(TokenType.NUMBER, 10.0),
            Token(TokenType.PLUS),
            Token(TokenType.NUMBER, 20.0),
            Token(TokenType.EOF),
        ]
        parser = Parser(tokens)
        ast = parser.parse()

        self.assertEqual(eval_expr(ast), 30.0)

    def test_subtraction(self):
        tokens = [
            Token(TokenType.NUMBER, 50.0),
            Token(TokenType.MINUS),
            Token(TokenType.NUMBER, 20.0),
            Token(TokenType.EOF),
        ]
        parser = Parser(tokens)
        ast = parser.parse()

        self.assertEqual(eval_expr(ast), 30.0)

    def test_multiplication(self):
        tokens = [
            Token(TokenType.NUMBER, 5.0),
            Token(TokenType.STAR),
            Token(TokenType.NUMBER, 6.0),
            Token(TokenType.EOF),
        ]
        parser = Parser(tokens)
        ast = parser.parse()

        self.assertEqual(eval_expr(ast), 30.0)

    def test_division(self):
        tokens = [
            Token(TokenType.NUMBER, 60.0),
            Token(TokenType.SLASH),
            Token(TokenType.NUMBER, 2.0),
            Token(TokenType.EOF),
        ]
        parser = Parser(tokens)
        ast = parser.parse()

        self.assertEqual(eval_expr(ast), 30.0)

    def test_operator_precedence(self):
        # 2 + 3 * 4 should be 14, not 20
        tokens = [
            Token(TokenType.NUMBER, 2.0),
            Token(TokenType.PLUS),
            Token(TokenType.NUMBER, 3.0),
            Token(TokenType.STAR),
            Token(TokenType.NUMBER, 4.0),
            Token(TokenType.EOF),
        ]
        parser = Parser(tokens)
        ast = parser.parse()

        self.assertEqual(eval_expr(ast), 14.0)

    def test_parentheses(self):
        # (2 + 3) * 4 should be 20
        tokens = [
            Token(TokenType.LEFT_PAREN),
            Token(TokenType.NUMBER, 2.0),
            Token(TokenType.PLUS),
            Token(TokenType.NUMBER, 3.0),
            Token(TokenType.RIGHT_PAREN),
            Token(TokenType.STAR),
            Token(TokenType.NUMBER, 4.0),
            Token(TokenType.EOF),
        ]
        parser = Parser(tokens)
        ast = parser.parse()

        self.assertEqual(eval_expr(ast), 20.0)

    def test_nested_parentheses(self):
        # ((10 + 5) * 2) / 3 should be 10
        tokens = [
            Token(TokenType.LEFT_PAREN),
            Token(TokenType.LEFT_PAREN),
            Token(TokenType.NUMBER, 10.0),
            Token(TokenType.PLUS),
            Token(TokenType.NUMBER, 5.0),
            Token(TokenType.RIGHT_PAREN),
            Token(TokenType.STAR),
            Token(TokenType.NUMBER, 2.0),
            Token(TokenType.RIGHT_PAREN),
            Token(TokenType.SLASH),
            Token(TokenType.NUMBER, 3.0),
            Token(TokenType.EOF),
        ]
        parser = Parser(tokens)
        ast = parser.parse()

        self.assertEqual(eval_expr(ast), 10.0)

    def test_complex_expression(self):
        # 10 + 20 * 30 - 40 / 2 should be 10 + 600 - 20 = 590
        tokens = [
            Token(TokenType.NUMBER, 10.0),
            Token(TokenType.PLUS),
            Token(TokenType.NUMBER, 20.0),
            Token(TokenType.STAR),
            Token(TokenType.NUMBER, 30.0),
            Token(TokenType.MINUS),
            Token(TokenType.NUMBER, 40.0),
            Token(TokenType.SLASH),
            Token(TokenType.NUMBER, 2.0),
            Token(TokenType.EOF),
        ]
        parser = Parser(tokens)
        ast = parser.parse()

        self.assertEqual(eval_expr(ast), 590.0)

    def test_left_associativity(self):
        # 10 - 5 - 2 should be (10 - 5) - 2 = 3, not 10 - (5 - 2) = 7
        tokens = [
            Token(TokenType.NUMBER, 10.0),
            Token(TokenType.MINUS),
            Token(TokenType.NUMBER, 5.0),
            Token(TokenType.MINUS),
            Token(TokenType.NUMBER, 2.0),
            Token(TokenType.EOF),
        ]
        parser = Parser(tokens)
        ast = parser.parse()

        self.assertEqual(eval_expr(ast), 3.0)


if __name__ == '__main__':
    unittest.main()
