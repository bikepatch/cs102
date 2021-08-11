import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        screen.border(0)

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        for i in range(self.life.rows):
            for j in range(self.life.cols):
                if not self.life.curr_generation[i][j]:
                    screen.addch(i + 1, j + 1, ' ')
                else:
                    screen.addch(i + 1, j + 1, '*')

    def run(self) -> None:
        screen = curses.initscr()
        screen.clear()
        self.draw_borders(screen)
        screen.refresh()
        flag = True
        while flag:
            self.draw_grid(screen)
            screen.refresh()
            self.life.step()
            if self.life.is_max_generations_exceed:
                flag = False
        curses.endwin()
