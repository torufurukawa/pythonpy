from dataclasses import dataclass


@dataclass
class Token:
    type: str
    value: str


def tokenize_program(code):
    lines = code.splitlines()
    return [tokenize_line(line) for line in lines if line.strip()]


def tokenize_line(line):
    tokens = []
    i = 0

    while i < len(line):
        c = line[i]

        if c in " \t\n":
            i += 1

        elif line[i:].startswith("print", i):
            tokens.append(Token("PRINT", "print"))
            i += 5

        elif c == "(":
            tokens.append(Token("LPAREN", c))
            i += 1

        elif c == ")":
            tokens.append(Token("RPAREN", c))
            i += 1

        elif c == "+":
            tokens.append(Token("PLUS", c))
            i += 1

        elif c == "-":
            tokens.append(Token("MINUS", c))
            i += 1

        elif c == "*":
            tokens.append(Token("MULTIPLY", c))
            i += 1

        elif c == "/":
            tokens.append(Token("DIVIDE", c))
            i += 1

        elif c == "=":
            tokens.append(Token("EQUALS", c))
            i += 1

        elif c.isdigit():
            start = i
            while i < len(line) and line[i].isdigit():
                i += 1
            number = line[start:i]
            tokens.append(Token("NUMBER", number))

        elif c.isalpha():
            start = i
            while i < len(line) and line[i].isalnum():
                i += 1
            ident = line[start:i]
            tokens.append(Token("IDENTIFIER", ident))

        else:
            raise SyntaxError(f"Unexpected character: '{c}' at position {i}")

    return tokens
