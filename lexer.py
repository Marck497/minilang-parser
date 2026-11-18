import ply.lex as lex


reserved = {
    "break": "BREAK",
    "do": "DO",
    "else": "ELSE",
    "float": "FLOAT",
    "for": "FOR",
    "if": "IF",
    "int": "INT",
    "while": "WHILE",
    "repeat": "KW_REPEAT",
    "print": "PRINT",
    "endif": "ENDIF",
}


tokens = tuple(reserved.values()) + (
    "ID",
    "LIT_INT",
    "LIT_FLOAT",

    "GREATER_THAN",
    "GREATER_EQUALS",
    "LESS_THAN",
    "LESS_EQUALS",
    "EQUALS",
    "NOT_EQUALS",
    "ASSIGNMENT",

    "ADD",
    "SUBTRACT",
    "MULTIPLY",
    "DIVIDE",
    "REMAINDER",

    "AND",
    "OR",
    "NOT",
    "BITWISE_AND",
    "BITWISE_OR",

    "COLON",
    "SEMICOLON",

    "OPEN_PARENTHESIS",
    "CLOSED_PARENTHESIS",
    "OPEN_SQUARE_BRACKET",
    "CLOSED_SQUARE_BRACKET",
    "OPEN_BRACKET",
    "CLOSED_BRACKET",

    "END_PROGRAM",
)


def t_LIT_FLOAT(t):
    r"\d+\.\d+"
    t.value = float(t.value)
    return t


def t_LIT_INT(t):
    r"\d+"
    t.value = int(t.value)
    return t


def t_ID(t):
    r"[a-zA-Z][a-zA-Z0-9]*"
    # Keywords are case-insensitive (IF, if, If...)
    t.type = reserved.get(t.value.lower(), "ID")
    return t


def t_newline(t):
    r"(\r\n|\r|\n)+"
    newlines = t.value.replace("\r\n", "\n").replace("\r", "\n")
    t.lexer.lineno += len(newlines)


# Two-character operators go before their single-character versions.
t_GREATER_EQUALS = r">="
t_LESS_EQUALS = r"<="
t_EQUALS = r"=="
t_NOT_EQUALS = r"!="

t_GREATER_THAN = r">"
t_LESS_THAN = r"<"
t_ASSIGNMENT = r"="

t_AND = r"&&"
t_OR = r"\|\|"
t_NOT = r"!"

t_BITWISE_AND = r"&"
t_BITWISE_OR = r"\|"

t_ADD = r"\+"
t_SUBTRACT = r"-"
t_MULTIPLY = r"\*"
t_DIVIDE = r"/"
t_REMAINDER = r"%"

t_SEMICOLON = r";"
t_COLON = r":"

t_OPEN_PARENTHESIS = r"\("
t_CLOSED_PARENTHESIS = r"\)"

t_OPEN_SQUARE_BRACKET = r"\["
t_CLOSED_SQUARE_BRACKET = r"\]"

t_OPEN_BRACKET = r"\{"
t_CLOSED_BRACKET = r"\}"

t_END_PROGRAM = r"\#"

t_ignore = " \t"


def t_error(t):
    print(
        "Lexical error: invalid character",
        repr(t.value[0]),
        "on line",
        t.lineno,
    )
    t.lexer.skip(1)


lexer = lex.lex()
