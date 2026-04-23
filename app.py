"""
Compiler Construction Project - Streamlit Interface
===================================================
Main Streamlit application for demonstrating all six compiler phases:
1. Lexical Analysis (Scanner)
2. Syntax Analysis (Parser)
3. Semantic Analysis (Symbol Table & Type Checking)
4. Intermediate Code Generation (Three-Address Code)
5. Optimization (Constant Folding, Dead Code Elimination)
6. Code Generation (Interpreter/Executable)
"""

import streamlit as st
import json
from lexical_analyzer import LexicalAnalyzer
from syntax_analyzer import SyntaxAnalyzer
from semantic_analyzer import SemanticAnalyzer
from intermediate_code_generator import IntermediateCodeGenerator
from optimizer import Optimizer
from code_generator import CodeGenerator


def display_parse_tree(node, level=0):
    """Display parse tree in a readable format"""
    indent = "  " * level
    if node.value is not None:
        return f"{indent}{node.node_type}: {node.value}\n"
    else:
        result = f"{indent}{node.node_type}\n"
        for child in node.children:
            result += display_parse_tree(child, level + 1)
        return result


def display_symbol_table(symbol_table):
    """Format symbol table for display"""
    result = []
    tables = symbol_table.get_all_symbols()
    
    for scope_name, symbols in tables.items():
        if symbols:
            result.append(f"\n**Scope: {scope_name}**")
            result.append("| Variable | Type | Declared At | Scope |")
            result.append("|----------|------|-------------|-------|")
            for var_name, info in symbols.items():
                result.append(
                    f"| {var_name} | {info['type']} | Line {info['declared_at']} | {info['scope']} |"
                )
    
    return "\n".join(result) if result else "No symbols declared"


# Page configuration
st.set_page_config(
    page_title="Compiler Construction Project",
    page_icon="🔧",
    layout="wide"
)

st.title("🔧 Compiler Construction Project")
st.markdown("""
This application demonstrates a complete compiler with all six phases:
1. **Lexical Analysis** - Tokenization using DFA
2. **Syntax Analysis** - Parse tree construction using recursive descent
3. **Semantic Analysis** - Symbol table and type checking
4. **Intermediate Code Generation** - Three-address code generation
5. **Optimization** - Constant folding and dead code elimination
6. **Code Generation** - Executable code generation and interpretation
""")

# Sidebar for sample programs
st.sidebar.header("📝 Sample Programs")

sample_programs = {
    "Example 1: Simple Arithmetic": """
Adad x = 10;
Adad y = 20;
Adad z = x + y;
Dikhao(z);
""",
    "Example 2: If-Else Statement": """
Adad age = 18;
Agar (age >= 18) {
    Dikhao("Adult");
} Warna {
    Dikhao("Minor");
}
""",
    "Example 3: While Loop": """
Adad i = 0;
JabTak (i < 5) {
    Dikhao(i);
    i = i + 1;
}
""",
    "Example 4: Type Checking": """
TairtaAdad pi = 3.14;
Adad radius = 5;
TairtaAdad area = pi * radius * radius;
Dikhao(area);
""",
    "Example 5: Complex Expression": """
Adad a = 10;
Adad b = 20;
Adad c = 30;
Adad result = a + b * c;
SahiGhalat isPositive = result > 0;
Dikhao(isPositive);
"""
}

# Initialize session state
if 'source_code' not in st.session_state:
    st.session_state.source_code = sample_programs["Example 1: Simple Arithmetic"]

for name, code in sample_programs.items():
    if st.sidebar.button(name, key=name):
        st.session_state.source_code = code

# Main input area
st.header("📄 Source Code Input")
source_code = st.text_area(
    "Enter your source code:",
    height=200,
    value=st.session_state.source_code,
    key="source_code"
)

if st.button("🚀 Compile", type="primary"):
    if not source_code.strip():
        st.error("Please enter some source code!")
    else:
        # Initialize tabs for each phase
        tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
            "🔍 Lexical Analysis",
            "🌳 Syntax Analysis",
            "✅ Semantic Analysis",
            "⚙️ Intermediate Code",
            "🚀 Optimization",
            "💻 Code Generation",
            "📊 Summary"
        ])
        
        # ========== LEXICAL ANALYSIS ==========
        with tab1:
            st.subheader("Tokenization Results")
            
            lexer = LexicalAnalyzer(source_code)
            tokens = lexer.tokenize()
            
            # Display tokens in a table
            if tokens:
                token_data = []
                for token in tokens:
                    if token.type.value != "EOF":
                        token_data.append({
                            "Type": token.type.value,
                            "Value": token.value,
                            "Line": token.line,
                            "Column": token.column
                        })
                
                st.dataframe(token_data, use_container_width=True)
                
                # Display token count
                st.info(f"**Total tokens:** {len([t for t in tokens if t.type.value != 'EOF'])}")
            
            # Display errors
            lexical_errors = lexer.get_errors()
            if lexical_errors:
                st.error("**Lexical Errors:**")
                for error in lexical_errors:
                    st.error(f"  - {error}")
            else:
                st.success("✅ No lexical errors found!")
            
            # Display token grouping
            st.subheader("Token Groups")
            token_groups = {}
            for token in tokens:
                if token.type.value != "EOF":
                    group = token.type.value
                    if group not in token_groups:
                        token_groups[group] = []
                    token_groups[group].append(token.value)
            
            for group, values in token_groups.items():
                st.write(f"**{group}:** {', '.join(values)}")
        
        # ========== SYNTAX ANALYSIS ==========
        with tab2:
            st.subheader("Parse Tree")
            
            parser = SyntaxAnalyzer(tokens)
            ast = parser.parse()
            
            if ast:
                # Display parse tree
                st.code(display_parse_tree(ast), language="text")
                
                # Display AST as JSON
                with st.expander("View AST as JSON"):
                    st.json(ast.to_dict())
                
                # Display parse tree visualization info
                st.info("""
                **Parse Tree Structure:**
                - Each node represents a grammar production
                - Leaf nodes are terminals (tokens)
                - Internal nodes are non-terminals (grammar rules)
                """)
            else:
                st.error("Failed to parse the source code")
            
            # Display syntax errors
            syntax_errors = parser.get_errors()
            if syntax_errors:
                st.error("**Syntax Errors:**")
                for error in syntax_errors:
                    st.error(f"  - {error}")
            else:
                st.success("✅ No syntax errors found!")
        
        # ========== SEMANTIC ANALYSIS ==========
        with tab3:
            if ast and len(syntax_errors) == 0:
                st.subheader("Symbol Table")
                
                semantic_analyzer = SemanticAnalyzer(ast)
                is_valid = semantic_analyzer.analyze()
                
                # Display symbol table
                symbol_table_display = display_symbol_table(semantic_analyzer.get_symbol_table())
                st.markdown(symbol_table_display)
                
                # Display semantic errors
                semantic_errors = semantic_analyzer.get_errors()
                if semantic_errors:
                    st.error("**Semantic Errors:**")
                    for error in semantic_errors:
                        st.error(f"  - {error}")
                
                # Display warnings
                semantic_warnings = semantic_analyzer.get_warnings()
                if semantic_warnings:
                    st.warning("**Semantic Warnings:**")
                    for warning in semantic_warnings:
                        st.warning(f"  - {warning}")
                
                if not semantic_errors:
                    st.success("✅ No semantic errors found!")
                
                # Scope example
                st.subheader("Scope Analysis")
                st.info("""
                **Scope Rules:**
                - Global scope: Variables declared at top level
                - Local scope: Variables declared inside blocks (if/while)
                - Inner scopes can access outer scope variables
                - Variables must be declared before use
                """)
            else:
                st.warning("⚠️ Please fix syntax errors before semantic analysis")
        
        # ========== INTERMEDIATE CODE GENERATION ==========
        with tab4:
            if ast and len(syntax_errors) == 0:
                semantic_analyzer = SemanticAnalyzer(ast)
                semantic_analyzer.analyze()
                semantic_errors = semantic_analyzer.get_errors()
                
                if len(semantic_errors) == 0:
                    st.subheader("Three-Address Code (TAC)")
                    
                    # Generate intermediate code
                    icg = IntermediateCodeGenerator(ast)
                    tac_list = icg.generate()
                    
                    if tac_list:
                        st.code(icg.format_tac(), language="text")
                        
                        st.info("""
                        **Three-Address Code Format:**
                        - Each instruction has at most one operator and three operands
                        - Format: `result = operand1 operator operand2`
                        - Temporary variables (t0, t1, ...) store intermediate results
                        - Labels (L0, L1, ...) mark control flow points
                        """)
                        
                        # Show TAC statistics
                        st.metric("Total TAC Instructions", len(tac_list))
                    else:
                        st.warning("No intermediate code generated")
                else:
                    st.warning("⚠️ Please fix semantic errors before code generation")
            else:
                st.warning("⚠️ Please fix syntax errors before code generation")
        
        # ========== OPTIMIZATION ==========
        with tab5:
            if ast and len(syntax_errors) == 0:
                semantic_analyzer = SemanticAnalyzer(ast)
                semantic_analyzer.analyze()
                semantic_errors = semantic_analyzer.get_errors()
                
                if len(semantic_errors) == 0:
                    st.subheader("Optimized Three-Address Code")
                    
                    # Generate and optimize code
                    icg = IntermediateCodeGenerator(ast)
                    tac_list = icg.generate()
                    
                    if tac_list:
                        optimizer = Optimizer(tac_list)
                        optimized_tac = optimizer.optimize()
                        
                        st.code(optimizer.format_optimized_tac(), language="text")
                        
                        st.info("""
                        **Optimizations Applied:**
                        - **Constant Folding**: Evaluate constant expressions at compile time
                          Example: `t1 = 5 + 3` → `t1 = 8`
                        - **Dead Code Elimination**: Remove unreachable code after jumps
                        - **Constant Propagation**: Replace variables with known constant values
                        """)
                        
                        # Show optimization statistics
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Original Instructions", len(tac_list))
                        with col2:
                            st.metric("Optimized Instructions", len(optimized_tac))
                            reduction = len(tac_list) - len(optimized_tac)
                            if reduction > 0:
                                st.success(f"Reduced by {reduction} instructions")
                    else:
                        st.warning("No code to optimize")
                else:
                    st.warning("⚠️ Please fix semantic errors before optimization")
            else:
                st.warning("⚠️ Please fix syntax errors before optimization")
        
        # ========== CODE GENERATION ==========
        with tab6:
            if ast and len(syntax_errors) == 0:
                semantic_analyzer = SemanticAnalyzer(ast)
                semantic_analyzer.analyze()
                semantic_errors = semantic_analyzer.get_errors()
                
                if len(semantic_errors) == 0:
                    st.subheader("Generated Executable Code")
                    
                    # Generate, optimize, and execute
                    icg = IntermediateCodeGenerator(ast)
                    tac_list = icg.generate()
                    
                    if tac_list:
                        optimizer = Optimizer(tac_list)
                        optimized_tac = optimizer.optimize()
                        
                        code_generator = CodeGenerator(optimized_tac)
                        generated_code = code_generator.generate()
                        
                        st.code(generated_code, language="python")
                        
                        # Automatically execute the code
                        st.markdown("---")
                        st.subheader("📤 Program Output")
                        
                        # Execute the program automatically
                        exec_code_generator = CodeGenerator(optimized_tac)
                        output = exec_code_generator.execute()
                        
                        if output:
                            # Display output in a nice box
                            output_text = "\n".join(str(line) for line in output)
                            st.success("✅ **Execution Successful!**")
                            st.code(output_text, language="text")
                            
                            # Show output as individual lines
                            with st.expander("View Output Details"):
                                for i, line in enumerate(output, 1):
                                    st.write(f"Line {i}: `{line}`")
                        else:
                            st.info("ℹ️ Program executed but produced no output")
                        
                        # Show final memory state
                        memory = exec_code_generator.get_memory_state()
                        if memory:
                            st.markdown("---")
                            st.subheader("💾 Final Memory State")
                            st.json(memory)
                            
                            # Show memory as table
                            with st.expander("View Memory as Table"):
                                memory_data = [{"Variable": k, "Value": v, "Type": type(v).__name__} for k, v in memory.items()]
                                st.dataframe(memory_data, use_container_width=True)
                        
                        st.info("""
                        **Code Generation:**
                        - Generates executable code from optimized three-address code
                        - Implements a simple stack-based interpreter
                        - Executes TAC instructions to produce program output
                        """)
                    else:
                        st.warning("No code to generate")
                else:
                    st.warning("⚠️ Please fix semantic errors before code generation")
            else:
                st.warning("⚠️ Please fix syntax errors before code generation")
        
        # ========== SUMMARY ==========
        with tab7:
            st.subheader("Compilation Summary")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Lexical Errors", len(lexical_errors))
            
            with col2:
                st.metric("Syntax Errors", len(syntax_errors))
            
            with col3:
                if ast and len(syntax_errors) == 0:
                    semantic_analyzer = SemanticAnalyzer(ast)
                    semantic_analyzer.analyze()
                    st.metric("Semantic Errors", len(semantic_analyzer.get_errors()))
                else:
                    st.metric("Semantic Errors", "N/A")
            
            # Overall status
            total_errors = len(lexical_errors) + len(syntax_errors)
            if ast and len(syntax_errors) == 0:
                semantic_analyzer = SemanticAnalyzer(ast)
                semantic_analyzer.analyze()
                total_errors += len(semantic_analyzer.get_errors())
            
            if total_errors == 0:
                st.success("🎉 **Compilation Successful!** All phases passed.")
            else:
                st.error(f"❌ **Compilation Failed** with {total_errors} error(s)")
            
            # Phase details
            st.subheader("All Six Compiler Phases")
            st.markdown("""
            **1. Lexical Analysis (Scanner)**
            - Tokenized input into tokens
            - Used DFA-based state machine
            - Recognized keywords, identifiers, literals, operators
            
            **2. Syntax Analysis (Parser)**
            - Built parse tree using recursive descent
            - Validated grammar rules
            - Constructed Abstract Syntax Tree (AST)
            
            **3. Semantic Analysis**
            - Built symbol table with scope tracking
            - Performed type checking
            - Validated variable declarations and usage
            
            **4. Intermediate Code Generation**
            - Generated three-address code (TAC)
            - Each instruction has at most one operator
            - Created temporary variables for intermediate results
            
            **5. Optimization**
            - Constant folding: Evaluate constant expressions
            - Dead code elimination: Remove unreachable code
            - Constant propagation: Replace variables with constants
            
            **6. Code Generation**
            - Generated executable code
            - Implemented interpreter for TAC execution
            - Produced program output
            """)

# Footer
st.markdown("---")
st.markdown("""
**Compiler Construction Project** | 
Lexical Analyzer | Syntax Analyzer | Semantic Analyzer
""")

