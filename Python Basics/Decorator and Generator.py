import time
import random


# -------- Decorator --------
def log_time_safe(func):
    def wrapper(*args, **kwargs):
        print(f"[LOG] Starting '{func.__name__}'")
        start = time.time()
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            print(f"[ERROR] {e}")
        finally:
            end = time.time()
            print(f"[LOG] Finished in {end - start:.4f} sec\n")
    return wrapper


# -------- Generator --------
def data_stream(n):
    """Simulate a stream of random numbers"""
    for _ in range(n):
        yield random.randint(1, 10)


# -------- Processing Function --------
@log_time_safe
def process_data(stream):
    """Square only even numbers"""
    result = []
    for value in stream:
        if value % 2 == 0:
            result.append(value ** 2)
    return result


# -------- Main --------
def main():
    stream = data_stream(10)
    output = process_data(stream)
    print("Processed Data:", output)


if __name__ == "__main__":
    main()