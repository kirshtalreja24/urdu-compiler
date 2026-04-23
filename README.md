# Compiler Construction Project

A complete compiler implementation in Python with Streamlit interface, demonstrating all **six phases** of compilation: Lexical Analysis, Syntax Analysis, Semantic Analysis, Intermediate Code Generation, Optimization, and Code Generation.

## Features

### 1. Lexical Analyzer (Scanner)
- **DFA-based tokenization** with state transitions
- Recognizes keywords, identifiers, numbers (int/float), strings
- Handles operators and punctuation
- Error reporting for invalid characters

### 2. Syntax Analyzer (Parser)
- **Recursive descent parser** implementing top-down parsing
- Builds **Abstract Syntax Tree (AST)** from tokens
- Supports grammar rules for:
  - Variable declarations and assignments
  - Arithmetic and logical expressions
  - Control flow (if/else, while loops)
  - Print statements

### 3. Semantic Analyzer
- **Symbol table management** with scope tracking
- **Type checking** for variables and expressions
- **Scope validation** (global and local scopes)
- Use-before-declaration detection
- Type compatibility checking

### 4. Intermediate Code Generator
- **Three-address code (TAC)** generation
- Each instruction has at most one operator
- Temporary variable management
- Control flow with labels and jumps

### 5. Optimizer
- **Constant folding**: Evaluate constant expressions at compile time
- **Dead code elimination**: Remove unreachable code
- **Constant propagation**: Replace variables with known constants

### 6. Code Generator
- **Executable code generation** from optimized TAC
- **Interpreter implementation** for code execution
- Program output generation
- Memory state tracking

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the Streamlit application:
```bash
streamlit run app.py
```

## Usage

1. Open the application in your browser (usually `http://localhost:8501`)
2. Enter source code in the text area or select a sample program from the sidebar
3. Click "Compile" to see results from all six phases:
   - **Lexical Analysis**: View tokens and token groups
   - **Syntax Analysis**: View parse tree and AST
   - **Semantic Analysis**: View symbol table and type checking results
   - **Intermediate Code**: View three-address code generation
   - **Optimization**: View optimized code with optimizations applied
   - **Code Generation**: View generated executable code and program output
   - **Summary**: Overall compilation status

## Sample Programs

The application includes 5 sample programs:
1. Simple Arithmetic
2. If-Else Statement
3. While Loop
4. Type Checking
5. Complex Expression

## Language Grammar

The compiler supports a simplified language with:

- **Data Types**: `int`, `float`, `string`, `bool`
- **Variables**: Declaration and assignment
- **Expressions**: Arithmetic (`+`, `-`, `*`, `/`), Comparison (`<`, `>`, `==`, `!=`), Logical (`&&`, `||`, `!`)
- **Control Flow**: `if`/`else`, `while`
- **Output**: `print()` function

## Project Structure

```
.
├── lexical_analyzer.py           # Phase 1: Lexical Analysis
├── syntax_analyzer.py            # Phase 2: Syntax Analysis
├── semantic_analyzer.py          # Phase 3: Semantic Analysis
├── intermediate_code_generator.py  # Phase 4: Intermediate Code Generation
├── optimizer.py                  # Phase 5: Optimization
├── code_generator.py             # Phase 6: Code Generation
├── app.py                        # Streamlit interface
├── test_cases.py                 # Test suite
├── requirements.txt              # Python dependencies
├── LANGUAGE_SPECIFICATION.md      # Language specification document
└── README.md                     # This file
```

## Compiler Phases

### Phase 1: Lexical Analysis
- Converts source code into tokens
- Uses DFA (Deterministic Finite Automaton) for state transitions
- Groups tokens by type (keywords, identifiers, literals, operators)

### Phase 2: Syntax Analysis
- Parses tokens according to grammar rules
- Builds parse tree (AST)
- Validates syntax correctness

### Phase 3: Semantic Analysis
- Constructs symbol table with scope information
- Performs type checking
- Validates variable declarations and usage
- Checks scope rules

### Phase 4: Intermediate Code Generation
- Generates three-address code (TAC) from AST
- Each instruction has at most one operator
- Creates temporary variables for intermediate results
- Handles control flow with labels and jumps

### Phase 5: Optimization
- Constant folding: Evaluates constant expressions at compile time
- Dead code elimination: Removes unreachable code
- Constant propagation: Replaces variables with known constants

### Phase 6: Code Generation
- Generates executable code from optimized TAC
- Implements interpreter for code execution
- Produces program output
- Tracks memory state

## Test Cases

The application includes 3+ unique test cases demonstrating:
1. Basic variable operations
2. Control flow structures
3. Type checking and conversions
4. Complex expressions
5. Scope management

## Deliverables

This project includes:
- ✅ Complete compiler implementation (all six phases)
- ✅ Annotated source code with detailed comments
- ✅ Streamlit interface for demonstration
- ✅ Multiple test cases
- ✅ Symbol table with scope examples
- ✅ Parse tree visualization
- ✅ Three-address code generation
- ✅ Code optimization
- ✅ Executable code generation and interpretation

## Notes

- The compiler performs complete compilation from source to execution
- Error messages include line numbers for debugging
- Symbol table shows scope hierarchy
- Parse trees are displayed in text format and JSON
- Three-address code is optimized before code generation
- Generated code can be executed to produce program output

## Author

Compiler Construction Project - Academic Assignment

