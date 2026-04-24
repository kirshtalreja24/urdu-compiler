"""
Optimizer
=========
This module performs basic optimizations on three-address code:
1. Constant Folding
2. Dead Code Elimination
3. Constant Propagation

FIXES ADDED:
- Do not propagate constants across labels/basic blocks
- Kill constants after control flow instructions
- Invalidate constants on reassignment
"""

from typing import List, Dict, Optional
from intermediate_code_generator import ThreeAddressCode


class Optimizer:

    def __init__(self, tac_list: List[ThreeAddressCode]):
        self.tac_list = tac_list
        self.optimized_tac: List[ThreeAddressCode] = []
        self.constants: Dict[str, str] = {}

    def optimize(self) -> List[ThreeAddressCode]:

        self.optimized_tac = []
        self.constants = {}

        # Pass 1
        self.optimized_tac = self.constant_folding()

        # Pass 2
        self.optimized_tac = self.dead_code_elimination(
            self.optimized_tac
        )

        return self.optimized_tac


    def constant_folding(self) -> List[ThreeAddressCode]:

        optimized = []

        for tac in self.tac_list:

            # -----------------------------------
            # FIX:
            # Stop constant propagation at labels
            # -----------------------------------
            if tac.label:
                self.constants = {}
                optimized.append(tac)
                continue


            # ---------------------------
            # Arithmetic Folding
            # ---------------------------
            if tac.op in ['ADD','SUB','MUL','DIV']:

                arg1_val = self.get_constant_value(tac.arg1)
                arg2_val = self.get_constant_value(tac.arg2)

                if arg1_val is not None and arg2_val is not None:

                    result_val = self.evaluate_operation(
                        tac.op,
                        arg1_val,
                        arg2_val
                    )

                    if result_val is not None:

                        self.constants[tac.result] = str(result_val)

                        optimized.append(
                            ThreeAddressCode(
                                "ASSIGN",
                                str(result_val),
                                None,
                                tac.result
                            )
                        )
                        continue


            # ---------------------------
            # Comparison Folding
            # ---------------------------
            if tac.op in ['EQ','NE','LT','GT','LE','GE']:

                arg1_val = self.get_constant_value(tac.arg1)
                arg2_val = self.get_constant_value(tac.arg2)

                if arg1_val is not None and arg2_val is not None:

                    result_val = self.evaluate_comparison(
                        tac.op,
                        arg1_val,
                        arg2_val
                    )

                    if result_val is not None:

                        val = 'Sahi' if result_val else 'Ghalat'

                        self.constants[tac.result] = val

                        optimized.append(
                            ThreeAddressCode(
                                "ASSIGN",
                                val,
                                None,
                                tac.result
                            )
                        )
                        continue


            # ---------------------------
            # Logical Folding
            # ---------------------------
            if tac.op in ['AND','OR']:

                arg1_val = self.get_constant_value(tac.arg1)
                arg2_val = self.get_constant_value(tac.arg2)

                if arg1_val is not None and arg2_val is not None:

                    result_val = self.evaluate_logical(
                        tac.op,
                        arg1_val,
                        arg2_val
                    )

                    if result_val is not None:

                        val = 'Sahi' if result_val else 'Ghalat'

                        self.constants[tac.result] = val

                        optimized.append(
                            ThreeAddressCode(
                                "ASSIGN",
                                val,
                                None,
                                tac.result
                            )
                        )
                        continue


            # ---------------------------
            # Unary Folding
            # ---------------------------
            if tac.op in ['NOT','NEG']:

                arg1_val = self.get_constant_value(tac.arg1)

                if arg1_val is not None:

                    result_val = self.evaluate_unary(
                        tac.op,
                        arg1_val
                    )

                    if result_val is not None:

                        self.constants[tac.result] = str(result_val)

                        optimized.append(
                            ThreeAddressCode(
                                "ASSIGN",
                                str(result_val),
                                None,
                                tac.result
                            )
                        )
                        continue


            # ---------------------------
            # Assignment
            # ---------------------------
            if tac.op == "ASSIGN":

                # FIX:
                # kill old constant when variable changes
                self.constants.pop(tac.result, None)

                const_val = self.get_constant_value(
                    tac.arg1
                )

                if const_val is not None:
                    self.constants[tac.result] = str(
                        const_val
                    )

                optimized.append(tac)

            else:

                # Constant propagation
                new_tac = ThreeAddressCode(
                    tac.op,
                    tac.arg1,
                    tac.arg2,
                    tac.result,
                    tac.label
                )

                if tac.arg1 in self.constants:
                    new_tac.arg1 = self.constants[tac.arg1]

                if tac.arg2 and tac.arg2 in self.constants:
                    new_tac.arg2 = self.constants[tac.arg2]

                optimized.append(new_tac)


            # -----------------------------------
            # FIX:
            # kill constants after control flow
            # -----------------------------------
            if tac.op in [
                "GOTO",
                "IF_GOTO",
                "IF_FALSE_GOTO"
            ]:
                self.constants = {}

        return optimized


    def get_constant_value(self, var: str) -> Optional[float]:

        if var is None:
            return None

        try:
            if '.' in var:
                return float(var)
            return int(var)

        except ValueError:
            pass


        if var == 'Sahi':
            return 1.0

        if var == 'Ghalat':
            return 0.0


        if var in self.constants:

            try:
                const_val = self.constants[var]

                if '.' in const_val:
                    return float(const_val)

                return int(const_val)

            except ValueError:

                if const_val == 'Sahi':
                    return 1.0

                if const_val == 'Ghalat':
                    return 0.0

        return None


    def evaluate_operation(
        self,
        op:str,
        val1:float,
        val2:float
    ):

        try:

            if op == 'ADD':
                return val1 + val2

            elif op == 'SUB':
                return val1 - val2

            elif op == 'MUL':
                return val1 * val2

            elif op == 'DIV':

                if val2 == 0:
                    return None

                return val1 / val2

        except:
            return None

        return None


    def evaluate_comparison(
        self,
        op:str,
        val1:float,
        val2:float
    ):

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


    def evaluate_logical(
        self,
        op:str,
        val1:float,
        val2:float
    ):

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


    def evaluate_unary(
        self,
        op:str,
        val:float
    ):

        try:

            if op == 'NOT':
                return 0.0 if bool(val) else 1.0

            elif op == 'NEG':
                return -val

        except:
            return None

        return None


    def dead_code_elimination(
        self,
        tac_list: List[ThreeAddressCode]
    ):

        optimized = []
        i = 0

        while i < len(tac_list):

            tac = tac_list[i]

            optimized.append(tac)

            if tac.op == "GOTO" and tac.arg1:

                i += 1

                while i < len(tac_list):

                    if tac_list[i].label is not None:
                        break

                    i += 1

                continue

            i += 1

        return optimized


    def get_optimized_tac(self):
        return self.optimized_tac


    def format_optimized_tac(self):

        lines = []

        for i,tac in enumerate(
            self.optimized_tac
        ):

            if tac.label:
                lines.append(
                    f"{tac.label}:"
                )

            elif tac.op == "ASSIGN":
                lines.append(
                    f"  {tac.result} = {tac.arg1}"
                )

            elif tac.op == "PRINT":
                lines.append(
                    f"  print {tac.arg1}"
                )

            elif tac.op in [
                "GOTO",
                "IF_GOTO",
                "IF_FALSE_GOTO"
            ]:

                if tac.arg2:
                    lines.append(
                        f"  {tac.op.lower()} {tac.arg1} {tac.arg2}"
                    )
                else:
                    lines.append(
                        f"  {tac.op.lower()} {tac.arg1}"
                    )

            elif tac.arg2:
                lines.append(
                    f"  {tac.result} = {tac.arg1} {tac.op.lower()} {tac.arg2}"
                )

            else:
                lines.append(
                    f"  {tac.result} = {tac.op.lower()} {tac.arg1}"
                )

        return "\n".join(lines)