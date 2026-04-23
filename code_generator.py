"""
Code Generator
==============
This module generates executable code (interpreter) from optimized three-address code.
The generated code can be executed to produce the program output.

This implements a simple stack-based interpreter that executes the TAC instructions.
"""

from typing import List, Dict, Any
from intermediate_code_generator import ThreeAddressCode


class CodeGenerator:
    """
    Generates executable code from optimized three-address code
    
    This implementation creates a simple interpreter that executes TAC instructions.
    The interpreter maintains:
    - Variable storage (memory)
    - Stack for expression evaluation
    - Program counter for control flow
    """
    
    def __init__(self, optimized_tac: List[ThreeAddressCode]):
        self.tac_list = optimized_tac
        self.memory: Dict[str, Any] = {}  # Variable storage
        self.output: List[str] = []  # Program output
        self.label_map: Dict[str, int] = {}  # Map labels to instruction indices
    
    def generate(self) -> str:
        """Generate executable code representation"""
        # Build label map
        self.build_label_map()
        
        # Generate code
        code_lines = []
        code_lines.append("# Generated Executable Code")
        code_lines.append("# This code can be executed by the interpreter")
        code_lines.append("")
        
        for i, tac in enumerate(self.tac_list):
            if tac.label:
                code_lines.append(f"{tac.label}:")
            else:
                code_lines.append(self.generate_instruction(tac, i))
        
        return "\n".join(code_lines)
    
    def build_label_map(self):
        """Build map from labels to instruction indices"""
        self.label_map = {}
        for i, tac in enumerate(self.tac_list):
            if tac.label:
                self.label_map[tac.label] = i
    
    def generate_instruction(self, tac: ThreeAddressCode, index: int) -> str:
        """Generate code for a single instruction"""
        if tac.op == "ASSIGN":
            return f"  memory['{tac.result}'] = {self.format_value(tac.arg1)}"
        
        elif tac.op == "PRINT":
            return f"  print({self.format_value(tac.arg1)})"
        
        elif tac.op == "ADD":
            return f"  memory['{tac.result}'] = {self.format_value(tac.arg1)} + {self.format_value(tac.arg2)}"
        
        elif tac.op == "SUB":
            return f"  memory['{tac.result}'] = {self.format_value(tac.arg1)} - {self.format_value(tac.arg2)}"
        
        elif tac.op == "MUL":
            return f"  memory['{tac.result}'] = {self.format_value(tac.arg1)} * {self.format_value(tac.arg2)}"
        
        elif tac.op == "DIV":
            return f"  memory['{tac.result}'] = {self.format_value(tac.arg1)} / {self.format_value(tac.arg2)}"
        
        elif tac.op == "EQ":
            return f"  memory['{tac.result}'] = ({self.format_value(tac.arg1)} == {self.format_value(tac.arg2)})"
        
        elif tac.op == "NE":
            return f"  memory['{tac.result}'] = ({self.format_value(tac.arg1)} != {self.format_value(tac.arg2)})"
        
        elif tac.op == "LT":
            return f"  memory['{tac.result}'] = ({self.format_value(tac.arg1)} < {self.format_value(tac.arg2)})"
        
        elif tac.op == "GT":
            return f"  memory['{tac.result}'] = ({self.format_value(tac.arg1)} > {self.format_value(tac.arg2)})"
        
        elif tac.op == "LE":
            return f"  memory['{tac.result}'] = ({self.format_value(tac.arg1)} <= {self.format_value(tac.arg2)})"
        
        elif tac.op == "GE":
            return f"  memory['{tac.result}'] = ({self.format_value(tac.arg1)} >= {self.format_value(tac.arg2)})"
        
        elif tac.op == "AND":
            return f"  memory['{tac.result}'] = ({self.format_value(tac.arg1)} and {self.format_value(tac.arg2)})"
        
        elif tac.op == "OR":
            return f"  memory['{tac.result}'] = ({self.format_value(tac.arg1)} or {self.format_value(tac.arg2)})"
        
        elif tac.op == "NOT":
            return f"  memory['{tac.result}'] = (not {self.format_value(tac.arg1)})"
        
        elif tac.op == "NEG":
            return f"  memory['{tac.result}'] = (-{self.format_value(tac.arg1)})"
        
        elif tac.op == "GOTO":
            return f"  goto {tac.arg1}"
        
        elif tac.op == "IF_FALSE_GOTO":
            return f"  if not {self.format_value(tac.arg1)}: goto {tac.arg2}"
        
        elif tac.op == "IF_GOTO":
            return f"  if {self.format_value(tac.arg1)}: goto {tac.arg2}"
        
        return f"  # Unknown operation: {tac.op}"
    
    def format_value(self, value: str) -> str:
        """Format value for code generation"""
        if value is None:
            return "None"
        
        # Check if it's a string literal
        if value.startswith('"') and value.endswith('"'):
            return value
        
        # Check if it's a boolean
        if value == 'Sahi':
            return "True"
        if value == 'Ghalat':
            return "False"
        
        # Check if it's a number
        try:
            float(value)
            return value
        except ValueError:
            pass
        
        # It's a variable
        return f"memory.get('{value}', 0)"
    
    def execute(self) -> List[str]:
        """
        Execute the three-address code and return output
        This is a simple interpreter implementation
        """
        # Build label map if not already built
        if not self.label_map:
            self.build_label_map()
        
        self.memory = {}
        self.output = []
        
        pc = 0  # Program counter
        
        while pc < len(self.tac_list):
            tac = self.tac_list[pc]
            
            if tac.label:
                pc += 1
                continue
            
            if tac.op == "ASSIGN":
                val = self.get_value(tac.arg1)
                self.memory[tac.result] = val
                pc += 1
            
            elif tac.op == "PRINT":
                val = self.get_value(tac.arg1)
                self.output.append(str(val))
                pc += 1
            
            elif tac.op in ["ADD", "SUB", "MUL", "DIV"]:
                val1 = self.get_value(tac.arg1)
                val2 = self.get_value(tac.arg2)
                result = self.evaluate_arithmetic(tac.op, val1, val2)
                self.memory[tac.result] = result
                pc += 1
            
            elif tac.op in ["EQ", "NE", "LT", "GT", "LE", "GE"]:
                val1 = self.get_value(tac.arg1)
                val2 = self.get_value(tac.arg2)
                result = self.evaluate_comparison(tac.op, val1, val2)
                self.memory[tac.result] = result
                pc += 1
            
            elif tac.op in ["AND", "OR"]:
                val1 = self.get_value(tac.arg1)
                val2 = self.get_value(tac.arg2)
                result = self.evaluate_logical(tac.op, val1, val2)
                self.memory[tac.result] = result
                pc += 1
            
            elif tac.op == "NOT":
                val1 = self.get_value(tac.arg1)
                self.memory[tac.result] = not bool(val1)
                pc += 1
            
            elif tac.op == "NEG":
                val1 = self.get_value(tac.arg1)
                self.memory[tac.result] = -val1
                pc += 1
            
            elif tac.op == "GOTO":
                if tac.arg1 in self.label_map:
                    pc = self.label_map[tac.arg1]
                else:
                    pc += 1
            
            elif tac.op == "IF_FALSE_GOTO":
                val1 = self.get_value(tac.arg1)
                if not bool(val1):
                    if tac.arg2 in self.label_map:
                        pc = self.label_map[tac.arg2]
                    else:
                        pc += 1
                else:
                    pc += 1
            
            elif tac.op == "IF_GOTO":
                val1 = self.get_value(tac.arg1)
                if bool(val1):
                    if tac.arg2 in self.label_map:
                        pc = self.label_map[tac.arg2]
                    else:
                        pc += 1
                else:
                    pc += 1
            
            else:
                pc += 1
        
        return self.output
    
    def get_value(self, var: str) -> Any:
        """Get value of variable or constant"""
        if var is None:
            return None
        
        # Check if it's a string literal (with quotes)
        if isinstance(var, str) and len(var) >= 2 and var.startswith('"') and var.endswith('"'):
            return var[1:-1]
        
        # Check if it's a boolean
        if var == 'Sahi':
            return True
        if var == 'Ghalat':
            return False
        
        # Check if it's a number
        try:
            if isinstance(var, str) and '.' in var:
                return float(var)
            if isinstance(var, str):
                return int(var)
        except (ValueError, AttributeError):
            pass
        
        # It's a variable - check memory
        if isinstance(var, str):
            return self.memory.get(var, 0)
        
        return var
    
    def evaluate_arithmetic(self, op: str, val1: Any, val2: Any) -> Any:
        """Evaluate arithmetic operation"""
        if op == "ADD":
            return val1 + val2
        elif op == "SUB":
            return val1 - val2
        elif op == "MUL":
            return val1 * val2
        elif op == "DIV":
            return val1 / val2 if val2 != 0 else 0
        return None
    
    def evaluate_comparison(self, op: str, val1: Any, val2: Any) -> bool:
        """Evaluate comparison operation"""
        if op == "EQ":
            return val1 == val2
        elif op == "NE":
            return val1 != val2
        elif op == "LT":
            return val1 < val2
        elif op == "GT":
            return val1 > val2
        elif op == "LE":
            return val1 <= val2
        elif op == "GE":
            return val1 >= val2
        return False
    
    def evaluate_logical(self, op: str, val1: Any, val2: Any) -> bool:
        """Evaluate logical operation"""
        if op == "AND":
            return bool(val1) and bool(val2)
        elif op == "OR":
            return bool(val1) or bool(val2)
        return False
    
    def get_output(self) -> List[str]:
        """Get program output"""
        return self.output
    
    def get_memory_state(self) -> Dict[str, Any]:
        """Get final memory state"""
        return self.memory.copy()

