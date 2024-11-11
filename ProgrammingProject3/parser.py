# Maria Estrada 
# Programming Project 3 - Due Dec 1
# parser.py 
#-------------------------------------------
from lexer import DIGITS, Token, ME_INT, ME_FLOAT, ME_PLUS, ME_MINUS, ME_MULTIPLY, ME_DIVIDE, ME_LPAREN, ME_RPAREN, ME_ILLEGAL, Position

# Base class for nodes in AST
class ASTNode:
    pass

# Binary operations
class BinOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f'({self.left}, {self.op}, {self.right})'

# Class to represent numbers in AST
class Num(ASTNode):
    def __init__(self, token):
        self.value = token.value

    def __repr__(self):
        return f'ME_INT:{self.value}'

class Parser:
    def __init__(self, text, fn="<stdin>"):
        self.text = text
        self.pos = Position(-1, 1, 0, fn, text)
        self.current_char = None
        self.tokens = self.make_tokens()  
        self.current_token = None
        self.token_idx = -1  
        self.advance()  

    #Advance to the next token
    def advance(self):
        self.token_idx += 1
        if self.token_idx < len(self.tokens):
            self.current_token = self.tokens[self.token_idx]
        else:
            self.current_token = None
        return self.current_token

    # Begin parsing the input
    def parse(self):
        result = self.expression()
        if self.current_token is not None:
            raise Exception(f"Unexpected token: {self.current_token}")
        return result

    # Tokenize the input string into a list of tokens
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
            else:
                tokens.append(self.make_illegal())
                self.advance_char()
        return tokens

    # Advances to the next character in the input string
    def advance_char(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.index] if self.pos.index < len(self.text) else None

    # Create a token for a number by reading digits from the input
    def make_digit(self):
        num_str = ''
        dot_count = 0  # Track if there's more than one dot
        while self.current_char is not None and (self.current_char in DIGITS or self.current_char == '.'):
            if self.current_char == '.':
                if dot_count == 1:  
                    break
                dot_count += 1
            num_str += self.current_char
            self.advance_char()
        
        if dot_count == 0:
            return Token(ME_INT, int(num_str))  # No dot means it's an integer
        else:
            return Token(ME_FLOAT, float(num_str))  # One dot means it's a float


    # Handle illegal characters
    def make_illegal(self):
        pos_copy = self.pos.copy()
        illegal_char = self.current_char
        self.advance_char()
        print(f"Illegal Character: '{illegal_char}'")
        print(f"File {self.pos.fn}, line {pos_copy.line_num}, column {pos_copy.column_num}")
        return Token(ME_ILLEGAL, illegal_char)

    # Parse a factor - int or parentheses
    def factor(self):
        token = self.current_token
        if token.type == ME_INT or token.type == ME_FLOAT: 
            self.advance()
            return Num(token)
        elif token.type == ME_LPAREN:
            self.advance()
            expr = self.expression()
            if self.current_token is not None and self.current_token.type == ME_RPAREN:
                self.advance()
                return expr
            else:
                raise Exception("Missing closing parenthesis")
        else:
            raise Exception(f"Unexpected token: {token}")


    # Parse a term - mul or div
    def term(self):
        left = self.factor()
        while self.current_token is not None and self.current_token.type in (ME_MULTIPLY, ME_DIVIDE):
            op_token = self.current_token
            self.advance()
            right = self.factor()
            left = BinOp(left, op_token, right)
        return left

    # Parse an expression - plus or minus
    def expression(self):
        left = self.term()
        while self.current_token is not None and self.current_token.type in (ME_PLUS, ME_MINUS):
            op_token = self.current_token
            self.advance()
            right = self.term()
            left = BinOp(left, op_token, right)
        return left