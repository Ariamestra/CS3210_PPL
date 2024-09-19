# Maria Estrada 
#Programming Project 1 - Due Sep 22
# Sep 19, 2024 - About 2.5 hours to complete
#-------------------------------------------
'''
M@E > 1+2
[ME_INT:1, ME_PLUS, ME_INT:2]
M@E > 2-1
[ME_INT:2, ME_MINUS, ME_INT:1]
M@E > 4*5
[ME_INT:4, ME_MULTIPLY, ME_INT:5]
M@E > 8/4
[ME_INT:8, ME_DIVIDE, ME_INT:4]
M@E > (1+2)*3
[ME_LPAREN, ME_INT:1, ME_PLUS, ME_INT:2, ME_RPAREN, ME_MULTIPLY, ME_INT:3]
M@E > d+1
Illegal Character: 'd'
File <stdin>, line 1, column 1
[ME_ILLEGAL:d, ME_PLUS, ME_INT:1]
'''

DIGITS = '0123456789'

# Position class to track current position in the input
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

# Lexer class that tokenizes input
class Lexer:
    def __init__(self, text, fn="<stdin>"):
        self.text = text
        self.pos = Position(-1, 1, 0, fn, text)  # Initialize with a Position object
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.index] if self.pos.index < len(self.text) else None

    def make_tokens(self):
        tokens = []
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
        return tokens

    def make_digit(self):
        num_str = ''
        while self.current_char is not None and self.current_char in DIGITS:
            num_str += self.current_char
            self.advance()
        return Token(ME_INT, int(num_str))

    def make_illegal(self):
        pos_copy = self.pos.copy()
        illegal_char = self.current_char
        self.advance()
        print(f"Illegal Character: '{illegal_char}'")
        print(f"File {self.pos.fn}, line {pos_copy.line_num}, column {pos_copy.column_num}")
        return Token(ME_ILLEGAL, illegal_char)

def run(text):
    lexer = Lexer(text)
    tokens = lexer.make_tokens()
    return tokens





