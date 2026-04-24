"""
Syntax Analyzer (Parser)
========================
This module implements a recursive descent parser that builds parse trees.
It uses the tokens from the lexical analyzer to construct an Abstract Syntax Tree (AST).

Grammar (simplified):
    program -> statement_list
    statement_list -> statement statement_list | ε
    statement -> declaration | assignment | if_statement | while_statement | print_statement
    declaration -> type IDENTIFIER '=' expression ';'
    assignment -> IDENTIFIER '=' expression ';'
    if_statement -> 'if' '(' expression ')' '{' statement_list '}' ('else' '{' statement_list '}')?
    while_statement -> 'while' '(' expression ')' '{' statement_list '}'
    print_statement -> 'print' '(' expression ')' ';'
    expression -> logical_or
    logical_or -> logical_and ('||' logical_and)*
    logical_and -> equality ('&&' equality)*
    equality -> comparison (('==' | '!=') comparison)*
    comparison -> term (('<' | '>' | '<=' | '>=') term)*
    term -> factor (('+' | '-') factor)*
    factor -> unary (('*' | '/') unary)*
    unary -> ('!' | '-')? primary
    primary -> IDENTIFIER | INTEGER | FLOAT | STRING | '(' expression ')'
"""

from typing import Optional, List, Dict, Any
from lexical_analyzer import Token, TokenType, LexicalAnalyzer


class ASTNode:
    """Base class for AST nodes"""
    
    def __init__(self, node_type: str, children: List['ASTNode'] = None, value: Any = None, token: Token = None):
        self.node_type = node_type
        self.children = children or []
        self.value = value
        self.token = token  # Reference to original token
    
    def __repr__(self):
        if self.value is not None:
            return f"{self.node_type}({self.value})"
        return f"{self.node_type}({len(self.children)} children)"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert AST node to dictionary for visualization"""
        result = {
            'type': self.node_type,
            'value': self.value,
        }
        if self.token:
            result['token'] = {
                'type': self.token.type.value,
                'value': self.token.value,
                'line': self.token.line
            }
        if self.children:
            result['children'] = [child.to_dict() for child in self.children]
        return result


class SyntaxAnalyzer:
    """
    Recursive Descent Parser
    
    Implements top-down parsing with recursive descent.
    Builds parse tree (AST) from tokens.
    """
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current_index = 0
        self.errors: List[str] = []
        self.ast: Optional[ASTNode] = None
    
    def current_token(self) -> Optional[Token]:
        """Get current token"""
        if self.current_index < len(self.tokens):
            return self.tokens[self.current_index]
        return None
    
    def peek_token(self, offset: int = 1) -> Optional[Token]:
        """Peek at token ahead"""
        idx = self.current_index + offset
        if idx < len(self.tokens):
            return self.tokens[idx]
        return None
    
    def advance(self) -> Optional[Token]:
        """Advance to next token"""
        if self.current_index < len(self.tokens):
            token = self.tokens[self.current_index]
            self.current_index += 1
            return token
        return None
    
    def expect(self, token_type: TokenType, error_msg: str = None) -> Optional[Token]:
        """Expect a specific token type, return it or report error"""
        token = self.current_token()
        if token and token.type == token_type:
            return self.advance()
        else:
            msg = error_msg or f"Expected {token_type.value}, got {token.type.value if token else 'EOF'}"
            self.errors.append(f"{msg} at line {token.line if token else 'unknown'}")
            return None
    
    def parse(self) -> Optional[ASTNode]:
        """Main parse function - entry point"""
        self.current_index = 0
        self.errors = []
        self.ast = self.parse_program()
        return self.ast
    
    def parse_program(self) -> ASTNode:
        """program -> statement_list"""
        statements = self.parse_statement_list()
        return ASTNode('PROGRAM', statements)
    
    def parse_statement_list(self) -> List[ASTNode]:
        """statement_list -> statement statement_list | ε"""
        statements = []
        while self.current_token() and self.current_token().type != TokenType.EOF:
            if self.current_token().type == TokenType.RBRACE:
                break  # End of block
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            else:
                break
        return statements
    
    def parse_statement(self) -> Optional[ASTNode]:
        """statement -> declaration | assignment | if_statement | while_statement | print_statement"""
        token = self.current_token()
        if not token:
            return None
        
        # Check for keyword statements
        if token.type == TokenType.KEYWORD:
            if token.value == 'Agar':
                return self.parse_if_statement()
            elif token.value == 'JabTak':
                return self.parse_while_statement()
            elif token.value == 'Dikhao':
                return self.parse_print_statement()
            elif token.value in ['Adad', 'TairtaAdad', 'Lafz', 'SahiGhalat', 'Mutaghayyar']:
                return self.parse_declaration()
        
        # Assignment statement
        if token.type == TokenType.IDENTIFIER:
            return self.parse_assignment()
        
        self.errors.append(f"Unexpected token {token.value} at line {token.line}")
        return None
    
    def parse_declaration(self) -> Optional[ASTNode]:
        """declaration -> type IDENTIFIER '=' expression ';'"""
        type_token = self.expect(TokenType.KEYWORD, "Expected type keyword")
        if not type_token:
            return None
        
        var_name = self.expect(TokenType.IDENTIFIER, "Expected identifier")
        if not var_name:
            return None
        
        self.expect(TokenType.ASSIGN, "Expected '='")
        
        expr = self.parse_expression()
        if not expr:
            return None
        
        self.expect(TokenType.SEMICOLON, "Expected ';'")
        
        return ASTNode('DECLARATION', [
            ASTNode('TYPE', value=type_token.value, token=type_token),
            ASTNode('IDENTIFIER', value=var_name.value, token=var_name),
            expr
        ])
    
    def parse_assignment(self) -> Optional[ASTNode]:
        """assignment -> IDENTIFIER '=' expression ';'"""
        var_name = self.expect(TokenType.IDENTIFIER, "Expected identifier")
        if not var_name:
            return None
        
        self.expect(TokenType.ASSIGN, "Expected '='")
        
        expr = self.parse_expression()
        if not expr:
            return None
        
        self.expect(TokenType.SEMICOLON, "Expected ';'")
        
        return ASTNode('ASSIGNMENT', [
            ASTNode('IDENTIFIER', value=var_name.value, token=var_name),
            expr
        ])
    
    def parse_if_statement(self) -> Optional[ASTNode]:
        """if_statement -> 'if' '(' expression ')' '{' statement_list '}' ('else' '{' statement_list '}')?"""
        self.expect(TokenType.KEYWORD, "Expected 'Agar'")
        self.expect(TokenType.LPAREN, "Expected '('")
        
        condition = self.parse_expression()
        if not condition:
            return None
        
        self.expect(TokenType.RPAREN, "Expected ')'")
        self.expect(TokenType.LBRACE, "Expected '{'")
        
        then_block = self.parse_statement_list()
        self.expect(TokenType.RBRACE, "Expected '}'")
        
        else_block = None
        if self.current_token() and self.current_token().type == TokenType.KEYWORD and self.current_token().value == 'Warna':
            self.advance()  # Skip 'else'
            self.expect(TokenType.LBRACE, "Expected '{'")
            else_block = self.parse_statement_list()
            self.expect(TokenType.RBRACE, "Expected '}'")
        
        children = [condition, ASTNode('THEN_BLOCK', then_block)]
        if else_block:
            children.append(ASTNode('ELSE_BLOCK', else_block))
        
        return ASTNode('IF_STATEMENT', children)
    
    def parse_while_statement(self) -> Optional[ASTNode]:
        """while_statement -> 'while' '(' expression ')' '{' statement_list '}'"""
        self.expect(TokenType.KEYWORD, "Expected 'JabTak'")
        self.expect(TokenType.LPAREN, "Expected '('")
        
        condition = self.parse_expression()
        if not condition:
            return None
        
        self.expect(TokenType.RPAREN, "Expected ')'")
        self.expect(TokenType.LBRACE, "Expected '{'")
        
        body = self.parse_statement_list()
        self.expect(TokenType.RBRACE, "Expected '}'")
        
        return ASTNode('WHILE_STATEMENT', [
            condition,
            ASTNode('BODY', body)
        ])
    
    def parse_print_statement(self) -> Optional[ASTNode]:
        """print_statement -> 'print' '(' expression ')' ';'"""
        self.expect(TokenType.KEYWORD, "Expected 'Dikhao'")
        self.expect(TokenType.LPAREN, "Expected '('")
        
        expr = self.parse_expression()
        if not expr:
            return None
        
        self.expect(TokenType.RPAREN, "Expected ')'")
        self.expect(TokenType.SEMICOLON, "Expected ';'")
        
        return ASTNode('PRINT_STATEMENT', [expr])
    
    def parse_expression(self) -> Optional[ASTNode]:
        """expression -> logical_or"""
        return self.parse_logical_or()
    
    def parse_logical_or(self) -> Optional[ASTNode]:
        """logical_or -> logical_and ('||' logical_and)*"""
        left = self.parse_logical_and()
        if not left:
            return None
        
        while self.current_token() and self.current_token().type == TokenType.OR:
            op_token = self.advance()
            right = self.parse_logical_and()
            if right:
                left = ASTNode('BINARY_OP', [left, right], value='||', token=op_token)
            else:
                break
        
        return left
    
    def parse_logical_and(self) -> Optional[ASTNode]:
        """logical_and -> equality ('&&' equality)*"""
        left = self.parse_equality()
        if not left:
            return None
        
        while self.current_token() and self.current_token().type == TokenType.AND:
            op_token = self.advance()
            right = self.parse_equality()
            if right:
                left = ASTNode('BINARY_OP', [left, right], value='&&', token=op_token)
            else:
                break
        
        return left
    
    def parse_equality(self) -> Optional[ASTNode]:
        """equality -> comparison (('==' | '!=') comparison)*"""
        left = self.parse_comparison()
        if not left:
            return None
        
        while self.current_token() and self.current_token().type in [TokenType.EQUAL, TokenType.NOT_EQUAL]:
            op_token = self.advance()
            op_value = op_token.value
            right = self.parse_comparison()
            if right:
                left = ASTNode('BINARY_OP', [left, right], value=op_value, token=op_token)
            else:
                break
        
        return left
    
    def parse_comparison(self) -> Optional[ASTNode]:
        """comparison -> term (('<' | '>' | '<=' | '>=') term)*"""
        left = self.parse_term()
        if not left:
            return None
        
        while self.current_token() and self.current_token().type in [
            TokenType.LESS, TokenType.GREATER, TokenType.LESS_EQUAL, TokenType.GREATER_EQUAL
        ]:
            op_token = self.advance()
            op_value = op_token.value
            right = self.parse_term()
            if right:
                left = ASTNode('BINARY_OP', [left, right], value=op_value, token=op_token)
            else:
                break
        
        return left
    
    def parse_term(self) -> Optional[ASTNode]:
        """term -> factor (('+' | '-') factor)*"""
        left = self.parse_factor()
        if not left:
            return None
        
        while self.current_token() and self.current_token().type in [TokenType.PLUS, TokenType.MINUS]:
            op_token = self.advance()
            op_value = op_token.value
            right = self.parse_factor()
            if right:
                left = ASTNode('BINARY_OP', [left, right], value=op_value, token=op_token)
            else:
                break
        
        return left
    
    def parse_factor(self) -> Optional[ASTNode]:
        """factor -> unary (('*' | '/') unary)*"""
        left = self.parse_unary()
        if not left:
            return None
        
        while self.current_token() and self.current_token().type in [TokenType.MULTIPLY, TokenType.DIVIDE]:
            op_token = self.advance()
            op_value = op_token.value
            right = self.parse_unary()
            if right:
                left = ASTNode('BINARY_OP', [left, right], value=op_value, token=op_token)
            else:
                break
        
        return left
    
    def parse_unary(self) -> Optional[ASTNode]:
        """unary -> ('!' | '-')? primary"""
        token = self.current_token()
        if token and token.type in [TokenType.NOT, TokenType.MINUS]:
            op_token = self.advance()
            operand = self.parse_primary()
            if operand:
                return ASTNode('UNARY_OP', [operand], value=op_token.value, token=op_token)
            return None
        
        return self.parse_primary()
    
    def parse_primary(self) -> Optional[ASTNode]:
        """primary -> IDENTIFIER | INTEGER | FLOAT | STRING | '(' expression ')'"""
        token = self.current_token()
        if not token:
            return None
        
        if token.type == TokenType.IDENTIFIER:
            self.advance()
            return ASTNode('IDENTIFIER', value=token.value, token=token)
        
        if token.type == TokenType.INTEGER:
            self.advance()
            return ASTNode('INTEGER', value=int(token.value), token=token)
        
        if token.type == TokenType.FLOAT:
            self.advance()
            return ASTNode('FLOAT', value=float(token.value), token=token)
        
        if token.type == TokenType.STRING:
            self.advance()
            # Keep quotes for code generator to identify as literal
            value = token.value
            return ASTNode('STRING', value=value, token=token)
        
        if token.type == TokenType.KEYWORD and token.value in ['Sahi', 'Ghalat']:
            self.advance()
            return ASTNode('BOOLEAN', value=(token.value == 'Sahi'), token=token)
        
        if token.type == TokenType.LPAREN:
            self.advance()
            expr = self.parse_expression()
            if expr:
                self.expect(TokenType.RPAREN, "Expected ')'")
                return expr
        
        self.errors.append(f"Unexpected token {token.value} at line {token.line}")
        return None
    
    def get_ast(self) -> Optional[ASTNode]:
        """Get the generated AST"""
        return self.ast
    
    def get_errors(self) -> List[str]:
        """Get list of syntax errors"""
        return self.errors

