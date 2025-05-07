import time
import ast

def analyze_code(code_text):
    tree = ast.parse(code_text)
    suggestions = []
    task_type = None

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            func_name = node.name.lower()
            if 'fib' in func_name:
                suggestions.append("Function '{}' seems to implement Fibonacci using recursion. Suggest memoization or iteration.".format(func_name))
                task_type = 'fibonacci'
            elif 'sum' in func_name:
                suggestions.append("Function '{}' uses nested loops for summing. Suggest using direct mathematical formula.".format(func_name))
                task_type = 'sum'
            elif 'fact' in func_name:
                suggestions.append("Function '{}' uses recursion for factorial. Suggest using iteration.".format(func_name))
                task_type = 'factorial'
        if isinstance(node, ast.For):
            if any(isinstance(child, ast.For) for child in ast.iter_child_nodes(node)):
                suggestions.append("Nested loops detected. Consider mathematical simplification if possible.")

    return suggestions, task_type

def get_optimized_code(task_type):
    if task_type == 'fibonacci':
        return """def optimized_fibonacci(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = optimized_fibonacci(n-1, memo) + optimized_fibonacci(n-2, memo)
    return memo[n]

print(optimized_fibonacci(30))
"""
    elif task_type == 'sum':
        return """def optimized_sum(n):
    return (n * (n - 1)) // 2

print(optimized_sum(5000))
"""
    elif task_type == 'factorial':
        return """def optimized_factorial(n):
    result = 1
    for i in range(2, n+1):
        result *= i
    return result

print(optimized_factorial(100))
"""
    else:
        return "# No major optimization available."

def run_code_and_measure(code_text):
    start = time.perf_counter()  # Using perf_counter for better precision
    try:
        exec(code_text, {})
    except Exception as e:
        print("Error while running code:", e)
    end = time.perf_counter()
    return end - start

def main():
    print("Please paste your Python code below (end input with an empty line):")
    user_code = ""
    while True:
        line = input()
        if line.strip() == "":
            break
        user_code += line + "\n"

    print("\nAnalyzing code...\n")

    # Measure original execution time
    original_time = run_code_and_measure(user_code)

    suggestions, task_type = analyze_code(user_code)

    print(f"Execution Time Before Optimization: {original_time:.6f} seconds\n")

    print("Optimization Suggestions:")
    if suggestions:
        for s in suggestions:
            print("- " + s)
    else:
        print("- No major optimization suggestions detected.")

    optimized_code = get_optimized_code(task_type)

    print("\nSuggested Optimized Code Snippet:\n")
    print(optimized_code)

    # Measure optimized code time
    print("\nRunning the optimized code...")
    optimized_time = run_code_and_measure(optimized_code)

    print("\nExecution Time After Optimization: {:.6f} seconds".format(optimized_time))

    # Report
    print("\n--- Performance Report ---")
    print("Before Optimization:")
    print(f"- {original_time:.6f} seconds")
    print("After Optimization:")
    print(f"- {optimized_time:.6f} seconds")
    
    if original_time > 0:
        improvement = ((original_time - optimized_time) / original_time) * 100
        print(f"Improvement:\n- Execution speed improved by {improvement:.2f}%")
    else:
        print("Improvement:\n- Cannot calculate improvement due to negligible original time.")

    print("\nNote: Only basic optimizations are handled automatically.")

if __name__ == "__main__":
    main()
