from parser import BinOp, Num, UnaryOp
from lexer import DIGITS, Token, ME_INT, ME_FLOAT, ME_PLUS, ME_MINUS, ME_MULTIPLY, ME_DIVIDE, ME_LPAREN, ME_RPAREN, ME_ILLEGAL, Position, ME_AND, ME_OR, ME_NOT, ME_EQ, ME_NEQ, ME_LT, ME_GT, ME_LTE, ME_GTE

def eval_ast(node):
    if isinstance(node, Num):
        return node.value
    elif isinstance(node, BinOp):
        left = eval_ast(node.left)
        right = eval_ast(node.right)
        op_type = node.op.type
        
        # Arithmetic Operations
        if op_type == ME_PLUS:
            return left + right
        elif op_type == ME_MINUS:
            return left - right
        elif op_type == ME_MULTIPLY:
            return left * right
        elif op_type == ME_DIVIDE:
            return left / right
        
        # Relational Operations
        elif op_type == ME_EQ:
            return left == right
        elif op_type == ME_NEQ:
            return left != right
        elif op_type == ME_LT:
            return left < right
        elif op_type == ME_GT:
            return left > right
        elif op_type == ME_LTE:
            return left <= right
        elif op_type == ME_GTE:
            return left >= right

        # Logical Operations
        elif op_type == ME_AND:
            return bool(left) and bool(right)
        elif op_type == ME_OR:
            return bool(left) or bool(right)
        
    elif isinstance(node, UnaryOp):
        op_type = node.op.type
        operand = eval_ast(node.operand)
        if op_type == ME_MINUS:
            return -operand
        elif op_type == ME_NOT:
            return not operand
    raise SyntaxError("Invalid syntax")
