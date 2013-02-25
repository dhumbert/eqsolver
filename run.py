import argparse
import sys
import solver

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Solve an equation in one variable')
    parser.add_argument('-e', help='An equation to solve', metavar='equation')
    parser.add_argument('-f', help='A file containing an equation to solve',
        metavar='filepath')

    args = parser.parse_args()
    filename = args.f
    equation = args.e

    if filename is not None and equation is not None:
        print("You cannot specify both a file and an equation")
        sys.exit(1)
    elif filename is None and equation is None:
        print("You must specify either a file to process or an equation")
        sys.exit(1)
    elif filename is not None:
        try:
            f = open(filename)
            equation = f.read()
        except IOError:
            print("Could not open file %s" % filename)
            sys.exit(1)

    equation_solver = solver.Solver(equation)
    result = equation_solver.solve()
