# minilang-parser

A lexer and LALR parser for a small imperative language, written in Python with [PLY](https://github.com/dabeaz/ply) (Python Lex-Yacc). It reads source code, checks it against the grammar, and builds an abstract syntax tree (AST).

```text
price = 12.5;
units = 4;
total = price * units - 3;
IF total > (units + 30) :
    PRINT total;
    total = total - 10;
ELSE :
    PRINT 0;
ENDIF;
```

```text
$ python parser.py examples/program.ml
Assign price
    Number 12.5
Assign units
    Number 4
Assign total
    BinaryOp -
        BinaryOp *
            Variable price
            Variable units
        Number 3
If
    BinaryOp >
        Variable total
        BinaryOp +
            Variable units
            Number 30
Then
    Print
        Variable total
    Assign total
        BinaryOp -
            Variable total
            Number 10
Else
    Print
        Number 0
Parsing completed successfully.
```

## Language

- **Statements:** assignment (`x = expr;`), `PRINT expr;`, and `IF cond : ... [ELSE : ...] ENDIF;`
- **Literals:** integers and floats
- **Arithmetic:** `+ - * / %` and unary minus
- **Comparisons:** `== != < <= > >=` (non-associative, so `a < b < c` is a syntax error)
- **Logic:** `&&`, `||`, `!`
- Keywords are case-insensitive (`IF`, `if` and `If` are the same token).

Operator precedence, from lowest to highest:

| Level | Operators | Associativity |
|---|---|---|
| 1 | `\|\|` | left |
| 2 | `&&` | left |
| 3 | `!` | right |
| 4 | `== != < <= > >=` | none |
| 5 | `+ -` | left |
| 6 | `* / %` | left |
| 7 | unary `-` | right |

## Grammar

```text
program        : statement_list
statement_list : statement_list statement
               | statement
statement      : ID '=' expression ';'
               | PRINT expression ';'
               | IF expression ':' statement_list ENDIF ';'
               | IF expression ':' statement_list ELSE ':' statement_list ENDIF ';'
expression     : expression (|| | && ) expression
               | '!' expression
               | expression (== | != | < | <= | > | >=) expression
               | expression (+ | - | * | / | %) expression
               | '-' expression
               | '(' expression ')'
               | LIT_INT | LIT_FLOAT | ID
```

`statement_list` is left-recursive on purpose. In a bottom-up LALR parser each statement is reduced and appended as soon as it is recognised, so the parser stack does not grow with the length of the program. (A top-down LL parser would need the left recursion removed.)

Parentheses don't produce a node of their own: they only affect grouping, so the tree for `(a + b) * c` is just a `*` node whose left child is the `+` node.

### Why the precedence table matters

`parser_no_precedence.py` builds the same expression grammar without the precedence table. PLY then reports **49 shift/reduce conflicts** and resolves all of them by shifting, which gives wrong trees:

- `10 - 3 - 2` is grouped as `10 - (3 - 2)` instead of `(10 - 3) - 2`
- `a < b < c` is accepted as `a < (b < c)` instead of being rejected

```bash
python parser_no_precedence.py
```

## Project layout

```text
lexer.py                  token definitions (PLY lex)
parser.py                 grammar, precedence table and AST construction (PLY yacc)
ast_nodes.py              AST node classes and a tree printer
parser_no_precedence.py   the grammar without precedence rules, for comparison
demo.py                   runs the precedence cases and every file in examples/
examples/                 sample programs, including two with syntax errors
tests/                    pytest suite
```

## Usage

```bash
pip install -r requirements.txt

python parser.py examples/program.ml   # parse a file and print its AST
python demo.py                         # run all the examples
python -m pytest                       # run the tests (pip install pytest)
```

Syntax errors are reported with the line and the offending token, and no AST is returned:

```text
$ python parser.py examples/error_incomplete_condition.ml
Syntax error on line 1: unexpected token COLON (':').
Syntax error on line 3: unexpected token ENDIF ('ENDIF').
Could not parse the program.
```

The lexer also recognises some tokens the grammar doesn't use yet (`while`, `for`, `do`, `break`, brackets, bitwise `&` and `|`), which leaves room to extend the language with loops and arrays.

## Author

Juan Marcos Pairola. Originally developed for the *Language Processors* course.

## License

[MIT](LICENSE)
