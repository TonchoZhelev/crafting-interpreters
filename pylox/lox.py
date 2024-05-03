import sys

from scanner import Scanner
from errors import hadError

def run(source: str) -> None:
    scanner = Scanner(source)
    tokens = scanner.scanTokens()
    print(tokens)


def runFile(path: str) -> None:
    global hadError
    bytes = open(path).read()
    run(bytes);

    # Indicate an error in the exit code.
    if hadError:
        exit(65)


def runPrompt() -> None:
    global hadError

    print("""Press Ctrl+C or Ctrl+D to exit""")
    try:
        while True:
            line = input("> ")
            run(line);

            # Reset flag in REPL
            hadError = False
    except (KeyboardInterrupt, EOFError):
        print("\nProgram terminated by user.")


if __name__ == "__main__":
    if len(sys.argv) > 2:
        print("Usage: python lox.py [script]")
    elif len(sys.argv) == 2:
        runFile(sys.argv[1])
    else:
        runPrompt();
