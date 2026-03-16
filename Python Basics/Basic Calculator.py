def add(a, b): return a + b

def subtract(a, b): return a - b

def multiply(a, b): return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

operations = {'+': add, '-': subtract, '*': multiply, '/': divide}

print("Calculator Running (type 'quit' to exit) - \n")

while True:
    expr = input("Enter expression (e.g. 5 + 3): ").strip()
    if expr.lower() == 'quit':
        print("Goodbye!")
        break

    parts = expr.split()
    if len(parts) != 3:
        print("Invalid format. Use: number operator number\n")
        continue

    num1_str, operator, num2_str = parts

    if operator not in operations:
        print(f"Unknown operator '{operator}'. Use +, -, *, /\n")
        continue

    try:
        num1, num2 = float(num1_str), float(num2_str)
        result = operations[operator](num1, num2)
        print(f"= {result:g}\n")
    except ValueError as e:
        print(f"Error: {e}\n")

