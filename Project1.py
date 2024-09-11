#------------------------------------------------------
DIGITS = '0123456789'
 
class Token:
 
  def __init__(self, type_, value=None):
    self.type = type_
    self.value = value
 
  def __repr__(self):
    return f"Token('{self.value}', '{self.type}')"
 
# TOKENS
ME_INT  = 'ME_INT'
ME_FLOAT = 'ME_FLOAT'
ME_PLUS  = 'ME_PLUS'
ME_MINUS = 'ME_MINUS'
ME_DIGIT = 'ME_DIGIT'
 
class Lexer:
  def __init__(self, fn, text):
    self.text = text
    self.pos = -1
    self.current_char = None
    self.advance()
 
  def advance(self):
    self.pos+=1
   
    if self.pos < len(self.text):
       self.current_char = self.text[self.pos]  
    else:
       self.current_char=None
 
  def make_tokens(self):
    tokens = []
    print(self.current_char)
    while self.current_char != None:
       if self.current_char == '+':
         tokens.append(Token(ME_PLUS))
       self.advance()
    return tokens
 
  def make_digit(self):
     num_str = ''
     dot_count = 0
 
     while self.current_char != None and self.current_char in DIGITS + '.':
 
      if self.current_char == '.':
        if dot_count == 1: break
        dot_count += 1
        num_str += '.'
     else:
         num_str += self.current_char
     self.advance()
     #if dot_count <= 0 and <=9:
        #return Token(ME_DIGIT, digit(num_str))
     if dot_count == 0:
        return Token(ME_INT, int(num_str))
     else:
        return Token(ME_FLOAT, float(num_str))
 
def run(fn, text):
  lexer = Lexer(fn, text)
  tokens = lexer.make_tokens()
  return tokens
#------------------------------------------------------