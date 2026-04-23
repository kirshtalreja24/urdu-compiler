# Handwritten Design Documents - Creation Guide

This guide helps you create the handwritten design documents required for submission.

## What to Create

You need to create **one handwritten artifact** for each phase:

1. **Lexical Phase**: DFA/transition table OR regex grouping
2. **Syntax Phase**: At least two parse-tree derivations
3. **Semantic Phase**: Sample symbol-table fill-in with scope example

## 1. Lexical Phase Document

### Option A: DFA Transition Table

Create a table showing state transitions:

```
┌──────────────┬──────────────────┬─────────────┬──────────────┐
│ Current State│ Input Character  │ Next State  │    Action    │
├──────────────┼──────────────────┼─────────────┼──────────────┤
│ START        │ letter or '_'   │ IDENTIFIER  │ -            │
│ START        │ digit (0-9)      │ NUMBER      │ -            │
│ START        │ '"'              │ STRING      │ -            │
│ IDENTIFIER   │ letter/digit/_   │ IDENTIFIER  │ -            │
│ IDENTIFIER   │ other            │ START       │ Emit token   │
│ NUMBER       │ digit            │ NUMBER      │ -            │
│ NUMBER       │ '.'              │ FLOAT       │ -            │
│ NUMBER       │ other            │ START       │ Emit INTEGER│
│ FLOAT        │ digit            │ FLOAT       │ -            │
│ FLOAT        │ other            │ START       │ Emit FLOAT   │
│ STRING       │ any except '"'   │ STRING      │ -            │
│ STRING       │ '"'              │ START       │ Emit STRING  │
└──────────────┴──────────────────┴─────────────┴──────────────┘
```

### Option B: DFA State Diagram

Draw circles for states and arrows for transitions:

```
        [letter/_]
    START ────────> IDENTIFIER
     │                  │
     │                  │ [letter/digit/_]
     │                  │
     │                  ▼
     │              [other] ──> Emit IDENTIFIER/KEYWORD
     │
     │ [digit]
     ├──────────> NUMBER
     │               │
     │               │ [digit]
     │               │
     │               ▼
     │            ['.'] ──> FLOAT ──> [digit] ──> Emit FLOAT
     │               │
     │               │ [other]
     │               └──> Emit INTEGER
     │
     │ ['"']
     └──────────> STRING ──> [any] ──> ['"'] ──> Emit STRING
```

### Option C: Regex Grouping

List regex patterns for each token group:

```
Keywords:     (int|float|string|bool|if|else|while|for|return|function|var|true|false|print)
Identifiers:  [a-zA-Z_][a-zA-Z0-9_]*
Integers:     [0-9]+
Floats:       [0-9]+\.[0-9]+
Strings:      "[^"]*"
Operators:    (\+|\-|\*|/|==|!=|<=|>=|&&|\|\||!|=|<|>)
Punctuation:  (;|,|\(|\)|\{|\}|\[|\])
```

**Choose ONE of the above options** and create it by hand.

## 2. Syntax Phase Document

Create **at least two parse-tree derivations** showing how your parser builds parse trees.

### Example 1: Simple Declaration

**Source Code:**
```
int x = 10;
```

**Hand-drawn Parse Tree:**
```
                    PROGRAM
                       │
                  statement_list
                       │
                  DECLARATION
            ┌──────────┼──────────┐
            │          │          │
          TYPE    IDENTIFIER  expression
            │          │          │
          'int'       'x'      INTEGER
                                    │
                                   '10'
```

### Example 2: If-Else Statement

**Source Code:**
```
int age = 18;
if (age >= 18) {
    print("Adult");
} else {
    print("Minor");
}
```

**Hand-drawn Parse Tree:**
```
                              PROGRAM
                                 │
                          statement_list
                    ┌────────────┼────────────┐
                    │                         │
              DECLARATION              IF_STATEMENT
         ┌──────────┼──────────┐      ┌───────┼──────────────┐
         │          │          │      │       │              │
       TYPE    IDENTIFIER  expression condition THEN_BLOCK ELSE_BLOCK
         │          │          │      │       │              │
       'int'      'age'    INTEGER  BINARY_OP statement_list statement_list
                        │      │       │       │              │
                       '18'  'age'   '>='  PRINT_STATEMENT PRINT_STATEMENT
                                    │       │              │
                                  '18'   expression    expression
                                           │              │
                                        STRING         STRING
                                           │              │
                                        "Adult"        "Minor"
```

**Tips:**
- Use boxes or circles for nodes
- Draw lines connecting parent to children
- Label each node with its type
- Show terminal values (tokens) at leaves
- Make it clear and readable

## 3. Semantic Phase Document

Create a **symbol-table fill-in example** showing step-by-step how the symbol table is built.

### Example: Symbol Table Construction

**Source Code:**
```
int x = 10;
int y = 20;
if (x > 5) {
    int z = x + y;
    print(z);
}
```

**Hand-drawn Symbol Table Fill-in:**

Create a table showing each step:

```
┌──────┬──────────────┬──────────┬──────────┬──────┬─────────────────────────────┐
│ Step │    Action    │  Scope   │ Variable │ Type │   Symbol Table State        │
├──────┼──────────────┼──────────┼──────────┼──────┼─────────────────────────────┤
│  1   │ Declare x   │  global  │    x     │ int  │ global: {x: int, line 1}     │
│  2   │ Declare y   │  global  │    y     │ int  │ global: {x: int, y: int}    │
│  3   │ Enter if    │ local_0  │    -     │  -   │ Enter scope: local_0         │
│  4   │ Lookup x    │ local_0  │    x     │ int  │ Found in global              │
│  5   │ Declare z   │ local_0  │    z     │ int  │ local_0: {z: int, line 4}    │
│  6   │ Lookup x    │ local_0  │    x     │ int  │ Found in global              │
│  7   │ Lookup y    │ local_0  │    y     │ int  │ Found in global              │
│  8   │ Exit if     │    -     │    -     │  -   │ Exit scope: local_0         │
└──────┴──────────────┴──────────┴──────────┴──────┴─────────────────────────────┘
```

**Scope Hierarchy Diagram:**

```
Global Scope
├── x (int, line 1)
└── y (int, line 2)
    │
    └── local_0 (if block)
        └── z (int, line 4)
```

## Submission Format

1. **Handwritten or neatly drawn** (not computer-generated)
2. **Clear and readable** - use rulers for tables, clear handwriting
3. **Scanned or photographed** - high quality, readable images
4. **One document per phase** (or combined in one document with clear sections)
5. **Include your name and student ID** on each page

## Tips for Creating Handwritten Documents

1. **Use graph paper** for diagrams and tables
2. **Use different colors** for different node types (optional but helpful)
3. **Label everything clearly** - states, transitions, nodes, scopes
4. **Show step-by-step** - especially for parse trees and symbol tables
5. **Include examples** - use actual code from your test cases
6. **Be neat** - take your time, use erasers if needed

## Reference Files

See the `DESIGN_DOCUMENTS/` folder for detailed examples:
- `LEXICAL_PHASE.md` - DFA table and regex patterns
- `SYNTAX_PHASE.md` - Grammar rules and parse tree examples
- `SEMANTIC_PHASE.md` - Symbol table examples and scope hierarchy

Use these as references when creating your handwritten documents.

