# Maria Estrada 
# Programming Project 3 - Due Dec 1
#-----------------------------------------------

# Represents Tokens
class Token:
    def __init__(self, type_, value=None, pos=None):
        self.type = type_ 
        self.value = value # Value of the Token
        self.pos = pos # Position 

    def __repr__(self):
        return f"Token({self.type}, {self.value}, {self.pos})"

# Takes a text input, tokenizes it, and parses it
class Parser:
    def __init__(self, text):
        self.text = text  # Keep original input
        self.clean_text = text.replace(' ', '')  # Remove 
        self.pos = 0
        self.tokens = self.tokenize()

    def tokenize(self):
        tokens = []
        while self.pos < len(self.clean_text):
            # Handle numbers 
            if self.clean_text[self.pos].isdigit() or \
               (self.clean_text[self.pos] == '-' and self.pos + 1 < len(self.clean_text) and self.clean_text[self.pos + 1].isdigit()):
                num_start = self.pos
                if self.clean_text[self.pos] == '-':
                    self.pos += 1
                while self.pos < len(self.clean_text) and (self.clean_text[self.pos].isdigit() or self.clean_text[self.pos] == '.'):
                    self.pos += 1
                num_str = self.clean_text[num_start:self.pos]

                try:
                    # Find more dots for error handling
                    if num_str.count('.') > 1:
                        second_dot = num_str.find('.', num_str.find('.') + 1)
                        raise ValueError(f"Unexpected token '.' at position {self.original_position(num_start + second_dot)}")
                    value = float(num_str) if '.' in num_str else int(num_str)
                    tokens.append(Token('NUMBER', value, self.original_position(num_start)))
                except ValueError:
                    raise ValueError(f"Unexpected token '{num_str}' at position {self.original_position(num_start)}")
                continue
            
            # Handle operators and unexpected characters
            if self.clean_text[self.pos] in '+-*/()><=!,':
                if self.clean_text[self.pos] == ',':
                    raise ValueError(f"Unexpected token ',' at position {self.original_position(self.pos)}")
                if self.pos + 1 < len(self.clean_text):
                    two_char_op = self.clean_text[self.pos:self.pos + 2]
                    if two_char_op in ['==', '!=', '<=', '>=']:
                        tokens.append(Token(two_char_op, two_char_op, self.original_position(self.pos)))
                        self.pos += 2
                        continue
                # Token Types    
                op_map = {
                    '+': 'PLUS',
                    '-': 'MINUS',
                    '*': 'MULTIPLY',
                    '/': 'DIVIDE',
                    '(': 'LPAREN',
                    ')': 'RPAREN',
                    '>': 'GT',
                    '<': 'LT',
                    '>=': 'GTE',
                    '<=': 'LTE',
                    '=': 'EQ',
                    '!': 'NOT',
                    '!=': 'NEQ',
                    '|':'OR',
                    '&': 'AND'

                }
                tokens.append(Token(op_map[self.clean_text[self.pos]], self.clean_text[self.pos], self.original_position(self.pos)))
                self.pos += 1
            else:
                raise ValueError(f"Unexpected token '{self.clean_text[self.pos]}' at position {self.original_position(self.pos)}")
        return tokens

    def original_position(self, clean_pos):
        original_pos = 0
        clean_index = 0
        for i, char in enumerate(self.text):
            if char == ' ':
                continue  # Skip spaces in the original string
            if clean_index == clean_pos:
                return i
            clean_index += 1
        return -1  # Return -1 if the position is invalid

    def parse(self):
        def expression():
            return comparison()

        def comparison():
            left = addition()
            while self.current_token and self.current_token.type in ['==', '!=', '>', '<', '>=', '<=']:
                op = self.current_token
                self.advance()
                right = addition()
                left = {'type': 'binary', 'op': op, 'left': left, 'right': right}
            return left

        def addition():
            left = multiplication()
            while self.current_token and self.current_token.type in ['PLUS', 'MINUS']:
                op = self.current_token
                self.advance()
                right = multiplication()
                left = {'type': 'binary', 'op': op, 'left': left, 'right': right}
            return left

        def multiplication():
            left = parse_negative()
            while self.current_token and self.current_token.type in ['MULTIPLY', 'DIVIDE']:
                op = self.current_token
                self.advance()
                right = parse_negative()
                left = {'type': 'binary', 'op': op, 'left': left, 'right': right}
            return left

        def parse_negative(): 
            if self.current_token and self.current_token.type in ['MINUS', 'NOT']:
                op = self.current_token
                self.advance()
                return {'type': 'parse_negative', 'op': op, 'expr': parse_negative()}
            return primary()

        def primary():
            if self.current_token and self.current_token.type == 'NUMBER':
                node = self.current_token
                self.advance()
                return node
            if self.current_token and self.current_token.type == 'LPAREN':
                self.advance()
                node = expression()
                if not self.current_token or self.current_token.type != 'RPAREN':
                    raise ValueError("Expected closing parenthesis")
                self.advance()
                return node
            raise ValueError(f"Unexpected token '{self.current_token.value}' at position {self.current_token.pos}")

        self.current_token = self.tokens[0] if self.tokens else None
        self.token_index = 0
        return expression()

    def advance(self):
        self.token_index += 1
        self.current_token = self.tokens[self.token_index] if self.token_index < len(self.tokens) else None

# Evaluate the result of the expression.
def evaluate(node):
    if isinstance(node, Token):
        return node.value

    if node['type'] == 'binary':
        left = evaluate(node['left'])
        right = evaluate(node['right'])
        op = node['op'].type

        # Arithmetic operations
        if op == 'PLUS': return left + right
        if op == 'MINUS': return left - right
        if op == 'MULTIPLY': return left * right
        if op == 'DIVIDE': return left / right

        # Comparison operations
        if op == '==': return left == right
        if op == '!=': return left != right
        if op == '>': return left > right
        if op == '<': return left < right
        if op == '>=': return left >= right
        if op == '<=': return left <= right

    if node['type'] == 'parse_negative':
        value = evaluate(node['expr'])
        op = node['op'].type

        if op == 'MINUS': return -value
        if op == 'NOT': return not value

    raise ValueError("Invalid node type")

# Test the expressions given
def Test(expression):
    try:
        parser = Parser(expression)
        parsed = parser.parse()
        result = evaluate(parsed)
        print(f"{expression} = {result}")
    except Exception as e:
        print(f"{expression}         {str(e)}")


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
    Test(test)
