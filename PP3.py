# Maria Estrada 
# Programming Project 3 - Due Dec 1
#-----------------------------------------------
# Main.py
DIGITS = '0123456789'

class ASTNode:
    pass

class BinOp(ASTNode):
    """Represents a binary operation node in the AST."""
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f'({self.left}, {self.op}, {self.right})'

class Num(ASTNode):
    """Represents a numeric node in the AST."""
    def __init__(self, token):
        self.value = token.value

    def __repr__(self):
        return f'{self.value}'

class UnaryOp(ASTNode):
    """Represents a unary operation node in the AST."""
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand

    def __repr__(self):
        return f'({self.op}, {self.operand})'

class Position:
    def __init__(self, index, line_num, column_num, fn, text):
        self.index = index
        self.line_num = line_num
        self.column_num = column_num
        self.fn = fn
        self.text = text

    def advance(self, current_char=None):
        self.index += 1
        self.column_num += 1
        if current_char == '\n':
            self.line_num += 1
            self.column_num = 0
        return self

    def copy(self):
        return Position(self.index, self.line_num, self.column_num, self.fn, self.text)

class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.value is not None:
            return f"{self.type}:{self.value}"
        return f"{self.type}"

ME_INT = 'ME_INT'
ME_FLOAT = 'ME_FLOAT'
ME_PLUS = 'ME_PLUS'
ME_MINUS = 'ME_MINUS'
ME_MULTIPLY = 'ME_MULTIPLY'
ME_DIVIDE = 'ME_DIVIDE'
ME_LPAREN = 'ME_LPAREN'
ME_RPAREN = 'ME_RPAREN'
ME_ILLEGAL = 'ME_ILLEGAL'
ME_AND = 'ME_AND'
ME_OR = 'ME_OR'
ME_NOT = 'ME_NOT'
ME_EQ = 'ME_EQ'
ME_NEQ = 'ME_NEQ'
ME_LT = 'ME_LT'
ME_GT = 'ME_GT'
ME_LTE = 'ME_LTE'
ME_GTE = 'ME_GTE'

class Parser:
    def __init__(self, text, fn="<stdin>"):
        self.text = text
        self.pos = Position(-1, 1, 0, fn, text)
        self.current_char = None
        self.tokens = self.make_tokens()
        self.current_token = None
        self.token_idx = -1
        self.advance()

    def advance(self):
        self.token_idx += 1
        if self.token_idx < len(self.tokens):
            self.current_token = self.tokens[self.token_idx]
        else:
            self.current_token = None
        return self.current_token

    def advance_char(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.index] if self.pos.index < len(self.text) else None

    def peek_next(self):
        next_index = self.pos.index + 1
        if next_index < len(self.text):
            return self.text[next_index]
        return None
    
    def make_tokens(self):
        tokens = []
        self.advance_char()
        while self.current_char is not None:
            if self.current_char in ' \t':
                self.advance_char()
            elif self.current_char in DIGITS:
                tokens.append(self.make_digit())
            elif self.current_char == '+':
                tokens.append(Token(ME_PLUS))
                self.advance_char()
            elif self.current_char == '-':
                tokens.append(Token(ME_MINUS))
                self.advance_char()
            elif self.current_char == '*':
                if self.peek_next() == '*':  # Handle unexpected '**'
                    raise Exception(f"Unexpected token '*' at position {self.pos.index}")
                tokens.append(Token(ME_MULTIPLY))
                self.advance_char()
            elif self.current_char == '/':
                tokens.append(Token(ME_DIVIDE))
                self.advance_char()
            elif self.current_char == '(':
                tokens.append(Token(ME_LPAREN))
                self.advance_char()
            elif self.current_char == ')':
                tokens.append(Token(ME_RPAREN))
                self.advance_char()
            elif self.current_char == '&':
                if self.peek_next() == '&':
                    tokens.append(Token(ME_AND))
                    self.advance_char()
                    self.advance_char()
                else:
                    raise Exception(f"Unexpected token '&' at position {self.pos.index}")
            elif self.current_char == '|':
                if self.peek_next() == '|':
                    tokens.append(Token(ME_OR))
                    self.advance_char()
                    self.advance_char()
                else:
                    raise Exception(f"Unexpected token '|' at position {self.pos.index}")
            elif self.current_char == '=':
                if self.peek_next() == '=':
                    tokens.append(Token(ME_EQ))
                    self.advance_char()
                    self.advance_char()
                else:
                    raise Exception(f"Unexpected token '=' at position {self.pos.index}")
            elif self.current_char == '!':
                if self.peek_next() == '=':
                    tokens.append(Token(ME_NEQ))
                    self.advance_char()
                    self.advance_char()
                else:
                    tokens.append(Token(ME_NOT))
                    self.advance_char()
            elif self.current_char == '<':
                if self.peek_next() == '=':
                    tokens.append(Token(ME_LTE))
                    self.advance_char()
                    self.advance_char()
                else:
                    tokens.append(Token(ME_LT))
                    self.advance_char()
            elif self.current_char == '>':
                if self.peek_next() == '=':
                    tokens.append(Token(ME_GTE))
                    self.advance_char()
                    self.advance_char()
                else:
                    tokens.append(Token(ME_GT))
                    self.advance_char()
            else:
                raise Exception(f"Unexpected token '{self.current_char}' at position {self.pos.index}")
        return tokens
    
    def make_digit(self):
        """Recognizes integer and float numbers in the input text."""
        num_str = ''
        dot_count = 0  # Keep track of decimal points to identify floats

        while self.current_char is not None and (self.current_char in DIGITS or self.current_char == '.'):
            if self.current_char == '.':
                if dot_count == 1:  # If there's already one dot, break to prevent two decimal points
                    break
                dot_count += 1
            num_str += self.current_char
            self.advance_char()

        # Determine if the number is an integer or a float
        if dot_count == 0:
            return Token(ME_INT, int(num_str))  # Integer
        else:
            return Token(ME_FLOAT, float(num_str))  # Float

    def parse(self):
        # Placeholder parse method to allow parsing.
        # For demonstration, let's assume it just returns a simple Num node.
        if len(self.tokens) == 1 and isinstance(self.tokens[0], Token):
            return Num(self.tokens[0])
        raise NotImplementedError("Parser's parse method needs to be fully implemented")

def eval_ast(node):
    if isinstance(node, Num):
        return node.value
    elif isinstance(node, BinOp):
        left = eval_ast(node.left)
        right = eval_ast(node.right)
        op_type = node.op.type
        
        # Arithmetic Operations
        if op_type == ME_PLUS:
            return left + right
        elif op_type == ME_MINUS:
            return left - right
        elif op_type == ME_MULTIPLY:
            return left * right
        elif op_type == ME_DIVIDE:
            return left / right
        
        # Relational Operations
        elif op_type == ME_EQ:
            return left == right
        elif op_type == ME_NEQ:
            return left != right
        elif op_type == ME_LT:
            return left < right
        elif op_type == ME_GT:
            return left > right
        elif op_type == ME_LTE:
            return left <= right
        elif op_type == ME_GTE:
            return left >= right

        # Logical Operations
        elif op_type == ME_AND:
            return bool(left) and bool(right)
        elif op_type == ME_OR:
            return bool(left) or bool(right)
        
    elif isinstance(node, UnaryOp):
        op_type = node.op.type
        operand = eval_ast(node.operand)
        if op_type == ME_MINUS:
            return -operand
        elif op_type == ME_NOT:
            return not operand
    raise SyntaxError("Invalid syntax")

def evaluate_expression(expression):
    try:
        parser = Parser(expression)
        ast = parser.parse()
        result = eval_ast(ast)  # Evaluates the AST to get the final result
        return f"{expression} = {result}"
    except Exception as e:
        # Displaying any errors, including unexpected tokens or syntax issues
        return f"{expression}            {e}"

# Run the test cases
test_cases = [
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
    "-1+(-2.0)", 
    "1*2,5", 
    "1*2.5e2", 
    "M1 + 2.5", 
    "1 + 2&5", 
    "1 * 2.5.6", 
    "1 ** 2.5",
    "*1 / 2.5", 
    "(1 + 2) > (2 * 1)", 
    "(3 * 2) == 6", 
    "10 != 5 + 5"
]

for test in test_cases:
    print(evaluate_expression(test))
