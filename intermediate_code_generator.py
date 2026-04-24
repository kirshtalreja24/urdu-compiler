"""
Intermediate Code Generator
===========================
This module generates three-address code (TAC) from the AST.
Three-address code is an intermediate representation where each instruction
has at most one operator and three operands.

Format: result = operand1 operator operand2
Example: t1 = x + y
"""

from typing import List, Dict, Optional
from syntax_analyzer import ASTNode


class ThreeAddressCode:
    """Represents a three-address code instruction"""
    
    def __init__(self, op: str, arg1: str = None, arg2: str = None, result: str = None, label: str = None):
        self.op = op  # Operation: ADD, SUB, MUL, DIV, ASSIGN, GOTO, IF_GOTO, LABEL, etc.
        self.arg1 = arg1  # First operand
        self.arg2 = arg2  # Second operand
        self.result = result  # Result variable
        self.label = label  # Label for control flow
    
    def __repr__(self):
        if self.label:
            return f"{self.label}:"
        if self.op == "ASSIGN":
            return f"{self.result} = {self.arg1}"
        if self.op in ["GOTO", "IF_GOTO", "IF_FALSE_GOTO"]:
            if self.arg2:
                return f"{self.op} {self.arg1} {self.arg2}"
            return f"{self.op} {self.arg1}"
        if self.arg2:
            return f"{self.result} = {self.arg1} {self.op} {self.arg2}"
        return f"{self.result} = {self.op} {self.arg1}"


class IntermediateCodeGenerator:
    """
    Generates three-address code from AST
    
    Three-address code format:
    - Arithmetic: t1 = x + y
    - Assignment: x = t1
    - Comparison: t1 = x > y
    - Control flow: IF x GOTO L1
    """
    
    def __init__(self, ast: ASTNode):
        self.ast = ast
        self.tac_list: List[ThreeAddressCode] = []
        self.temp_counter = 0
        self.label_counter = 0
        self.symbol_table: Dict[str, str] = {}  # Maps variable names to their types
    
    def generate(self) -> List[ThreeAddressCode]:
        """Main generation function"""
        if not self.ast:
            return []
        
        self.tac_list = []
        self.temp_counter = 0
        self.label_counter = 0
        
        self.generate_from_node(self.ast)
        
        return self.tac_list
    
    def new_temp(self) -> str:
        """Generate a new temporary variable name"""
        temp = f"t{self.temp_counter}"
        self.temp_counter += 1
        return temp
    
    def new_label(self) -> str:
        """Generate a new label name"""
        label = f"L{self.label_counter}"
        self.label_counter += 1
        return label
    
    def generate_from_node(self, node: ASTNode) -> Optional[str]:
        """Generate TAC from AST node, returns result variable name"""
        if not node:
            return None
        
        if node.node_type == 'PROGRAM':
            for stmt in node.children:
                self.generate_from_node(stmt)
            return None
        
        elif node.node_type == 'DECLARATION':
            return self.generate_declaration(node)
        
        elif node.node_type == 'ASSIGNMENT':
            return self.generate_assignment(node)
        
        elif node.node_type == 'IF_STATEMENT':
            self.generate_if_statement(node)
            return None
        
        elif node.node_type == 'WHILE_STATEMENT':
            self.generate_while_statement(node)
            return None
        
        elif node.node_type == 'PRINT_STATEMENT':
            self.generate_print_statement(node)
            return None
        
        elif node.node_type == 'BINARY_OP':
            return self.generate_binary_op(node)
        
        elif node.node_type == 'UNARY_OP':
            return self.generate_unary_op(node)
        
        elif node.node_type in ['IDENTIFIER', 'INTEGER', 'FLOAT', 'STRING', 'BOOLEAN']:
            # For literals and identifiers, return their value directly
            if node.node_type == 'IDENTIFIER':
                return node.value
            elif node.node_type == 'INTEGER':
                return str(node.value)
            elif node.node_type == 'FLOAT':
                return str(node.value)
            elif node.node_type == 'STRING':
                return node.value
            elif node.node_type == 'BOOLEAN':
                return 'Sahi' if node.value else 'Ghalat'
        
        return None
    
    def generate_declaration(self, node: ASTNode) -> str:
        """Generate TAC for variable declaration: type x = expr;"""
        if len(node.children) < 3:
            return None
        
        type_node = node.children[0]
        id_node = node.children[1]
        expr_node = node.children[2]
        
        var_name = id_node.value
        var_type = type_node.value
        
        # Generate code for expression
        result = self.generate_from_node(expr_node)
        
        # Store variable in symbol table
        self.symbol_table[var_name] = var_type
        
        # If expression result is a temp or literal, assign it
        if result and result != var_name:
            self.tac_list.append(ThreeAddressCode("ASSIGN", result, None, var_name))
        
        return var_name
    
    def generate_assignment(self, node: ASTNode) -> str:
        """Generate TAC for assignment: x = expr;"""
        if len(node.children) < 2:
            return None
        
        id_node = node.children[0]
        expr_node = node.children[1]
        
        var_name = id_node.value
        
        # Generate code for expression
        result = self.generate_from_node(expr_node)
        
        # Assign result to variable
        if result and result != var_name:
            self.tac_list.append(ThreeAddressCode("ASSIGN", result, None, var_name))
        
        return var_name
    
    def generate_if_statement(self, node: ASTNode):
        """Generate TAC for if-else statement"""
        if len(node.children) < 2:
            return
        
        condition = node.children[0]
        then_block = node.children[1]
        else_block = node.children[2] if len(node.children) > 2 else None
        
        # Generate condition
        cond_result = self.generate_from_node(condition)
        
        # Create labels
        else_label = self.new_label() if else_block else None
        end_label = self.new_label()
        
        # If condition is false, jump to else or end
        if else_block:
            self.tac_list.append(ThreeAddressCode("IF_FALSE_GOTO", cond_result, else_label))
        else:
            self.tac_list.append(ThreeAddressCode("IF_FALSE_GOTO", cond_result, end_label))
        
        # Generate then block
        for stmt in then_block.children:
            self.generate_from_node(stmt)
        
        # Jump to end (skip else block)
        if else_block:
            self.tac_list.append(ThreeAddressCode("GOTO", end_label))
            self.tac_list.append(ThreeAddressCode("LABEL", None, None, None, else_label))
            
            # Generate else block
            for stmt in else_block.children:
                self.generate_from_node(stmt)
        
        # End label
        self.tac_list.append(ThreeAddressCode("LABEL", None, None, None, end_label))
    
    def generate_while_statement(self, node: ASTNode):
        """Generate TAC for while statement"""
        if len(node.children) < 2:
            return
        
        condition = node.children[0]
        body = node.children[1]
        
        # Create labels
        loop_label = self.new_label()
        end_label = self.new_label()
        
        # Loop label
        self.tac_list.append(ThreeAddressCode("LABEL", None, None, None, loop_label))
        
        # Generate condition
        cond_result = self.generate_from_node(condition)
        
        # If condition is false, jump to end
        self.tac_list.append(ThreeAddressCode("IF_FALSE_GOTO", cond_result, end_label))
        
        # Generate body
        for stmt in body.children:
            self.generate_from_node(stmt)
        
        # Jump back to loop start
        self.tac_list.append(ThreeAddressCode("GOTO", loop_label))
        
        # End label
        self.tac_list.append(ThreeAddressCode("LABEL", None, None, None, end_label))
    
    def generate_print_statement(self, node: ASTNode):
        """Generate TAC for print statement"""
        if len(node.children) < 1:
            return
        
        expr = node.children[0]
        result = self.generate_from_node(expr)
        
        if result:
            self.tac_list.append(ThreeAddressCode("PRINT", result))
    
    def generate_binary_op(self, node: ASTNode) -> str:
        """Generate TAC for binary operation"""
        if len(node.children) < 2:
            return None
        
        left = node.children[0]
        right = node.children[1]
        op = node.value
        
        # Generate code for operands
        left_result = self.generate_from_node(left)
        right_result = self.generate_from_node(right)
        
        # Map operators to TAC operations
        op_map = {
            '+': 'ADD',
            '-': 'SUB',
            '*': 'MUL',
            '/': 'DIV',
            '==': 'EQ',
            '!=': 'NE',
            '<': 'LT',
            '>': 'GT',
            '<=': 'LE',
            '>=': 'GE',
            '&&': 'AND',
            '||': 'OR'
        }
        
        tac_op = op_map.get(op)
        if not tac_op:
            return None
        
        # Create temporary for result
        temp = self.new_temp()
        
        # Generate TAC instruction
        self.tac_list.append(ThreeAddressCode(tac_op, left_result, right_result, temp))
        
        return temp
    
    def generate_unary_op(self, node: ASTNode) -> str:
        """Generate TAC for unary operation"""
        if len(node.children) < 1:
            return None
        
        operand = node.children[0]
        op = node.value
        
        # Generate code for operand
        operand_result = self.generate_from_node(operand)
        
        if op == '!':
            temp = self.new_temp()
            self.tac_list.append(ThreeAddressCode("NOT", operand_result, None, temp))
            return temp
        elif op == '-':
            temp = self.new_temp()
            self.tac_list.append(ThreeAddressCode("NEG", operand_result, None, temp))
            return temp
        
        return operand_result
    
    def get_tac_list(self) -> List[ThreeAddressCode]:
        """Get the generated three-address code list"""
        return self.tac_list
    
    def format_tac(self) -> str:
        """Format TAC as readable string"""
        lines = []
        for i, tac in enumerate(self.tac_list):
            if tac.label:
                lines.append(f"{tac.label}:")
            elif tac.op == "ASSIGN":
                lines.append(f"  {tac.result} = {tac.arg1}")
            elif tac.op == "PRINT":
                lines.append(f"  Dikhao {tac.arg1}")
            elif tac.op in ["GOTO", "IF_GOTO", "IF_FALSE_GOTO"]:
                if tac.arg2:
                    lines.append(f"  {tac.op.lower()} {tac.arg1} {tac.arg2}")
                else:
                    lines.append(f"  {tac.op.lower()} {tac.arg1}")
            elif tac.arg2:
                lines.append(f"  {tac.result} = {tac.arg1} {tac.op.lower()} {tac.arg2}")
            else:
                lines.append(f"  {tac.result} = {tac.op.lower()} {tac.arg1}")
        return "\n".join(lines)

