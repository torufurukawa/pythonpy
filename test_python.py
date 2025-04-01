import unittest
import io
from python import tokenize, parse, parse_atom, parse_expr, evaluate, main
from python import PrintNode, BinOpNode


class TestTokenize(unittest.TestCase):
    def test(self):
        specs = [
            {
                "code": "print()",
                "expected": [
                    ("PRINT", "print"), ("LPAREN", "("), ("RPAREN", ")")
                ],
            },
            {
                "code": "print(123)",
                "expected": [
                    ("PRINT", "print"), ("LPAREN", "("), ("NUMBER", "123"),
                    ("RPAREN", ")")
                ],
            },
            {
                "code": "+",
                "expected": [("PLUS", "+")],
            }
        ]

        for spec in specs:
            with self.subTest(spec=spec):
                tokens = tokenize(spec['code'])
                self.assertEqual(tokens, spec['expected'])

    def test_syntax_erros(self):
        with self.assertRaises(SyntaxError):
            tokenize("log()")


class TestParseAtom(unittest.TestCase):
    def test(self):
        for val in [42, 3]:
            token = ("NUMBER", str(val))
            result = parse_atom(token)
            self.assertEqual(result, val)

    def test_error(self):
        token = ("LPAREN", ")")
        with self.assertRaises(SyntaxError):
            parse_atom(token)


class TestParseExpr(unittest.TestCase):
    def test(self):
        specs = [
            {"tokens": [("NUMBER", "42")], "expected": 42},
            {
                "tokens": [("NUMBER", "2"), ("PLUS", "+"), ("NUMBER", "3")],
                "expected": BinOpNode(2, "+", 3)
            }
        ]
        for spec in specs:
            with self.subTest(spec=spec):
                result = parse_expr(spec['tokens'])
                self.assertEqual(result, spec['expected'])

    def test_exceptions(self):
        specs = [{"tokens": [("NUMBER", "2"), ("PLUS", "+")]}]
        for spec in specs:
            with self.subTest(sepc=spec):
                with self.assertRaises(SyntaxError):
                    parse_expr(spec['tokens'])


# TODO: add NUMBER + NUMBER
class TestParse(unittest.TestCase):
    def test(self):
        specs = [
            {
                "tokens": [
                    ("PRINT", "print"), ("LPAREN", "("), ("RPAREN", ")")
                ],
                "expected": PrintNode()
            },
            {
                "tokens": [
                    ("PRINT", "print"), ("LPAREN", "("), ("NUMBER", "123"),
                    ("RPAREN", ")")
                ],
                "expected": PrintNode(123)
            }
        ]

        for spec in specs:
            with self.subTest(spec=spec):
                ast = parse(spec['tokens'])
                self.assertEqual(ast, spec['expected'])

    def test_errors(self):
        specs = [
            {"tokens": [("PRINT", "print"), ("LPAREN", "(")]}
        ]
        for spec in specs:
            with self.subTest(spec=spec):
                with self.assertRaises(SyntaxError):
                    parse(spec['tokens'])


# TODO: add evaluate_expr()

# TODO: add using evaluate_expr()
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


# TODO: print(1+2)
class TestPython(unittest.TestCase):
    def test(self):
        specs = [
            {"code": "print()", "expected": "\n"},
            {"code": "print(123)", "expected": "123\n"}
        ]
        for spec in specs:
            with self.subTest(spec=spec):
                fin = io.StringIO(spec['code'])
                fout = io.StringIO()
                main(fin, fout)

                self.assertEqual(fout.getvalue(), spec['expected'])


# TODO: define Token data structure?


if __name__ == "__main__":
    unittest.main()
