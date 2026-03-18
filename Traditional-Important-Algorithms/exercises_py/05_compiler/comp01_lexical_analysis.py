# I AM NOT DONE

"""
comp01_lexical_analysis.py

Lexical analysis (tokenization) is the first phase of compilation where
source code is converted into a sequence of tokens. A token represents
the smallest meaningful unit of the language (keywords, identifiers, operators, etc.).

Your task: Implement a lexer that tokenizes a simple expression language.

The language supports:
- Numbers: 123, 45.6
- Identifiers: x, foo, bar_baz
- Operators: +, -, *, /, =
- Parentheses: (, )
- Whitespace (ignored)
"""

from enum import Enum, auto
from typing import List, Optional
import unittest


class TokenType(Enum):
    """Enumeration of token types."""
    NUMBER = auto()
    IDENTIFIER = auto()
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    EQUAL = auto()
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    EOF = auto()


class Token:
    """Represents a single token in the input."""

    def __init__(self, token_type: TokenType, value=None):
        self.type = token_type
        self.value = value

    def __eq__(self, other):
        if not isinstance(other, Token):
            return False
        return self.type == other.type and self.value == other.value

    def __repr__(self):
        if self.value is not None:
            return f"Token({self.type}, {self.value})"
        return f"Token({self.type})"

    def __str__(self):
        if self.type == TokenType.NUMBER:
            return f"Number({self.value})"
        elif self.type == TokenType.IDENTIFIER:
            return f"Identifier({self.value})"
        elif self.type == TokenType.PLUS:
            return "+"
        elif self.type == TokenType.MINUS:
            return "-"
        elif self.type == TokenType.STAR:
            return "*"
        elif self.type == TokenType.SLASH:
            return "/"
        elif self.type == TokenType.EQUAL:
            return "="
        elif self.type == TokenType.LEFT_PAREN:
            return "("
        elif self.type == TokenType.RIGHT_PAREN:
            return ")"
        elif self.type == TokenType.EOF:
            return "EOF"


class Lexer:
    """Lexical analyzer for tokenizing input strings."""

    def __init__(self, input_str: str):
        """Initialize the lexer with input string."""
        self.input = list(input_str)
        self.position = 0

    def current_char(self) -> Optional[str]:
        """Return the current character or None if at end."""
        if self.position < len(self.input):
            return self.input[self.position]
        return None

    def peek_char(self, offset: int = 1) -> Optional[str]:
        """Look ahead at a character without consuming it."""
        pos = self.position + offset
        if pos < len(self.input):
            return self.input[pos]
        return None

    def advance(self):
        """Move to the next character."""
        self.position += 1

    def skip_whitespace(self):
        """
        TODO: Skip all whitespace characters.

        Hint: Use str.isspace() to check if a character is whitespace.
        Continue advancing while current character is whitespace.
        """
        pass  # TODO: Implement this

    def read_number(self) -> float:
        """
        TODO: Read a number (integer or float).

        Handle digits and decimal point.
        Examples: "123", "45.6", "0.5"

        Algorithm:
        1. Build a string of all consecutive digits
        2. If you encounter a '.', include it and continue with more digits
        3. Convert the final string to a float and return it
        """
        pass  # TODO: Implement this

    def read_identifier(self) -> str:
        """
        TODO: Read an identifier.

        Identifiers start with a letter or underscore
        and can contain letters, digits, and underscores.
        Examples: "x", "foo", "bar_baz", "var123"

        Algorithm:
        1. Build a string while current character is alphanumeric or underscore
        2. Return the accumulated string
        """
        pass  # TODO: Implement this

    def next_token(self) -> Token:
        """
        TODO: Return the next token from the input.

        Steps:
        1. Skip whitespace
        2. Check for EOF
        3. Match single-character tokens (+, -, *, /, =, (, ))
        4. Match numbers (digit or '.')
        5. Match identifiers (letter or '_')
        6. Handle unexpected characters (raise an exception)
        """
        pass  # TODO: Implement this

    def tokenize(self) -> List[Token]:
        """
        TODO: Tokenize the entire input into a list of tokens.

        Keep calling next_token() until EOF is reached.
        Return the list including the EOF token.
        """
        pass  # TODO: Implement this


# Unit Tests
class TestLexer(unittest.TestCase):

    def test_single_tokens(self):
        lexer = Lexer("+ - * / = ( )")
        tokens = lexer.tokenize()

        expected = [
            Token(TokenType.PLUS),
            Token(TokenType.MINUS),
            Token(TokenType.STAR),
            Token(TokenType.SLASH),
            Token(TokenType.EQUAL),
            Token(TokenType.LEFT_PAREN),
            Token(TokenType.RIGHT_PAREN),
            Token(TokenType.EOF),
        ]
        self.assertEqual(tokens, expected)

    def test_numbers(self):
        lexer = Lexer("123 45.6 0.5 99")
        tokens = lexer.tokenize()

        expected = [
            Token(TokenType.NUMBER, 123.0),
            Token(TokenType.NUMBER, 45.6),
            Token(TokenType.NUMBER, 0.5),
            Token(TokenType.NUMBER, 99.0),
            Token(TokenType.EOF),
        ]
        self.assertEqual(tokens, expected)

    def test_identifiers(self):
        lexer = Lexer("x foo bar_baz var123")
        tokens = lexer.tokenize()

        expected = [
            Token(TokenType.IDENTIFIER, "x"),
            Token(TokenType.IDENTIFIER, "foo"),
            Token(TokenType.IDENTIFIER, "bar_baz"),
            Token(TokenType.IDENTIFIER, "var123"),
            Token(TokenType.EOF),
        ]
        self.assertEqual(tokens, expected)

    def test_expression(self):
        lexer = Lexer("x = 10 + 20 * 30")
        tokens = lexer.tokenize()

        expected = [
            Token(TokenType.IDENTIFIER, "x"),
            Token(TokenType.EQUAL),
            Token(TokenType.NUMBER, 10.0),
            Token(TokenType.PLUS),
            Token(TokenType.NUMBER, 20.0),
            Token(TokenType.STAR),
            Token(TokenType.NUMBER, 30.0),
            Token(TokenType.EOF),
        ]
        self.assertEqual(tokens, expected)

    def test_complex_expression(self):
        lexer = Lexer("result = (a + b) * (c - d) / 2.5")
        tokens = lexer.tokenize()

        expected = [
            Token(TokenType.IDENTIFIER, "result"),
            Token(TokenType.EQUAL),
            Token(TokenType.LEFT_PAREN),
            Token(TokenType.IDENTIFIER, "a"),
            Token(TokenType.PLUS),
            Token(TokenType.IDENTIFIER, "b"),
            Token(TokenType.RIGHT_PAREN),
            Token(TokenType.STAR),
            Token(TokenType.LEFT_PAREN),
            Token(TokenType.IDENTIFIER, "c"),
            Token(TokenType.MINUS),
            Token(TokenType.IDENTIFIER, "d"),
            Token(TokenType.RIGHT_PAREN),
            Token(TokenType.SLASH),
            Token(TokenType.NUMBER, 2.5),
            Token(TokenType.EOF),
        ]
        self.assertEqual(tokens, expected)

    def test_no_whitespace(self):
        lexer = Lexer("x=10+20")
        tokens = lexer.tokenize()

        expected = [
            Token(TokenType.IDENTIFIER, "x"),
            Token(TokenType.EQUAL),
            Token(TokenType.NUMBER, 10.0),
            Token(TokenType.PLUS),
            Token(TokenType.NUMBER, 20.0),
            Token(TokenType.EOF),
        ]
        self.assertEqual(tokens, expected)

    def test_empty_input(self):
        lexer = Lexer("")
        tokens = lexer.tokenize()

        expected = [Token(TokenType.EOF)]
        self.assertEqual(tokens, expected)

    def test_whitespace_only(self):
        lexer = Lexer("   \t\n  ")
        tokens = lexer.tokenize()

        expected = [Token(TokenType.EOF)]
        self.assertEqual(tokens, expected)


if __name__ == '__main__':
    unittest.main()
