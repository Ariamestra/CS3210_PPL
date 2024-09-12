DIGITS = '0123456789'

class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.value:
            return f"{self.type}:{self.value}"
        return f"{self.type}"

# Token Types
RR_INT  = 'RR_INT'
RR_FLOAT = 'RR_FLOAT'
RR_PLUS  = 'RR_PLUS'
RR_MINUS = 'RR_MINUS'
RR_ILLEGAL = 'RR_ILLEGAL'

class Lexer: # Converts input to tokens
    def __init__(self, text):
        self.text = text
        self.pos = -1 # Starting Position 
        self.current_char = None
        self.advance()

    def advance(self): # Go to next character
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def make_tokens(self): # Make tokens from input
        tokens = []
        while self.current_char is not None:
            if self.current_char in ' \t':
                self.advance()  # Skip spaces and tabs
            elif self.current_char in DIGITS:
                tokens.append(self.make_digit())
            elif self.current_char == '+':
                tokens.append(Token(RR_PLUS))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(RR_MINUS))
                self.advance()
            else:
                tokens.append(self.make_illegal())
        return tokens

    def make_digit(self): # Return tockens
        num_str = ''
        while self.current_char is not None and self.current_char in DIGITS:
            num_str += self.current_char
            self.advance()
        return Token(RR_INT, int(num_str))

    def make_illegal(self): # Handle illegal characters
        illegal_char = self.current_char
        self.advance()  # Move past the illegal character
        print(f"Illegal Character: '{illegal_char}'")
        return Token(RR_ILLEGAL, illegal_char)

def run(text):
    lexer = Lexer(text)
    tokens = lexer.make_tokens()
    return tokens

# Test Cases
print(run("1 + 2"))
print(run("1 - 2"))
print(run("d + 1"))



