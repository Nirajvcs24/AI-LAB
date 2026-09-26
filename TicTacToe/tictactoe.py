import random

def showBoard(board):
    print("\n")
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("-----------")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("-----------")
    print(f" {board[6]} | {board[7]} | {board[8]} ")
    print("\n")

def check(board):
    allWinConditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]
    
    for ch in allWinConditions:
        if board[ch[0]] == board[ch[1]] == board[ch[2]] and board[ch[0]] != '.':
            return board[ch[0]]  # Returns 'X' or 'O'
            
    if '.' not in board:
        return "Draw"
        
    return None

def playGame():
    board = ['.', '.', '.', '.', '.', '.', '.', '.', '.']
    currentPlayer = 'X' 
    
    while True:
        showBoard(board)
        
        if currentPlayer == 'X':
            try:
                move = int(input(f"Player {currentPlayer} (You), enter your move (0-8): "))
                if move < 0 or move > 8:
                    print("Invalid range! Please enter a number between 0 and 8.")
                    continue
                if board[move] != '.':
                    print("That spot is already taken! Try another.")
                    continue
            except ValueError:
                print("Invalid input! Please enter an integer between 0 and 8.")
                continue
        else:
            print("Computer 'O' is thinking...")
            available_moves = [i for i, spot in enumerate(board) if spot == '.']
            move = random.choice(available_moves)
            print(f"Computer chose position: {move}")
            
        board[move] = currentPlayer
        
        result = check(board)
        if result:
            showBoard(board)
            if result == "Draw":
                print("It's a Draw!")
            else:
                if result == 'X':
                    print("Congratulations, You Won! 🎉")
                else:
                    print("Computer Won! Better luck next time. 🤖")
            break
            
        # Switch players
        currentPlayer = 'O' if currentPlayer == 'X' else 'X'

if __name__ == "__main__":
    playGame()
