import unittest
import io
from pythonpy.lexer import Token, tokenize
from pythonpy.parser import parse, parse_atom, parse_expr
from pythonpy.evaluator import evaluate, evaluate_expr
from pythonpy.nodes import PrintNode, BinOpNode
from pythonpy.main import main


# TODO: "print(2+3-5)" => 0

class TestTokenize(unittest.TestCase):
    def test(self):
        specs = [
            {
                "code": "print()",
                "expected": [
                    Token("PRINT", "print"),
                    Token("LPAREN", "("),
                    Token("RPAREN", ")"),
                ],
            },
            {
                "code": "print(123)",
                "expected": [
                    Token("PRINT", "print"),
                    Token("LPAREN", "("),
                    Token("NUMBER", "123"),
                    Token("RPAREN", ")"),
                ],
            },
            {
                "code": "+",
                "expected": [Token("PLUS", "+")],
            },
            {
                "code": "-",
                "expected": [Token("MINUS", "-")],
            },
        ]

        for spec in specs:
            with self.subTest(spec=spec):
                tokens = tokenize(spec["code"])
                self.assertEqual(tokens, spec["expected"])

    def test_syntax_erros(self):
        with self.assertRaises(SyntaxError):
            tokenize("log()")


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
        ]
        for spec in specs:
            with self.subTest(spec=spec):
                result = parse_expr(spec["tokens"])
                self.assertEqual(result, spec["expected"])

    def test_syntax_error(self):
        specs = [
            {"tokens": [Token("NUMBER", "2"), Token("PLUS", "+")]},
            {"tokens": [Token("NUMBER", "2"), Token("ERROR", "~")]},
            {"tokens": []},
        ]
        for spec in specs:
            with self.subTest(sepc=spec):
                with self.assertRaises(SyntaxError):
                    parse_expr(spec["tokens"])


class TestParse(unittest.TestCase):
    def test(self):
        specs = [
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
                ast = parse(spec["tokens"])
                self.assertEqual(ast, spec["expected"])

    def test_errors(self):
        specs = [{"tokens": [Token("PRINT", "print"), Token("LPAREN", "(")]}]
        for spec in specs:
            with self.subTest(spec=spec):
                with self.assertRaises(SyntaxError):
                    parse(spec["tokens"])


class TestEvaluatExpr(unittest.TestCase):
    def test(self):
        specs = [
            {"expr": 2, "expected": 2},
            {"expr": BinOpNode(2, "+", 3), "expected": 5},
            {"expr": BinOpNode(2, "-", 3), "expected": -1},
        ]
        for spec in specs:
            with self.subTest(spec=spec):
                result = evaluate_expr(spec["expr"])
                self.assertEqual(result, spec["expected"])

    def test_exceptions(self):
        specs = [
            {"expr": BinOpNode(2, "~", 3), "exception": ValueError},
            {"expr": None, "exception": TypeError},
        ]
        for spec in specs:
            with self.subTest(spec=spec):
                with self.assertRaises(spec["exception"]):
                    evaluate_expr(spec["expr"])


class TestEvaluate(unittest.TestCase):
    def test_without_args(self):
        node = PrintNode()
        fout = io.StringIO()
        evaluate(node, fout)
        self.assertEqual(fout.getvalue(), "\n")

    def test_with_args(self):
        val = 123
        node = PrintNode(val)
        fout = io.StringIO()
        evaluate(node, fout)
        self.assertEqual(fout.getvalue(), f"{val}\n")

    def test_errors(self):
        nodes = [None]
        for node in nodes:
            with self.subTest(node=node):
                fout = io.StringIO()
                with self.assertRaises(TypeError):
                    evaluate(node, fout)

    def test_plus_expr(self):
        node = PrintNode(BinOpNode(2, "+", 3))
        fout = io.StringIO()
        evaluate(node, fout)
        self.assertEqual(fout.getvalue(), "5\n")


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


class TestPython(unittest.TestCase):
    def test(self):
        specs = [
            {"code": "print()", "expected": "\n"},
            {"code": "print(123)", "expected": "123\n"},
            {"code": "print(2+3)", "expected": "5\n"},
            {"code": "print(2+3+5)", "expected": "10\n"},
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
