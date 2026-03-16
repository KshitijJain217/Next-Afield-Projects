
# Concepts covered:
#   • Functions & modules (modular design)
#   • Input validation & error handling (try/except)
#   • Loops & conditionals
#   • History tracking with a list
#   • A dispatch-table (dict of functions) — intermediate trick


import math


# MODULE 1 – Basic Arithmetic


def add(a, b):
    """Return the sum of a and b."""
    return a + b


def subtract(a, b):
    """Return the difference of a and b."""
    return a - b


def multiply(a, b):
    """Return the product of a and b."""
    return a * b


def divide(a, b):
    """Return the quotient of a divided by b.
    Raises ValueError if b is zero.
    """
    if b == 0:
        raise ValueError("Cannot divide by zero!")
    return a / b


# MODULE 2 – Advanced Operations

def power(a, b):
    """Return a raised to the power b."""
    return a ** b


def square_root(a, _=None):   # second arg ignored (keeps signature uniform)
    """Return the square root of a.
    Raises ValueError for negative input.
    """
    if a < 0:
        raise ValueError("Cannot take square root of a negative number!")
    return math.sqrt(a)


def modulus(a, b):
    """Return the remainder when a is divided by b."""
    if b == 0:
        raise ValueError("Cannot find modulus with zero divisor!")
    return a % b


def integer_divide(a, b):
    """Return the floor (integer) division of a by b."""
    if b == 0:
        raise ValueError("Cannot divide by zero!")
    return a // b


# MODULE 3 – History Manager


history = []   # stores every calculation as a string


def add_to_history(expression: str, result):
    """Append a completed calculation to history."""
    entry = f"{expression} = {result}"
    history.append(entry)


def show_history():
    """Print all past calculations."""
    if not history:
        print("\n  (No calculations yet.)\n")
    else:
        print("\n  -- Calculation History --")
        for i, item in enumerate(history, start=1):
            print(f"  {i:>3}. {item}")
        print()


def clear_history():
    """Wipe all history entries."""
    history.clear()
    print("\n  History cleared.\n")


# MODULE 4 – Input Helpers


def get_number(prompt: str) -> float:
    """
    Keep asking until the user enters a valid number.
    Returns a float.
    """
    while True:
        raw = input(prompt).strip()
        try:
            return float(raw)
        except ValueError:
            print(f"  X  '{raw}' is not a valid number. Please try again.")


def get_menu_choice(valid_choices: set) -> str:
    """
    Keep asking until the user enters one of the valid choices.
    Returns the choice as a lowercase string.
    """
    while True:
        choice = input("\n  Your choice: ").strip().lower()
        if choice in valid_choices:
            return choice
        print(f"  X  Invalid option. Choose from: {sorted(valid_choices)}")


# MODULE 5 – Display / UI Helpers


SEPARATOR = "  " + "-" * 40


def print_header():
    print("\n" + "=" * 44)
    print("         MODULAR CALCULATOR")
    print("=" * 44)


def print_main_menu():
    print(SEPARATOR)
    print("  MAIN MENU")
    print(SEPARATOR)
    print("  1  Basic Arithmetic   (+  -  *  /)")
    print("  2  Advanced Operations (^  sqrt  %  //)")
    print("  3  View History")
    print("  4  Clear History")
    print("  0  Quit")
    print(SEPARATOR)


def print_basic_menu():
    print(SEPARATOR)
    print("  BASIC ARITHMETIC")
    print(SEPARATOR)
    print("  1  Add          (a + b)")
    print("  2  Subtract     (a - b)")
    print("  3  Multiply     (a * b)")
    print("  4  Divide       (a / b)")
    print("  0  Back to Main Menu")
    print(SEPARATOR)


def print_advanced_menu():
    print(SEPARATOR)
    print("  ADVANCED OPERATIONS")
    print(SEPARATOR)
    print("  1  Power        (a ^ b)")
    print("  2  Square Root  (sqrt a)")
    print("  3  Modulus      (a mod b)")
    print("  4  Integer Div  (a // b)")
    print("  0  Back to Main Menu")
    print(SEPARATOR)


# MODULE 6 – Operation Runner


# Dispatch tables: map menu keys -> (function, symbol, needs_two_args)
BASIC_OPS = {
    "1": (add,      "+",   True),
    "2": (subtract, "-",   True),
    "3": (multiply, "*",   True),
    "4": (divide,   "/",   True),
}

ADVANCED_OPS = {
    "1": (power,          "^",    True),
    "2": (square_root,    "sqrt", False),   # only needs one number
    "3": (modulus,        "mod",  True),
    "4": (integer_divide, "//",   True),
}


def run_operation(ops_table: dict, choice: str):
    """
    Execute the selected operation:
      1. Look up the function and meta-info from the dispatch table.
      2. Collect inputs (one or two numbers).
      3. Call the function inside a try/except so errors are caught cleanly.
      4. Show and store the result.
    """
    func, symbol, needs_two = ops_table[choice]

    print()
    a = get_number("  Enter first number : ")

    if needs_two:
        b = get_number("  Enter second number: ")
        expression = f"{a} {symbol} {b}"
    else:
        b = None
        expression = f"{symbol}({a})"

    try:
        result = func(a, b) if needs_two else func(a)

        # Format: integers look cleaner without a decimal point
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        else:
            result = round(result, 10)   # trim floating-point noise

        print(f"\n  OK  {expression} = {result}\n")
        add_to_history(expression, result)

    except ValueError as err:
        print(f"\n  X  Error: {err}\n")


# MODULE 7 – Sub-menus


def basic_menu_loop():
    while True:
        print_basic_menu()
        choice = get_menu_choice({"1", "2", "3", "4", "0"})
        if choice == "0":
            break
        run_operation(BASIC_OPS, choice)


def advanced_menu_loop():
    while True:
        print_advanced_menu()
        choice = get_menu_choice({"1", "2", "3", "4", "0"})
        if choice == "0":
            break
        run_operation(ADVANCED_OPS, choice)


# MODULE 8 – Main Entry Point


def main():
    print_header()

    while True:
        print_main_menu()
        choice = get_menu_choice({"1", "2", "3", "4", "0"})

        if choice == "1":
            basic_menu_loop()
        elif choice == "2":
            advanced_menu_loop()
        elif choice == "3":
            show_history()
        elif choice == "4":
            clear_history()
        elif choice == "0":
            print("\n  Goodbye! Thanks for using Modular Calculator.\n")
            break


# -- Entry guard
if __name__ == "__main__":
    main()