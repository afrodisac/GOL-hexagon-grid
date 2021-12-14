import pygame
import random
import numpy as np
from math import cos, sin, pi, tan

width, height = 1000, 1000
size = (width, height)
bgcolour = (0, 0, 0)
ON_COLOUR = (0, 0, 0)
OFF_COLOUR = (255, 255, 255)
radius = 20
fps = 30
columns = width//radius
rows = height//radius
grid_size =(columns, rows)
apothem = radius / (2*tan(pi/6))
#dick ={}
def main():
    run = True
    pause = False
    pygame.init()
    pygame.display.set_caption("hexagrid")
    surface = pygame.display.set_mode(size)
    surface.fill(bgcolour)
    array = make_random_grid()
    clock = pygame.time.Clock()
    while run:
        game_of_life(surface, array)
        array = next_array(array, pause)
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                run = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_p:
                    pause = not pause
        # if pygame.mouse.get_pressed()[0]:
        #     hex_x, hex_y = pygame.mouse.get_pos()
        #     # x = x//radius
        #     # y = y//radius
        #     x = dick[[hex_x, hex_y]][0]
        #     y = dick[[hex_x, hex_y]][1]
        #     print(x, y)
        #     array[x][y] = 1 
        pygame.display.update()

def draw_hexagram(surface, x, y, radius, colour):
    pts = []
    for i in range(6):
        pt_x = x + sin(i/6 * pi*2)* radius
        pt_y = y + cos(i/6 * pi*2)* radius
        pts.append([pt_x, pt_y])
    pygame.draw.polygon(surface, colour, pts)

def game_of_life(surface, array):
    for x in range(columns):
        for y in range(rows):
            #random_colour = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
            hex_x = (x + y * 0.5 - y // 2 ) * (apothem * 2) #(x + z * 0.5f - z / 2) * (HexMetrics.innerRadius * 2f)
            hex_y = (y * radius * 1.5) #position.z = z * (HexMetrics.outerRadius * 1.5f);
            #dick[[hex_x, hex_y]] = [x, y]
            if array[x][y] == 1:
                draw_hexagram(surface, hex_x, hex_y, radius - 2, ON_COLOUR)
            else:
                draw_hexagram(surface, hex_x, hex_y, radius - 2, OFF_COLOUR)

def next_array(array, pause):
    if pause == False:
        next = array.copy()
        for x in range(columns):
            for y in range(rows):
                state = next[x][y]
                neighbours = get_neighbours(array, x, y)
                if state == 1 and (neighbours < 2 or neighbours > 3):
                    next[x][y] = 0
                elif state == 0 and neighbours == 3:
                    next[x][y] = 1
        array = next
        return array    


def get_neighbours(next, x, y):
    total = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            x_edge = (x + i + columns)%columns
            y_edge = (y + j + rows)%rows
            total += next[x_edge][y_edge]
    total -= next[x][y]
    return total

def make_random_grid():
    array = np.ndarray(shape=(grid_size))
    for i in range(columns):
        for j in range(rows):
            array[i][j] = random.randint(0,1)
    return array

if __name__ == '__main__':
    main()