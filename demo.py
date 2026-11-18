from pathlib import Path

from parser import parse_program


PRECEDENCE_CASES = [
    ("Arithmetic precedence", "x = 2 + 3 * 4;"),
    ("Left associativity", "x = 10 - 3 - 2;"),
    ("Non-associative comparisons (should fail)", "x = a < b < c;"),
]


def run(title, code):
    print()
    print("=" * 60)
    print(title)
    print("-" * 60)
    print(code.rstrip())
    print("-" * 60)

    tree = parse_program(code)
    if tree is None:
        print("No valid AST was built for this input.")
    else:
        print("Parsing completed successfully.")


if __name__ == "__main__":
    for title, code in PRECEDENCE_CASES:
        run(title, code)

    for path in sorted(Path(__file__).parent.joinpath("examples").glob("*.ml")):
        run(path.name, path.read_text(encoding="utf-8"))
