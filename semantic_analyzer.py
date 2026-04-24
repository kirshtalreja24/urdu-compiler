"""
Semantic Analyzer
=================
This module performs semantic analysis including:
- Symbol table management
- Scope tracking
- Type checking
- Variable declaration validation
- Use-before-declaration checks

Symbol Table Structure:
    {
        'global': {
            'var_name': {
                'type': 'Adad'|'TairtaAdad'|'Lafz'|'SahiGhalat',
                'declared_at': line_number,
                'scope': 'global'|'local'
            }
        },
        'local_1': { ... },
        ...
    }
"""

from typing import Dict, List, Optional, Any
from lexical_analyzer import TokenType
from syntax_analyzer import ASTNode


class SymbolTable:
    """Manages symbol tables for different scopes"""
    
    def __init__(self):
        self.tables: Dict[str, Dict[str, Dict[str, Any]]] = {
            'global': {}
        }
        self.scope_stack: List[str] = ['global']
        self.scope_counter = 0
    
    def enter_scope(self) -> str:
        """Enter a new local scope"""
        scope_name = f'local_{self.scope_counter}'
        self.scope_counter += 1
        self.tables[scope_name] = {}
        self.scope_stack.append(scope_name)
        return scope_name
    
    def exit_scope(self):
        """Exit current scope"""
        if len(self.scope_stack) > 1:
            self.scope_stack.pop()
    
    def current_scope(self) -> str:
        """Get current scope name"""
        return self.scope_stack[-1]
    
    def declare(self, name: str, var_type: str, line: int) -> bool:
        """
        Declare a variable in current scope
        Returns True if successful, False if already declared
        """
        scope = self.current_scope()
        
        # Check if already declared in current scope
        if name in self.tables[scope]:
            return False
        
        self.tables[scope][name] = {
            'type': var_type,
            'declared_at': line,
            'scope': scope
        }
        return True
    
    def lookup(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Look up variable in current and enclosing scopes
        Returns symbol info or None if not found
        """
        # Search from current scope up to global
        for scope in reversed(self.scope_stack):
            if name in self.tables[scope]:
                return self.tables[scope][name]
        return None
    
    def get_all_symbols(self) -> Dict[str, Dict[str, Dict[str, Any]]]:
        """Get all symbol tables for display"""
        return self.tables.copy()


class SemanticAnalyzer:
    """
    Semantic Analyzer
    
    Performs:
    1. Symbol table construction
    2. Type checking
    3. Scope validation
    4. Use-before-declaration checks
    """
    
    def __init__(self, ast: ASTNode):
        self.ast = ast
        self.symbol_table = SymbolTable()
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    def analyze(self) -> bool:
        """Main analysis function"""
        if not self.ast:
            self.errors.append("No AST to analyze")
            return False
        
        self.errors = []
        self.warnings = []
        self.symbol_table = SymbolTable()
        
        self.analyze_node(self.ast)
        
        return len(self.errors) == 0
    
    def analyze_node(self, node: ASTNode):
        """Recursively analyze AST nodes"""
        if node.node_type == 'PROGRAM':
            for stmt in node.children:
                self.analyze_node(stmt)
        
        elif node.node_type == 'DECLARATION':
            self.analyze_declaration(node)
            # Don't recursively process children - they're already handled in analyze_declaration
        
        elif node.node_type == 'ASSIGNMENT':
            self.analyze_assignment(node)
            # Don't recursively process children - they're already handled in analyze_assignment
        
        elif node.node_type == 'IF_STATEMENT':
            self.analyze_if_statement(node)
            # Don't recursively process children - they're already handled in analyze_if_statement
        
        elif node.node_type == 'WHILE_STATEMENT':
            self.analyze_while_statement(node)
            # Don't recursively process children - they're already handled in analyze_while_statement
        
        elif node.node_type == 'PRINT_STATEMENT':
            self.analyze_print_statement(node)
            # Don't recursively process children - they're already handled in analyze_print_statement
        
        else:
            # For other node types (expressions, etc.), recursively process children
            # These are handled by get_expression_type which is called from analyze methods
            for child in node.children:
                if isinstance(child, ASTNode):
                    self.analyze_node(child)
    
    def analyze_declaration(self, node: ASTNode):
        """Analyze variable declaration"""
        if len(node.children) < 3:
            return
        
        type_node = node.children[0]
        id_node = node.children[1]
        expr_node = node.children[2]
        
        var_type = type_node.value
        var_name = id_node.value
        line = id_node.token.line if id_node.token else 0
        
        # Check if already declared
        if not self.symbol_table.declare(var_name, var_type, line):
            existing = self.symbol_table.lookup(var_name)
            if existing:
                self.errors.append(
                    f"Variable '{var_name}' already declared at line {existing['declared_at']}"
                )
            return
        
        # Type check the expression
        expr_type = self.get_expression_type(expr_node)
        if expr_type and not self.is_compatible_type(var_type, expr_type):
            self.warnings.append(
                f"Type mismatch: '{var_name}' declared as {var_type}, assigned {expr_type} at line {line}"
            )
    
    def analyze_assignment(self, node: ASTNode):
        """Analyze variable assignment"""
        if len(node.children) < 2:
            return
        
        id_node = node.children[0]
        expr_node = node.children[1]
        
        var_name = id_node.value
        line = id_node.token.line if id_node.token else 0
        
        # Check if variable is declared
        symbol = self.symbol_table.lookup(var_name)
        if not symbol:
            self.errors.append(
                f"Variable '{var_name}' used before declaration at line {line}"
            )
            return
        
        # Type check
        expr_type = self.get_expression_type(expr_node)
        if expr_type and not self.is_compatible_type(symbol['type'], expr_type):
            self.warnings.append(
                f"Type mismatch: '{var_name}' is {symbol['type']}, assigned {expr_type} at line {line}"
            )
    
    def analyze_if_statement(self, node: ASTNode):
        """Analyze if statement - enter new scope"""
        if len(node.children) < 2:
            return
        
        condition = node.children[0]
        condition_type = self.get_expression_type(condition)
        
        if condition_type and condition_type != 'SahiGhalat':
            line = condition.token.line if condition.token else 0
            self.errors.append(
                f"If condition must be boolean (SahiGhalat), got {condition_type} at line {line}"
            )
        elif not condition_type:
            line = condition.token.line if condition.token else 0
            self.errors.append(f"Invalid condition in if statement at line {line}")
        
        # Analyze then block in new scope
        then_block = node.children[1]
        self.symbol_table.enter_scope()
        self.analyze_node(then_block)
        self.symbol_table.exit_scope()
        
        # Analyze else block if present
        if len(node.children) > 2:
            else_block = node.children[2]
            self.symbol_table.enter_scope()
            self.analyze_node(else_block)
            self.symbol_table.exit_scope()
    
    def analyze_while_statement(self, node: ASTNode):
        """Analyze while statement - enter new scope"""
        if len(node.children) < 2:
            return
        
        condition = node.children[0]
        condition_type = self.get_expression_type(condition)
        
        if condition_type and condition_type != 'SahiGhalat':
            line = condition.token.line if condition.token else 0
            self.errors.append(
                f"While condition must be boolean (SahiGhalat), got {condition_type} at line {line}"
            )
        elif not condition_type:
            line = condition.token.line if condition.token else 0
            self.errors.append(f"Invalid condition in while statement at line {line}")
        
        # Analyze body in new scope
        body = node.children[1]
        self.symbol_table.enter_scope()
        self.analyze_node(body)
        self.symbol_table.exit_scope()
    
    def analyze_print_statement(self, node: ASTNode):
        """Analyze print statement"""
        if len(node.children) < 1:
            return
        
        expr = node.children[0]
        expr_type = self.get_expression_type(expr)
        # Print can handle any type, so no error, just note the type
    
    def get_expression_type(self, node: ASTNode) -> Optional[str]:
        """Determine the type of an expression"""
        if not node:
            return None
        
        if node.node_type == 'IDENTIFIER':
            var_name = node.value
            symbol = self.symbol_table.lookup(var_name)
            if symbol:
                return symbol['type']
            
            line = node.token.line if node.token else 0
            self.errors.append(f"Variable '{var_name}' used before declaration at line {line}")
            return None
        
        if node.node_type == 'INTEGER':
            return 'Adad'
        
        if node.node_type == 'FLOAT':
            return 'TairtaAdad'
        
        if node.node_type == 'STRING':
            return 'Lafz'
        
        if node.node_type == 'BOOLEAN':
            return 'SahiGhalat'
        
        if node.node_type == 'BINARY_OP':
            if len(node.children) < 2:
                return None
            
            left_type = self.get_expression_type(node.children[0])
            right_type = self.get_expression_type(node.children[1])
            op = node.value
            
            # Arithmetic operations
            if op in ['+', '-', '*', '/']:
                if left_type == 'Lafz' or right_type == 'Lafz':
                    if op == '+':
                        return 'Lafz'  # String concatenation
                    return None
                if left_type == 'TairtaAdad' or right_type == 'TairtaAdad':
                    return 'TairtaAdad'
                if left_type == 'Adad' and right_type == 'Adad':
                    return 'Adad'
                return None
            
            # Comparison and logical operations return bool
            if op in ['==', '!=', '<', '>', '<=', '>=', '&&', '||']:
                return 'SahiGhalat'
        
        if node.node_type == 'UNARY_OP':
            if len(node.children) < 1:
                return None
            operand_type = self.get_expression_type(node.children[0])
            op = node.value
            
            if op == '!' and operand_type == 'SahiGhalat':
                return 'SahiGhalat'
            if op == '-' and operand_type in ['Adad', 'TairtaAdad']:
                return operand_type
        
        return None
    
    def is_compatible_type(self, target: str, source: str) -> bool:
        """Check if source type can be assigned to target type"""
        if target == source:
            return True
        
        # Allow int to float conversion
        if target == 'TairtaAdad' and source == 'Adad':
            return True
        
        # Mutaghayyar is compatible with anything
        if target == 'Mutaghayyar' or source == 'Mutaghayyar':
            return True
        
        return False
    
    def get_symbol_table(self) -> SymbolTable:
        """Get the symbol table"""
        return self.symbol_table
    
    def get_errors(self) -> List[str]:
        """Get semantic errors"""
        return self.errors
    
    def get_warnings(self) -> List[str]:
        """Get semantic warnings"""
        return self.warnings

