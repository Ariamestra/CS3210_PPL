# Maria Estrada 
# Programming Project 3 - Due Dec 1
#-----------------------------------------------

import operator

class ExpressionTree:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def evaluate(self):
        if isinstance(self.value, bool) or isinstance(self.value, (int, float)):
            return self.value
        elif self.value == 'AND':
            return self.left.evaluate() and self.right.evaluate()
        elif self.value == 'OR':
            return self.left.evaluate() or self.right.evaluate()
        elif self.value == 'NOT':
            return not self.left.evaluate()
        else:
            left_value = self.left.evaluate() if self.left else None
            right_value = self.right.evaluate() if self.right else None
            return self.apply_operator(self.value, left_value, right_value)

    @staticmethod
    def apply_operator(op, left, right):
        ops = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv,
            '==': operator.eq,
            '!=': operator.ne,
            '<': operator.lt,
            '>': operator.gt,
            '<=': operator.le,
            '>=': operator.ge
        }
        if op in ops:
            if left is None or right is None:
                raise ValueError("Invalid expression: missing operand")
            return ops[op](left, right)
        else:
            raise ValueError(f"Unsupported operator: {op}")


def parse_expression(expression):
    tokens = tokenize(expression)
    output, operators = [], []
    precedence = {'OR': 1, 'AND': 2, 'NOT': 3, '==': 4, '!=': 4, '<': 4, '>': 4, '<=': 4, '>=': 4, '+': 5, '-': 5, '*': 6, '/': 6}

    for token in tokens:
        if token.isdigit() or token in ('True', 'False'):
            output.append(ExpressionTree(int(token) if token.isdigit() else token == 'True'))
        elif token in precedence:
            while (operators and operators[-1] != '(' and
                   precedence[operators[-1]] >= precedence[token]):
                output.append(ExpressionTree(operators.pop()))
            operators.append(token)
        elif token == '(':
            operators.append(token)
        elif token == ')':
            while operators and operators[-1] != '(':
                output.append(ExpressionTree(operators.pop()))
            if not operators:
                raise ValueError("Mismatched parentheses")
            operators.pop()
        else:
            raise ValueError(f"Unexpected token: {token}")

    while operators:
        if operators[-1] == '(':
            raise ValueError("Mismatched parentheses")
        output.append(ExpressionTree(operators.pop()))

    return build_tree(output)


def tokenize(expression):
    tokens, i = [], 0
    while i < len(expression):
        if expression[i].isspace():
            i += 1
        elif expression[i] in '()+-*/':
            tokens.append(expression[i])
            i += 1
        elif expression[i:i+3] in ('AND', 'NOT'):
            tokens.append(expression[i:i+3])
            i += 3
        elif expression[i:i+2] == 'OR':
            tokens.append(expression[i:i+2])
            i += 2
        elif expression[i:i+2] in ('==', '!=', '<=', '>='):
            tokens.append(expression[i:i+2])
            i += 2
        elif expression[i] in ('<', '>'):
            tokens.append(expression[i])
            i += 1
        elif expression[i].isdigit() or expression[i] == '-':
            num = expression[i]
            i += 1
            while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                num += expression[i]
                i += 1
            tokens.append(num)
        else:
            raise ValueError(f"Unexpected token: {expression[i]}")
    return tokens


def build_tree(postfix_tokens):
    stack = []
    for token in postfix_tokens:
        if isinstance(token.value, (int, float, bool)):
            stack.append(token)
        else:
            if token.value == 'NOT':
                if not stack:
                    raise ValueError("Invalid expression: missing operand for 'NOT'")
                node = token
                node.left = stack.pop()
                stack.append(node)
            else:
                if len(stack) < 2:
                    raise ValueError("Invalid expression: missing operand")
                node = token
                node.right = stack.pop()
                node.left = stack.pop()
                stack.append(node)
    if len(stack) != 1:
        raise ValueError("Invalid expression: too many operands")
    return stack[0]


def evaluate_expression(expression):
    tree = parse_expression(expression)
    return tree.evaluate()

# Example usage
tests = [
    "1+2+3+4",
    "1*2*3*4",
    "1-2-3-4",
    "1/2/3/4",
    "1*2+3*4",
    "1+2*3+4",
    "(1+2)*(3+4)",
    "1+(2*3)*(4+5)",
    "1+(2*3)/4+5",
    "5/(4+3)/2",
    "1 + 2.5",
    "125",
    "-1",
    "-1+(-2)",
    "-1+(-2.0)"
]

for test in tests:
    try:
        print(f"{test} = {evaluate_expression(test)}")
    except ValueError as e:
        print(f"{test}            {e}")


