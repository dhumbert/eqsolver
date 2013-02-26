import unittest
import solver


class TestSolver(unittest.TestCase):
    """ Test the tokenizer. Pretty white-box, but parsing is new to me"""
    def test_tokenize(self):
        eqs = solver.Solver('4+3')
        eqs.tokenize()
        self.assertEqual(list(eqs.output_queue), ['4', '3', 'PLUS'])

        eqs = solver.Solver('4+3*5-2')
        eqs.tokenize()
        self.assertEqual(list(eqs.output_queue), ['4', '3', '5', 'TIMES', 'PLUS', '2', 'MINUS'])

        eqs = solver.Solver('4123*10')
        eqs.tokenize()
        self.assertEqual(list(eqs.output_queue), ['4123', '10', 'TIMES'])

        eqs = solver.Solver('(2 + 3) * 2')
        eqs.tokenize()
        self.assertEqual(list(eqs.output_queue), ['2', '3', 'PLUS', '2', 'TIMES'])


if __name__ == '__main__':
    unittest.main()
