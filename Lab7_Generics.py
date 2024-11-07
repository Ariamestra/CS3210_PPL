# Maria Estrada - Lab 7 Generics
# Due Sunday Nov 10

from typing import TypeVar, Generic, List

T = TypeVar('T')  # Declare a type variable 'T'

class Stack(Generic[T]):
    def __init__(self):
        self.items: List[T] = []

    def push(self, item: T) -> None:
        """Push an item onto the stack."""
        self.items.append(item)

    def pop(self) -> T:
        """Pop an item from the stack and return it."""
        if not self.is_empty():
            return self.items.pop()
        else:
            raise IndexError("pop from an empty stack")

    def peek(self) -> T:
        """Return the top item on the stack without removing it."""
        if not self.is_empty():
            return self.items[-1]
        else:
            raise IndexError("peek from an empty stack")

    def is_empty(self) -> bool:
        """Check if the stack is empty."""
        return len(self.items) == 0

    def size(self) -> int:
        """Return the number of items in the stack."""
        return len(self.items)
    
# Evaluate expression and give result
def evaluate_postfix(expression: str) -> int:
    # Empty stack
    stack = Stack[int]()

    # Make tokens
    for token in expression.split():
        if token.isdigit():
            # Push to stack
            stack.push(int(token))
        else:
            # Pop the top 2 operands 
            operand2 = stack.pop()
            operand1 = stack.pop()

            # Perform the operation 
            if token == '+':
                result = operand1 + operand2
            elif token == '-':
                result = operand1 - operand2
            elif token == '*':
                result = operand1 * operand2
            elif token == '/':
                result = operand1 // operand2  

            # Push the result back to the stack
            stack.push(result)

    # The final result is the only item in the stack
    return stack.pop()

# Get expression and give result
expression = input("Enter an expression: ")
result = evaluate_postfix(expression)
print("The result of the expression is:", result)


'''
$ python3 Lab7_Generics.py
Enter an expression: 1 2 + 3 * 5 /
The result of the expression is: 1
'''