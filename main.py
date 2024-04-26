import pygame
import copy
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

    def render(self, screen, play=False):
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

    # TODO: Add brush size.
    def on_click(self, cell, drawing=False, erase=False):
        if drawing:
            self.board[cell[1]][cell[0]] = 1
        elif erase:
            self.board[cell[1]][cell[0]] = 0

    def get_click(self, mouse_pos, drawing=False, erase=False):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell, drawing, erase)


def main():
    pygame.init()

    # pygame.mixer.music.load('Electrodynam.mp3')
    # pygame.mixer.music.set_volume(1)
    # pygame.mixer.music.play(-1)
    # pygame.mixer.music.pause()

    clock = pygame.time.Clock()

    info = pygame.display.Info()
    size = info.current_w, info.current_h
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

    pygame.display.set_caption('Pause')

    cell_size = 10
    width, height = size[0] // cell_size, size[1] // cell_size
    board = Board(width, height)
    default = np.zeros(width * height, dtype=np.uint8).reshape(height, width)
    left = 0
    top = 1
    board.set_view(left, top, cell_size)

    running = True
    play = False
    drawing = False
    erase = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if play:
                        play = False
                    else:
                        play = True
                if event.key == pygame.K_r:
                    play = False
                    board.board = copy.deepcopy(default)
                if event.key == pygame.K_q:
                    running = False
                    break

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    drawing = True
                    board.get_click(event.pos, drawing)
                elif event.button == 3:
                    erase = True
                    board.get_click(event.pos, erase=erase)
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False
                elif event.button == 3:
                    erase = False
            if event.type == pygame.MOUSEMOTION:
                if drawing:
                    x, y = event.pos
                    if 0 <= x <= size[0] - 1 and 0 <= y <= size[1] - 1:
                        board.get_click(event.pos, drawing)
                elif erase:
                    x, y = event.pos
                    if 0 <= x <= size[0] - 1 and 0 <= y <= size[1] - 1:
                        board.get_click(event.pos, erase=erase)
        if play:
            pygame.display.set_caption('Play')
            # pygame.mixer.music.unpause()
            fps = 10
        else:
            pygame.display.set_caption('Pause')
            # pygame.mixer.music.pause()
            fps = 240
        clock.tick(fps)

        screen.fill((0, 0, 0))
        board.render(screen, play)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
