import pygame
import sys
import random
from Tile import Tile
from cell import Cell

BLACK = (0,0,0)



pygame.init()
DIM = 20
scale = 0.8
CELL_SIZE = 50 * scale
width = DIM*CELL_SIZE 
height = DIM*CELL_SIZE
WINDOW_SIZE = (width,height)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("WaveCollapeTeste")



grid = []

tiles = []
tilesImages=[]


def checkValid(arr,valid):
    return [item for item in arr if (item in valid)]


def preload():
    
    tilesImages.append(pygame.transform.scale(pygame.image.load("TileTXT/waveCollapse/Teste/blank.png"), (CELL_SIZE, CELL_SIZE)))
    tilesImages.append(pygame.transform.scale(pygame.image.load("TileTXT/waveCollapse/Teste/up.png"), (CELL_SIZE, CELL_SIZE)))
    #tilesImages.append(pygame.transform.scale(pygame.image.load("TileTXT/waveCollapse/Teste/right.png"), (CELL_SIZE, CELL_SIZE)))
    #tilesImages.append(pygame.transform.scale(pygame.image.load("TileTXT/waveCollapse/Teste/down.png"), (CELL_SIZE, CELL_SIZE)))
    #tilesImages.append(pygame.transform.scale(pygame.image.load("TileTXT/waveCollapse/Teste/left.png"), (CELL_SIZE, CELL_SIZE)))


def draw_matrix(grid):

    for row in range(DIM):
        for col in range(DIM):
            cell = grid[col+row*DIM] 
            if cell.collapsed:
                tile_index = cell.options[0]
                tile = tiles[tile_index]
                screen.blit(tile.img, (col * CELL_SIZE, row * CELL_SIZE))
            else:
                rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, BLACK, rect)


def update_matrix(grid):
    
    gridCopy = grid.copy()
    gridCopy = [i for i in gridCopy if i.collapsed==False]
    if len(gridCopy)==0:
        return
    gridCopy = sorted(gridCopy, key=lambda x: len(x.options) )
    
    lenG = len(gridCopy[0].options)
    stopIndex = 0
    for i in range(len(gridCopy)):
        if (len(gridCopy[i].options)>lenG):
            stopIndex=i
            break
    if stopIndex>0:
        del gridCopy[stopIndex:]
    
    cell = random.choice(gridCopy)
    if cell.options!=[]:
            

        cell.collapsed=True
        pick = random.choice(cell.options)
        cell.options = [pick]


    

    nextGrid = [None for i in range(DIM*DIM)]
    for j in range(DIM):
        for i in range(DIM):

            index = i+j*DIM
            #print("index:"+str(index))
            if grid[index].collapsed:
                nextGrid[index] = grid[index] 
            else:
                opitions=[i for i in range(len(tiles))]

                
                #Look up
                if (j>0):
                    up = grid[i + (j -1) * DIM]
                    validOptions=[]
                    for opition in up.options:
                        valid = tiles[opition].down
                        validOptions = list( set(validOptions + valid) )
                    #print("Look up:"+str(validOptions))
                    opitions = checkValid(opitions,validOptions)
                #Look right
                if (i< DIM -1 ):
                    right = grid[(i+1) + j * DIM]
                    validOptions=[]
                    for opition in right.options:
                        valid = tiles[opition].left
                        validOptions =list(set(validOptions+valid))
                    #print("Look right:"+str(validOptions))
                    opitions = checkValid(opitions,validOptions)
                #Look down 
                if (j<DIM - 1):
                    down = grid[i + (j + 1) * DIM]
                    validOptions=[]
                    for opition in down.options:
                        valid = tiles[opition].up
                        validOptions =list(set(validOptions+valid)) 
                    #print("Look down:"+str(validOptions))
                    opitions = checkValid(opitions,validOptions)
                #Look left
                if (i>0):
                    left = grid[(i-1) + j * DIM]
                    validOptions=[]
                    for opition in left.options:
                        valid = tiles[opition].right
                        validOptions =list(set(validOptions+valid))
                    #print("Look left:"+str(validOptions))
                    opitions = checkValid(opitions,validOptions)

                nextGrid[index] = Cell(len(tiles),opitions)

    return nextGrid
    

def newLOOP(grid):
    screen.fill((255, 255, 255)) 
    grid = update_matrix(grid)
    #print(grid[0].options)
    draw_matrix(grid)
    pygame.display.flip()
    return grid


#--------------------------------
#LOAD IMAGES       
preload()


#[UP,RIGHT,DOWN,LEFT]
tiles.append(Tile(tilesImages[0],[0,0,0,0]))
tiles.append(Tile(tilesImages[1],[1,1,0,1]))
#ROTATE
tiles.append(tiles[1].rotate(1))
tiles.append(tiles[1].rotate(2))
tiles.append(tiles[1].rotate(3))

#SETTING GRID
for i in range(DIM*DIM):
    grid.append(Cell(len(tiles)))

# GENERATE THE ADJACENCY RULES BASED ON EDGES
for i in range(len(tiles)):
    tile = tiles[i]
    tile.analyze(tiles)



#TESTE
for i in range(DIM*DIM):
    grid=newLOOP(grid)



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            grid=newLOOP(grid)

