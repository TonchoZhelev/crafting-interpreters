import pytest
from scanner import Scanner

def test_isAtMultilineCommentStart():
    scanner = Scanner('/*')
    assert(scanner.isAtMultilineCommentStart())

def test_isAtMultilineCommentEnd():
    scanner = Scanner('*/')
    assert(scanner.isAtMultilineCommentEnd())
