import curses
from time import sleep

from life import GameOfLife
from ui import UI

screen = curses.initscr()


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        # Добавляем +2 из-за рамки
        width = self.life.cols + 2
        height = self.life.rows + 2
        for x in range(width):
            if x == 0 or x == (width - 1):
                char = '+'
            else:
                char = "-"
            screen.addstr(0, x, char)
            screen.addstr(height - 1, x, char)

        for y in range(height):
            if y == 0 or y == (height - 1):
                char = '+'
            else:
                char = "|"
            screen.addstr(y, 0, char)
            screen.addstr(y, width - 1, char)

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        for row in range(self.life.rows):
            for col in range(self.life.cols):
                x = col + 1
                y = row + 1
                if self.life.curr_generation[row][col] == 1:
                    char = "*"
                else:
                    char = " "
                screen.addstr(y, x, char)

    def run(self) -> None:
        screen = curses.initscr()
        running = True
        while running:
            if not self.life.is_changing:
                running = False
            if self.life.is_max_generations_exceeded:
                running = False
            self.draw_borders(screen)
            self.draw_grid(screen)
            self.life.step()
            sleep(0.2)
            screen.refresh()
        curses.endwin()


if __name__ == '__main__':
    c = Console(GameOfLife((30, 50)))
    c.run()
