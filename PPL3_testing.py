class Token:
    def __init__(self, type_, value=None, pos=None):
        self.type = type_
        self.value = value
        self.pos = pos

class Parser:
    def __init__(self, text):
        self.text = text.replace(' ', '')  # Remove whitespace
        self.pos = 0
        self.tokens = self.tokenize()

    def tokenize(self):
        tokens = []
        while self.pos < len(self.text):
            # Handle digits (including negative numbers and decimals)
            if self.text[self.pos].isdigit() or \
               (self.text[self.pos] == '-' and self.pos+1 < len(self.text) and self.text[self.pos+1].isdigit()):
                num_start = self.pos
                # Handle negative number
                if self.text[self.pos] == '-':
                    self.pos += 1
                
                # Parse number (integer or float)
                while self.pos < len(self.text) and (self.text[self.pos].isdigit() or self.text[self.pos] == '.'):
                    self.pos += 1
                
                num_str = self.text[num_start:self.pos]
                try:
                    # Check for multiple decimal points
                    if num_str.count('.') > 1:
                        raise ValueError(f"Invalid number format: {num_str}")
                    
                    value = float(num_str) if '.' in num_str else int(num_str)
                    tokens.append(Token('NUMBER', value, num_start))
                except ValueError:
                    raise ValueError(f"Invalid number: {num_str} at position {num_start}")
                continue

            # Handle operators and parentheses
            if self.text[self.pos] in '+-*/()><=!':
                # Handle multi-character operators
                if self.pos + 1 < len(self.text):
                    two_char_op = self.text[self.pos:self.pos+2]
                    if two_char_op in ['==', '!=', '<=', '>=']:
                        tokens.append(Token(two_char_op, two_char_op, self.pos))
                        self.pos += 2
                        continue

                # Single character operators
                op_map = {
                    '+': 'PLUS',
                    '-': 'MINUS',
                    '*': 'MULTIPLY',
                    '/': 'DIVIDE',
                    '(': 'LPAREN',
                    ')': 'RPAREN',
                    '>': 'GT',
                    '<': 'LT',
                    '=': 'EQ',
                    '!': 'NOT'
                }
                tokens.append(Token(op_map[self.text[self.pos]], self.text[self.pos], self.pos))
                self.pos += 1
            else:
                # Unexpected character
                raise ValueError(f"Unexpected token '{self.text[self.pos]}' at position {self.pos}")

        return tokens

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
            left = unary()
            while self.current_token and self.current_token.type in ['MULTIPLY', 'DIVIDE']:
                op = self.current_token
                self.advance()
                right = unary()
                left = {'type': 'binary', 'op': op, 'left': left, 'right': right}
            return left

        def unary():
            if self.current_token and self.current_token.type in ['MINUS', 'NOT']:
                op = self.current_token
                self.advance()
                return {'type': 'unary', 'op': op, 'expr': unary()}
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
            
            raise ValueError(f"Unexpected token {self.current_token}")

        # Initialize parsing
        self.current_token = self.tokens[0] if self.tokens else None
        self.token_index = 0
        return expression()

    def advance(self):
        self.token_index += 1
        self.current_token = self.tokens[self.token_index] if self.token_index < len(self.tokens) else None

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

    if node['type'] == 'unary':
        value = evaluate(node['expr'])
        op = node['op'].type

        if op == 'MINUS': return -value
        if op == 'NOT': return not value

    raise ValueError("Invalid node type")

def Test(expression):
    try:
        parser = Parser(expression)
        parsed = parser.parse()
        result = evaluate(parsed)
        print(f"{expression} = {result}")
    except Exception as e:
        print(f"{expression}            {str(e)}")

# Test cases
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

# Run tests
for test in test_cases:
    Test(test)