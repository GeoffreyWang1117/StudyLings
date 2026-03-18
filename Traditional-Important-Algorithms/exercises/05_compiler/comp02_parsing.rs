// comp02_parsing.rs
//
// Parsing is the process of analyzing a sequence of tokens to determine
// their grammatical structure according to a formal grammar. A recursive
// descent parser is a top-down parser built from mutually recursive functions.
//
// Your task: Implement a recursive descent parser for simple arithmetic expressions.
//
// Grammar:
//   expression → term (('+' | '-') term)*
//   term       → factor (('*' | '/') factor)*
//   factor     → NUMBER | '(' expression ')'

// I AM NOT DONE

use std::fmt;

#[derive(Debug, Clone, PartialEq)]
pub enum Token {
    Number(f64),
    Plus,
    Minus,
    Star,
    Slash,
    LeftParen,
    RightParen,
    Eof,
}

#[derive(Debug, Clone, PartialEq)]
pub enum Expr {
    Number(f64),
    Binary {
        op: BinaryOp,
        left: Box<Expr>,
        right: Box<Expr>,
    },
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum BinaryOp {
    Add,
    Sub,
    Mul,
    Div,
}

impl fmt::Display for Expr {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            Expr::Number(n) => write!(f, "{}", n),
            Expr::Binary { op, left, right } => {
                write!(f, "({} {:?} {})", left, op, right)
            }
        }
    }
}

pub struct Parser {
    tokens: Vec<Token>,
    position: usize,
}

impl Parser {
    pub fn new(tokens: Vec<Token>) -> Self {
        Self {
            tokens,
            position: 0,
        }
    }

    fn current_token(&self) -> &Token {
        if self.position < self.tokens.len() {
            &self.tokens[self.position]
        } else {
            &Token::Eof
        }
    }

    fn advance(&mut self) {
        if self.position < self.tokens.len() {
            self.position += 1;
        }
    }

    fn expect(&mut self, expected: Token) -> Result<(), String> {
        // TODO: Check if current token matches expected token
        // If yes, advance and return Ok(())
        // If no, return Err with message
        todo!()
    }

    pub fn parse(&mut self) -> Result<Expr, String> {
        // TODO: Parse the token stream and return an AST
        // Start by calling parse_expression()
        // After parsing, verify we reached EOF
        todo!()
    }

    fn parse_expression(&mut self) -> Result<Expr, String> {
        // TODO: Parse expression → term (('+' | '-') term)*
        // 1. Parse the first term
        // 2. While current token is + or -, parse another term and build Binary node
        // 3. Return the resulting expression
        todo!()
    }

    fn parse_term(&mut self) -> Result<Expr, String> {
        // TODO: Parse term → factor (('*' | '/') factor)*
        // Similar structure to parse_expression but for * and /
        todo!()
    }

    fn parse_factor(&mut self) -> Result<Expr, String> {
        // TODO: Parse factor → NUMBER | '(' expression ')'
        // If current token is a number, return Number node
        // If current token is '(', parse expression and expect ')'
        // Otherwise, return error
        todo!()
    }
}

pub fn eval(expr: &Expr) -> f64 {
    // Helper function to evaluate the AST
    match expr {
        Expr::Number(n) => *n,
        Expr::Binary { op, left, right } => {
            let l = eval(left);
            let r = eval(right);
            match op {
                BinaryOp::Add => l + r,
                BinaryOp::Sub => l - r,
                BinaryOp::Mul => l * r,
                BinaryOp::Div => l / r,
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_simple_number() {
        let tokens = vec![Token::Number(42.0), Token::Eof];
        let mut parser = Parser::new(tokens);
        let ast = parser.parse().unwrap();

        assert_eq!(ast, Expr::Number(42.0));
        assert_eq!(eval(&ast), 42.0);
    }

    #[test]
    fn test_addition() {
        let tokens = vec![
            Token::Number(10.0),
            Token::Plus,
            Token::Number(20.0),
            Token::Eof,
        ];
        let mut parser = Parser::new(tokens);
        let ast = parser.parse().unwrap();

        assert_eq!(eval(&ast), 30.0);
    }

    #[test]
    fn test_subtraction() {
        let tokens = vec![
            Token::Number(50.0),
            Token::Minus,
            Token::Number(20.0),
            Token::Eof,
        ];
        let mut parser = Parser::new(tokens);
        let ast = parser.parse().unwrap();

        assert_eq!(eval(&ast), 30.0);
    }

    #[test]
    fn test_multiplication() {
        let tokens = vec![
            Token::Number(5.0),
            Token::Star,
            Token::Number(6.0),
            Token::Eof,
        ];
        let mut parser = Parser::new(tokens);
        let ast = parser.parse().unwrap();

        assert_eq!(eval(&ast), 30.0);
    }

    #[test]
    fn test_division() {
        let tokens = vec![
            Token::Number(60.0),
            Token::Slash,
            Token::Number(2.0),
            Token::Eof,
        ];
        let mut parser = Parser::new(tokens);
        let ast = parser.parse().unwrap();

        assert_eq!(eval(&ast), 30.0);
    }

    #[test]
    fn test_operator_precedence() {
        // 2 + 3 * 4 should be 14, not 20
        let tokens = vec![
            Token::Number(2.0),
            Token::Plus,
            Token::Number(3.0),
            Token::Star,
            Token::Number(4.0),
            Token::Eof,
        ];
        let mut parser = Parser::new(tokens);
        let ast = parser.parse().unwrap();

        assert_eq!(eval(&ast), 14.0);
    }

    #[test]
    fn test_parentheses() {
        // (2 + 3) * 4 should be 20
        let tokens = vec![
            Token::LeftParen,
            Token::Number(2.0),
            Token::Plus,
            Token::Number(3.0),
            Token::RightParen,
            Token::Star,
            Token::Number(4.0),
            Token::Eof,
        ];
        let mut parser = Parser::new(tokens);
        let ast = parser.parse().unwrap();

        assert_eq!(eval(&ast), 20.0);
    }

    #[test]
    fn test_nested_parentheses() {
        // ((10 + 5) * 2) / 3 should be 10
        let tokens = vec![
            Token::LeftParen,
            Token::LeftParen,
            Token::Number(10.0),
            Token::Plus,
            Token::Number(5.0),
            Token::RightParen,
            Token::Star,
            Token::Number(2.0),
            Token::RightParen,
            Token::Slash,
            Token::Number(3.0),
            Token::Eof,
        ];
        let mut parser = Parser::new(tokens);
        let ast = parser.parse().unwrap();

        assert_eq!(eval(&ast), 10.0);
    }

    #[test]
    fn test_complex_expression() {
        // 10 + 20 * 30 - 40 / 2 should be 10 + 600 - 20 = 590
        let tokens = vec![
            Token::Number(10.0),
            Token::Plus,
            Token::Number(20.0),
            Token::Star,
            Token::Number(30.0),
            Token::Minus,
            Token::Number(40.0),
            Token::Slash,
            Token::Number(2.0),
            Token::Eof,
        ];
        let mut parser = Parser::new(tokens);
        let ast = parser.parse().unwrap();

        assert_eq!(eval(&ast), 590.0);
    }

    #[test]
    fn test_left_associativity() {
        // 10 - 5 - 2 should be (10 - 5) - 2 = 3, not 10 - (5 - 2) = 7
        let tokens = vec![
            Token::Number(10.0),
            Token::Minus,
            Token::Number(5.0),
            Token::Minus,
            Token::Number(2.0),
            Token::Eof,
        ];
        let mut parser = Parser::new(tokens);
        let ast = parser.parse().unwrap();

        assert_eq!(eval(&ast), 3.0);
    }
}
