class ASTNode:
    pass

class BinOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Num(ASTNode):
    def __init__(self, value):
        self.value = value

def print_ast(node, indent=""):
    if isinstance(node, Num):
        print(f"{indent}Num({node.value})")
    elif isinstance(node, BinOp):
        print(f"{indent}BinOp({node.op})")
        print_ast(node.left, indent + "  ")
        print_ast(node.right, indent + "  ")

ast_tree = BinOp(
    left=BinOp(left=Num(7), op='+', right=Num(3)),
    op='*',
    right=BinOp(left=Num(5), op='-', right=Num(2)),
)

print("Abstract Syntax Tree:")
print_ast(ast_tree)