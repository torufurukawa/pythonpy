import unittest
import io
from python import tokeinze, parse, evaluate, main
from python import PrintNode


class TestTokenize(unittest.TestCase):
    def test(self):
        specs = [
            {
                "code": "print()",
                "expected": [
                    ("PRINT", "print"), ("LPAREN", "("), ("RPAREN", ")")
                ],
            }
        ]

        for spec in specs:
            with self.subTest(spec=spec):
                tokens = tokeinze(spec['code'])
                self.assertEqual(tokens, spec['expected'])

    def test_syntax_erros(self):
        with self.assertRaises(SyntaxError):
            tokeinze("log()")


class TestParse(unittest.TestCase):
    def test(self):
        specs = [
            {
                "tokens": [
                    ("PRINT", "print"), ("LPAREN", "("), ("RPAREN", ")")
                ],
                "expected": PrintNode
            }
        ]

        for spec in specs:
            with self.subTest(spec=spec):
                ast = parse(spec['tokens'])
                self.assertIsInstance(ast, spec['expected'])

    def test_errors(self):
        specs = [
            {"tokens": [("PRINT", "print"), ("LPAREN", "(")]}
        ]
        for spec in specs:
            with self.subTest(spec=spec):
                with self.assertRaises(SyntaxError):
                    parse(spec['tokens'])


class TestEvaluate(unittest.TestCase):
    def test(self):
        node = PrintNode()
        fout = io.StringIO()
        evaluate(node, fout)
        self.assertEqual(fout.getvalue(), "\n")

    def test_errors(self):
        nodes = [None]
        for node in nodes:
            with self.subTest(node=node):
                fout = io.StringIO()
                with self.assertRaises(TypeError):
                    evaluate(node, fout)


# TODO: add print(123) case
# DOING: test main()
class TestPython(unittest.TestCase):
    def test(self):
        # given
        code = "print()"

        # when
        fin = io.StringIO(code)
        fout = io.StringIO()
        main(fin, fout)

        # then
        self.assertEqual(fout.getvalue(), "\n")


# TODO: tokenize print(123)
# TODO: evaluate PrintNode(123)
# TODO: parse [print, (, 123, )]


if __name__ == "__main__":
    unittest.main()
