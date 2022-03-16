# here is a link to the website I got the rules: I was successful!:
# https://arunarjunakani.github.io/HexagonalGameOfLife/

import pygame
import random
import numpy as np
from math import cos, sin, pi, tan
from copy import deepcopy

# screen dimensions
width, height = 800, 800
size = (width, height)
#colours of the board and the hexagons
bgcolour = (0, 0, 0)
ON_COLOUR = (106,13, 173)
OFF_COLOUR = (60, 60, 60)
#size of hexagons
radius = 25
fps = 60
#creating rows and columns based on the screen dimensions
columns = round(width/1.7)//radius
rows = round(height/1.5)//radius
grid_size =(columns, rows)
apothem = radius / (2*tan(pi/6))

def main():
    #I use pygame to visualize everything based on the array.
    # It also allows me to click on hexagons to turn them on or off
    # left click = ON; right click = OFF
    # *quick footnote is I couldn't get the mapping to work so if you
    # want to draw on the board you need to play around with it
    run = True
    pause = False
    pygame.init()
    pygame.display.set_caption("hexagrid")
    surface = pygame.display.set_mode(size)
    surface.fill(bgcolour)
    array = make_random_grid()
    clock = pygame.time.Clock()
    # main game loop. when you run the code you must press p to play
    # or pause
    while run:
        array = next_array(array, pause)
        game_of_life(surface, array)
        # setting framerate
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
            if pygame.mouse.get_pressed()[2]:
                x,y = pygame.mouse.get_pos()
                x= x//radius%rows
                y= y//radius%columns
                array[x][y] = 0

        pygame.display.update()

# function to draw a hexagon based the co-ordinate of in the grid
def draw_hexagram(surface, x, y, radius, colour):
    pts = []
    for i in range(6):
        pt_x = x + sin(i/6 * pi*2)* radius
        pt_y = y + cos(i/6 * pi*2)* radius
        pts.append([pt_x, pt_y])
    pygame.draw.polygon(surface, colour, pts)

#function to get the co-ordinates for the hexagons and draw them
# with colours and includes the offsets
def game_of_life(surface, array):
    for x in range(columns):
        for y in range(rows):
            hex_x = (0.5 + x + y * 0.5 - y // 2 ) * (apothem * 2) #(x + z * 0.5f - z / 2) * (HexMetrics.innerRadius * 2f)
            hex_y = ((y+0.86)  * radius * 1.5) #position.z = z * (HexMetrics.outerRadius * 1.5f);
            if array[x][y] == 1:
                draw_hexagram(surface, hex_x, hex_y, radius - 2, ON_COLOUR)
            else:
                draw_hexagram(surface, hex_x, hex_y, radius - 2, OFF_COLOUR)
# This function returns the new array based on the neighbours
def next_array(array, pause):
    number_of_neighbours_array = deepcopy(array)
    if pause == True:
        
        next = deepcopy(array)
        for x in range(columns):
            for y in range(rows):
                state = array[x][y]
                neighbours = get_neighbours(array, x, y)
                number_of_neighbours_array[x][y] = neighbours
                if state == 1 and neighbours < 2:
                    next[x][y] = 0
                elif state == 1 and neighbours > 2:
                    next[x][y] = 0
                elif state == 0 and neighbours == 2:
                    next[x][y] = 1
                else: next[x][y] = state
        array = next
        print(number_of_neighbours_array)
        return array  
    else:
        return array    

# function to calculate the neighbours depending on the co-ordinates
# I believe you said this was a periodic method? if you are on the 
# first or last column/row you look at the other side of the grid to 
# calculate neighbours (that's why you see the mod(%) here)
def get_neighbours(next, x,y):

    total = 0
    #co-ordinates of neighbours for even and odd row (my_row is even)
    my_row = [[-1, -1], [-1, +1], [0, +1], [+1, 0], [0, -1], [-1, 0]]
    my_row_odd = [[1, 1], [-1, 0], [0, -1], [+1, 0], [0, +1], [+1, -1]]
    # looks at even and odd row. The following I realise I could have 
    # done in a for loop but I am too lazy to do it. Also it works now and
    # i'm scared i'll break it haha
    if y%2 == 0:
        total += next[(x +my_row[0][0] + columns)%columns][(y + my_row[0][1] +rows)%rows]
        total += next[(x +my_row[1][0] + columns)%columns][(y + my_row[1][1] +rows)%rows]
        total += next[(x +my_row[2][0] + columns)%columns][(y + my_row[2][1] +rows)%rows]
        total += next[(x +my_row[3][0] + columns)%columns][(y + my_row[3][1] +rows)%rows]
        total += next[(x +my_row[4][0] + columns)%columns][(y + my_row[4][1] +rows)%rows]
        total += next[(x +my_row[5][0] + columns)%columns][(y + my_row[5][1] +rows)%rows]
    else:
        total += next[(x +my_row_odd[0][0] + columns)%columns][(y+ my_row_odd[0][1] +rows)%rows]
        total += next[(x +my_row_odd[1][0] + columns)%columns][(y+ my_row_odd[1][1] +rows)%rows]
        total += next[(x +my_row_odd[2][0] + columns)%columns][(y+ my_row_odd[2][1] +rows)%rows]
        total += next[(x +my_row_odd[3][0] + columns)%columns][(y+ my_row_odd[3][1] +rows)%rows]
        total += next[(x +my_row_odd[4][0] + columns)%columns][(y+ my_row_odd[4][1] +rows)%rows]
        total += next[(x +my_row_odd[5][0] + columns)%columns][(y+ my_row_odd[5][1] +rows)%rows]

    return total

def make_random_grid():
    # Here is where I make the array. I' ve set each element
    # to zero but if you uncomment and remove the zero it will 
    #create a random board
    array = np.ndarray(shape=(grid_size))
    for i in range(columns):
        for j in range(rows):
            array[i][j] =  0 #random.randint(0,1)
    
    # So the following could be commented out but I used to it test the
    # the neighbouring scheme which I ultimately used to calculate the neighbours

    x = 7
    y = 7
    my_row_even = [[-1, -1], [-1, +1], [0, +1], [+1, 0], [0, -1], [-1, 0]]
    my_row_odd = [[1, 1], [-1, 0], [0, -1], [+1, 0], [0, +1], [+1, -1]]
    if y%2 == 0:
        array[(x +my_row_even[0][0] + columns)%columns][(y+ my_row_even[0][1] +rows)%rows] = 1
        array[(x +my_row_even[1][0] + columns)%columns][(y+ my_row_even[1][1] +rows)%rows] = 1
        array[(x +my_row_even[2][0] + columns)%columns][(y+ my_row_even[2][1] +rows)%rows] = 1
        array[(x +my_row_even[3][0] + columns)%columns][(y+ my_row_even[3][1] +rows)%rows] = 1
        array[(x +my_row_even[4][0] + columns)%columns][(y+ my_row_even[4][1] +rows)%rows] = 1
        array[(x +my_row_even[5][0] + columns)%columns][(y+ my_row_even[5][1] +rows)%rows] = 1
    else:
        array[(x +my_row_odd[0][0] + columns)%columns][(y+ my_row_odd[0][1] +rows)%rows] = 1
        array[(x +my_row_odd[1][0] + columns)%columns][(y+ my_row_odd[1][1] +rows)%rows] = 1
        array[(x +my_row_odd[2][0] + columns)%columns][(y+ my_row_odd[2][1] +rows)%rows] = 1
        array[(x +my_row_odd[3][0] + columns)%columns][(y+ my_row_odd[3][1] +rows)%rows] = 1
        array[(x +my_row_odd[4][0] + columns)%columns][(y+ my_row_odd[4][1] +rows)%rows] = 1
        array[(x +my_row_odd[5][0] + columns)%columns][(y+my_row_odd[5][1] + rows)%rows] = 1
    array[x][y] = 1

    return array

if __name__ == '__main__':
    main()