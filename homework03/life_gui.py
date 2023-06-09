import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        super().__init__(life)
        self.cell_size = cell_size
        self.height = cell_size * life.rows
        self.width = cell_size * life.cols
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.speed = speed

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))

    def draw_grid(self) -> None:
        for row in range(self.life.rows):
            for col in range(self.life.cols):
                if self.life.curr_generation[row][col] == 1:
                    color = pygame.Color('green')
                else:
                    color = pygame.Color('white')
                x = col * self.cell_size
                y = row * self.cell_size
                rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, color, rect)

    def pause_mode(self) -> bool:
        while True:
            for event in pygame.event.get():
                # Обработка выхода
                if event.type == QUIT:
                    return False
                # Обработка ввода с клавиатуры
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        return True
                    # выход при помощи кнопки "o" во время паузы
                    if event.key == pygame.K_o:
                        return False

                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    row = pos[1] // self.cell_size
                    col = pos[0] // self.cell_size
                    self.life.toggle_grid_element(row, col)
                    self.draw_grid()
                    self.draw_lines()
                    pygame.display.flip()

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        running = True
        while running:
            this_iter_pause = False
            for event in pygame.event.get():
                # Обработка выхода
                if event.type == QUIT:
                    running = False
                # Обработка ввода с клавиатуры
                if event.type == pygame.KEYDOWN:
                    # английская "p" = пауза
                    if event.key == pygame.K_p:
                        running = self.pause_mode()
                        # Переменная, отвечающая за то, что в данный итерации была поставлена пауза
                        this_iter_pause = True

            if not self.life.is_changing and not this_iter_pause:
                running = False
            if self.life.is_max_generations_exceeded:
                running = False

            self.life.step()
            self.draw_grid()
            self.draw_lines()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

if __name__ == '__main__':
    g = GUI(GameOfLife((20, 20)), 20, 10)
    g.run()
