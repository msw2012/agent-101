"""
Sample Python file for testing the File Explainer Agent.
"""


def calculate_fibonacci(n: int) -> int:
    """Calculate the nth Fibonacci number."""
    if n <= 1:
        return n
    return calculate_fibonacci(n - 1) + calculate_fibonacci(n - 2)


def main():
    """Print the first 10 Fibonacci numbers."""
    for i in range(10):
        print(f"F({i}) = {calculate_fibonacci(i)}")


if __name__ == "__main__":
    main()
