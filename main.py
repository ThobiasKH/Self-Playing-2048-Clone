import pygame
import sys
import time
from bestMove import minimax, best_move
from board import Board

def display_message(message, waitTime):
    font = pygame.font.Font(None, int(window_size[0] / 4))
    window.fill((255, 255, 255))  
    
    text = font.render(message, True, (0, 0, 0))  
    text_rect = text.get_rect(center=(window.get_width() // 2, window.get_height() // 2))
    
    window.blit(text, text_rect)
    pygame.display.flip()  

    pygame.time.delay(waitTime)

pygame.init()
pygame.font.init()

window_size = (500, 500)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption('2048')

BGCOLOR = (150, 150, 130)

board = Board()
Board.init_random_board_state(board)

botIsPlaying = True

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and not botIsPlaying:
            if event.key == pygame.K_a:
                board.play_move("left")
            elif event.key == pygame.K_d:
                board.play_move("right")
            elif event.key == pygame.K_w:
                board.play_move("up")
            elif event.key == pygame.K_s:
                board.play_move("down")
                
    if botIsPlaying and board.win_state == 0:
        bestMove = best_move(board, 5)
        board.play_move(bestMove) 

    window.fill(BGCOLOR)

    board.draw(window, window_size[0], window_size[1])
    if (board.win_state == -1 and not botIsPlaying):
        display_message("You Lose", 3000)
        running = False
        
    elif (board.win_state == 1 and not botIsPlaying):
        # listeningForInputs = False
        display_message("You Win", 3000)
        running = False

    pygame.display.flip()

pygame.quit()
sys.exit()
