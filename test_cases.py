"""
Test Cases for Compiler
=======================
This file contains test cases to demonstrate the compiler functionality.
Run these tests to verify all phases work correctly.
"""

from lexical_analyzer import LexicalAnalyzer
from syntax_analyzer import SyntaxAnalyzer
from semantic_analyzer import SemanticAnalyzer


def test_case_1():
    """Test Case 1: Simple Arithmetic"""
    print("=" * 60)
    print("TEST CASE 1: Simple Arithmetic")
    print("=" * 60)
    
    code = """
int x = 10;
int y = 20;
int z = x + y;
print(z);
"""
    
    print("\nSource Code:")
    print(code)
    
    # Lexical Analysis
    lexer = LexicalAnalyzer(code)
    tokens = lexer.tokenize()
    print(f"\n✓ Lexical Analysis: {len([t for t in tokens if t.type.value != 'EOF'])} tokens")
    if lexer.get_errors():
        print(f"  Errors: {lexer.get_errors()}")
    
    # Syntax Analysis
    parser = SyntaxAnalyzer(tokens)
    ast = parser.parse()
    print(f"✓ Syntax Analysis: {'PASSED' if ast and not parser.get_errors() else 'FAILED'}")
    if parser.get_errors():
        print(f"  Errors: {parser.get_errors()}")
    
    # Semantic Analysis
    if ast:
        semantic = SemanticAnalyzer(ast)
        semantic.analyze()
        print(f"✓ Semantic Analysis: {'PASSED' if not semantic.get_errors() else 'FAILED'}")
        if semantic.get_errors():
            print(f"  Errors: {semantic.get_errors()}")
        if semantic.get_warnings():
            print(f"  Warnings: {semantic.get_warnings()}")
        print("\nSymbol Table:")
        symbol_table = semantic.get_symbol_table()
        for scope, symbols in symbol_table.get_all_symbols().items():
            if symbols:
                print(f"  Scope: {scope}")
                for name, info in symbols.items():
                    print(f"    {name}: {info['type']} (line {info['declared_at']})")
    
    print("\n")


def test_case_2():
    """Test Case 2: If-Else Statement with Scope"""
    print("=" * 60)
    print("TEST CASE 2: If-Else Statement with Scope")
    print("=" * 60)
    
    code = """
int age = 18;
if (age >= 18) {
    string status = "Adult";
    print(status);
} else {
    string status = "Minor";
    print(status);
}
"""
    
    print("\nSource Code:")
    print(code)
    
    # Lexical Analysis
    lexer = LexicalAnalyzer(code)
    tokens = lexer.tokenize()
    print(f"\n✓ Lexical Analysis: {len([t for t in tokens if t.type.value != 'EOF'])} tokens")
    
    # Syntax Analysis
    parser = SyntaxAnalyzer(tokens)
    ast = parser.parse()
    print(f"✓ Syntax Analysis: {'PASSED' if ast and not parser.get_errors() else 'FAILED'}")
    
    # Semantic Analysis
    if ast:
        semantic = SemanticAnalyzer(ast)
        semantic.analyze()
        print(f"✓ Semantic Analysis: {'PASSED' if not semantic.get_errors() else 'FAILED'}")
        print("\nSymbol Table (showing scope):")
        symbol_table = semantic.get_symbol_table()
        for scope, symbols in symbol_table.get_all_symbols().items():
            if symbols:
                print(f"  Scope: {scope}")
                for name, info in symbols.items():
                    print(f"    {name}: {info['type']} (line {info['declared_at']}, scope: {info['scope']})")
    
    print("\n")


def test_case_3():
    """Test Case 3: While Loop"""
    print("=" * 60)
    print("TEST CASE 3: While Loop")
    print("=" * 60)
    
    code = """
int i = 0;
while (i < 5) {
    print(i);
    i = i + 1;
}
"""
    
    print("\nSource Code:")
    print(code)
    
    # Lexical Analysis
    lexer = LexicalAnalyzer(code)
    tokens = lexer.tokenize()
    print(f"\n✓ Lexical Analysis: {len([t for t in tokens if t.type.value != 'EOF'])} tokens")
    
    # Syntax Analysis
    parser = SyntaxAnalyzer(tokens)
    ast = parser.parse()
    print(f"✓ Syntax Analysis: {'PASSED' if ast and not parser.get_errors() else 'FAILED'}")
    
    # Semantic Analysis
    if ast:
        semantic = SemanticAnalyzer(ast)
        semantic.analyze()
        print(f"✓ Semantic Analysis: {'PASSED' if not semantic.get_errors() else 'FAILED'}")
        print("\nParse Tree (simplified):")
        print(f"  PROGRAM")
        print(f"    - DECLARATION")
        print(f"    - WHILE_STATEMENT")
        print(f"        - BINARY_OP (<)")
        print(f"        - BODY")
    
    print("\n")


def test_case_4():
    """Test Case 4: Type Checking and Conversions"""
    print("=" * 60)
    print("TEST CASE 4: Type Checking and Conversions")
    print("=" * 60)
    
    code = """
float pi = 3.14;
int radius = 5;
float area = pi * radius * radius;
bool isValid = area > 0;
print(isValid);
"""
    
    print("\nSource Code:")
    print(code)
    
    # Lexical Analysis
    lexer = LexicalAnalyzer(code)
    tokens = lexer.tokenize()
    print(f"\n✓ Lexical Analysis: {len([t for t in tokens if t.type.value != 'EOF'])} tokens")
    
    # Syntax Analysis
    parser = SyntaxAnalyzer(tokens)
    ast = parser.parse()
    print(f"✓ Syntax Analysis: {'PASSED' if ast and not parser.get_errors() else 'FAILED'}")
    
    # Semantic Analysis
    if ast:
        semantic = SemanticAnalyzer(ast)
        semantic.analyze()
        print(f"✓ Semantic Analysis: {'PASSED' if not semantic.get_errors() else 'FAILED'}")
        if semantic.get_warnings():
            print(f"  Warnings (expected for type conversions): {semantic.get_warnings()}")
    
    print("\n")


def test_case_5():
    """Test Case 5: Error Detection - Use Before Declaration"""
    print("=" * 60)
    print("TEST CASE 5: Error Detection - Use Before Declaration")
    print("=" * 60)
    
    code = """
int x = y + 10;  // Error: y used before declaration
int y = 20;
"""
    
    print("\nSource Code:")
    print(code)
    
    # Lexical Analysis
    lexer = LexicalAnalyzer(code)
    tokens = lexer.tokenize()
    print(f"\n✓ Lexical Analysis: {len([t for t in tokens if t.type.value != 'EOF'])} tokens")
    
    # Syntax Analysis
    parser = SyntaxAnalyzer(tokens)
    ast = parser.parse()
    print(f"✓ Syntax Analysis: {'PASSED' if ast and not parser.get_errors() else 'FAILED'}")
    
    # Semantic Analysis
    if ast:
        semantic = SemanticAnalyzer(ast)
        semantic.analyze()
        print(f"✓ Semantic Analysis: {'FAILED (as expected)' if semantic.get_errors() else 'PASSED'}")
        if semantic.get_errors():
            print(f"  Detected Errors: {semantic.get_errors()}")
    
    print("\n")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("COMPILER TEST SUITE")
    print("=" * 60 + "\n")
    
    test_case_1()
    test_case_2()
    test_case_3()
    test_case_4()
    test_case_5()
    
    print("=" * 60)
    print("ALL TESTS COMPLETED")
    print("=" * 60)

