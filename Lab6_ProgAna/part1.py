def example_function():
    x = 5
    y = 10
    z = 15
    print(x)

def another_function():
    if True:
      print("Check Indentation")

function analyze_code(file_path):
    code_lines = read_file(file_path)
    indentation_issues = []
    unused_variables = []
    defined_variables = {}
    
    # Check indentation
    for line_number, line in enumerate(code_lines):
        if is_code_line(line) and not line.startswith(" " * 4):
            indentation_issues.append((line_number, line))

    # Check for unused variables
    for function in find_functions(code_lines):
        variables = extract_variables(function)
        for variable in variables:
            if variable not used in function:
                unused_variables.append(variable)
    
    return {
        "Indentation Issues": indentation_issues,
        "Unused Variables": unused_variables
    }

