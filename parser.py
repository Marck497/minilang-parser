import sys

import ply.yacc as yacc

from lexer import tokens, lexer  # noqa: F401  (PLY reads `tokens` from this module)
from ast_nodes import (
    NumberNode,
    VarNode,
    BinaryOpNode,
    UnaryOpNode,
    AssignNode,
    PrintNode,
    IfNode,
    show,
)


# Lowest to highest precedence.
precedence = (
    ("left", "OR"),
    ("left", "AND"),
    ("right", "NOT"),
    (
        "nonassoc",
        "EQUALS",
        "GREATER_THAN",
        "LESS_THAN",
        "GREATER_EQUALS",
        "LESS_EQUALS",
        "NOT_EQUALS",
    ),
    ("left", "ADD", "SUBTRACT"),
    ("left", "MULTIPLY", "DIVIDE", "REMAINDER"),
    ("right", "UMINUS"),
)


errors = 0


def p_program(p):
    """program : statement_list"""
    p[0] = p[1]


# Left recursion is the natural choice for an LALR parser: each statement is
# reduced as soon as it is seen, so the stack does not grow with program size.
def p_statement_list(p):
    """statement_list : statement_list statement
                      | statement"""
    if len(p) == 3:
        p[1].append(p[2])
        p[0] = p[1]
    else:
        p[0] = [p[1]]


def p_statement_assign(p):
    """statement : ID ASSIGNMENT expression SEMICOLON"""
    p[0] = AssignNode(p[1], p[3])


def p_statement_print(p):
    """statement : PRINT expression SEMICOLON"""
    p[0] = PrintNode(p[2])


def p_statement_if(p):
    """statement : IF expression COLON statement_list ENDIF SEMICOLON
                 | IF expression COLON statement_list ELSE COLON statement_list ENDIF SEMICOLON"""
    if len(p) == 7:
        p[0] = IfNode(p[2], p[4])
    else:
        p[0] = IfNode(p[2], p[4], p[7])


def p_expression_logical(p):
    """expression : expression OR expression
                  | expression AND expression"""
    p[0] = BinaryOpNode(p[2], p[1], p[3])


def p_expression_not(p):
    """expression : NOT expression"""
    p[0] = UnaryOpNode(p[1], p[2])


def p_expression_comparison(p):
    """expression : expression EQUALS expression
                  | expression GREATER_THAN expression
                  | expression LESS_THAN expression
                  | expression GREATER_EQUALS expression
                  | expression LESS_EQUALS expression
                  | expression NOT_EQUALS expression"""
    p[0] = BinaryOpNode(p[2], p[1], p[3])


def p_expression_arithmetic(p):
    """expression : expression ADD expression
                  | expression SUBTRACT expression
                  | expression MULTIPLY expression
                  | expression DIVIDE expression
                  | expression REMAINDER expression"""
    p[0] = BinaryOpNode(p[2], p[1], p[3])


def p_expression_uminus(p):
    """expression : SUBTRACT expression %prec UMINUS"""
    p[0] = UnaryOpNode("-", p[2])


# Parentheses only group; they don't get a node of their own.
def p_expression_group(p):
    """expression : OPEN_PARENTHESIS expression CLOSED_PARENTHESIS"""
    p[0] = p[2]


def p_expression_number(p):
    """expression : LIT_INT
                  | LIT_FLOAT"""
    p[0] = NumberNode(p[1])


def p_expression_variable(p):
    """expression : ID"""
    p[0] = VarNode(p[1])


def p_error(p):
    global errors
    errors += 1

    if p is None:
        print(
            "Syntax error: unexpected end of input; "
            "an expression or delimiter may be missing."
        )
    else:
        print(
            f"Syntax error on line {p.lineno}: "
            f"unexpected token {p.type} ({p.value!r})."
        )


parser = yacc.yacc(
    start="program",
    write_tables=False,
    debug=False,
    errorlog=yacc.NullLogger(),
)


def parse_program(code, print_tree=True):
    """Parse `code` and return the AST (a list of statements), or None on error."""
    global errors
    errors = 0
    lexer.lineno = 1

    tree = parser.parse(code, lexer=lexer, tracking=True)

    if errors > 0:
        return None

    if tree is not None and print_tree:
        show(tree)

    return tree


def main(argv):
    if len(argv) != 2:
        print(f"Usage: python {argv[0]} <source-file>")
        return 2

    with open(argv[1], encoding="utf-8") as f:
        code = f.read()

    tree = parse_program(code)
    if tree is None:
        print("Could not parse the program.")
        return 1

    print("Parsing completed successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
