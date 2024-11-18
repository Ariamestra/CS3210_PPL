# Maria Estrada 
# Programming Project 3 - Due Dec 1
# Main.py
#-------------------------------------------
from parser import Parser
from evaluator import eval_ast  # Import the evaluator function from evaluator.py

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
