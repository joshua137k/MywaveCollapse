import pygame
import sys
import os
import re
import random
import asyncio
from Tile import Tile
from cell import Cell

BLACK = (0, 0, 0)

pygame.init()
DIM = 50
scale = 0.8
CELL_SIZE = 16 * scale
width = DIM * CELL_SIZE
height = DIM * CELL_SIZE
WINDOW_SIZE = (width, height)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("WaveCollapseTeste")

grid = [[None for _ in range(DIM)] for _ in range(DIM)]
tiles = []
tilesImages = []

block_weights = {}


def startOver(grid, tiles):
    for x in range(DIM):
        for y in range(DIM):
            grid[x][y] = Cell(len(tiles))
    return grid


def checkValid(arr, valid):
    return [item for item in arr if (item in valid)]


def ordenacao_natural(arquivo):
    return [int(texto) if texto.isdigit() else texto.lower() for texto in re.split(r'(\d+)', arquivo)]


def preload():
    diretorio = "mapTile/"

    f = open(diretorio + "tileMap.txt", "r")
    ignore = []
    for i, v in enumerate(f):
        v = v.split("|")
        m = eval(v[1].strip())
        block_weights[i] = float(v[2])
        tilesImages.append(pygame.transform.scale(
            pygame.image.load(diretorio + v[0]), (CELL_SIZE, CELL_SIZE)))
        tiles.append(Tile(tilesImages[i], m))
        if v[0] in ["0_dirt.png", "17_sand.png", "9_grass.png", "24_stone.png", "33_water.png"]:
            ignore.append(v[0])
    f.close()
    index = len(tiles)
    # ROTATE
    for i in range(index):
        if not (i in ignore):

            for j in range(1, 4):
                tiles.append(tiles[i].rotate(j))
                if "GG" in tiles[-1].edges:
                    block_weights[len(tiles) - 1] = 0.5
                else:
                    block_weights[len(tiles) - 1] = 0.1

    #print(block_weights)


def draw_matrix(grid):
    for x in range(DIM):
        for y in range(DIM):
            cell = grid[x][y]
            if cell.collapsed:
                tile_index = cell.options[0]
                tile = tiles[tile_index]
                screen.blit(tile.img, (x * CELL_SIZE, y * CELL_SIZE))
            else:
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, BLACK, rect)


async def update_matrix_part(grid, start_x, end_x, start_y, end_y):
    gridCopy = [grid[x][y] for x in range(start_x, end_x) for y in range(start_y, end_y) if grid[x][y] and not grid[x][y].collapsed]
    if len(gridCopy) == 0:
        return

    gridCopy = sorted(gridCopy, key=lambda x: len(x.options))

    lenG = len(gridCopy[0].options)
    stopIndex = 0
    for i in range(len(gridCopy)):
        if len(gridCopy[i].options) > lenG:
            stopIndex = i
            break
    if stopIndex > 0:
        del gridCopy[stopIndex:]

    cell = random.choice(gridCopy)
    cell.collapsed = True
    #print("options:" + str(cell.options))
    weights = [block_weights.get(opt, 0.05) for opt in cell.options]
    #print("WEIGHTS:" + str(weights))
    pick = random.choices(cell.options, weights=weights, k=1)[0]
    #print("pick:" + str(pick))
    cell.options = [pick]

    for x in range(start_x, end_x):
        for y in range(start_y, end_y):
            if grid[x][y].collapsed:
                continue
            options = list(range(len(tiles)))
            # Look up
            if y > 0:
                up = grid[x][y - 1]
                validOptions = []
                for option in up.options:
                    valid = tiles[option].down
                    validOptions = list(set(validOptions + valid))
                options = checkValid(options, validOptions)
            # Look right
            if x < DIM - 1:
                right = grid[x + 1][y]
                validOptions = []
                for option in right.options:
                    valid = tiles[option].left
                    validOptions = list(set(validOptions + valid))
                options = checkValid(options, validOptions)
            # Look down
            if y < DIM - 1:
                down = grid[x][y + 1]
                validOptions = []
                for option in down.options:
                    valid = tiles[option].up
                    validOptions = list(set(validOptions + valid))
                options = checkValid(options, validOptions)
            # Look left
            if x > 0:
                left = grid[x - 1][y]
                validOptions = []
                for option in left.options:
                    valid = tiles[option].right
                    validOptions = list(set(validOptions + valid))
                options = checkValid(options, validOptions)

            grid[x][y] = Cell(len(tiles), options)


async def async_main():
    preload()
    startOver(grid, tiles)
    for tile in tiles:
        tile.analyze(tiles)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mX, mY = pygame.mouse.get_pos()
                    mX = int(mX // CELL_SIZE)
                    mY = int(mY // CELL_SIZE)

                    #print(mX, mY)
                    md = 2
                    for x in range(-md+1, md):
                        for y in range(-md+1, md):
                            cX = mX + x
                            cY = mY + y
                            if 0 <= cX < DIM and 0 <= cY < DIM:
                                grid[cX][cY].options = [0]
                                grid[cX][cY].collapsed = True

        screen.fill((255, 255, 255))
        draw_matrix(grid)
        pygame.display.flip()

        # Chama cada corrotina para atualizar diferentes partes da matriz
        await asyncio.gather(
            update_matrix_part(grid, 0, 12, 0, 12),
            update_matrix_part(grid, 0, 12, 12, 24),
            update_matrix_part(grid, 0, 12, 24, 36),
            update_matrix_part(grid, 0, 12, 36, 48),
            update_matrix_part(grid, 12, 24, 0, 12),
            update_matrix_part(grid, 12, 24, 12, 24),
            update_matrix_part(grid, 12, 24, 24, 36),
            update_matrix_part(grid, 12, 24, 36, 48),
            update_matrix_part(grid, 24, 36, 0, 12),
            update_matrix_part(grid, 24, 36, 12, 24),
            update_matrix_part(grid, 24, 36, 24, 36),
            update_matrix_part(grid, 24, 36, 36, 48),
            update_matrix_part(grid, 36, 48, 0, 12),
            update_matrix_part(grid, 36, 48, 12, 24),
            update_matrix_part(grid, 36, 48, 24, 36),
            update_matrix_part(grid, 36, 48, 36, 48)
        )

if __name__ == "__main__":
    asyncio.run(async_main())