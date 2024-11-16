import pygame
import numpy as np


def next_population(population):
    neighbors = sum([
        np.roll(np.roll(population, -1, 1), 1, 0),
        np.roll(np.roll(population, 1, 1), -1, 0),
        np.roll(np.roll(population, 1, 1), 1, 0),
        np.roll(np.roll(population, -1, 1), -1, 0),
        np.roll(population, 1, 1),
        np.roll(population, -1, 1),
        np.roll(population, 1, 0),
        np.roll(population, -1, 0)
    ])
    return (neighbors == 3) | (population & (neighbors == 2))


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = np.zeros(width * height, dtype=np.uint8).reshape(height,
                                                                      width)

        self.left = 10
        self.top = 10
        self.cell_size = 30

    def update(self, screen, play=False):
        colors = [pygame.Color('black'), pygame.Color('white')]

        if play:
            border = pygame.Color('#013220')
            self.board = next_population(self.board)
        else:
            border = pygame.Color('#8b0000')

        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, colors[self.board[y][x]], (
                    x * self.cell_size + self.left,
                    y * self.cell_size + self.top,
                    self.cell_size, self.cell_size))
                pygame.draw.rect(screen, border, (
                    x * self.cell_size + self.left,
                    y * self.cell_size + self.top,
                    self.cell_size, self.cell_size), 1)

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if cell_x < 0 or cell_x >= self.width or \
                cell_y < 0 or cell_y >= self.height:
            return
        return cell_x, cell_y

    def on_click(self, cell, drawing=False, erase=False, brush_size=1):
        if drawing:
            self.board[cell[1]][cell[0]] = 1

            for i in range(brush_size):
                self.board[cell[1] + i][cell[0]] = 1
                self.board[cell[1]][cell[0] + i] = 1
                self.board[cell[1] - i][cell[0]] = 1
                self.board[cell[1]][cell[0] - i] = 1

                self.board[cell[1] + i][cell[0] + 1] = 1
                self.board[cell[1] + 1][cell[0] + i] = 1
                self.board[cell[1] - i][cell[0] - 1] = 1
                self.board[cell[1] - 1][cell[0] - i] = 1

                self.board[cell[1] + i][cell[0] - 1] = 1
                self.board[cell[1] - 1][cell[0] + i] = 1
                self.board[cell[1] - i][cell[0] + 1] = 1
                self.board[cell[1] + 1][cell[0] - i] = 1

                self.board[cell[1] + i][cell[0] + i] = 1
                self.board[cell[1] - i][cell[0] - i] = 1
                self.board[cell[1] + i][cell[0] - i] = 1
                self.board[cell[1] - i][cell[0] + i] = 1


        elif erase:
            self.board[cell[1]][cell[0]] = 0

            for i in range(brush_size):
                self.board[cell[1] + i][cell[0]] = 0
                self.board[cell[1]][cell[0] + i] = 0
                self.board[cell[1] - i][cell[0]] = 0
                self.board[cell[1]][cell[0] - i] = 0

                self.board[cell[1] + i][cell[0] + 1] = 0
                self.board[cell[1] + 1][cell[0] + i] = 0
                self.board[cell[1] - i][cell[0] - 1] = 0
                self.board[cell[1] - 1][cell[0] - i] = 0

                self.board[cell[1] + i][cell[0] - 1] = 0
                self.board[cell[1] - 1][cell[0] + i] = 0
                self.board[cell[1] - i][cell[0] + 1] = 0
                self.board[cell[1] + 1][cell[0] - i] = 0

                self.board[cell[1] + i][cell[0] + i] = 0
                self.board[cell[1] - i][cell[0] - i] = 0
                self.board[cell[1] + i][cell[0] - i] = 0
                self.board[cell[1] - i][cell[0] + i] = 0

    def get_click(self, mouse_pos, drawing=False, erase=False, brush_size=1):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell, drawing, erase, brush_size)
