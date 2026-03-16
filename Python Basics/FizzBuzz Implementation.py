def fizzbuzz(n, rules):
    """Apply fizzbuzz rules to a number. Returns the label or the number itself."""
    result = ''.join(label for divisor, label in rules if n % divisor == 0)
    return result if result else str(n)


def run_fizzbuzz(start, end, rules, output_format='list'):
    """Run fizzbuzz over a range and return results in the chosen format."""
    results = [fizzbuzz(n, rules) for n in range(start, end + 1)]

    if output_format == 'list':
        for i, val in enumerate(results, start=start):
            print(f"{i:>4}: {val}")

    elif output_format == 'stats':
        total = len(results)
        fizz_count    = sum(1 for r in results if r == 'Fizz')
        buzz_count    = sum(1 for r in results if r == 'Buzz')
        fizzbuzz_count= sum(1 for r in results if r == 'FizzBuzz')
        number_count  = sum(1 for r in results if r.isdigit())

        print(f"\n--- FizzBuzz Stats ({start} to {end}) ---")
        print(f"  Total numbers : {total}")
        print(f"  Fizz          : {fizz_count}  ({fizz_count/total*100:.1f}%)")
        print(f"  Buzz          : {buzz_count}  ({buzz_count/total*100:.1f}%)")
        print(f"  FizzBuzz      : {fizzbuzz_count}  ({fizzbuzz_count/total*100:.1f}%)")
        print(f"  Plain numbers : {number_count}  ({number_count/total*100:.1f}%)")

    elif output_format == 'inline':
        print(', '.join(results))

    return results


def get_custom_rules():
    """Prompt user to enter custom divisor-label rules."""
    rules = []
    print("\nEnter custom rules (leave divisor blank to finish):")
    while True:
        divisor = input("  Divisor: ").strip()
        if not divisor:
            break
        label = input("  Label  : ").strip()
        try:
            rules.append((int(divisor), label))
        except ValueError:
            print("  Invalid divisor, skipping.")
    return rules if rules else [(3, 'Fizz'), (5, 'Buzz')]


def get_int(prompt, default):
    """Helper to get an integer input with a default fallback."""
    val = input(prompt).strip()
    try:
        return int(val)
    except ValueError:
        return default


def main():
    print("=== Intermediate FizzBuzz ===\n")

    # --- Range ---
    start = get_int("Start of range (default 1) : ", 1)
    end   = get_int("End of range   (default 100): ", 100)
    if start > end:
        print("Start must be <= end. Swapping values.")
        start, end = end, start

    # --- Rules ---
    print("\nUse default rules? (3=Fizz, 5=Buzz)")
    use_default = input("Enter 'y' for default, 'n' for custom: ").strip().lower()
    rules = [(3, 'Fizz'), (5, 'Buzz')] if use_default != 'n' else get_custom_rules()

    print("\nRules active:")
    for divisor, label in rules:
        print(f"  {divisor} → {label}")

    # --- Output format ---
    print("\nOutput format:")
    print("  1. List (numbered)")
    print("  2. Stats summary")
    print("  3. Inline (comma-separated)")
    print("  4. All of the above")
    choice = input("Choose (1-4, default 1): ").strip()

    format_map = {'1': 'list', '2': 'stats', '3': 'inline'}

    print()
    if choice == '4':
        run_fizzbuzz(start, end, rules, 'inline')
        run_fizzbuzz(start, end, rules, 'stats')
    else:
        run_fizzbuzz(start, end, rules, format_map.get(choice, 'list'))


if __name__ == '__main__':
    main()