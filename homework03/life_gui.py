import pygame
from pygame.locals import *

from life import GameOfLife
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed
        self.width = self.life.cols * cell_size
        self.height = self.life.rows * cell_size
        self.screen_size = self.width, self.height
        self.screen = pygame.display.set_mode(self.screen_size)

    def draw_lines(self) -> None:
        # Copy from previous assignment
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        # Copy from previous assignment
        for i in range(self.life.rows):
            for j in range(self.life.cols):
                if not self.life.curr_generation[i][j]:
                    color = pygame.Color("white")
                else:
                    color = pygame.Color("green")
                tmp = self.cell_size - 1
                pygame.draw.rect(
                    self.screen, color, (j * self.cell_size + 1, i * self.cell_size + 1, tmp, tmp)
                )

    def run(self) -> None:
        # Copy from previous assignment
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    pause = not pause
                if event.type == pygame.MOUSEBUTTONDOWN and pause:
                    position = pygame.mouse.get_pos()
                    x = position[0] // self.cell_size
                    y = position[1] // self.cell_size
                    self.life.curr_generation[x][y] = abs(self.life.curr_generation[x][y] - 1)

            self.screen.fill(pygame.Color("white"))
            self.draw_lines()
            self.draw_grid()

            if pause:
                pass
            else:
                if self.life.is_max_generations_exceeded:
                    pygame.display.set_caption("Game of Life | Generations limit exceed")
                else:
                    self.life.step()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()
