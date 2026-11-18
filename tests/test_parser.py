import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from ast_nodes import AssignNode, BinaryOpNode, IfNode, NumberNode, PrintNode, UnaryOpNode, VarNode  # noqa: E402
from parser import parse_program  # noqa: E402


def to_tuple(node):
    """Turn an AST into nested tuples so it can be compared easily."""
    if isinstance(node, list):
        return [to_tuple(n) for n in node]
    if isinstance(node, NumberNode):
        return node.value
    if isinstance(node, VarNode):
        return node.name
    if isinstance(node, BinaryOpNode):
        return (node.op, to_tuple(node.left), to_tuple(node.right))
    if isinstance(node, UnaryOpNode):
        return (node.op, to_tuple(node.expr))
    if isinstance(node, AssignNode):
        return ("=", node.name, to_tuple(node.expr))
    if isinstance(node, PrintNode):
        return ("print", to_tuple(node.expr))
    if isinstance(node, IfNode):
        return ("if", to_tuple(node.cond), to_tuple(node.then_branch), to_tuple(node.else_branch))
    return node


def expr(code):
    tree = parse_program(f"x = {code};", print_tree=False)
    assert tree is not None
    return to_tuple(tree[0])[2]


def test_mul_binds_tighter_than_add():
    assert expr("2 + 3 * 4") == ("+", 2, ("*", 3, 4))


def test_subtraction_is_left_associative():
    assert expr("10 - 3 - 2") == ("-", ("-", 10, 3), 2)


def test_parentheses_override_precedence():
    assert expr("(2 + 3) * 4") == ("*", ("+", 2, 3), 4)


def test_comparisons_are_not_associative():
    assert parse_program("x = a < b < c;", print_tree=False) is None


def test_unary_minus_and_modulo():
    assert expr("-10 % 3") == ("%", ("-", 10), 3)


def test_logical_operator_precedence():
    assert expr("a || b && !c") == ("||", "a", ("&&", "b", ("!", "c")))


def test_keywords_are_case_insensitive():
    tree = parse_program("if 1 : print 2; endif;", print_tree=False)
    assert to_tuple(tree) == [("if", 1, [("print", 2)], None)]


def test_if_else():
    code = "IF a > 1 : PRINT a; ELSE : PRINT 0; ENDIF;"
    tree = parse_program(code, print_tree=False)
    assert to_tuple(tree) == [("if", (">", "a", 1), [("print", "a")], [("print", 0)])]


def test_sample_program_parses():
    code = (ROOT / "examples" / "program.ml").read_text(encoding="utf-8")
    assert parse_program(code, print_tree=False) is not None


def test_missing_semicolon_is_an_error():
    assert parse_program("x = 10\n", print_tree=False) is None


def test_incomplete_condition_is_an_error():
    assert parse_program("IF x > :\n PRINT x;\nENDIF;\n", print_tree=False) is None
