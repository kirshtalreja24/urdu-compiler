"""
Lexical Analyzer (Scanner)
==========================
This module implements a DFA-based lexical analyzer that tokenizes source code.
It recognizes keywords, identifiers, numbers, operators, and punctuation.

DFA States:
- START: Initial state
- IDENTIFIER: Reading identifier/keyword
- NUMBER: Reading integer or float
- STRING: Reading string literal
- OPERATOR: Reading operator
- COMMENT: Reading comment
"""

import re
from enum import Enum
from typing import List, Tuple, Optional


class TokenType(Enum):
    """Token types recognized by the lexical analyzer"""
    # Keywords
    KEYWORD = "KEYWORD"
    # Identifiers
    IDENTIFIER = "IDENTIFIER"
    # Literals
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    STRING = "STRING"
    # Operators
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"
    ASSIGN = "ASSIGN"
    EQUAL = "EQUAL"
    NOT_EQUAL = "NOT_EQUAL"
    LESS = "LESS"
    LESS_EQUAL = "LESS_EQUAL"
    GREATER = "GREATER"
    GREATER_EQUAL = "GREATER_EQUAL"
    AND = "AND"
    OR = "OR"
    NOT = "NOT"
    # Punctuation
    SEMICOLON = "SEMICOLON"
    COMMA = "COMMA"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    LBRACKET = "LBRACKET"
    RBRACKET = "RBRACKET"
    # Special
    EOF = "EOF"
    ERROR = "ERROR"


class Token:
    """Represents a token with type, value, line, and column"""
    
    def __init__(self, token_type: TokenType, value: str, line: int, column: int):
        self.type = token_type
        self.value = value
        self.line = line
        self.column = column
    
    def __repr__(self):
        return f"Token({self.type.value}, '{self.value}', line={self.line}, col={self.column})"


class LexicalAnalyzer:
    """
    DFA-based Lexical Analyzer
    
    Transition Table (simplified):
    State | Input          | Next State
    ------|----------------|------------
    START | letter         | IDENTIFIER
    START | digit          | NUMBER
    START | "              | STRING
    START | operator       | OPERATOR
    START | whitespace     | START
    START | comment_start  | COMMENT
    """
    
    # Keywords of the language
    KEYWORDS = {
        'Adad', 'TairtaAdad', 'Lafz', 'SahiGhalat',
        'Agar', 'Warna', 'JabTak', 'Dubara',
        'Wapas', 'Kaam', 'Mutaghayyar',
        'Sahi', 'Ghalat', 'Dikhao'
    }
    
    # Operator patterns (order matters - longer patterns first)
    OPERATORS = {
        '==': TokenType.EQUAL,
        '!=': TokenType.NOT_EQUAL,
        '<=': TokenType.LESS_EQUAL,
        '>=': TokenType.GREATER_EQUAL,
        '&&': TokenType.AND,
        '||': TokenType.OR,
        '=': TokenType.ASSIGN,
        '+': TokenType.PLUS,
        '-': TokenType.MINUS,
        '*': TokenType.MULTIPLY,
        '/': TokenType.DIVIDE,
        '<': TokenType.LESS,
        '>': TokenType.GREATER,
        '!': TokenType.NOT,
    }
    
    def __init__(self, source_code: str):
        self.source_code = source_code
        self.tokens: List[Token] = []
        self.current_pos = 0
        self.current_line = 1
        self.current_column = 1
        self.errors: List[str] = []
    
    def peek(self, offset: int = 0) -> Optional[str]:
        """Peek at character at current position + offset"""
        pos = self.current_pos + offset
        if pos >= len(self.source_code):
            return None
        return self.source_code[pos]
    
    def advance(self) -> Optional[str]:
        """Advance position and return current character"""
        if self.current_pos >= len(self.source_code):
            return None
        
        char = self.source_code[self.current_pos]
        self.current_pos += 1
        
        if char == '\n':
            self.current_line += 1
            self.current_column = 1
        else:
            self.current_column += 1
        
        return char
    
    def skip_whitespace(self):
        """Skip whitespace characters"""
        while self.current_pos < len(self.source_code):
            char = self.source_code[self.current_pos]
            if char in ' \t\n\r':
                self.advance()
            else:
                break
    
    def skip_comment(self):
        """Skip single-line comments (//)"""
        while self.current_pos < len(self.source_code):
            char = self.advance()
            if char == '\n' or char is None:
                break
    
    def read_identifier(self) -> str:
        """Read identifier or keyword (DFA: START -> IDENTIFIER)"""
        start_pos = self.current_pos
        while self.current_pos < len(self.source_code):
            char = self.peek()
            if char and (char.isalnum() or char == '_'):
                self.advance()
            else:
                break
        return self.source_code[start_pos:self.current_pos]
    
    def read_number(self) -> Tuple[str, TokenType]:
        """Read number (DFA: START -> NUMBER)"""
        start_pos = self.current_pos
        is_float = False
        
        # Read integer part
        while self.current_pos < len(self.source_code):
            char = self.peek()
            if char and char.isdigit():
                self.advance()
            else:
                break
        
        # Check for decimal point
        if self.peek() == '.':
            self.advance()
            is_float = True
            # Read fractional part
            while self.current_pos < len(self.source_code):
                char = self.peek()
                if char and char.isdigit():
                    self.advance()
                else:
                    break
        
        value = self.source_code[start_pos:self.current_pos]
        token_type = TokenType.FLOAT if is_float else TokenType.INTEGER
        return value, token_type
    
    def read_string(self) -> str:
        """Read string literal (DFA: START -> STRING)"""
        start_pos = self.current_pos
        self.advance()  # Skip opening quote
        
        while self.current_pos < len(self.source_code):
            char = self.advance()
            if char == '"':
                break
            elif char == '\n' or char is None:
                self.errors.append(f"Unterminated string at line {self.current_line}")
                break
        
        return self.source_code[start_pos:self.current_pos]
    
    def tokenize(self) -> List[Token]:
        """
        Main tokenization function - implements DFA transitions
        """
        self.tokens = []
        self.current_pos = 0
        self.current_line = 1
        self.current_column = 1
        self.errors = []
        
        while self.current_pos < len(self.source_code):
            self.skip_whitespace()
            
            if self.current_pos >= len(self.source_code):
                break
            
            char = self.peek()
            line = self.current_line
            column = self.current_column
            
            # Handle comments
            if char == '/' and self.peek(1) == '/':
                self.skip_comment()
                continue
            
            # Handle identifiers and keywords (DFA: letter -> IDENTIFIER)
            if char.isalpha() or char == '_':
                value = self.read_identifier()
                if value in self.KEYWORDS:
                    token_type = TokenType.KEYWORD
                else:
                    token_type = TokenType.IDENTIFIER
                self.tokens.append(Token(token_type, value, line, column))
                continue
            
            # Handle numbers (DFA: digit -> NUMBER)
            if char.isdigit():
                value, token_type = self.read_number()
                self.tokens.append(Token(token_type, value, line, column))
                continue
            
            # Handle string literals (DFA: " -> STRING)
            if char == '"':
                value = self.read_string()
                self.tokens.append(Token(TokenType.STRING, value, line, column))
                continue
            
            # Handle operators and punctuation
            if char in ';':
                self.advance()
                self.tokens.append(Token(TokenType.SEMICOLON, char, line, column))
                continue
            
            if char == ',':
                self.advance()
                self.tokens.append(Token(TokenType.COMMA, char, line, column))
                continue
            
            if char == '(':
                self.advance()
                self.tokens.append(Token(TokenType.LPAREN, char, line, column))
                continue
            
            if char == ')':
                self.advance()
                self.tokens.append(Token(TokenType.RPAREN, char, line, column))
                continue
            
            if char == '{':
                self.advance()
                self.tokens.append(Token(TokenType.LBRACE, char, line, column))
                continue
            
            if char == '}':
                self.advance()
                self.tokens.append(Token(TokenType.RBRACE, char, line, column))
                continue
            
            if char == '[':
                self.advance()
                self.tokens.append(Token(TokenType.LBRACKET, char, line, column))
                continue
            
            if char == ']':
                self.advance()
                self.tokens.append(Token(TokenType.RBRACKET, char, line, column))
                continue
            
            # Handle operators (check longer patterns first)
            matched = False
            for op, token_type in self.OPERATORS.items():
                if self.source_code[self.current_pos:].startswith(op):
                    self.current_pos += len(op)
                    self.current_column += len(op)
                    self.tokens.append(Token(token_type, op, line, column))
                    matched = True
                    break
            
            if not matched:
                # Unknown character
                self.advance()
                self.errors.append(f"Unknown character '{char}' at line {line}, column {column}")
                self.tokens.append(Token(TokenType.ERROR, char, line, column))
        
        # Add EOF token
        self.tokens.append(Token(TokenType.EOF, "", self.current_line, self.current_column))
        
        return self.tokens
    
    def get_tokens(self) -> List[Token]:
        """Get list of tokens"""
        return self.tokens
    
    def get_errors(self) -> List[str]:
        """Get list of lexical errors"""
        return self.errors

