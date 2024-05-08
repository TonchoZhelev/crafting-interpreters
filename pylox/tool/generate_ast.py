"""
Following this part of the book, but in Python, proved to be somewhat difficult.
For a start, it seems like in Python it would have been easier to use pattern 
matching instead of the "visitor" pattern. And in python there are better ways to
generate the code rather than using strings, but for the sake of accuracy,
I decided to follow the path that has been taken by the book.
"""

from io import TextIOWrapper
import sys

def defineAst(outputDir: str, baseName: str, types: list[str]):
    path = outputDir + "/" + (baseName[0].lower() + baseName[1:]) + ".g.py"

    with open(path, 'w', encoding='utf-8') as writer:
        writer.write("from typing import Protocol\n")
        writer.write("from dataclasses import dataclass\n")
        writer.write("from loxtoken import Token\n")
        writer.write("\n\n")
        writer.write("class " + baseName + "(Protocol):\n\tpass\n") 
        writer.write("\n\n")

        for type in types:
            className = type.split('=')[0].strip()
            fields = type.split('=')[1].strip()
            defineType(writer, baseName, className, fields)

def defineType(writer: TextIOWrapper, baseName: str,\
                className: str, fields: str):
    writer.write("@dataclass\n")
    writer.write("class " + className + "(" + baseName + "):\n")

    fieldsList = fields.split(",")
    for field in fieldsList:
        field = field.strip()
        writer.write("\t" + field + "\n")

    writer.write("\n\n")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: generate_ast <output directory>", file=sys.stderr)
        sys.exit(64)

    outputDir = sys.argv[1]

    # For the sake of supporting python types properly, I decided to use '='
    # as the separator between the class name and it's fields, so that I can use
    # ":" for the types
    defineAst(outputDir, "Expr", [
        "Binary   = left: Expr, operator: Token, right: Expr",
        "Grouping = expression: Expr",
        "Literal  = value: object",
        "Unary    = operator: Token, right: Expr",
        ])
