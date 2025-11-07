from typing import List

def collatz_sequence(n: int) -> List[int]:

    if n <= 0:
        raise ValueError("Input must be a positive integer")
    
    # Base case: if we've reached 1, return it
    if n == 1:
        return [1]
    
    # If n is even, we need to divide by 2; if odd, multiply by 3 and add 1
    if n % 2 == 0:
        # Even: divide by 2
        next_n = n // 2
    else:
        # Odd: multiply by 3 and add 1
        next_n = 3 * n + 1
    # We need to wrap the `n` in a list
    return [n] + collatz_sequence(next_n)


def main():
    print("\n" + "=" * 50)
    print("\nEnter positive integers to see their Collatz sequences.")
    print("Type 'quit' to exit.\n")
    
    while True:
        user_input = input("Enter a number (or 'quit'): ").strip()
        
        if user_input.lower() == 'quit':
            print("Exiting interactive mode.")
            break
        
        # Handle number input
        try:
            n = int(user_input)
            if n <= 0:
                print("Please enter a positive integer.\n")
                continue
            
            # Generate and display the sequence
            sequence = collatz_sequence(n)
            
            print(f"\n{'=' * 50}")
            print(f"Collatz Sequence for n = {n}")
            print(f"{'=' * 50}")
            
            print(f"Sequence: {' → '.join(map(str, sequence))}")

        except ValueError:
            print("Invalid input. Please enter a positive integer.\n")


if __name__ == "__main__":
    main()
