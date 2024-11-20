# Homework 5 Part 3 & 4
# Due Dec 1

def solve(letters, equation, mapping={}):
    if len(mapping) == len(letters):
        if equation_is_satisfied(mapping, equation):
            return mapping
        else:
            return None

    # Go through digits for the current letter
    current_letter = next(letter for letter in letters if letter not in mapping)
    for digit in range(10):
        if is_valid(current_letter, digit, mapping, letters):
            # Assign the digit to the current letter
            mapping[current_letter] = digit

            # Solve for the remaining letters
            result = solve(letters, equation, mapping)
            if result:
                return result

            # Backtrack if no solution
            del mapping[current_letter]

    return None  

def is_valid(letter, digit, mapping, letters):
    first_letters = {word[0] for word in equation.split() if word.isalpha()} # First letter in any word cannot be 0
    if letter in first_letters and digit == 0:
        return False

    # Digits must be unique for each letter
    if digit in mapping.values():
        return False

    return True

def equation_is_satisfied(mapping, equation):
    # Replace letters with digits
    equation_translated = ""
    for char in equation:
        if char.isalpha():
            equation_translated += str(mapping[char])
        else:
            equation_translated += char

    # Check equation
    try:
        return eval(equation_translated)
    except:
        return False


letters = set("TWOTWOTWENTY") 
equation = "TWO x TWO == TWENTY"  

solution = solve(letters, equation)
if solution:
    print("Solution:", solution)
else:
    print("No solution found.")


'''
Testing
--------------------------------------------------------------------------
letters = set("SENDMOREMONEY") 
equation = "SEND + MORE == MONEY"
Solution: {'S': 9, 'E': 5, 'N': 6, 'R': 8, 'M': 1, 'Y': 2, 'O': 0, 'D': 7}

letters = set("LEETCODEPOINT") 
equation = "LEET + CODE == POINT"
No solution found.

letters = set("TOGOOUT") 
equation = "TO + GO == OUT"  
Solution: {'O': 1, 'U': 0, 'G': 8, 'T': 2}

letters = set("TWOTWOFOUR") 
equation = "TWO + TWO == FOUR" 
Solution: {'W': 2, 'R': 6, 'T': 9, 'U': 5, 'F': 1, 'O': 8}

letters = set("TESTINGTOSEE") 
equation = "TESTING + TO == SEE" 
No solution found.

letters = set("TWOTWOTWENTY") 
equation = "TWO x TWO == TWENTY"  
KeyError: 'x'
'''