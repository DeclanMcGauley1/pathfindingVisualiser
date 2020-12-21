import pygame
import random
import math
import time

#create the window
WIDTH = 800
WINDOW = pygame.display.set_mode((WIDTH, WIDTH))
ROWS = 50
GAP = WIDTH // ROWS
pygame.display.set_caption("Pathfinding visualiser")

class Node:

    def __init__(self, row, col, width, totalRows):
        self.row = row
        self.col = col
        self.width = width
        self.totalRows = totalRows
        self.neighbors = []
        self.x = row * width
        self.y = col * width
        self.visited = False
        self.barrior = False
        self.start = False
        self.end = False
        self.colour = (255,255,255)

    def getPosition(self):
        return self.row, self.col

    def isVisited(self):
        return self.visited

    def isBarrior(self):
        return self.barrior

    def isStart(self):
        return self.start

    def isEnd(self):
        return self.end

    def setBarrior(self):
        self.barrior = bool
        self.colour = (0,0,0)

    def setVisited(self):
        self.visited = True
        self.colour = (255,0,0)

    def setStart(self):
        self.start = True
        self.colour = (0,0,200)

    def setEnd(self):
        self.end = True
        self.colour = (0,150,150)

    def clearBarrior(self):
        self.barrior = False
        self.colour = (255,255,255)

    def draw(self, window):
        pygame.draw.rect(window, self.colour, (self.x, self.y, self.width, self.width))

def eucDistance(pointA, pointB):
    x1, y1 = pointA
    x2, y2 = pointB

    xDist = abs(x2 - x1)
    yDist = abs(y2 - y1)

    eucDist = math.sqrt((xDist ** 2) + (yDist ** 2))
    print(eucDist)

def makeGrid(rows, width):
    grid = []
    for row in range(rows):
        grid.append([])
        for col in range(rows):
            node = Node(row, col, GAP, rows)
            grid[row].append(node)

    return grid

def drawGrid(window, width, rows):
    for row in range(rows):
        pygame.draw.line(window, (220,220,220), (0, row * GAP), (width, row * GAP))
        for col in range(rows):
            pygame.draw.line(window, (220, 220, 220), (col * GAP, 0), (col*GAP, width))


def draw(window, grid, rows, width):
    window.fill((0,0,0))
    for row in grid:
        for node in row:
            node.draw(window)

    drawGrid(window, width, rows)
    pygame.display.update()

def main():
    run = True
    startSet = False
    endSet = False
    grid = makeGrid(50, WIDTH)
    while run:
        draw(WINDOW, grid, 50, WIDTH)

        for event in pygame.event.get():
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                x, y = pos
                xRow = x // GAP
                yRow = y // GAP
                grid[xRow][yRow].setBarrior()

            if pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                x, y = pos
                xRow = x // GAP
                yRow = y // GAP
                grid[xRow][yRow].clearBarrior()

            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_s]:
            if startSet == False:
                pos = pygame.mouse.get_pos()
                x, y = pos
                xRow = x // GAP
                yRow = y // GAP
                if grid[xRow][yRow].isEnd() == False:
                    grid[xRow][yRow].setStart()
                    startSet = True

        if keys[pygame.K_e]:
            if endSet == False:
                pos = pygame.mouse.get_pos()
                x, y = pos
                xRow = x // GAP
                yRow = y // GAP
                if grid[xRow][yRow].isStart() == False:
                    grid[xRow][yRow].setEnd()
                    endSet = True
main()
