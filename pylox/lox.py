import sys

import loxtoken

hadError: bool = False

def error(line: int, message: str):
    report(line, "", message)


def report(line: int, where: str, message: str):
    global hadError
    print("[line", line, "] Error", where, ": ", message, file=sys.stderr)
    hadError = True


def run(source: str) -> None:
    for s in source:
        print(s)


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
