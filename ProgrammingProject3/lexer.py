# Maria Estrada 
# Programming Project 3 - Due Dec 1
# lexer.py
#-------------------------------------------

DIGITS = '0123456789'

# Class to track the current position
class Position:
    def __init__(self, index, line_num, column_num, fn, text):
        self.index = index
        self.line_num = line_num
        self.column_num = column_num
        self.fn = fn
        self.text = text
        
    # Track the position of the current character in the input
    def advance(self, current_char=None):
        self.index += 1
        self.column_num += 1
        if current_char == '\n':
            self.line_num += 1
            self.column_num = 0
        return self
    

    def copy(self):
        return Position(self.index, self.line_num, self.column_num, self.fn, self.text)

# Token class to represent the type and value of tokens
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
ME_MULTIPLY = 'ME_MULTIPLY'
ME_DIVIDE = 'ME_DIVIDE'
ME_LPAREN = 'ME_LPAREN'
ME_RPAREN = 'ME_RPAREN'
ME_ILLEGAL = 'ME_ILLEGAL'
