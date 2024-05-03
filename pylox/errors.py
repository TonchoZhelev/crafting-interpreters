import sys

hadError: bool = False

def error(line: int, message: str):
    report(line, "", message)


def report(line: int, where: str, message: str):
    global hadError
    print("[line", line, "] Error", where, ": ", message, file=sys.stderr)
    hadError = True
