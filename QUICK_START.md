# Quick Start Guide

## Installation

1. Install Python 3.7 or higher
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

Start the Streamlit interface:
```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## Running Tests

Run the test suite:
```bash
python test_cases.py
```

## Project Structure

- `lexical_analyzer.py` - DFA-based tokenizer
- `syntax_analyzer.py` - Recursive descent parser
- `semantic_analyzer.py` - Symbol table and type checker
- `app.py` - Streamlit web interface
- `test_cases.py` - Test suite with 5 test cases

## Features Demonstrated

1. **Lexical Analysis**: Tokenization with DFA state machine
2. **Syntax Analysis**: Parse tree construction
3. **Semantic Analysis**: Symbol table with scope management

## Sample Code

Try this in the application:

```python
int x = 10;
int y = 20;
int result = x + y;
print(result);
```

