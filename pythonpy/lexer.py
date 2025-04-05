from dataclasses import dataclass


@dataclass
class Token:
    type: str
    value: str


def tokenize(code):
    tokens = []
    i = 0

    while i < len(code):
        c = code[i]

        if c in " \t\n":
            i += 1

        elif code[i:].startswith("print", i):
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

        elif c.isdigit():
            start = i
            while i < len(code) and code[i].isdigit():
                i += 1
            number = code[start:i]
            tokens.append(Token("NUMBER", number))

        else:
            raise SyntaxError(f"Unexpected character: '{c}' at position {i}")

    return tokens

