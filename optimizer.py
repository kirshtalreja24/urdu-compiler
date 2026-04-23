"""
Optimizer
=========
This module performs basic optimizations on three-address code:
1. Constant Folding: Evaluate constant expressions at compile time
2. Dead Code Elimination: Remove unreachable code
3. Constant Propagation: Replace variables with their constant values
"""

from typing import List, Dict, Optional
from intermediate_code_generator import ThreeAddressCode


class Optimizer:
    """
    Performs optimizations on three-address code
    
    Optimizations:
    - Constant folding: t1 = 5 + 3 → t1 = 8
    - Dead code elimination: Remove code after unconditional jumps
    - Constant propagation: Replace variables with known constant values
    """
    
    def __init__(self, tac_list: List[ThreeAddressCode]):
        self.tac_list = tac_list
        self.optimized_tac: List[ThreeAddressCode] = []
        self.constants: Dict[str, str] = {}  # Maps variables to constant values
    
    def optimize(self) -> List[ThreeAddressCode]:
        """Main optimization function"""
        self.optimized_tac = []
        self.constants = {}
        
        # First pass: Constant folding and propagation
        self.optimized_tac = self.constant_folding()
        
        # Second pass: Dead code elimination
        self.optimized_tac = self.dead_code_elimination(self.optimized_tac)
        
        return self.optimized_tac
    
    def constant_folding(self) -> List[ThreeAddressCode]:
        """Perform constant folding: evaluate constant expressions"""
        optimized = []
        
        for tac in self.tac_list:
            if tac.label:
                optimized.append(tac)
                continue
            
            # Try to fold constants
            if tac.op in ['ADD', 'SUB', 'MUL', 'DIV']:
                # Check if both operands are constants
                arg1_val = self.get_constant_value(tac.arg1)
                arg2_val = self.get_constant_value(tac.arg2)
                
                if arg1_val is not None and arg2_val is not None:
                    # Evaluate the expression
                    result_val = self.evaluate_operation(tac.op, arg1_val, arg2_val)
                    if result_val is not None:
                        # Store constant value
                        self.constants[tac.result] = str(result_val)
                        # Replace with assignment: t1 = 8
                        optimized.append(ThreeAddressCode("ASSIGN", str(result_val), None, tac.result))
                        continue
            
            # Check for constant comparisons
            if tac.op in ['EQ', 'NE', 'LT', 'GT', 'LE', 'GE']:
                arg1_val = self.get_constant_value(tac.arg1)
                arg2_val = self.get_constant_value(tac.arg2)
                
                if arg1_val is not None and arg2_val is not None:
                    result_val = self.evaluate_comparison(tac.op, arg1_val, arg2_val)
                    if result_val is not None:
                        self.constants[tac.result] = 'true' if result_val else 'false'
                        optimized.append(ThreeAddressCode("ASSIGN", 'true' if result_val else 'false', None, tac.result))
                        continue
            
            # Check for constant logical operations
            if tac.op in ['AND', 'OR']:
                arg1_val = self.get_constant_value(tac.arg1)
                arg2_val = self.get_constant_value(tac.arg2)
                
                if arg1_val is not None and arg2_val is not None:
                    result_val = self.evaluate_logical(tac.op, arg1_val, arg2_val)
                    if result_val is not None:
                        self.constants[tac.result] = 'true' if result_val else 'false'
                        optimized.append(ThreeAddressCode("ASSIGN", 'true' if result_val else 'false', None, tac.result))
                        continue
            
            # Check for constant unary operations
            if tac.op in ['NOT', 'NEG']:
                arg1_val = self.get_constant_value(tac.arg1)
                
                if arg1_val is not None:
                    result_val = self.evaluate_unary(tac.op, arg1_val)
                    if result_val is not None:
                        self.constants[tac.result] = str(result_val)
                        optimized.append(ThreeAddressCode("ASSIGN", str(result_val), None, tac.result))
                        continue
            
            # Constant propagation: replace variables with constants
            if tac.op == "ASSIGN":
                # If assigning a constant, store it
                const_val = self.get_constant_value(tac.arg1)
                if const_val is not None:
                    self.constants[tac.result] = str(const_val)
                optimized.append(tac)
            else:
                # Propagate constants in operands
                new_tac = ThreeAddressCode(tac.op, tac.arg1, tac.arg2, tac.result, tac.label)
                if tac.arg1 in self.constants:
                    new_tac.arg1 = self.constants[tac.arg1]
                if tac.arg2 and tac.arg2 in self.constants:
                    new_tac.arg2 = self.constants[tac.arg2]
                optimized.append(new_tac)
        
        return optimized
    
    def get_constant_value(self, var: str) -> Optional[float]:
        """Get constant value if variable is a constant"""
        if var is None:
            return None
        
        # Check if it's already a number
        try:
            if '.' in var:
                return float(var)
            return int(var)
        except ValueError:
            pass
        
        # Check if it's a boolean
        if var == 'true':
            return 1.0
        if var == 'false':
            return 0.0
        
        # Check if it's in constants table
        if var in self.constants:
            try:
                const_val = self.constants[var]
                if '.' in const_val:
                    return float(const_val)
                return int(const_val)
            except ValueError:
                if const_val == 'true':
                    return 1.0
                if const_val == 'false':
                    return 0.0
        
        return None
    
    def evaluate_operation(self, op: str, val1: float, val2: float) -> Optional[float]:
        """Evaluate arithmetic operation"""
        try:
            if op == 'ADD':
                return val1 + val2
            elif op == 'SUB':
                return val1 - val2
            elif op == 'MUL':
                return val1 * val2
            elif op == 'DIV':
                if val2 == 0:
                    return None  # Division by zero
                return val1 / val2
        except:
            return None
        return None
    
    def evaluate_comparison(self, op: str, val1: float, val2: float) -> Optional[bool]:
        """Evaluate comparison operation"""
        try:
            if op == 'EQ':
                return val1 == val2
            elif op == 'NE':
                return val1 != val2
            elif op == 'LT':
                return val1 < val2
            elif op == 'GT':
                return val1 > val2
            elif op == 'LE':
                return val1 <= val2
            elif op == 'GE':
                return val1 >= val2
        except:
            return None
        return None
    
    def evaluate_logical(self, op: str, val1: float, val2: float) -> Optional[bool]:
        """Evaluate logical operation"""
        try:
            bool1 = bool(val1)
            bool2 = bool(val2)
            if op == 'AND':
                return bool1 and bool2
            elif op == 'OR':
                return bool1 or bool2
        except:
            return None
        return None
    
    def evaluate_unary(self, op: str, val: float) -> Optional[float]:
        """Evaluate unary operation"""
        try:
            if op == 'NOT':
                return 0.0 if bool(val) else 1.0
            elif op == 'NEG':
                return -val
        except:
            return None
        return None
    
    def dead_code_elimination(self, tac_list: List[ThreeAddressCode]) -> List[ThreeAddressCode]:
        """Remove unreachable code after unconditional jumps"""
        optimized = []
        i = 0
        
        while i < len(tac_list):
            tac = tac_list[i]
            optimized.append(tac)
            
            # If this is an unconditional GOTO, mark next instructions as dead
            if tac.op == "GOTO" and tac.arg1:
                # Skip instructions until we reach the target label
                i += 1
                target_label = tac.arg1
                
                # Find the target label
                while i < len(tac_list):
                    if tac_list[i].label == target_label:
                        break
                    i += 1
                continue
            
            i += 1
        
        return optimized
    
    def get_optimized_tac(self) -> List[ThreeAddressCode]:
        """Get optimized three-address code"""
        return self.optimized_tac
    
    def format_optimized_tac(self) -> str:
        """Format optimized TAC as readable string"""
        lines = []
        for i, tac in enumerate(self.optimized_tac):
            if tac.label:
                lines.append(f"{tac.label}:")
            elif tac.op == "ASSIGN":
                lines.append(f"  {tac.result} = {tac.arg1}")
            elif tac.op == "PRINT":
                lines.append(f"  print {tac.arg1}")
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

