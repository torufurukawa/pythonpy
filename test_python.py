import unittest
import io
from python import tokenize, parse, evaluate, main
from python import PrintNode


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
            }

        ]

        for spec in specs:
            with self.subTest(spec=spec):
                tokens = tokenize(spec['code'])
                self.assertEqual(tokens, spec['expected'])

    def test_syntax_erros(self):
        with self.assertRaises(SyntaxError):
            tokenize("log()")


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
            {"code": "print(123)", "expected": "123\n"}
        ]
        for spec in specs:
            with self.subTest(spec=spec):
                fin = io.StringIO(spec['code'])
                fout = io.StringIO()
                main(fin, fout)

                self.assertEqual(fout.getvalue(), spec['expected'])


if __name__ == "__main__":
    unittest.main()
