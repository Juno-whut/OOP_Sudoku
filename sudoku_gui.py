import pygame
from sudoku_solver_gen3 import Board

solver = Board()
grid = solver.get_grid()
solution = solver.solve()

pygame.font.init()
# Constants
BOARD_SIZE = 9
SCREEN_WIDTH = 540
SCREEN_HEIGHT = 600
CELL_SIZE = 60
GRID_THICKNESS = 4
FONT_SIZE = 50
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)


class SudokuGUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Sudoku by Owen")
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.clock = pygame.time.Clock()
        self.board = grid
        self.selected = None
        self.running = True

    def draw_board(self, surface):
        surface.fill(WHITE)
        for i in range(BOARD_SIZE + 1):
            if i % 3 == 0:
                thickness = GRID_THICKNESS * 2
            else:
                thickness = GRID_THICKNESS
            pygame.draw.line(surface, BLACK, (0, i * CELL_SIZE), (SCREEN_WIDTH, i * CELL_SIZE), thickness)
            pygame.draw.line(surface, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, SCREEN_HEIGHT - 60), thickness)
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board[i][j] != 0:
                    value = self.font.render(str(self.board[i][j]), True, BLACK)
                    x_pos = j * CELL_SIZE + (CELL_SIZE - FONT_SIZE) / 2
                    y_pos = i * CELL_SIZE + (CELL_SIZE - FONT_SIZE) / 2
                    surface.blit(value, (x_pos, y_pos))

    def draw_selected_cell(self, surface):
        if self.selected:
            i, j = self.selected
            pygame.draw.rect(surface, GRAY, pygame.Rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def update(self, surface):
        self.draw_board(surface)
        self.draw_selected_cell(surface)
        pygame.display.update()
    
    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x, y = event.pos
                        if y < SCREEN_HEIGHT - 60:
                            row = y // CELL_SIZE
                            col = x // CELL_SIZE
                            self.selected = (row, col)
                if event.type == pygame.KEYDOWN:
                    if self.selected:
                        i, j = self.selected
                        if event.unicode.isdigit():
                            self.board[i][j] = int(event.unicode)
                        elif event.key == pygame.K_BACKSPACE:
                            self.board[i][j] = 0
                        self.selected = None

            self.update(self.screen)
            self.clock.tick(60)

        pygame.quit()
        
        
if __name__ == '__main__':
    gui = SudokuGUI()
    gui.run()
