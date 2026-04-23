# Submission Checklist

Use this checklist to ensure all deliverables are complete before submission.

## ✅ Deliverables Checklist

### 1. Handwritten Design Documents

#### Lexical Phase
- [ ] DFA/Transition Table OR Regex Grouping
- [ ] Clear and readable (scanned/photographed)
- [ ] Shows state transitions or regex patterns
- [ ] Includes example tokenization

#### Syntax Phase
- [ ] At least 2 parse tree derivations
- [ ] Shows complete parse trees with nodes and connections
- [ ] Includes grammar rules
- [ ] Clear and readable (scanned/photographed)

#### Semantic Phase
- [ ] Symbol table fill-in example
- [ ] Step-by-step construction shown
- [ ] Scope hierarchy diagram
- [ ] Shows scope resolution
- [ ] Clear and readable (scanned/photographed)

**Note:** All handwritten documents should include your name and student ID.

### 2. Printed Code with Annotations

- [ ] `lexical_analyzer.py` printed (fully annotated)
- [ ] `syntax_analyzer.py` printed (fully annotated)
- [ ] `semantic_analyzer.py` printed (fully annotated)
- [ ] Code includes:
  - [ ] Module docstrings
  - [ ] Class docstrings
  - [ ] Method docstrings
  - [ ] Inline comments for complex logic
  - [ ] Algorithm explanations

**Printing Tips:**
- Use line numbers
- Use readable font (monospace recommended)
- Staple or bind pages together
- Add cover page with project info

### 3. Git Repository (or Zip)

#### Option A: Git Repository
- [ ] Git repository initialized
- [ ] All source files committed
- [ ] Commit history shows development process
- [ ] Repository includes:
  - [ ] Source code files
  - [ ] Documentation files
  - [ ] Design documents
  - [ ] Test cases
  - [ ] README.md

**To set up Git repository:**
```bash
# Windows
setup_git.bat

# Linux/Mac
bash setup_git.sh
```

#### Option B: Zip File
- [ ] Create zip file with all project files
- [ ] Include:
  - [ ] All .py files
  - [ ] Documentation (.md files)
  - [ ] Design documents
  - [ ] Test cases
  - [ ] README.md
  - [ ] requirements.txt
  - [ ] .git folder (if using git)

**Zip file name:** `Compiler_Construction_Project_[TeamName].zip`

### 4. Demonstration and Viva

- [ ] Prepare at least 3 unique test cases
- [ ] Test cases demonstrate:
  - [ ] Lexical analysis (tokenization)
  - [ ] Syntax analysis (parse trees)
  - [ ] Semantic analysis (symbol table, type checking)
- [ ] Streamlit app runs successfully
- [ ] Can demonstrate compilation process
- [ ] Can explain each phase

**Test Cases to Prepare:**
1. Simple arithmetic operations
2. Control flow (if/else or while loop)
3. Type checking and scope management

### 5. Reflection Document

- [ ] 1-page reflection written
- [ ] Includes:
  - [ ] What you learned
  - [ ] Challenges faced
  - [ ] What you would improve
  - [ ] How phases interact

## File Organization

### Project Structure
```
Compiler Construction Project/
├── lexical_analyzer.py          # Phase 1: Lexical Analysis
├── syntax_analyzer.py           # Phase 2: Syntax Analysis
├── semantic_analyzer.py         # Phase 3: Semantic Analysis
├── app.py                       # Streamlit interface
├── test_cases.py                # Test suite
├── requirements.txt             # Dependencies
├── README.md                    # Project documentation
├── DESIGN_DOCUMENTS/            # Design document references
│   ├── LEXICAL_PHASE.md
│   ├── SYNTAX_PHASE.md
│   └── SEMANTIC_PHASE.md
├── HANDWRITTEN_DOCUMENTS/       # Your handwritten docs (scans/photos)
│   ├── lexical_design.pdf
│   ├── syntax_design.pdf
│   └── semantic_design.pdf
└── .git/                        # Git repository (if using git)
```

## Pre-Submission Testing

Before submitting, verify:

- [ ] All code runs without errors
- [ ] Streamlit app launches successfully
- [ ] Test cases pass
- [ ] All three phases work correctly
- [ ] Documentation is complete
- [ ] Design documents are ready
- [ ] Git repository has commit history (if using git)

## Submission Package

Your final submission should include:

1. **Handwritten Design Documents** (scanned/photographed)
   - Lexical phase document
   - Syntax phase document
   - Semantic phase document

2. **Printed Code** (stapled/bound)
   - lexical_analyzer.py
   - syntax_analyzer.py
   - semantic_analyzer.py

3. **Digital Submission** (Git repo or Zip)
   - All source code
   - Documentation
   - Design document references
   - Test cases

4. **Reflection Document** (1 page)

5. **Demonstration** (during viva)
   - Streamlit app running
   - 3+ test cases demonstrated
   - Explanation of each phase

## Quick Commands

### Test the Compiler
```bash
python test_cases.py
```

### Run Streamlit App
```bash
streamlit run app.py
```

### Set Up Git Repository
```bash
# Windows
setup_git.bat

# Linux/Mac
bash setup_git.sh
```

### Create Zip File
```bash
# Windows PowerShell
Compress-Archive -Path * -DestinationPath Compiler_Project.zip

# Linux/Mac
zip -r Compiler_Project.zip . -x "*.git*"
```

## Final Notes

- Double-check all files are included
- Verify handwritten documents are readable
- Ensure code is properly annotated
- Test everything before submission
- Prepare for viva demonstration

Good luck with your submission! 🎉

