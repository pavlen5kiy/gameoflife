import asyncio
import copy

import numpy as np
import pygame
import time

from ui import Text
from board import Board


async def main():
    pygame.init()

    clock = pygame.time.Clock()

    info = pygame.display.Info()
    # size = info.current_w, info.current_h
    size = 1920, 1080
    screen = pygame.display.set_mode(size, pygame.DOUBLEBUF)

    pygame.display.set_caption('Game of Life')

    cell_size = 20
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

    last_time = time.time()

    brush_size_text = Text(screen, size, 50, pos=(30, 30), center_align=True)

    mouse_wheel_cd = 0

    brush_size = 1

    while running:
        dt = time.time() - last_time
        dt *= 60
        last_time = time.time()

        mouse_wheel_cd += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    play = not play

                if event.key == pygame.K_r:
                    play = False
                    board.board = copy.deepcopy(default)

                if event.key == pygame.K_F1:
                    play = False
                    board.board = np.random.randint(0, 2, (height, width))

            try:
                if event.type == pygame.MOUSEWHEEL:
                    if mouse_wheel_cd >= 5:
                        mouse_wheel_cd = 0
                        if event.y == -1:
                            brush_size += 1
                            if brush_size > 10:
                                brush_size = 10
                        else:
                            brush_size -= 1
                            if brush_size < 1:
                                brush_size = 1

                if event.type == pygame.MOUSEBUTTONDOWN:
                    play = False

                    if event.button == 1:
                        drawing = True
                        board.get_click(event.pos, drawing=drawing, brush_size=brush_size)
                    elif event.button == 3:
                        erase = True
                        board.get_click(event.pos, erase=erase, brush_size=brush_size)

                if event.type == pygame.MOUSEBUTTONUP:
                    play = False

                    if event.button == 1:
                        drawing = False
                    elif event.button == 3:
                        erase = False

                if event.type == pygame.MOUSEMOTION:
                    if drawing:
                        x, y = event.pos
                        if 0 <= x <= size[0] - 1 and 0 <= y <= size[1] - 1:
                            board.get_click(event.pos, drawing=drawing, brush_size=brush_size)
                    elif erase:
                        x, y = event.pos
                        if 0 <= x <= size[0] - 1 and 0 <= y <= size[1] - 1:
                            board.get_click(event.pos, erase=erase, brush_size=brush_size)
            except Exception as e:
                pass

        if play:
            fps = 10
        else:
            fps = 60
        clock.tick(fps)

        screen.fill((0, 0, 0))

        board.update(screen, play)
        brush_size_text.update(brush_size)

        pygame.display.flip()

        await asyncio.sleep(0)

    pygame.quit()


if __name__ == '__main__':
    asyncio.run(main())
