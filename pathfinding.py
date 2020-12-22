import pygame
import time
import math
pygame.init()

WIDTH = 1000
ROWS = 50
GAP = WIDTH // ROWS
WINDOW = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("pathfinding")

WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0, 0, 210)
RED = (255, 0, 0)
YELLOW = (255,255,0)
GREEN = (0, 255, 0)
PURPLE = (255,0,255)


class Node:
    def __init__(self, colour, row, col):
        self.colour = colour
        self.row = row
        self.col = col
        self.isStart = False
        self.f = math.inf
        self.g = math.inf
        self.h = math.inf
        self.parent = None
        self.children = []
        self.x = row * GAP
        self.y = col * GAP

    def setColour(self, colour):
        self.colour = colour

    def draw(self, window):
        pygame.draw.rect(window, self.colour, (self.x, self.y, GAP, GAP))

    def getChildren(self, grid):
        row = self.row
        col = self.col
        if row > 0:
            up = grid[row - 1][col]
            if not up.colour == BLACK:
                self.children.append(up)
        if row < ROWS - 1:
            down = grid[row + 1][col]
            if not down.colour == BLACK:
                self.children.append(down)
        if col > 0:
            left = grid[row][col - 1]
            if not left.colour == BLACK:
                self.children.append(left)
        if col < ROWS - 1:
            right = grid[row][col + 1]
            if not right.colour == BLACK:
                self.children.append(right)


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

def eucDistance(pointA, pointB):
    x1, y1 = pointA
    x2, y2 = pointB
    eucDist = math.sqrt((abs(x2 - x1) **2) + (abs(y2 - y1) **2))
    return eucDist

def aStar(grid, start, end):
    #positions of the start and the end nodes of the search
    startPos = (start.row, start.col)
    endPos = (end.row, end.col)
    openSet = list()
    closedSet = list()
    cameFrom = dict()
    openSet.append(start)
    start.f = eucDistance(startPos, endPos)
    start.g = 0

    while len(openSet) > 0:
        pygame.event.get()
        current = openSet[0]
        for node in openSet:
            if node.f < current.f:
                current = node

        if current == end:
            print("success")
            shortestPath = getPath(cameFrom, current, grid)
            break


        openSet.remove(current)
        closedSet.append(current)
        current.getChildren(grid)

        for child in current.children:
            tempG = current.g + 1
            childPos = (child.row, child.col)
            if tempG < child.g:
                cameFrom[child] = current
                child.g = tempG
                child.h = eucDistance(childPos, endPos)
                child.f = child.g + child.h
                if child not in openSet:
                    openSet.append(child)

        for node in openSet:
            node.colour = YELLOW
        for node in closedSet:
            node.colour = GREEN

        draw(grid)

def dijkstras(grid, start, end):
    openSet = list()
    cameFrom = dict()
    start.g = 0
    openSet.append(start)

    while len(openSet) > 0:
        pygame.event.get()
        current = openSet[0]
        current.colour = YELLOW
        for node in openSet:
            if node.g < current.g:
                current = node

        if current == end:
            print("success")
            getPath(cameFrom, current, grid)
            break

        openSet.remove(current)
        current.getChildren(grid)

        for child in current.children:
            alt = current.g + 1
            if alt < child.g:
                child.g = alt
                cameFrom[child] = current
                if child not in openSet:
                    openSet.append(child)


        draw(grid)

def getPath(cameFrom, current, grid):
    while current in cameFrom:
        current = cameFrom[current]
        if not current.isStart:
            current.colour = PURPLE
        draw(grid)
    time.sleep(3)

def main():
    grid = Grid()
    run = True
    startSet = False
    endSet = False
    start = None
    end = None
    started = False
    while run:
        draw(grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = getIndex(pos)
                if not (grid[row][col].colour == RED) and not (grid[row][col].colour == BLUE):
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
                startPos = (row, col)
                grid[row][col].setColour(BLUE)
                startSet = True
                start = grid[row][col]
                start.isStart = True

        if keys[pygame.K_e]:
            if not endSet:
                pos = pygame.mouse.get_pos()
                row, col = getIndex(pos)
                endPos = (row, col)
                grid[row][col].setColour(RED)
                endSet = True
                end = grid[row][col]

        if keys[pygame.K_a] and startSet == True and endSet == True:
            started = True
            aStar(grid, start, end)
            run = False
        elif keys[pygame.K_d] and startSet == True and endSet == True:
            started = True
            dijkstras(grid, start, end)
            run = False

    pygame.quit()

main()
