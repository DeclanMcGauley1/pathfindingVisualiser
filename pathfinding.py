import pygame
import time
import math

WIDTH = 800
ROWS = 50
GAP = WIDTH // ROWS
WINDOW = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("pathfinding")

WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0, 0, 210)
RED = (255, 0, 0)


class Node:
    def __init__(self, colour, row, col):
        self.colour = colour
        self.row = row
        self.col = col
        self.x = row * GAP
        self.y = col * GAP

    def setColour(self, colour):
        self.colour = colour

    def draw(self, window):
        pygame.draw.rect(window, self.colour, (self.x, self.y, GAP, GAP))

def Grid():
    grid = list()
    for row in range(ROWS):
        grid.append([])
        for col in range(ROWS):
            node = Node(WHITE, row, col)
            grid[row].append(node)
    return grid

def drawGrid():
    for row in range(ROWS):
        pygame.draw.line(WINDOW, (100, 100, 100), (0, row * GAP), (WIDTH, row*GAP))
        for col in range(ROWS):
            pygame.draw.line(WINDOW, (100,100,100), (col * GAP, 0), (col*GAP, WIDTH))

def draw(grid):
    WINDOW.fill((0,0,0))
    for row in grid:
        for node in row:
            node.draw(WINDOW)

    drawGrid()
    pygame.display.update()

def getIndex(pos):
    x, y = pos
    row = x // GAP
    col = y // GAP
    return (row, col)

def main():
    grid = Grid()
    run = True
    startSet = False
    endSet = False

    while run:
        draw(grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = getIndex(pos)
                grid[row][col].setColour(BLACK)
            if pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = getIndex(pos)
                if grid[row][col].colour == RED:
                    endSet = False
                elif grid[row][col].colour == BLUE:
                    startSet = False
                grid[row][col].setColour(WHITE)


            keys = pygame.key.get_pressed()
            if keys[pygame.K_s]:
                if not startSet:
                    pos = pygame.mouse.get_pos()
                    row, col = getIndex(pos)
                    grid[row][col].setColour(BLUE)
                    startSet = True
            if keys[pygame.K_e]:
                if not endSet:
                    pos = pygame.mouse.get_pos()
                    row, col = getIndex(pos)
                    grid[row][col].setColour(RED)
                    endSet = True

main()
