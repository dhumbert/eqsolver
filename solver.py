import re
import collections

tokens = {
    'NUMBER': '\d',
    'PLUS': '\+',
    'MINUS': '\-',
    'TIMES': '\*',
    'DIVIDE': '/',
    'EQUALS': '=',
    'LPAREN': '\(',
    'RPAREN': '\)',
}

precedence = {
    'TIMES': 3,
    'DIVIDE': 3,
    'PLUS': 2,
    'MINUS': 2,
    'EQUALS': 1
}

left_assoc = ('PLUS', 'MINUS', 'TIMES', 'DIVIDE')


class Solver:
    def __init__(self, equation_string):
        self.equation_string = equation_string.replace(" ", "")
        self.output_queue = collections.deque()
        self.stack = collections.deque()

    def solve(self):
        self.parse()

    def parse(self):
        """Parse the equation using the shunting-yard algorithm"""
        # http://en.wikipedia.org/wiki/Shunting-yard_algorithm
        eq = self.equation_string
        i = 0
        while i < len(eq):
            for tok in tokens:
                if re.match(tokens[tok], eq[i]):
                    if tok == 'NUMBER':
                        number = str(eq[i])
                        for nexttok in eq[i + 1:]:
                            if re.match(tokens[tok], nexttok):
                                number += nexttok
                                i += 1  # skip next token
                            else:
                                break
                        self.output_queue.append(number)
                        i += 1
                        break
                    else:
                        for si in range(0, len(self.stack) - 1):
                            stack_op = self.stack[si]
                            if (precedence[tok] < precedence[stack_op] 
                                or (tok in left_assoc and precedence[tok] == precedence[stack_op])):
                                self.stack.popleft()
                                self.output_queue.append(stack_op)
                        self.stack.appendleft(tok)
                        i += 1
                        break

        # clean up stack
        for stack_op in self.stack:
            self.output_queue.append(stack_op)
