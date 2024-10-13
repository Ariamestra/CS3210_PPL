# Maria Estrada 
# Programming Project 2 - Due Oct 20
#-------------------------------------------
from parser import Parser

def run(text):
    parser = Parser(text)
    AST = parser.parse()
    return AST

if __name__ == "__main__":
    print("If you want to exit enter 'exit' ")
    while True:
        expr = input("M@E > ")
        if expr.lower() == 'exit':
            break
        try:
            parser = Parser(expr)
            ast = parser.parse()
            print(ast)
            print(" ")
        except Exception as e:
            print("Error:", e)
            print(" ")