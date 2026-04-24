
from intermediate_code_generator import ThreeAddressCode, IntermediateCodeGenerator
from optimizer import Optimizer
from syntax_analyzer import ASTNode

def test_while_optimization():
    # Simulate AST for:
    # number i = 0;
    # jab tak (i < 5) {
    #   dikhao i;
    #   i = i + 1;
    # }
    
    # Manually create TAC that resembles what would be generated
    tac_list = [
        ThreeAddressCode("ASSIGN", "0", None, "i"),
        ThreeAddressCode("LABEL", None, None, None, "L0"),
        ThreeAddressCode("LT", "i", "5", "t0"),
        ThreeAddressCode("IF_FALSE_GOTO", "t0", None, "L1"),
        ThreeAddressCode("PRINT", "i", None, None),
        ThreeAddressCode("ADD", "i", "1", "t1"),
        ThreeAddressCode("ASSIGN", "t1", None, "i"),
        ThreeAddressCode("GOTO", "L0", None, None),
        ThreeAddressCode("LABEL", None, None, None, "L1")
    ]
    
    optimizer = Optimizer(tac_list)
    optimized = optimizer.optimize()
    
    print("Original TAC:")
    for tac in tac_list:
        print(f"  {tac}")
        
    print("\nOptimized TAC:")
    for tac in optimized:
        print(f"  {tac}")

if __name__ == "__main__":
    test_while_optimization()
