import collections

tokens = {
    '+': 'PLUS',
    '-': 'MINUS',
    '*': 'TIMES',
    '/': 'DIVIDE',
    '=': 'EQUALS',
}

precedence = {
    'TIMES': 3,
    'DIVIDE': 3,
    'PLUS': 2,
    'MINUS': 2,
    'EQUALS': 1
}

left_assoc = ('PLUS', 'MINUS', 'TIMES', 'DIVIDE')


class ParseError(Exception):
    pass


class Solver:
    def __init__(self, equation_string):
        self.equation = equation_string.replace(" ", "")
        self.output_queue = collections.deque()

    def solve(self):
        if len(self.output_queue) == 0:
            self.tokenize();

        value = 0
        operands = []
        for token in self.output_queue:
            if self.is_number(token):
                operands.append(token)
            elif self.is_op_id(token):
                operands, value = self.evaluate(token, operands)
                operands.append(value)
            else:
                raise ParseError("Invalid token: %s" % token)

        return operands[0]

    def evaluate(self, op_id, operands):
        return {
            'TIMES': self.evaluate_multiply(operands),
            'DIVIDE': self.evaluate_divide(operands),
            'PLUS': self.evaluate_add(operands),
            'MINUS': self.evaluate_subtract(operands),
        }[op_id]

    def evaluate_add(self, operands):
        return (operands[:-2], float(operands[-2]) + float(operands[-1]))

    def evaluate_subtract(self, operands):
        return (operands[:-2], float(operands[-2]) - float(operands[-1]))

    def evaluate_multiply(self, operands):
        return (operands[:-2], float(operands[-2]) * float(operands[-1]))

    def evaluate_divide(self, operands):
        return (operands[:-2], float(operands[-2]) / float(operands[-1]))

    def is_op(self, token):
        return token in tokens

    def is_op_id(self, token):
        return token in tokens.values()

    def is_left_paren(self, token):
        return token == '('

    def is_right_paren(self, token):
        return token == ')'

    def is_number(self, token):
        try:
            float(token)
            return True
        except ValueError:
            return False

    def is_digit(self, token):
        return token.isdigit() or token == '.'

    def op_id(self, token):
        try:
            return tokens[token]
        except IndexError:
            raise ParseError("Invalid operator")

    def precedence(self, token):
        return precedence[token]

    def left_assoc(self, token):
        return token in left_assoc

    def has_tokens(self):
        return len(self.equation) > 0

    def next_token(self):
        next = self.equation[0]
        self.equation = self.equation[1:]
        return next

    def peek(self):
        return self.equation[0]

    def iterate_stack(self, stack, current_op_id):
        # while there is an operator token, o2, at the top of the stack, and
        # either o1 is left-associative and its precedence is
        # less than or equal to that of o2,
        # or o1 has precedence less than that of o2,
        while (
                len(stack) > 0
                and self.is_op_id(stack[0])
                and (
                    (
                        self.left_assoc(current_op_id)
                        and self.precedence(current_op_id)
                            <= self.precedence(stack[0])
                    )
                    or (
                        self.precedence(current_op_id)
                            < self.precedence(stack[0])
                    )
                )
            ):
            yield  # pass control back to pop off the stack

    def tokenize(self):
        """Parse the equation using the shunting-yard algorithm"""
        # http://en.wikipedia.org/wiki/Shunting-yard_algorithm
        stack = collections.deque()

        while self.has_tokens():
            token = self.next_token()

            if self.is_left_paren(token):
                stack.appendleft('LPAREN')
            elif self.is_right_paren(token):
                stack_op = stack.popleft()
                while stack_op != 'LPAREN':
                    self.output_queue.append(stack_op)
                    stack_op = stack.popleft()
            elif self.is_op(token):
                op_id = self.op_id(token)

                for _ in self.iterate_stack(stack, op_id):
                    self.output_queue.append(stack.popleft())
                stack.appendleft(op_id)
            elif self.is_digit(token):
                # peek ahead to see if it's a multi-digit number
                while self.has_tokens():
                    if self.is_digit(self.peek()):
                        token += self.next_token()
                    else:
                        break
                self.output_queue.append(token)
            else:
                raise ParseError("Invalid token: %s" % token)

        # clean up stack
        for stack_op in stack:
            self.output_queue.append(stack_op)
