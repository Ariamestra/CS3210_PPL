# Maria Estrada 
#Programming Project 1 - Due Sep 22
# Sep 19, 2024 - About 2.5 hours to complete
#-------------------------------------------

DIGITS = '0123456789'

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
            return f"RR_{self.type}:{self.value}"
        return f"RR_{self.type}"

# Token Types
ME_INT = 'ME_INT'
ME_FLOAT = 'ME_FLOAT'
ME_PLUS = 'ME_PLUS'
ME_MINUS = 'ME_MINUS'
ME_ILLEGAL = 'ME_ILLEGAL'
ME_MULTIPLY = 'ME_MULTIPLY'
ME_DIVIDE = 'ME_DIVIDE'
ME_LPAREN = 'ME_LPAREN'
ME_RPAREN = 'ME_RPAREN'

class ASTNode:
    pass

class BinOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f'({self.left}, {self.op}, {self.right})'

class Num(ASTNode):
    def __init__(self, token):
        self.value = token.value

    def __repr__(self):
        return f'ME_INT:{self.value}'

# Parser class that tokenizes input
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
        return self.current_token

    def parse(self):
        return self.expression()

    def make_tokens(self):
        tokens = []
        self.advance_char()
        while self.current_char is not None:
            if self.current_char in ' \t':
                self.advance()  # Skip spaces and tabs
            elif self.current_char in DIGITS:
                tokens.append(self.make_digit())
            elif self.current_char == '+':
                tokens.append(Token(ME_PLUS))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(ME_MINUS))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(ME_MULTIPLY))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(ME_DIVIDE))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(ME_LPAREN))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(ME_RPAREN))
                self.advance()
            else:
                tokens.append(self.make_illegal())
                self.advance_char()
        return tokens

    def advance_char(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.index] if self.pos.index < len(self.text) else None

    def make_digit(self):
        num_str = ''
        while self.current_char is not None and self.current_char in DIGITS:
            num_str += self.current_char
            self.advance_char()
        return Token(ME_INT, int(num_str))

    def factor(self):
        token = self.current_token
        if token.type == ME_INT:
            self.advance()
            return Num(token)
        else:
            raise Exception(f"Expected number, but got {token.type}")

    def term(self):
        left = self.factor()
        while self.current_token.type in (ME_MULTIPLY, ME_DIVIDE):
            op_token = self.current_token
            self.advance()
            right = self.factor()
            left = BinOp(left, op_token, right)
        return left

    def expression(self):
        left = self.term()
        while self.current_token.type in (ME_PLUS, ME_MINUS):
            op_token = self.current_token
            self.advance()
            right = self.term()
            left = BinOp(left, op_token, right)
        return left

def run(text):
    parser = Parser(text)
    AST = parser.parse()
    return AST





