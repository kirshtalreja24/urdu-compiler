# Design Documents Guide

This guide explains what should be included in your handwritten design documents for submission.

## 1. Lexical Analysis Design Document

### DFA/Transition Table
Create a table showing state transitions:

| Current State | Input Character | Next State | Action |
|--------------|-----------------|------------|--------|
| START | letter | IDENTIFIER | - |
| START | digit | NUMBER | - |
| START | " | STRING | - |
| START | operator | OPERATOR | - |
| IDENTIFIER | letter/digit/_ | IDENTIFIER | - |
| IDENTIFIER | other | START | Emit token |
| NUMBER | digit | NUMBER | - |
| NUMBER | . | FLOAT | - |
| FLOAT | digit | FLOAT | - |
| ... | ... | ... | ... |

### Regex Grouping
Document the regular expressions used:

- **Keywords**: `(int|float|string|bool|if|else|while|for|return|function|var|true|false|print)`
- **Identifier**: `[a-zA-Z_][a-zA-Z0-9_]*`
- **Integer**: `[0-9]+`
- **Float**: `[0-9]+\.[0-9]+`
- **String**: `"[^"]*"`
- **Operators**: `(\+|\-|\*|/|==|!=|<=|>=|&&|\|\||!)`

## 2. Syntax Analysis Design Document

### Parse Tree Derivations
Include at least 2 complete parse tree examples:

#### Example 1: Simple Assignment
```
PROGRAM
└── DECLARATION
    ├── TYPE (int)
    ├── IDENTIFIER (x)
    └── INTEGER (10)
```

#### Example 2: If Statement
```
PROGRAM
└── IF_STATEMENT
    ├── BINARY_OP (>=)
    │   ├── IDENTIFIER (age)
    │   └── INTEGER (18)
    ├── THEN_BLOCK
    │   └── PRINT_STATEMENT
    │       └── STRING ("Adult")
    └── ELSE_BLOCK
        └── PRINT_STATEMENT
            └── STRING ("Minor")
```

### Grammar Rules
Document the grammar productions:

```
program → statement_list
statement_list → statement statement_list | ε
statement → declaration | assignment | if_statement | while_statement | print_statement
declaration → type IDENTIFIER '=' expression ';'
assignment → IDENTIFIER '=' expression ';'
if_statement → 'if' '(' expression ')' '{' statement_list '}' ('else' '{' statement_list '}')?
while_statement → 'while' '(' expression ')' '{' statement_list '}'
expression → logical_or
logical_or → logical_and ('||' logical_and)*
...
```

## 3. Semantic Analysis Design Document

### Symbol Table Fill-in Example
Show how the symbol table is constructed:

**Source Code:**
```
int x = 10;
if (x > 5) {
    int y = 20;
    print(y);
}
```

**Symbol Table Construction:**

| Step | Scope | Variable | Type | Declared At | Action |
|------|-------|----------|------|-------------|--------|
| 1 | global | x | int | Line 1 | Declare |
| 2 | global | x | int | Line 1 | Lookup (use) |
| 3 | local_0 | y | int | Line 3 | Declare |
| 4 | local_0 | y | int | Line 3 | Lookup (use) |

### Scope Example
Demonstrate scope hierarchy:

```
Global Scope
├── x (int) - Line 1
└── local_0 (if block)
    └── y (int) - Line 3
```

**Scope Rules:**
- Variables in inner scopes can access outer scope variables
- Variables in outer scopes cannot access inner scope variables
- Same variable name can exist in different scopes (shadowing)

## Tips for Handwritten Documents

1. **Use clear diagrams**: Draw DFA states as circles with transitions as arrows
2. **Show step-by-step**: For parse trees, show how each production rule is applied
3. **Include examples**: Use actual code snippets from your test cases
4. **Be neat**: Use rulers for tables, clear handwriting
5. **Label everything**: Clearly label states, transitions, nodes, scopes

## What to Include

### For Lexical Phase:
- [ ] DFA state diagram or transition table
- [ ] Regex patterns for token groups
- [ ] Example tokenization of a small program

### For Syntax Phase:
- [ ] At least 2 complete parse tree derivations
- [ ] Grammar production rules
- [ ] Example showing how parser builds AST

### For Semantic Phase:
- [ ] Symbol table fill-in example (step by step)
- [ ] Scope hierarchy diagram
- [ ] Example showing scope resolution

## Submission Format

- Handwritten (or neatly drawn)
- Scanned or photographed (clear, readable)
- One document per phase (or combined in one document)
- Include your name and student ID

