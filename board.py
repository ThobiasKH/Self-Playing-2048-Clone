import random
import pygame

tileColorLookup = {
    2    : (238, 228, 218),  
    4    : (237, 224, 200),  
    8    : (242, 177, 121),  
    16   : (245, 149, 99),   
    32   : (246, 124, 95),  
    64   : (246, 94, 59),   
    128  : (237, 207, 114), 
    256  : (237, 204, 97),  
    512  : (237, 200, 80),  
    1024 : (237, 197, 63),  
    2048 : (255, 215, 0)    
}


class Board:
    def __init__(self):
        self.data = [[0, 0, 0, 0] for _ in range(4)]
        self.win_state = 0

    def clear(self):
        self.win_state = 0
        self.data = [[0, 0, 0, 0] for _ in range(4)]

    def init_random_board_state(self):
        self.clear()
        self.__add_random_tile()
        self.__add_random_tile()

    def __add_random_tile(self):
        empty_positions = [(r, c) for r in range(len(self.data)) for c in range(len(self.data[r])) if self.data[r][c] == 0]
        if empty_positions:
            r, c = random.choice(empty_positions)
            self.data[r][c] = 4 if random.random() < 0.1 else 2 

    def can_move(self):
        for row in range(4):
            for col in range(4):
                if self.data[row][col] == 0:
                    return True  
                if col < 3 and self.data[row][col] == self.data[row][col + 1]:
                    return True  
                if row < 3 and self.data[row][col] == self.data[row + 1][col]:
                    return True  
        return False

    def play_move(self, direction):
        new_board = self.__move_tiles(direction)
        if new_board is None:
            return self.data 

        if any(2048 in row for row in new_board):
            self.win_state = 1 

        if not self.can_move():
            self.win_state = -1 

        new_board = self.__add_random_tile_to_board(new_board)
        self.data = new_board
        return self.data

    def __move_tiles(self, direction):
        moved = False
        if direction == "up":
            for col in range(4):
                new_col = self.__merge([self.data[row][col] for row in range(4)])
                for row in range(4):
                    if new_col[row] != self.data[row][col]:
                        moved = True
                    self.data[row][col] = new_col[row]
        elif direction == "down":
            for col in range(4):
                new_col = self.__merge([self.data[row][col] for row in range(3, -1, -1)])
                for row in range(4):
                    if new_col[row] != self.data[3 - row][col]:
                        moved = True
                    self.data[3 - row][col] = new_col[row]
        elif direction == "left":
            for row in range(4):
                new_row = self.__merge(self.data[row])
                for col in range(4):
                    if new_row[col] != self.data[row][col]:
                        moved = True
                    self.data[row][col] = new_row[col]
        elif direction == "right":
            for row in range(4):
                new_row = self.__merge(self.data[row][::-1])
                for col in range(4):
                    if new_row[col] != self.data[row][3 - col]:
                        moved = True
                    self.data[row][3 - col] = new_row[col]
        return self.data if moved else None

    def __merge(self, line):
        non_zero = [tile for tile in line if tile != 0]
        merged = []
        skip = False
        for i in range(len(non_zero)):
            if skip:
                skip = False
                continue
            if i + 1 < len(non_zero) and non_zero[i] == non_zero[i + 1]:
                merged.append(non_zero[i] * 2)
                skip = True
            else:
                merged.append(non_zero[i])
        return merged + [0] * (4 - len(merged))

    def __add_random_tile_to_board(self, board):
        empty_positions = [(r, c) for r in range(4) for c in range(4) if board[r][c] == 0]
        if empty_positions:
            r, c = random.choice(empty_positions)
            board[r][c] = 4 if random.random() < 0.1 else 2 
        return board

    def draw(self, window, window_width, window_height):
        cell_size_x = window_width / 4
        cell_size_y = window_height / 4
        font = pygame.font.Font(None, int(cell_size_x / 2))
        
        for row in range(4):
            for col in range(4):
                x_coord = cell_size_x * col + cell_size_x / 2
                y_coord = cell_size_y * row + cell_size_y / 2
                
                num = self.data[row][col]
                if num == 0:
                    continue
                
                pygame.draw.rect(
                    window,
                    tileColorLookup[num],
                    (x_coord - cell_size_x / 2,
                     y_coord - cell_size_y / 2,
                     cell_size_x,
                     cell_size_y)
                )
                
                text_surface = font.render(str(num), True, (0, 0, 0))
                text_rect = text_surface.get_rect(center=(x_coord, y_coord))
                window.blit(text_surface, text_rect)
        
        self.__draw_lines(window, window_width, window_height)

    def __draw_lines(self, window, window_width, window_height):
        for row in range(4):
            y = (window_height / 4) * row
            pygame.draw.line(window, (0, 0, 0), (0, y), (window_width, y))
        
        for col in range(4):
            x = (window_width / 4) * col
            pygame.draw.line(window, (0, 0, 0), (x, 0), (x, window_height))
