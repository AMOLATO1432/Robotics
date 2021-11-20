import pygame
import math


WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pathfinder Visualizer Game")


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
ORANGE = (255, 215, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)


SQUARE_WIDTH, SQUARE_HEIGHT = 20, 20


class Node:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.color = GRAY
        self.neighbors = []
        self.distance = COLS * ROWS
        self.past_nodes = []
        self.f, self.g, self.h = 99999999999999, 99999999999999, 99999999999999
        self.prev = None

    def add_neighbors(self):
        if self.x < COLS - 1 and not grid[self.x + 1][self.y].is_wall() and not grid[self.x + 1][self.y].is_closed():
            self.neighbors.append(grid[self.x + 1][self.y])
        if self.x > 0 and not grid[self.x - 1][self.y].is_wall() and not grid[self.x - 1][self.y].is_closed():
            self.neighbors.append(grid[self.x - 1][self.y])
        if self.y < ROWS - 1 and not grid[self.x][self.y + 1].is_wall() and not grid[self.x][self.y + 1].is_closed():
            self.neighbors.append(grid[self.x][self.y + 1])
        if self.y > 0 and not grid[self.x][self.y - 1].is_wall() and not grid[self.x][self.y - 1].is_closed():
            self.neighbors.append(grid[self.x][self.y - 1])

    def getFGH(self, g, end):
        self.g = g
        self.h = math.sqrt((end[0] - self.x) ** 2 + (end[1] - self.y) ** 2)
        self.f = self.g + self.h

    def is_closed(self):
        return self.color == RED

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == BLUE

    def is_wall(self):
        return self.color == BLACK

    def draw(self):
        pygame.draw.rect(WIN, self.color, (self.x * SQUARE_WIDTH, self.y * SQUARE_HEIGHT, SQUARE_WIDTH, SQUARE_HEIGHT))



COLS = 50
ROWS = 50
grid = []


def draw_grid():

    WIN.fill(WHITE)
    for i in grid:
        for node in i:
            node.draw()

    # drawing lines
    for i in range(ROWS):
        pygame.draw.line(WIN, BLACK, (0, i * SQUARE_HEIGHT), (WIDTH, i * SQUARE_HEIGHT))
        for j in range(COLS):
            pygame.draw.line(WIN, BLACK, (i * SQUARE_WIDTH, 0), (i * SQUARE_WIDTH, HEIGHT))



def grid_loc():
    loc = pygame.mouse.get_pos()
    return loc[0] // SQUARE_WIDTH, loc[1] // SQUARE_HEIGHT



def left_mouse(which):
    loc = grid_loc()
    node = grid[loc[0]][loc[1]]
    if which == 'start':
        node.color = ORANGE
        return loc

    elif which == 'end' and not node.is_start():
        node.color = BLUE
        return loc

    elif not node.is_start() and not node.is_end():
        node.color = BLACK

    return None



def right_mouse(start, end):
    loc = grid_loc()
    node = grid[loc[0]][loc[1]]
    if node.is_start():
        start = None

    elif node.is_end():
        end = None

    node.color = GRAY
    return start, end



def grid_draw():
    run = True
    start, end = None, None


    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if pygame.mouse.get_pressed()[0]:
                if not start:
                    start = left_mouse('start')

                elif not end:
                    end = left_mouse('end')

                else:
                    left_mouse('wall')


            if pygame.mouse.get_pressed()[2]:
                remove_return = right_mouse(start, end)
                start = remove_return[0]
                end = remove_return[1]


            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    run = False


        draw_grid()
        pygame.display.update()

    return start, end



def a_star(speed):
    # variables
    if speed:
        FPS = speed
    else:
        FPS = 500
    clock = pygame.time.Clock()
    counter = -1
    grid.clear()
    for i in range(ROWS):
        grid.append([])
        for j in range(COLS):
            grid[i].append(Node(i, j))

    start_end = grid_draw()
    start = start_end[0]
    end = start_end[1]


    if not start or not end:
        return


    run = True
    curr = start
    curr_node = grid[curr[0]][curr[1]]
    curr_node.f, curr_node.g, curr_node.h = 0, 0, 0
    open_list = [curr_node]
    closed_list = []
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


        smallest_node = open_list[0]
        for i in range(len(open_list)):
            if open_list[i].f < smallest_node.f:
                smallest_node = open_list[i]


        closed_list.append(smallest_node)
        open_list.remove(smallest_node)
        curr = (smallest_node.x, smallest_node.y)
        smallest_node.color = RED
        curr_node = smallest_node

        grid[start[0]][start[1]].color = ORANGE
        grid[end[0]][end[1]].color = BLUE
        draw_grid()
        pygame.display.update()
        clock.tick(FPS)


        curr_node.add_neighbors()
        for neighbor in curr_node.neighbors:
            if not neighbor in closed_list:
                if not neighbor in open_list:
                    open_list.append(neighbor)
                    neighbor.color = YELLOW
                    neighbor.getFGH(curr_node.g + 1, end)
                    neighbor.prev = curr_node
                elif neighbor.g > curr_node.g + 1:
                    neighbor.g = curr_node.g + 1
                    neighbor.f = neighbor.g + neighbor.h
                    neighbor.prev = curr_node


        if len(open_list) == 0:
            return counter
        elif grid[end[0]][end[1]] in closed_list:

            for i in range(len(open_list)):
                open_list[i].color = RED


            counter = 1
            start_node = grid[start[0]][start[1]]
            curr_node = grid[end[0]][end[1]]
            while curr_node.prev != start_node:
                curr_node.prev.color = GREEN
                curr_node = curr_node.prev
                draw_grid()
                pygame.display.update()
                clock.tick(FPS)
                counter += 1
            break

    return counter



def dijkstra(speed):

    if speed:
        FPS = speed
    else:
        FPS = 500
    clock = pygame.time.Clock()
    grid.clear()
    for i in range(ROWS):
        grid.append([])
        for j in range(COLS):
            grid[i].append(Node(i, j))


    start_end = grid_draw()
    start = start_end[0]
    end = start_end[1]


    if not start or not end:
        return


    run = True
    curr = start
    curr_node = grid[curr[0]][curr[1]]
    curr_node.distance = 0
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


        curr_node = grid[curr[0]][curr[1]]
        curr_node.add_neighbors()
        for neighbor in curr_node.neighbors:

            if curr_node.distance + 1 < neighbor.distance:
                neighbor.distance = curr_node.distance + 1
                neighbor.past_nodes += curr_node.past_nodes
                neighbor.past_nodes.append(curr_node)


        if not curr_node.is_start():
            curr_node.color = RED


        smallest_dist = ROWS * COLS
        smallest_node = None
        for row in grid:
            for node in row:
                if not node.is_closed() and not node.is_start() and node.distance < smallest_dist:
                    smallest_node = node
                    smallest_dist = node.distance


        if smallest_dist == ROWS * COLS:
            break


        curr_node = smallest_node


        if curr_node.is_end():
            for node in curr_node.past_nodes:
                if not node.is_start():
                    node.color = GREEN
                draw_grid()
                pygame.display.update()
                clock.tick(FPS)
            return len(curr_node.past_nodes)

        curr_node.color = GREEN
        curr = (curr_node.x, curr_node.y)


        draw_grid()
        pygame.display.update()
        clock.tick(FPS)

    return -1