import pygame
import random
import numpy as np
from math import cos, sin, pi, tan



width, height = 800, 800
size = (width, height)
bgcolour = (0, 0, 0)
ON_COLOUR = (106,13, 173)
OFF_COLOUR = (60, 60, 60)
radius = 30
fps = 60
columns = round(width/1.7)//radius
rows = round(height/1.5)//radius
grid_size =(columns, rows)
apothem = radius / (2*tan(pi/6))
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
        pygame.time.delay(200)
        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                run = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_p:
                    pause = not pause
            if pygame.mouse.get_pressed()[0]:
                x,y = pygame.mouse.get_pos()
                x= x//radius%rows
                y= y//radius%columns
                array[x][y] = 1

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
            hex_x = (0.5 + x + y * 0.5 - y // 2 ) * (apothem * 2) #(x + z * 0.5f - z / 2) * (HexMetrics.innerRadius * 2f)
            hex_y = ((y+0.86)  * radius * 1.5) #position.z = z * (HexMetrics.outerRadius * 1.5f);
            if array[x][y] == 1:
                draw_hexagram(surface, hex_x, hex_y, radius - 2, ON_COLOUR)
            else:
                draw_hexagram(surface, hex_x, hex_y, radius - 2, OFF_COLOUR)

def next_array(array, pause):
    if pause == True:
        next = array.copy()
        for x in range(columns):
            for y in range(rows):
                state = next[x][y]
                neighbours = get_neighbours(array, x, y)
                if state == 1 and neighbours < 2 or neighbours >2:
                    next[x][y] = 0
                    # print(x,y)
                elif state == 0 and neighbours == 2:
                    next[x][y] = 1
                    print(x,y)
        array = next
        return array  
    else:
        return array    


# def get_neighbours(next, x, y):
#     total = 0
#     for i in range(-1, 1):
#         for j in range(-1, 1):
#             x_edge = (x + j + columns)%columns
#             y_edge = (y + i + rows)%rows
#             total += next[x_edge][y_edge]
#     total -= next[x][y]
#     return total

# def get_neighbours(next, x, y):
#     total = 0
#     total += next[(x+1 + columns)%columns][(y -1 + rows)%rows]
#     total += next[(x +1+ columns)%columns][(y + rows)%rows]
#     total += next[(x + columns)%columns][(y+1 +rows)%rows]
#     total += next[(x -1 + columns)%columns][(y +1 + rows)%rows]
#     total += next[(x-1 + columns)%columns][(y + rows)%rows]
#     total += next[(x + columns)%columns][(y -1 + rows)%rows]
    
#     total -= next[x][y]
#     return total

def get_neighbours(next, x,y):
    total = 0
    even_row = [[+1, 0], [0, -1], [-1, -1], [-1, 0], [-1, +1], [0, +1]]
    odd_row = [[+1,  0], [+1, -1], [ 0, -1], [-1,  0], [ 0, +1], [+1, +1]]
    if y %2 == 0:
        total += next[(x +even_row[0][0] + columns)%columns][(y+ even_row[0][1] +rows)%rows]
        total += next[(x +even_row[1][0] + columns)%columns][(y+ even_row[1][1] +rows)%rows]
        total += next[(x +even_row[2][0] + columns)%columns][(y+ even_row[2][1] +rows)%rows]
        total += next[(x +even_row[3][0] + columns)%columns][(y+ even_row[3][1] +rows)%rows]
        total += next[(x +even_row[4][0] + columns)%columns][(y+ even_row[4][1] +rows)%rows]
        total += next[(x +even_row[5][0] + columns)%columns][(y+ even_row[5][1] +rows)%rows]
    else:
        total += next[(x +odd_row[0][0] + columns)%columns][(y+ odd_row[0][1] +rows)%rows]
        total += next[(x +odd_row[1][0] + columns)%columns][(y+ odd_row[1][1] +rows)%rows]
        total += next[(x +odd_row[2][0] + columns)%columns][(y+ odd_row[2][1] +rows)%rows]
        total += next[(x +odd_row[3][0] + columns)%columns][(y+ odd_row[3][1] +rows)%rows]
        total += next[(x +odd_row[4][0] + columns)%columns][(y+ odd_row[4][1] +rows)%rows]
        total += next[(x +odd_row[5][0] + columns)%columns][(y+ odd_row[5][1] +rows)%rows]
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