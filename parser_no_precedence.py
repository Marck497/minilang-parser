"""Same expression grammar without a precedence table.

PLY reports shift/reduce conflicts and resolves them by shifting, which makes
`10 - 3 - 2` group as `10 - (3 - 2)` and lets `a < b < c` through.
"""

import ply.yacc as yacc

from lexer import tokens, lexer  # noqa: F401
from ast_nodes import NumberNode, VarNode, BinaryOpNode, AssignNode, show


def p_program(p):
    """program : statement_list"""
    p[0] = p[1]


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


def p_expression_binary(p):
    """expression : expression ADD expression
                  | expression SUBTRACT expression
                  | expression MULTIPLY expression
                  | expression DIVIDE expression
                  | expression EQUALS expression
                  | expression GREATER_THAN expression
                  | expression LESS_THAN expression"""
    p[0] = BinaryOpNode(p[2], p[1], p[3])


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
    if p is None:
        print("Syntax error: unexpected end of input.")
    else:
        print(
            f"Syntax error on line {p.lineno}: "
            f"unexpected token {p.type} ({p.value!r})."
        )


# debug=True writes parser.out with the LALR states and conflicts.
parser = yacc.yacc(start="program", write_tables=False, debug=True)


if __name__ == "__main__":
    for code in ["x = 2 + 3 * 4;", "x = 10 - 3 - 2;", "x = a < b < c;"]:
        print()
        print("Input:", code)

        lexer.lineno = 1
        tree = parser.parse(code, lexer=lexer)

        if tree is not None:
            show(tree)
