# Memory-Usage Hell Incoming
from board import Board

# Did not work as well as expected
# def minimax(board, depth, is_maximizing = True):
# if depth == 0 or board.win_state != 0:
# return evaluate_board(board)
#
# if is_maximizing:
# max_eval = float('-inf')
# for direction in ["up", "down", "left", "right"]:
# new_board = play_move(board, direction)
# if new_board:
# eval = minimax(new_board, depth - 1, False)
# max_eval = max(max_eval, eval)
# return max_eval
# else:
# empty_tiles = [(r, c) for r in range(4) for c in range(4) if board.data[r][c] == 0]
# if not empty_tiles:
# return evaluate_board(board)
#
# total_eval = 0
# for row, col in empty_tiles:
# board.data[row][col] = 2
# eval_2 = minimax(board, depth - 1, True)
# total_eval += 0.9 * eval_2
#
# board.data[row][col] = 4
# eval_4 = minimax(board, depth - 1, True)
# total_eval += 0.1 * eval_4
#
# board.data[row][col] = 0
#
# return total_eval / len(empty_tiles)

def best_move(board, depth):
    best_eval = float("-inf")
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
    if eval == float("inf") or eval == float("-inf"):
        return eval

    if depth == 0:
        return eval

    max_eval = float("-inf")

    for direction in ["up", "down", "left", "right"]:
        new_board = play_move(board, direction)
        if new_board:
            eval = minimax(new_board, depth - 1)
            max_eval = max(max_eval, eval)

    return max_eval


squareMultipliers = {
    0: 2,
    1: 2,
    2: 2,
    3: 2,
    4: 1.25,
    5: 1.25,
    6: 1.25,
    7: 1.25,
    8: 1,
    9: 1,
    10: 1,
    11: 1,
    12: 0.8,
    13: 0.8,
    14: 0.8,
    15: 0.8,
}
squareScores = {
    0: 0,
    2: 0,
    4: 4,
    8: 11,
    16: 28,
    32: 65,
    64: 141,
    128: 300,
    256: 627,
    512: 1292,
    1024: 2643,
    2048: 5372,
}


# !BADBADBAD
def evaluate_board(board):
    if board.win_state == 1:
        return float("inf")
    if board.win_state == -1:
        return float("-inf")

    highestTileValue = 0
    numEmptySquares = 0
    adjacencyScore = 0
    smoothness = 0
    monotonicity = 0
    sum = 0
    littleSum = 0

    WEIGHT_EMPTY = 1000
    WEIGHT_MERGING = 200
    WEIGHT_SMOOTHNESS = 0.1
    WEIGHT_MONOTONICITY = 50
    WEIGHT_MAX_TILE = 0.5
    WEIGHT_SUM = 0.4

    for row in range(4):
        for col in range(4):
            currentTile = board.data[row][col]
            currentTileValue = (
                squareScores[currentTile] * squareMultipliers[row * 4 + col]
            )

            if currentTile == 0:
                numEmptySquares += 1
            else:
                littleSum += currentTile
                sum += currentTileValue
                highestTileValue = max(highestTileValue, currentTile)

                if row < 3:
                    downTileValue = board.data[row + 1][col]
                    if downTileValue != 0:
                        smoothness += abs(currentTile - downTileValue) / min(
                            currentTile, downTileValue
                        )

                if col < 3:
                    rightTileValue = board.data[row][col + 1]
                    if rightTileValue != 0:
                        smoothness += abs(currentTile - rightTileValue) / min(
                            currentTile, rightTileValue
                        )

                if row < 3 and board.data[row + 1][col] == currentTile:
                    adjacencyScore += 1
                if col < 3 and board.data[row][col + 1] == currentTile:
                    adjacencyScore += 1

                if row < 3 and currentTile >= board.data[row + 1][col]:
                    monotonicity += 1
                if col < 3 and currentTile >= board.data[row][col + 1]:
                    monotonicity += 1

    score = (
        numEmptySquares * WEIGHT_EMPTY
        + adjacencyScore * WEIGHT_MERGING
        + monotonicity * WEIGHT_MONOTONICITY
        + highestTileValue * WEIGHT_MAX_TILE
        + sum * WEIGHT_SUM
        - smoothness * WEIGHT_SMOOTHNESS
    ) if littleSum < 2048 else (
        numEmptySquares * (highestTileValue / 1024)
    )


    if board.data[0][0] == highestTileValue:
        score *= 2

    score *= 0.9 if board.lastTileThatWasAdded == 2 else 0.1

    if score < 0:
        print("OVERFLOW!")

    return score


def play_move(board, direction):
    new_board = Board()
    new_board.data = [row[:] for row in board.data]

    new_board.play_move(direction)

    return new_board if new_board.data != board.data else None
