import unittest
import solver


class TestSolver(unittest.TestCase):
    """ Test the solver.Pretty white-box, but parsing is new to me"""
    def test_tokenize(self):
        eqs = solver.Solver('4+3')
        eqs.parse()
        self.assertEqual(len(eqs.output_queue), 3)

        eqs = solver.Solver('4+3*5-2')
        eqs.parse()
        self.assertEqual(len(eqs.output_queue), 7)

        eqs = solver.Solver('4123*10')
        eqs.parse()
        self.assertEqual(len(eqs.output_queue), 3)

        eqs = solver.Solver('(2 + 3) * 2')
        eqs.parse()
        self.assertEqual(len(eqs.output_queue), 5)


if __name__ == '__main__':
    unittest.main()
