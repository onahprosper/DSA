"""
Knight's Tour Problem - Simplified Version
Backtracking algorithm with Warnsdorff's heuristic

Author: Student
Date: November 7, 2025
"""

from typing import List, Tuple

# Board size (8x8 chessboard)
BOARD_SIZE = 8

# Knight's 8 possible moves
KNIGHT_MOVES = [
    (2, 1), (1, 2), (-1, 2), (-2, 1),
    (-2, -1), (-1, -2), (1, -2), (2, -1)
]


def is_valid(row: int, col: int, board: List[List[int]]) -> bool:
    """Check if position is valid and unvisited."""
    return (0 <= row < BOARD_SIZE and
            0 <= col < BOARD_SIZE and
            board[row][col] == 0)


def count_moves(row: int, col: int, board: List[List[int]]) -> int:
    """Count valid moves from a position (for Warnsdorff's heuristic)."""
    count = 0
    for dr, dc in KNIGHT_MOVES:
        if is_valid(row + dr, col + dc, board):
            count += 1
    return count


def can_return_to_start(current_pos: Tuple[int, int], start_pos: Tuple[int, int]) -> bool:
    """Check if knight can return to starting position."""
    curr_row, curr_col = current_pos
    start_row, start_col = start_pos

    for dr, dc in KNIGHT_MOVES:
        if curr_row + dr == start_row and curr_col + dc == start_col:
            return True
    return False


def knights_tour(start_row: int, start_col: int) -> Tuple[bool, List[List[int]]]:
    """
    Solve Knight's Tour using Backtracking with Warnsdorff's heuristic.

    Args:
        start_row: Starting row (0-7)
        start_col: Starting column (0-7)

    Returns:
        (success, board): success is True if closed tour found, board shows move sequence
    """
    # Create empty board
    board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]

    # Validate starting position
    if not (0 <= start_row < BOARD_SIZE and 0 <= start_col < BOARD_SIZE):
        return False, board

    def backtrack(row: int, col: int, move_num: int) -> bool:
        """Recursive backtracking function."""
        # Mark current position
        board[row][col] = move_num

        # Check if tour is complete
        if move_num == BOARD_SIZE * BOARD_SIZE:
            # Check if it's a closed tour (can return to start)
            if can_return_to_start((row, col), (start_row, start_col)):
                return True
            else:
                board[row][col] = 0  # Not closed, backtrack
                return False

        # Get all valid moves
        valid_moves = []
        for dr, dc in KNIGHT_MOVES:
            new_row, new_col = row + dr, col + dc
            if is_valid(new_row, new_col, board):
                valid_moves.append((new_row, new_col))

        # Apply Warnsdorff's heuristic: sort by fewest onward moves
        valid_moves.sort(key=lambda pos: count_moves(pos[0], pos[1], board))

        # Try each valid move
        for next_row, next_col in valid_moves:
            if backtrack(next_row, next_col, move_num + 1):
                return True

        # Backtrack: undo current move
        board[row][col] = 0
        return False

    # Start backtracking
    success = backtrack(start_row, start_col, 1)
    return success, board


def display_board(board: List[List[int]]) -> None:
    """Display the board in formatted table."""
    print("\n" + "=" * 50)
    print("Knight's Tour Board")
    print("=" * 50)

    # Column headers
    print("    ", end="")
    for col in range(BOARD_SIZE):
        print(f"{col:3d} ", end="")
    print("\n    " + "-" * (BOARD_SIZE * 4 + 1))

    # Rows with data
    for row in range(BOARD_SIZE):
        print(f"{row} | ", end="")
        for col in range(BOARD_SIZE):
            print(f"{board[row][col]:3d} ", end="")
        print("|")

    print("    " + "-" * (BOARD_SIZE * 4 + 1))
    print("=" * 50 + "\n")


def main():
    """Main function."""
    print("=" * 50)
    print("Knight's Tour - Backtracking Algorithm")
    print("=" * 50)

    # Display empty board
    empty_board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
    print("\nEmpty Chessboard:")
    display_board(empty_board)

    while True:
        # Get starting position
        try:
            print(f"Enter starting position (0-{BOARD_SIZE-1} for both):")
            row = int(input(f"  Row (0-{BOARD_SIZE-1}): ").strip())
            col = int(input(f"  Column (0-{BOARD_SIZE-1}): ").strip())

            if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE):
                print(f"❌ Position must be between 0 and {BOARD_SIZE-1}!\n")
                continue
        except ValueError:
            print("❌ Please enter valid integers!\n")
            continue

        # Run algorithm
        print(f"\n🔄 Running algorithm from position ({row}, {col})...\n")
        success, board = knights_tour(row, col)

        # Display results
        if success:
            print("✅ SUCCESS! Closed Knight's Tour found!")
        else:
            print("❌ FAILED! No closed tour found.")

        display_board(board)

        # Ask to continue
        choice = input("Try again? (y/n): ").strip().lower()
        if choice != 'y':
            print("\n👋 Goodbye!\n")
            break


if __name__ == "__main__":
    main()
