# Mini Language Specification

## Language Name: SimpleScript

**Category:** Numerical Pattern Generation

**Purpose:** A simple scripting language designed for generating numerical patterns (Fibonacci-like sequences, factorial-based computations, custom arithmetic logic) and performing basic numerical computations.

**Primary Use Cases:**
- Fibonacci and similar mathematical sequence generation
- Arithmetic and geometric progression generation
- Custom arithmetic pattern rules
- Iterative numerical computations
- Mathematical calculations and transformations

## 1. Lexical Rules

### Keywords
- Type keywords: `int`, `float`, `string`, `bool`
- Control flow: `if`, `else`, `while`, `for`
- Functions: `function`, `return`
- Variables: `var`
- Literals: `true`, `false`
- I/O: `print`

### Identifiers
- Must start with letter or underscore
- Can contain letters, digits, and underscores
- Case-sensitive
- Examples: `x`, `myVar`, `_temp`, `value123`

### Literals
- **Integers**: `0`, `123`, `-45`
- **Floats**: `3.14`, `-0.5`, `2.0`
- **Strings**: `"hello"`, `"world"`
- **Booleans**: `true`, `false`

### Operators
- Arithmetic: `+`, `-`, `*`, `/`
- Comparison: `==`, `!=`, `<`, `>`, `<=`, `>=`
- Logical: `&&`, `||`, `!`
- Assignment: `=`

### Punctuation
- `;` (semicolon) - statement terminator
- `,` (comma) - separator
- `(` `)` (parentheses) - expressions, function calls
- `{` `}` (braces) - blocks
- `[` `]` (brackets) - arrays (future)

### Comments
- Single-line: `// comment text`

## 2. Syntax (BNF Grammar)

```
program → statement_list
statement_list → statement statement_list | ε
statement → declaration | assignment | if_statement | while_statement | print_statement | function_declaration
declaration → type IDENTIFIER '=' expression ';'
assignment → IDENTIFIER '=' expression ';'
if_statement → 'if' '(' expression ')' '{' statement_list '}' ('else' '{' statement_list '}')?
while_statement → 'while' '(' expression ')' '{' statement_list '}'
print_statement → 'print' '(' expression ')' ';'
function_declaration → 'function' IDENTIFIER '(' parameter_list? ')' '{' statement_list '}'
parameter_list → type IDENTIFIER (',' type IDENTIFIER)*
expression → logical_or
logical_or → logical_and ('||' logical_and)*
logical_and → equality ('&&' equality)*
equality → comparison (('==' | '!=') comparison)*
comparison → term (('<' | '>' | '<=' | '>=') term)*
term → factor (('+' | '-') factor)*
factor → unary (('*' | '/') unary)*
unary → ('!' | '-')? primary
primary → IDENTIFIER | INTEGER | FLOAT | STRING | BOOLEAN | '(' expression ')'
```

## 3. Semantic Rules

### Type System
- **Static typing**: Variables must be declared with a type
- **Type compatibility**:
  - `int` can be implicitly converted to `float`
  - No other implicit conversions allowed
- **Type checking**: All expressions are type-checked

### Scope Rules
- **Global scope**: Variables declared at top level
- **Local scope**: Variables declared inside blocks (if/while/function)
- **Scope resolution**: Inner scopes can access outer scope variables
- **Variable shadowing**: Inner scope variables can shadow outer scope variables

### Variable Rules
- Variables must be declared before use
- Variables cannot be redeclared in the same scope
- Variables are initialized at declaration

### Expression Rules
- Arithmetic operations: `int + int = int`, `float + float = float`, `int + float = float`
- Comparison operations: Return `bool`
- Logical operations: Operate on `bool` values
- String concatenation: `string + string = string`

## 4. Example Programs

### Example 1: Simple Arithmetic
```javascript
int x = 10;
int y = 20;
int z = x + y;
print(z);
```
**Expected Output:** `30`

### Example 2: Pattern Generation (Fibonacci-like)
```javascript
int a = 0;
int b = 1;
int i = 0;
while (i < 10) {
    print(a);
    int temp = a + b;
    a = b;
    b = temp;
    i = i + 1;
}
```
**Expected Output:** `0 1 1 2 3 5 8 13 21 34`

### Example 3: Conditional Logic
```javascript
int age = 18;
if (age >= 18) {
    print("Adult");
} else {
    print("Minor");
}
```
**Expected Output:** `Adult`

### Example 4: Type Checking
```javascript
float pi = 3.14;
int radius = 5;
float area = pi * radius * radius;
print(area);
```
**Expected Output:** `78.5`

### Example 5: Boolean Logic
```javascript
bool isPositive = true;
bool isEven = false;
bool result = isPositive && !isEven;
print(result);
```
**Expected Output:** `true`

## 5. Language Features

### Supported Features
- ✅ Variable declarations and assignments
- ✅ Arithmetic expressions
- ✅ Comparison and logical expressions
- ✅ Conditional statements (if/else)
- ✅ Loops (while)
- ✅ Type system (int, float, string, bool)
- ✅ Scope management
- ✅ Print statements

### Future Extensions (Not Implemented)
- Function definitions and calls
- Arrays
- String operations
- Input statements
- For loops

## 6. Compilation Phases

1. **Lexical Analysis**: Tokenize source code
2. **Syntax Analysis**: Build parse tree (AST)
3. **Semantic Analysis**: Type checking and symbol table
4. **Intermediate Code Generation**: Generate three-address code
5. **Optimization**: Constant folding, dead code elimination
6. **Code Generation**: Generate executable/interpreter code

