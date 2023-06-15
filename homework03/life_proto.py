import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10
    ) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        # Создание списка клеток
        self.grid = self.create_grid(True)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            # Отрисовка списка клеток
            self.draw_grid()
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.grid = self.get_next_generation()
            # отрисовка линий
            self.draw_lines()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """

        def cell_val():
            return random.randrange(2) if randomize else 0

        return [[cell_val() for col in range(self.cell_width)] for row in range(self.cell_height)]

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for row in range(self.cell_height):
            for col in range(self.cell_width):
                if self.grid[row][col] == 1:
                    color = pygame.Color('green')
                else:
                    color = pygame.Color('white')
                x = col * self.cell_size
                y = row * self.cell_size
                rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, color, rect)

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        row, col = cell
        # Рассчитываем начальные и конечные ячейки
        st_row = row - 1 + int(row == 0)
        st_col = col - 1 + int(col == 0)
        en_row = (row + 1) - int(row == self.cell_height - 1)
        en_col = (col + 1) - int(col == self.cell_width - 1)
        res = []
        # Проходим по всем доступным ячейкам
        for for_row in range(st_row, en_row + 1):
            for for_col in range(st_col, en_col + 1):
                if for_row == row and for_col == col:
                    continue
                res.append(self.grid[for_row][for_col])
        return res

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        new_grid = [[0] * self.cell_width for row in range(self.cell_height)]

        for row in range(self.cell_height):
            for col in range(self.cell_width):
                neighbors = sum(self.get_neighbours((row, col)))
                alive = (self.grid[row][col] == 1)
                if alive:
                    if neighbors in [2, 3]:
                        new_grid[row][col] = 1
                else:
                    if neighbors == 3:
                        new_grid[row][col] = 1

        return new_grid

if __name__ == '__main__':
    g = GameOfLife(cell_size=20)
    g.run()
