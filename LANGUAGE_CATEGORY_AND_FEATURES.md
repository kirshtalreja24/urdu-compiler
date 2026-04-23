# Language Category and Features

## Category: **Numerical Pattern Generation**

**SimpleScript** belongs to the **Numerical Pattern Generation** category, specifically designed for:
- **Fibonacci-like sequences** and similar mathematical patterns
- **Factorial-based computations** and recursive arithmetic
- **Custom arithmetic logic** for generating numerical sequences
- **Iterative pattern generation** using loops

## Why This Category?

### 1. Primary Focus on Numerical Computations
The language is optimized for numerical operations:
- Strong support for integer and float arithmetic
- Efficient loop constructs for sequence generation
- Variable management for pattern state

### 2. Pattern Generation Capabilities
The language includes Example 2 in the specification that demonstrates **Fibonacci-like pattern generation**:
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

### 3. Custom Arithmetic Logic
Supports complex arithmetic expressions for custom patterns:
- Arithmetic operations: `+`, `-`, `*`, `/`
- Comparison operations for conditional pattern rules
- Logical operations for pattern filtering

## Language Features

### Core Features

#### 1. **Variable System**
- **Types**: `int`, `float`, `string`, `bool`
- **Static typing**: Variables must be declared with a type
- **Scope management**: Global and local scopes
- **Initialization**: Variables initialized at declaration

**Use Case**: Store pattern state, counters, and intermediate values

#### 2. **Arithmetic Operations**
- Addition: `+`
- Subtraction: `-`
- Multiplication: `*`
- Division: `/`
- Operator precedence: `*`, `/` before `+`, `-`

**Use Case**: Perform calculations for pattern generation

#### 3. **Control Flow**
- **Conditional**: `if`/`else` statements
- **Loops**: `while` loops for iteration
- **Nested structures**: Support for nested control flow

**Use Case**: Generate patterns iteratively, apply conditional rules

#### 4. **Type System**
- **Static typing**: Type checking at compile time
- **Type compatibility**: `int` can be converted to `float`
- **Type safety**: Prevents type-related errors

**Use Case**: Ensure correct numerical computations

#### 5. **Output**
- **Print statements**: Display pattern results
- **Expression evaluation**: Print computed values

**Use Case**: Display generated patterns

### Pattern Generation Features

#### 1. **Iterative Pattern Generation**
```javascript
// Generate sequence: 0, 1, 2, 3, 4
int i = 0;
while (i < 5) {
    print(i);
    i = i + 1;
}
```

#### 2. **Fibonacci-like Sequences**
```javascript
// Fibonacci sequence generation
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

#### 3. **Custom Arithmetic Patterns**
```javascript
// Generate squares: 0, 1, 4, 9, 16
int i = 0;
while (i < 5) {
    int square = i * i;
    print(square);
    i = i + 1;
}
```

#### 4. **Conditional Pattern Rules**
```javascript
// Generate even numbers only
int i = 0;
while (i < 10) {
    if (i % 2 == 0) {
        print(i);
    }
    i = i + 1;
}
```

#### 5. **Mathematical Computations**
```javascript
// Calculate area of circle
float pi = 3.14;
int radius = 5;
float area = pi * radius * radius;
print(area);
```

## Example Use Cases

### 1. **Fibonacci Sequence Generation**
Generate Fibonacci numbers up to a certain count.

### 2. **Arithmetic Progressions**
Generate sequences like: 2, 4, 6, 8, 10...

### 3. **Geometric Patterns**
Generate sequences like: 1, 2, 4, 8, 16...

### 4. **Factorial Calculations**
Calculate factorial values (with loop-based approach).

### 5. **Prime Number Generation**
Generate prime numbers using arithmetic logic.

### 6. **Custom Mathematical Functions**
Implement custom arithmetic rules for pattern generation.

## Comparison with Other Categories

### ❌ Not Game Scripting
- No game-specific constructs (movement, scoring, sprites)
- No event handling or game loops
- Focus is on computation, not game logic

### ❌ Not Story/Dialogue DSL
- No dialogue management
- No narrative flow control
- No text-based story structures

### ❌ Not Matrix Operations
- No built-in matrix types
- No matrix-specific operations
- Would require manual implementation

### ❌ Not Pure Data Manipulation
- Limited string operations
- No array support (yet)
- Focus is numerical, not general data

### ✅ Numerical Pattern Generation
- **Perfect fit**: Designed for numerical sequences
- **Arithmetic focus**: Strong numerical computation support
- **Pattern generation**: Loops and variables for sequences
- **Custom logic**: Supports custom arithmetic rules

## Language Strengths for Pattern Generation

1. **Simple Syntax**: Easy to write pattern generation code
2. **Efficient Loops**: `while` loops perfect for iteration
3. **Type Safety**: Prevents numerical errors
4. **Flexible Arithmetic**: Supports complex expressions
5. **Output Control**: Print statements for pattern display

## Limitations

1. **No Arrays**: Cannot store sequences in arrays (future extension)
2. **No Functions**: Cannot define reusable pattern functions (future extension)
3. **No Recursion**: No recursive function calls
4. **Limited String Operations**: Basic string support only

## Summary

**SimpleScript** is a **Numerical Pattern Generation** language that excels at:
- ✅ Generating mathematical sequences (Fibonacci, arithmetic, geometric)
- ✅ Performing custom arithmetic computations
- ✅ Iterative pattern generation using loops
- ✅ Conditional pattern rules
- ✅ Mathematical calculations and transformations

The language is specifically designed to make it easy to write code that generates numerical patterns, making it ideal for educational purposes, mathematical exploration, and pattern-based computations.

