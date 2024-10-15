# Memory-Usage Hell Incoming
from board import Board
import sys

def best_move(board, depth):
    best_eval = float('-inf')
    best_direction = None

    for direction in ["up", "down", "left", "right"]:
        new_board = play_move(board, direction) 
        if new_board:
            eval = minimax(new_board, depth)
            if eval > best_eval:
                best_eval = eval
                best_direction = direction

    return best_direction


# Not really a minimax algorithm since theres only one player
def minimax(board, depth):
    eval = evaluate_board(board)
    
    if depth == 0 or not board.can_move():
        return evaluate_board(board)  
    
    max_eval = float('-inf')
    for direction in ["up", "down", "left", "right"]:
        new_board = play_move(board, direction)  
        if new_board:
            eval = minimax(new_board, depth - 1)
            max_eval = max(max_eval, eval)
    return max_eval

def evaluate_board(board):
    if board.win_state == 1:
        return float('inf')
    if board.win_state == -1:
        return float('-inf')
    
    highestTileValue = 0
    boardValue = 0
    numEmptySquares = 16
    adjacencyScore = 0
    
    for row in range(4):
        for col in range(4):
            currentTileValue = board.data[row][col]
            if currentTileValue != 0:
                numEmptySquares -= 1
                boardValue += currentTileValue
                
                if row < 3 and board.data[row + 1][col] == currentTileValue:
                    adjacencyScore += 1
                if col < 3 and board.data[row][col + 1]:
                    adjacencyScore += 1 
                
                if currentTileValue > highestTileValue:
                    highestTileValue = currentTileValue
                
    return (highestTileValue / 2 + adjacencyScore) * pow(numEmptySquares, 2.5)    

def play_move(board, direction):
    new_board = Board()  
    new_board.data = [row[:] for row in board.data]  
    
    new_board.play_move(direction)  
    
    return new_board if new_board.data != board.data else None  
