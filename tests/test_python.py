import unittest
import io
from pythonpy.lexer import Token, tokenize_program, tokenize_line
from pythonpy.parser import parse_statement, parse_program
from pythonpy.parser import parse_atom, parse_expr, parse_factor, parse_term
from pythonpy.evaluator import evaluate, evaluate_expr
from pythonpy.nodes import (
    ProgramNode, PrintNode, BinOpNode, AssignNode, NameNode
)
from pythonpy.main import main


class TestTokenizeProgram(unittest.TestCase):
    def test(self):
        code = "\n".join(["print()", "print(1+2)"])
        token_lines = tokenize_program(code)
        self.assertEqual(
            token_lines,
            [
                [
                    Token("PRINT", "print"),
                    Token("LPAREN", "("),
                    Token("RPAREN", ")")
                ],
                [
                    Token("PRINT", "print"),
                    Token("LPAREN", "("),
                    Token("NUMBER", "1"),
                    Token("PLUS", "+"),
                    Token("NUMBER", "2"),
                    Token("RPAREN", ")")
                ],
            ]
        )


class TestTokenizeLine(unittest.TestCase):
    def test(self):
        specs = [
            {
                "line": "print()",
                "expected": [
                    Token("PRINT", "print"),
                    Token("LPAREN", "("),
                    Token("RPAREN", ")"),
                ],
            },
            {
                "line": "print(123)",
                "expected": [
                    Token("PRINT", "print"),
                    Token("LPAREN", "("),
                    Token("NUMBER", "123"),
                    Token("RPAREN", ")"),
                ],
            },
            {
                "line": "print(x)",
                "expected": [
                    Token("PRINT", "print"),
                    Token("LPAREN", "("),
                    Token("IDENTIFIER", "x"),
                    Token("RPAREN", ")"),
                ],
            },
            {
                "line": "+",
                "expected": [Token("PLUS", "+")],
            },
            {
                "line": "-",
                "expected": [Token("MINUS", "-")],
            },
            {
                "line": "*",
                "expected": [Token("MULTIPLY", "*")]
            },
            {
                "line": "/",
                "expected": [Token("DIVIDE", "/")],
            },
            {
                "line": "p = 1",
                "expected": [
                    Token("IDENTIFIER", "p"),
                    Token("EQUALS", "="),
                    Token("NUMBER", "1")
                ]
            }
        ]

        for spec in specs:
            with self.subTest(spec=spec):
                tokens = tokenize_line(spec["line"])
                self.assertEqual(tokens, spec["expected"])


class TestParseProgram(unittest.TestCase):
    def test(self):
        token_lines = [
            [
                Token("PRINT", "print"),
                Token("LPAREN", "("),
                Token("RPAREN", ")")
            ],
            [
                Token("PRINT", "print"),
                Token("LPAREN", "("),
                Token("NUMBER", "1"),
                Token("PLUS", "+"),
                Token("NUMBER", "2"),
                Token("RPAREN", ")")
            ],
        ]

        node = parse_program(token_lines)

        self.assertIsInstance(node, ProgramNode)
        self.assertEqual(
            node.statements,
            [PrintNode(), PrintNode(BinOpNode(1, "+", 2))]
        )


class TestParseAtom(unittest.TestCase):
    def test(self):
        for val in [42, 3]:
            token = Token("NUMBER", str(val))
            result = parse_atom(token)
            self.assertEqual(result, val)

    def test_error(self):
        token = Token("LPAREN", ")")
        with self.assertRaises(SyntaxError):
            parse_atom(token)


class TestParseExpr(unittest.TestCase):
    def test(self):
        specs = [
            {"tokens": [Token("NUMBER", "42")], "expected": 42},
            {
                "tokens": [
                    Token("NUMBER", "2"),
                    Token("PLUS", "+"),
                    Token("NUMBER", "3"),
                ],
                "expected": BinOpNode(2, "+", 3),
            },
            {
                "tokens": [
                    Token("NUMBER", "2"),
                    Token("MULTIPLY", "*"),
                    Token("NUMBER", "3"),
                ],
                "expected": BinOpNode(2, "*", 3),
            },
            {
                "tokens": [
                    Token("NUMBER", "4"),
                    Token("PLUS", "/"),
                    Token("NUMBER", "2"),
                ],
                "expected": BinOpNode(4, "/", 2),
            },
            {
                "tokens": [
                    Token("NUMBER", "2"),
                    Token("PLUS", "+"),
                    Token("NUMBER", "3"),
                    Token("PLUS", "+"),
                    Token("NUMBER", "5"),
                ],
                "expected": BinOpNode(BinOpNode(2, "+", 3), "+", 5),
            },
            {
                "tokens": [
                    Token("NUMBER", "2"),
                    Token("PLUS", "+"),
                    Token("NUMBER", "3"),
                    Token("MINUS", "-"),
                    Token("NUMBER", "5"),
                ],
                "expected": BinOpNode(BinOpNode(2, "+", 3), "-", 5),
            },
            {
                "tokens": [
                    Token("NUMBER", "2"),
                    Token("PLUS", "+"),
                    Token("NUMBER", "3"),
                    Token("PLUS", "+"),
                    Token("NUMBER", "5"),
                    Token("PLUS", "+"),
                    Token("NUMBER", "7"),
                ],
                "expected": BinOpNode(
                                BinOpNode(
                                    BinOpNode(2, "+", 3), "+", 5), "+", 7),
            },
            {
                "tokens": [
                    Token("NUMBER", "2"),
                    Token("PLUS", "+"),
                    Token("NUMBER", "3"),
                    Token("MULTIPLY", "*"),
                    Token("NUMBER", "5"),
                 ],
                "expected": BinOpNode(2, "+", BinOpNode(3, "*", 5))
            },
        ]
        for spec in specs:
            with self.subTest(spec=spec):
                result, i = parse_expr(spec["tokens"], 0)
                self.assertEqual(result, spec["expected"])

    def test_syntax_error(self):
        specs = [
            {"tokens": [Token("NUMBER", "2"), Token("PLUS", "+")]},
            {"tokens": []},
        ]
        for spec in specs:
            with self.subTest(sepc=spec):
                with self.assertRaises(SyntaxError):
                    parse_expr(spec["tokens"], 0)


class TestParseStatement(unittest.TestCase):
    def test(self):
        specs = [
            {
                "tokens": [
                    Token("PRINT", "print"),
                    Token("LPAREN", "("),
                    Token("NUMBER", "2"),
                    Token("PLUS", "+"),
                    Token("NUMBER", "3"),
                    Token("RPAREN", ")"),
                ],
                "expected": PrintNode(BinOpNode(2, "+", 3)),
            },
            {
                "tokens": [
                    Token("IDENTIFIER", "x"),
                    Token("EQUALS", "="),
                    Token("NUMBER", "2"),
                ],
                "expected": AssignNode("x", 2),
            },
            {
                "tokens": [
                    Token("IDENTIFIER", "x"),
                    Token("EQUALS", "="),
                    Token("NUMBER", "1"),
                    Token("PLUS", "+"),
                    Token("NUMBER", "2")
                ],
                "expected": AssignNode("x", BinOpNode(1, "+", 2)),
            },

            {
                "tokens": [
                    Token("PRINT", "print"),
                    Token("LPAREN", "("),
                    Token("IDENTIFIER", "x"),
                    Token("RPAREN", ")"),
                ],
                "expected": PrintNode(NameNode("x")),
            },
            {
                "tokens": [
                    Token("PRINT", "print"),
                    Token("LPAREN", "("),
                    Token("IDENTIFIER", "x"),
                    Token("PLUS", "+"),
                    Token("NUMBER", "3"),
                    Token("RPAREN", ")"),
                ],
                "expected": PrintNode(BinOpNode(NameNode("x"), "+", 3)),
            },
            {
                "tokens": [
                    Token("PRINT", "print"),
                    Token("LPAREN", "("),
                    Token("RPAREN", ")"),
                ],
                "expected": PrintNode(),
            },
            {
                "tokens": [
                    Token("PRINT", "print"),
                    Token("LPAREN", "("),
                    Token("NUMBER", "123"),
                    Token("RPAREN", ")"),
                ],
                "expected": PrintNode(123),
            },
            {
                "tokens": [
                    Token("PRINT", "print"),
                    Token("LPAREN", "("),
                    Token("NUMBER", "2"),
                    Token("PLUS", "+"),
                    Token("NUMBER", "3"),
                    Token("RPAREN", ")"),
                ],
                "expected": PrintNode(BinOpNode(2, "+", 3)),
            },
        ]

        for spec in specs:
            with self.subTest(spec=spec):
                ast = parse_statement(spec["tokens"])
                self.assertEqual(ast, spec["expected"])

    def test_errors(self):
        specs = [{"tokens": [Token("PRINT", "print"), Token("LPAREN", "(")]}]
        for spec in specs:
            with self.subTest(spec=spec):
                with self.assertRaises(SyntaxError):
                    parse_statement(spec["tokens"])


class TestParseFactor(unittest.TestCase):
    def test_simple_factor(self):
        left = 1
        right = 2
        tokens = [
            Token("NUMBER", left), Token("PLUS", "+"), Token("NUMBER", right)
        ]

        value, i = parse_factor(tokens, 0)
        self.assertEqual(value, left)
        self.assertEqual(i, 1)

        value, i = parse_factor(tokens, 2)
        self.assertEqual(value, right)
        self.assertEqual(i, 3)

    def test_cascaded_factor(self):
        inner_tokens = [
            Token("LPAREN", "("),
            Token("NUMBER", 1),
            Token("PLUS", "+"),
            Token("NUMBER", 2),
            Token("RPAREN", ")")
        ]
        tokens = [
            Token("LPAREN", "("),
            *inner_tokens,
            Token("MULTIPLY", "*"),
            *inner_tokens,
            Token("RPAREN", ")"),
        ]

        node, i = parse_factor(tokens, 0)
        self.assertEqual(
            node,
            BinOpNode(BinOpNode(1, "+", 2), "*", BinOpNode(1, "+", 2))
        )

    def test_pharen(self):
        tokens = [
            Token("LPAREN", "("),
            Token("NUMBER", 1),
            Token("PLUS", "+"),
            Token("NUMBER", 2),
            Token("RPAREN", ")"),
            Token("MULTIPLY", "*"),
            Token("NUMBER", 3),
        ]

        value, i = parse_factor(tokens, 0)
        self.assertEqual(value, BinOpNode(1, "+", 2))
        self.assertEqual(i, 5)

    def test_syntax_error(self):
        tokens = [Token("NUMBER", 1), Token("PLUS", "+")]
        specs = [{"index": 1}, {"index": 2}]

        for spec in specs:
            with self.subTest(spec=spec):
                with self.assertRaises(SyntaxError):
                    parse_factor(tokens, spec['index'])

    def test_incomplete_paren(self):
        tokens = [
            Token("LPAREN", "("),
            Token("NUMBER", 1),
            Token("PLUS", 1),
            Token("NUMBER", 2)
        ]
        with self.assertRaises(SyntaxError):
            parse_factor(tokens, 0)


class TestParseTerm(unittest.TestCase):
    def test(self):
        specs = [
            {
                "tokens": [
                    Token("NUMBER", "2"),
                    Token("PLUS", "+"),
                    Token("NUMBER", "3")
                 ],
                "index": 0,
                "expected": (2, 1)
            },
            {
                "tokens": [
                    Token("NUMBER", "2"),
                    Token("MULTIPLY", "*"),
                    Token("NUMBER", "3")
                 ],
                "index": 0,
                "expected": (BinOpNode(2, "*", 3), 3)
            },
            {
                "tokens": [
                    Token("NUMBER", "2"),
                    Token("DIVIDE", "/"),
                    Token("NUMBER", "3")
                 ],
                "index": 0,
                "expected": (BinOpNode(2, "/", 3), 3)
            },
        ]

        for spec in specs:
            with self.subTest(spec=spec):
                node, i = parse_term(spec['tokens'], spec['index'])
                self.assertEqual((node, i), spec['expected'])


class TestEvaluatExpr(unittest.TestCase):
    def test(self):
        specs = [
            {"expr": 2, "env": {}, "expected": 2},
            {"expr": BinOpNode(2, "+", 3), "env": {}, "expected": 5},
            {"expr": BinOpNode(2, "-", 3), "env": {}, "expected": -1},
            {"expr": BinOpNode(2, "*", 3), "env": {}, "expected": 6},
            {"expr": BinOpNode(6, "/", 3), "env": {}, "expected": 2},
            {"expr": NameNode("x"), "env": {"x": 1}, "expected": 1},
            {
                "expr": BinOpNode(NameNode("x"), "+", 2), "env": {"x": 1},
                "expected": 3
            },
        ]

        for spec in specs:
            with self.subTest(spec=spec):
                result = evaluate_expr(spec['expr'], spec['env'])
                self.assertEqual(result, spec['expected'])

    def test_exceptions(self):
        specs = [
            {"expr": BinOpNode(2, "~", 3), "env": {}, "exception": ValueError},
            {"expr": None, "env": {}, "exception": TypeError},
            {"expr": BinOpNode(2, "/", 0), "env": {}, "exception": ValueError},
            {"expr": NameNode("x"), "env": {}, "exception": NameError},
        ]
        for spec in specs:
            with self.subTest(spec=spec):
                with self.assertRaises(spec["exception"]):
                    evaluate_expr(spec["expr"], {})


class TestEvaluate(unittest.TestCase):
    def test_without_args(self):
        node = PrintNode()
        env = {}
        fout = io.StringIO()
        evaluate(node, env, fout)
        self.assertEqual(fout.getvalue(), "\n")

    def test_with_args(self):
        val = 123
        node = PrintNode(val)
        env = {}
        fout = io.StringIO()
        evaluate(node, env, fout)
        self.assertEqual(fout.getvalue(), f"{val}\n")

    def test_errors(self):
        nodes = [None]
        for node in nodes:
            with self.subTest(node=node):
                env = {}
                fout = io.StringIO()
                with self.assertRaises(TypeError):
                    evaluate(node, env, fout)

    def test_plus_expr(self):
        node = PrintNode(BinOpNode(2, "+", 3))
        env = {}
        fout = io.StringIO()
        evaluate(node, env, fout)
        self.assertEqual(fout.getvalue(), "5\n")

    def test_program(self):
        node = ProgramNode([PrintNode(), PrintNode(BinOpNode(1, "+", 2))])
        env = {}
        fout = io.StringIO()
        evaluate(node, env, fout)
        self.assertEqual(fout.getvalue(), "\n3\n")

    def test_assign(self):
        specs = [
            {"var_name": "x", "expr": 3, "expected": 3},
            {"var_name": "x", "expr": BinOpNode(1, "+", 2), "expected": 3}
        ]

        for spec in specs:
            with self.subTest(spec=spec):
                node = AssignNode(spec['var_name'], spec['expr'])
                env = {}
                fout = io.StringIO()

                evaluate(node, env, fout)
                self.assertEqual(env[spec['var_name']], spec['expected'])


class TestProgramNode(unittest.TestCase):
    def test(self):
        statements = [PrintNode(), PrintNode(1)]
        node = ProgramNode(statements)
        self.assertEqual(node.statements, statements)


class TestBinOpNode(unittest.TestCase):
    def test_init(self):
        left, op, right = "1", "+", "2"
        node = BinOpNode(left, op, right)
        self.assertEqual(node.left, left)
        self.assertEqual(node.op, op)
        self.assertEqual(node.left, left)

    def test_eq(self):
        a = BinOpNode("1", "+", "2")
        b = BinOpNode("1", "+", "2")
        self.assertEqual(a, b)

    def test_not_eq(self):
        a = BinOpNode("1", "+", "2")
        b = BinOpNode("3", "+", "7")
        self.assertNotEqual(a, b)


class TestPrintNode(unittest.TestCase):
    def test_init_without_args(self):
        node = PrintNode()
        self.assertIsNone(node.value)

    def test_init_with_args(self):
        val = 123
        node = PrintNode(val)
        self.assertEqual(node.value, val)


class TestAssignNode(unittest.TestCase):
    def test(self):
        specs = [
            {"var_name": "x", "expr": 1}
        ]
        for spec in specs:
            with self.subTest(spec=spec):
                n = AssignNode(spec['var_name'], spec['expr'])
                self.assertEqual(n.var_name, spec['var_name'])
                self.assertEqual(n.expr, spec['expr'])

    def test_eq(self):
        a = AssignNode("x", 1)
        b = AssignNode("x", 1)
        self.assertEqual(a, b)


class TestNameNode(unittest.TestCase):
    def test(self):
        specs = [{"name": "x"}, {"name": "a3"}]
        for spec in specs:
            with self.subTest(spec=spec):
                n = NameNode(spec['name'])
                self.assertEqual(n.var_name, spec['name'])

    def test_magic_methods(self):
        a = NameNode("x")
        b = NameNode("x")
        self.assertEqual(a, b)
        self.assertIsInstance(repr(a), str)


class TestPython(unittest.TestCase):
    def test(self):
        specs = [
            {"code": "print()", "expected": "\n"},
            {"code": "print(123)", "expected": "123\n"},
            {"code": "print(2+3)", "expected": "5\n"},
            {"code": "print(2+3+5)", "expected": "10\n"},
            {"code": "print(2+3-5)", "expected": "0\n"},
            {"code": "print(3*4)", "expected": "12\n"},
            {"code": "print(6/2)", "expected": "3\n"},
            {"code": "print(2+3*4)", "expected": "14\n"},
            {"code": "print((1+2)*3)", "expected": "9\n"},
            {"code": "print()\nprint(1+2)", "expected": "\n3\n"},
            {"code": "print()\n\nprint(1+2)", "expected": "\n3\n"},
            {"code": "a=1\nprint(a+2)", "expected": "3\n"},
        ]
        for spec in specs:
            with self.subTest(spec=spec):
                fin = io.StringIO(spec["code"])
                fout = io.StringIO()
                main(fin, fout)

                self.assertEqual(fout.getvalue(), spec["expected"])


class TestToken(unittest.TestCase):
    def test(self):
        type_ = "NUMBER"
        value = 3
        token = Token(type_, value)
        self.assertEqual(token.type, type_)
        self.assertEqual(token.value, value)


if __name__ == "__main__":
    unittest.main()
