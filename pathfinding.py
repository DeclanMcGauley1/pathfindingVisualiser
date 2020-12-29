import pygame
import time
import math
pygame.init()

#creating the window
WIDTH = 1000
ROWS = 50
GAP = WIDTH // ROWS
WINDOW = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("pathfinding")

#Creating constants for colours
WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0, 0, 210)
RED = (255, 0, 0)
YELLOW = (255,255,0)
GREEN = (0, 255, 0)
PURPLE = (255,0,255)

#Represents a single node on the full graph that our algorithms will traverse
class Node:
    def __init__(self, colour, row, col):
        self.colour = colour
        self.row = row
        self.col = col
        self.isStart = False
        self.isEnd = False
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

    #gets all the nodes that surround the current node, checks for edge cases of the window and barriror blocks
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

#Creates the grid that will hold all of the nodes in the graph
def Grid():
    grid = list()
    for row in range(ROWS):
        grid.append([])
        for col in range(ROWS):
            node = Node(WHITE, row, col)
            grid[row].append(node)
    return grid

#draws a grey line between all the nodes
def drawGrid():
    for row in range(ROWS):
        pygame.draw.line(WINDOW, (100, 100, 100), (0, row * GAP), (WIDTH, row*GAP))
        for col in range(ROWS):
            pygame.draw.line(WINDOW, (100,100,100), (col * GAP, 0), (col*GAP, WIDTH))

#draws all the nodes in the window using the draw method in the node class
def draw(grid):
    WINDOW.fill((0,0,0))
    for row in grid:
        for node in row:
            node.draw(WINDOW)

    drawGrid()
    pygame.display.update()

#gets the index on the grid from a coordinate position
def getIndex(pos):
    x, y = pos
    row = x // GAP
    col = y // GAP
    return (row, col)

#calculates the euclidean distance between two nodes
def eucDistance(pointA, pointB):
    x1, y1 = pointA
    x2, y2 = pointB
    eucDist = math.sqrt((abs(x2 - x1) **2) + (abs(y2 - y1) **2))
    return eucDist

#Implementation of the A* pathFinding algorithm
def aStar(grid, start, end):
    #positions of the start and the end nodes of the search
    startPos = (start.row, start.col)
    endPos = (end.row, end.col)
    openSet = list()
    closedSet = list()
    cameFrom = dict()
    found = False
    openSet.append(start)
    start.f = eucDistance(startPos, endPos)
    start.g = 0

    while len(openSet) > 0:
        pygame.event.get()
        current = openSet[0]
        for node in openSet:
            if node.f < current.f:
                current = node

        #If the current node is the end node, find the shortest path
        if current == end:
            found = True
            print("success")
            shortestPath = getPath(cameFrom, current, grid)
            break


        openSet.remove(current)
        closedSet.append(current)
        current.getChildren(grid)

        #calculates the g, h, and f values for all the children nodes, adds them to the open set
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


        #draws all the nodes in the open and closed set
        for node in openSet:
            if not node.isStart:
                if not node.isEnd:
                    node.colour = YELLOW
        for node in closedSet:
            if not node.isStart:
                if not node.isEnd:
                    node.colour = GREEN

        draw(grid)
    if found == False:
        print("There is no path")

#Implementation of Dijkstras algorithm
def dijkstras(grid, start, end):
    openSet = list()
    closedSet = list()
    cameFrom = dict()
    found = False
    start.g = 0
    openSet.append(start)

    while len(openSet) > 0:
        pygame.event.get()
        current = openSet[0]
        #sets the colour of the current node to green
        if current.isStart == False and current.isEnd == False:
            current.colour = GREEN
        #gets node with the lowest g value in the open set
        for node in openSet:
            if node.g < current.g:
                current = node

        #finds shortest path if end is found
        if current == end:
            found = True
            print("success")
            getPath(cameFrom, current, grid)
            break

        openSet.remove(current)
        current.getChildren(grid)
        closedSet.append(current)

        for child in current.children:
            alt = current.g + 1
            if alt < child.g:
                child.g = alt
                cameFrom[child] = current
                if child not in openSet:
                    openSet.append(child)

        for node in openSet:
            if node.isEnd == False:
                node.colour = YELLOW
        draw(grid)
    if (found == False):
        print("There is no shortest Path")

#finds the shortest path from a dictionary using each node as a key to find their parent
def getPath(cameFrom, current, grid):
    while current in cameFrom:
        current = cameFrom[current]
        #draws the path as it finds each node
        if not current.isStart:
            current.colour = PURPLE
        draw(grid)
    time.sleep(3)

#main loop for the project
def main():
    #creates an instance of grid
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
            #on left mouse button click, make the node at that index become a barrior
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = getIndex(pos)
                if not (grid[row][col].colour == RED) and not (grid[row][col].colour == BLUE):
                    grid[row][col].setColour(BLACK)
            #on right mouse click reset the node back to normal
            if pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = getIndex(pos)
                if grid[row][col].colour == RED:
                    endSet = False
                elif grid[row][col].colour == BLUE:
                    startSet = False
                grid[row][col].setColour(WHITE)


        keys = pygame.key.get_pressed()
        #sets the start node at the index of the current mouse position
        if keys[pygame.K_s]:
            if not startSet:
                pos = pygame.mouse.get_pos()
                row, col = getIndex(pos)
                startPos = (row, col)
                grid[row][col].setColour(BLUE)
                startSet = True
                start = grid[row][col]
                start.isStart = True
                if start == end:
                    endSet = False
        #sets the end node at the index of the current mouse position
        if keys[pygame.K_e]:
            if not endSet:
                pos = pygame.mouse.get_pos()
                row, col = getIndex(pos)
                endPos = (row, col)
                grid[row][col].setColour(RED)
                endSet = True
                end = grid[row][col]
                end.isEnd = True
                if end == start:
                    startSet = False

        #pressing a starts the A* algorithm only if there is a start and an end on the window
        if keys[pygame.K_a] and startSet == True and endSet == True:
            started = True
            aStar(grid, start, end)
            run = False
        #pressing d starts dijkstras algorithm only when there is a start and an end on the window
        elif keys[pygame.K_d] and startSet == True and endSet == True:
            started = True
            dijkstras(grid, start, end)
            run = False
    #closes the application
    pygame.quit()

main()
