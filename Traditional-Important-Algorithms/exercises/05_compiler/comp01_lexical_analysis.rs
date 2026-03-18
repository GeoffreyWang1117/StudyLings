// comp01_lexical_analysis.rs
//
// Lexical analysis (tokenization) is the first phase of compilation where
// source code is converted into a sequence of tokens. A token represents
// the smallest meaningful unit of the language (keywords, identifiers, operators, etc.).
//
// Your task: Implement a lexer that tokenizes a simple expression language.
//
// The language supports:
// - Numbers: 123, 45.6
// - Identifiers: x, foo, bar_baz
// - Operators: +, -, *, /, =
// - Parentheses: (, )
// - Whitespace (ignored)

// I AM NOT DONE

use std::fmt;

#[derive(Debug, Clone, PartialEq)]
pub enum Token {
    Number(f64),
    Identifier(String),
    Plus,
    Minus,
    Star,
    Slash,
    Equal,
    LeftParen,
    RightParen,
    Eof,
}

impl fmt::Display for Token {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            Token::Number(n) => write!(f, "Number({})", n),
            Token::Identifier(s) => write!(f, "Identifier({})", s),
            Token::Plus => write!(f, "+"),
            Token::Minus => write!(f, "-"),
            Token::Star => write!(f, "*"),
            Token::Slash => write!(f, "/"),
            Token::Equal => write!(f, "="),
            Token::LeftParen => write!(f, "("),
            Token::RightParen => write!(f, ")"),
            Token::Eof => write!(f, "EOF"),
        }
    }
}

pub struct Lexer {
    input: Vec<char>,
    position: usize,
}

impl Lexer {
    pub fn new(input: &str) -> Self {
        Self {
            input: input.chars().collect(),
            position: 0,
        }
    }

    fn current_char(&self) -> Option<char> {
        if self.position < self.input.len() {
            Some(self.input[self.position])
        } else {
            None
        }
    }

    fn peek_char(&self, offset: usize) -> Option<char> {
        let pos = self.position + offset;
        if pos < self.input.len() {
            Some(self.input[pos])
        } else {
            None
        }
    }

    fn advance(&mut self) {
        self.position += 1;
    }

    fn skip_whitespace(&mut self) {
        // TODO: Skip all whitespace characters
        // Hint: Use char::is_whitespace()
        todo!()
    }

    fn read_number(&mut self) -> f64 {
        // TODO: Read a number (integer or float)
        // Handle digits and decimal point
        // Examples: "123", "45.6", "0.5"
        todo!()
    }

    fn read_identifier(&mut self) -> String {
        // TODO: Read an identifier
        // Identifiers start with a letter or underscore
        // and can contain letters, digits, and underscores
        // Examples: "x", "foo", "bar_baz", "var123"
        todo!()
    }

    pub fn next_token(&mut self) -> Token {
        // TODO: Return the next token from the input
        // Steps:
        // 1. Skip whitespace
        // 2. Check for EOF
        // 3. Match single-character tokens (+, -, *, /, =, (, ))
        // 4. Match numbers (digit or '.')
        // 5. Match identifiers (letter or '_')
        // 6. Handle unexpected characters (panic or return error token)
        todo!()
    }

    pub fn tokenize(&mut self) -> Vec<Token> {
        // TODO: Tokenize the entire input into a vector of tokens
        // Keep calling next_token() until EOF
        todo!()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_single_tokens() {
        let mut lexer = Lexer::new("+ - * / = ( )");
        let tokens = lexer.tokenize();

        assert_eq!(tokens, vec![
            Token::Plus,
            Token::Minus,
            Token::Star,
            Token::Slash,
            Token::Equal,
            Token::LeftParen,
            Token::RightParen,
            Token::Eof,
        ]);
    }

    #[test]
    fn test_numbers() {
        let mut lexer = Lexer::new("123 45.6 0.5 99");
        let tokens = lexer.tokenize();

        assert_eq!(tokens, vec![
            Token::Number(123.0),
            Token::Number(45.6),
            Token::Number(0.5),
            Token::Number(99.0),
            Token::Eof,
        ]);
    }

    #[test]
    fn test_identifiers() {
        let mut lexer = Lexer::new("x foo bar_baz var123");
        let tokens = lexer.tokenize();

        assert_eq!(tokens, vec![
            Token::Identifier("x".to_string()),
            Token::Identifier("foo".to_string()),
            Token::Identifier("bar_baz".to_string()),
            Token::Identifier("var123".to_string()),
            Token::Eof,
        ]);
    }

    #[test]
    fn test_expression() {
        let mut lexer = Lexer::new("x = 10 + 20 * 30");
        let tokens = lexer.tokenize();

        assert_eq!(tokens, vec![
            Token::Identifier("x".to_string()),
            Token::Equal,
            Token::Number(10.0),
            Token::Plus,
            Token::Number(20.0),
            Token::Star,
            Token::Number(30.0),
            Token::Eof,
        ]);
    }

    #[test]
    fn test_complex_expression() {
        let mut lexer = Lexer::new("result = (a + b) * (c - d) / 2.5");
        let tokens = lexer.tokenize();

        assert_eq!(tokens, vec![
            Token::Identifier("result".to_string()),
            Token::Equal,
            Token::LeftParen,
            Token::Identifier("a".to_string()),
            Token::Plus,
            Token::Identifier("b".to_string()),
            Token::RightParen,
            Token::Star,
            Token::LeftParen,
            Token::Identifier("c".to_string()),
            Token::Minus,
            Token::Identifier("d".to_string()),
            Token::RightParen,
            Token::Slash,
            Token::Number(2.5),
            Token::Eof,
        ]);
    }

    #[test]
    fn test_no_whitespace() {
        let mut lexer = Lexer::new("x=10+20");
        let tokens = lexer.tokenize();

        assert_eq!(tokens, vec![
            Token::Identifier("x".to_string()),
            Token::Equal,
            Token::Number(10.0),
            Token::Plus,
            Token::Number(20.0),
            Token::Eof,
        ]);
    }

    #[test]
    fn test_empty_input() {
        let mut lexer = Lexer::new("");
        let tokens = lexer.tokenize();

        assert_eq!(tokens, vec![Token::Eof]);
    }

    #[test]
    fn test_whitespace_only() {
        let mut lexer = Lexer::new("   \t\n  ");
        let tokens = lexer.tokenize();

        assert_eq!(tokens, vec![Token::Eof]);
    }
}
