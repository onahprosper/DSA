import random
import numpy as np
from typing import List, Tuple

BOARD_SIZE = 8  # Standard chessboard size

# Knight's possible moves (8 directions)
KNIGHT_MOVES = [
    (2, 1), (1, 2), (-1, 2), (-2, 1),
    (-2, -1), (-1, -2), (1, -2), (2, -1)
]


def create_empty_board() -> np.ndarray:
    """
    Create and return an empty chessboard (8x8) using NumPy.
    
    Returns:
        np.ndarray: An 8x8 matrix initialized with zeros
    """
    return np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)


def display_board(board: List[List[int]]) -> None:
    """
    Display the chessboard in a formatted way.
    
    Args:
        board: The board to display
    """
    print("\n" + "=" * 50)
    print("Knight's Tour Board")
    print("=" * 50)
    
    # Print column headers
    print("    ", end="")
    for col in range(BOARD_SIZE):
        print(f"{col:3d} ", end="")
    print("\n    " + "-" * (BOARD_SIZE * 4 + 1))
    
    # Print rows with row numbers
    for row in range(BOARD_SIZE):
        print(f"{row} | ", end="")
        for col in range(BOARD_SIZE):
            print(f"{board[row][col]:3d} ", end="")
        print("|")
    
    print("    " + "-" * (BOARD_SIZE * 4 + 1))
    print("=" * 50 + "\n")


def is_valid_move(row: int, col: int, board: List[List[int]]) -> bool:
    """
    Check if a position is valid and unvisited.
    
    Args:
        row: Row position
        col: Column position
        board: Current board state
        
    Returns:
        bool: True if the move is valid, False otherwise
    """
    return (0 <= row < BOARD_SIZE and 
            0 <= col < BOARD_SIZE and 
            board[row][col] == 0)


def get_valid_moves(row: int, col: int, board: List[List[int]]) -> List[Tuple[int, int]]:
    """
    Get all valid moves from the current position.
    
    Args:
        row: Current row
        col: Current column
        board: Current board state
        
    Returns:
        List of valid (row, col) positions
    """
    valid_moves = []
    for dr, dc in KNIGHT_MOVES:
        new_row, new_col = row + dr, col + dc
        if is_valid_move(new_row, new_col, board):
            valid_moves.append((new_row, new_col))
    return valid_moves


def is_closed_tour(start_pos: Tuple[int, int], current_pos: Tuple[int, int]) -> bool:
    """
    Check if the knight can return to the starting position from current position.
    
    Args:
        board: Current board state
        start_pos: Starting position (row, col)
        current_pos: Current position (row, col)
        
    Returns:
        bool: True if knight can return to start, False otherwise
    """
    curr_row, curr_col = current_pos
    start_row, start_col = start_pos
    
    for dr, dc in KNIGHT_MOVES:
        new_row, new_col = curr_row + dr, curr_col + dc
        if new_row == start_row and new_col == start_col:
            return True
    return False


def KnightsTourBacktracking(startingPosition: Tuple[int, int]) -> Tuple[bool, List[List[int]]]:
    """
    Solve Knight's Tour using Backtracking with Warnsdorff's heuristic.
    
    Strategy:
    - Uses Warnsdorff's heuristic: always move to the square from which 
      the knight will have the fewest onward moves.
    - This heuristic significantly improves performance by reducing the search space.
    - Backtracking occurs when no valid moves are available and not all squares are visited.
    
    Args:
        startingPosition: Tuple (row, col) for starting position
        
    Returns:
        Tuple[bool, List[List[int]]]: 
            - bool: True if closed tour found, False otherwise
            - List[List[int]]: Board with move sequence (0 for unvisited)
    """
    board = create_empty_board()
    start_row, start_col = startingPosition
    
    # Validate starting position
    if not (0 <= start_row < BOARD_SIZE and 0 <= start_col < BOARD_SIZE):
        return False, board
    
    def backtrack(row: int, col: int, move_count: int) -> bool:
        """
        Recursive backtracking function.
        
        Args:
            row: Current row
            col: Current column
            move_count: Number of moves made so far
            
        Returns:
            bool: True if solution found, False otherwise
        """
        # Mark current position with move number
        board[row][col] = move_count
        
        # Check if tour is complete
        if move_count == BOARD_SIZE * BOARD_SIZE:
            # Check if it's a closed tour (can return to start)
            if is_closed_tour(startingPosition, (row, col)):
                return True
            else:
                # Not a closed tour, backtrack
                board[row][col] = 0
                return False
        
        # Get all valid moves
        valid_moves = get_valid_moves(row, col, board)
        
        # Apply Warnsdorff's heuristic: sort moves by number of onward moves
        # Prioritize squares with fewer onward moves (ties broken arbitrarily)
        
        valid_moves.sort(key=lambda pos: len(
            get_valid_moves(pos[0], pos[1], board)))
        
        # Try each valid move
        for next_row, next_col in valid_moves:
            if backtrack(next_row, next_col, move_count + 1):
                return True
        
        # Backtrack: undo the current move
        board[row][col] = 0
        return False
    
    # Start the backtracking from the starting position
    success = backtrack(start_row, start_col, 1)
    return success, board


def KnightsTourLasVegas(startingPosition: Tuple[int, int]) -> Tuple[bool, List[List[int]]]:
    """
    Solve Knight's Tour using Las Vegas (randomized) algorithm.
    
    Strategy:
    - Randomness is applied in the selection of the next move.
    - At each step, randomly choose one of the available valid moves.
    - This is a Monte Carlo approach: may succeed or fail randomly.
    - Alternative randomness: Could use Warnsdorff's heuristic with random tie-breaking.
    
    End conditions:
    - Success: All squares visited and can return to start
    - Failure: Knight gets stuck (no valid moves) or steps on visited square
    
    Args:
        startingPosition: Tuple (row, col) for starting position
        
    Returns:
        Tuple[bool, List[List[int]]]: 
            - bool: True if closed tour found, False otherwise
            - List[List[int]]: Board with move sequence (0 for unvisited)
    """
    board = create_empty_board()
    start_row, start_col = startingPosition
    
    # Validate starting position
    if not (0 <= start_row < BOARD_SIZE and 0 <= start_col < BOARD_SIZE):
        return False, board
    
    current_row, current_col = start_row, start_col
    move_count = 1
    
    # Mark starting position
    board[current_row][current_col] = move_count
    
    # Continue until all squares are visited or no valid moves
    while move_count < BOARD_SIZE * BOARD_SIZE:
        # Get all valid moves from current position
        valid_moves = get_valid_moves(current_row, current_col, board)
        
        # Check if knight is stuck (no valid moves)
        if not valid_moves:
            # Tour unsuccessful - knight ran out of moves
            return False, board
        
        # RANDOMNESS: Randomly select one of the valid moves
        next_row, next_col = random.choice(valid_moves)
        
        # Move to the selected position
        move_count += 1
        current_row, current_col = next_row, next_col
        board[current_row][current_col] = move_count
    
    # All squares visited - check if it's a closed tour
    if is_closed_tour(startingPosition, (current_row, current_col)):
        return True, board
    else:
        return False, board


def get_user_choice() -> str:
    """
    Get and validate user's choice of algorithm.
    
    Returns:
        str: User's choice ('backtracking', 'lasvegas', or 'exit')
    """
    while True:
        print("\n" + "=" * 50)
        print("Knight's Tour - Closed Version")
        print("=" * 50)
        print("Choose an approach:")
        print("  1. Backtracking")
        print("  2. Las Vegas (Randomized)")
        print("  3. Exit")
        print("=" * 50)
        
        choice = input("Enter your choice (1/2/3): ").strip()
        
        if choice == '1':
            return 'backtracking'
        elif choice == '2':
            return 'lasvegas'
        elif choice == '3':
            return 'exit'
        else:
            print("❌ Invalid input! Please enter 1, 2, or 3.")


def get_starting_position() -> Tuple[int, int]:
    """
    Get and validate starting position from user.
    
    Returns:
        Tuple[int, int]: Valid starting position (row, col)
    """
    while True:
        try:
            print(f"\nEnter starting position (0-{BOARD_SIZE-1} for both row and column):")
            row = int(input(f"  Row (0-{BOARD_SIZE-1}): ").strip())
            col = int(input(f"  Column (0-{BOARD_SIZE-1}): ").strip())
            
            if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
                return (row, col)
            else:
                print(f"❌ Invalid position! Row and column must be between 0 and {BOARD_SIZE-1}.")
        except ValueError:
            print("❌ Invalid input! Please enter integer values.")


def run_performance_test(num_runs: int = 10000) -> None:
    """
    Run performance test to compare success rates of both algorithms.
    
    Args:
        num_runs: Number of test runs for each algorithm
    """
    print(f"\n{'='*60}")
    print(f"Running Performance Test ({num_runs} runs each)")
    print(f"{'='*60}")
    
    # Test from position (0, 0) for consistency
    test_position = (0, 0)
    
    # Test Backtracking
    print("\nTesting Backtracking...")
    backtrack_success = 0
    for i in range(num_runs):
        if (i + 1) % 1000 == 0:
            print(f"  Progress: {i + 1}/{num_runs} runs completed")
        success, _ = KnightsTourBacktracking(test_position)
        if success:
            backtrack_success += 1
    
    backtrack_rate = (backtrack_success / num_runs) * 100
    
    # Test Las Vegas
    print("\nTesting Las Vegas...")
    lasvegas_success = 0
    for i in range(num_runs):
        if (i + 1) % 1000 == 0:
            print(f"  Progress: {i + 1}/{num_runs} runs completed")
        success, _ = KnightsTourLasVegas(test_position)
        if success:
            lasvegas_success += 1
    
    lasvegas_rate = (lasvegas_success / num_runs) * 100
    
    # Display results
    print(f"\n{'='*60}")
    print("Performance Test Results")
    print(f"{'='*60}")
    print(f"Backtracking Success Rate: {backtrack_success}/{num_runs} ({backtrack_rate:.2f}%)")
    print(f"Las Vegas Success Rate:    {lasvegas_success}/{num_runs} ({lasvegas_rate:.2f}%)")
    print(f"{'='*60}\n")


def main():
    """
    Main function to run the Knight's Tour program.
    """
    # Display empty board at start
    print("\nEmpty Chessboard:")
    display_board(create_empty_board())
    
    while True:
        # Get user's choice of algorithm
        choice = get_user_choice()
        
        if choice == 'exit':
            print("\n👋 Thank you for using Knight's Tour! Goodbye!\n")
            break
        
        # Get starting position
        starting_pos = get_starting_position()
        
        # Show board with only starting position marked
        start_board = create_empty_board()
        start_board[starting_pos[0]][starting_pos[1]] = 1
        print(f"\nStarting Position: {starting_pos}")
        display_board(start_board)
        
        # Run selected algorithm
        print(f"\n🔄 Running {choice.upper()} algorithm from position {starting_pos}...")
        
        if choice == 'backtracking':
            success, board = KnightsTourBacktracking(starting_pos)
        else:  # lasvegas
            success, board = KnightsTourLasVegas(starting_pos)
        
        # Display results
        if success:
            print("\n✅ SUCCESS! Closed Knight's Tour found!")
        else:
            print("\n❌ FAILED! No closed tour found.")
        
        # Visualize the board
        display_board(board)
        
        # Ask if user wants to continue
        continue_choice = input("Do you want to try again? (y/n): ").strip().lower()
        if continue_choice != 'y':
            print("\n👋 Thank you for using Knight's Tour! Goodbye!\n")
            break


if __name__ == "__main__":
    # Uncomment the line below to run performance tests
    run_performance_test(10000)
    
    # Run the main program
    main()
