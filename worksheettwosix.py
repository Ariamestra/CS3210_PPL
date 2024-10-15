import time

# Define the decorator
def log_execution_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()  # Record start time
        result = func(*args, **kwargs)  # Call the function
        end_time = time.time()  # Record end time
        execution_time = end_time - start_time  # Calculate execution time
        print(f"Function '{func.__name__}' executed in {execution_time:.4f} seconds")
        return result
    return wrapper

# Apply the decorator to the function
@log_execution_time
def find_max(numbers):
    return max(numbers)

# Example usage
print(find_max([1, 3, 7, 0, 5]))  # Output: 7 and logs execution time
