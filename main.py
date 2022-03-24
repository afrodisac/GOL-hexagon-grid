# here is a link to the website I got the rules: I was successful!:
# https://arunarjunakani.github.io/HexagonalGameOfLife/
# I should add a funcion to calculate the density and visualise it
# fix the mouse mapping
# make co-ordinate system axial / cubic

import pygame
import random
import numpy as np
from math import cos, sin, pi, tan, floor
from copy import deepcopy

# screen dimensions
width, height = 800, 800
size = (width, height)

#colours of the board and the hexagons
bgcolour = (0, 0, 0)
ON_COLOUR = (106,13, 173)
OFF_COLOUR = (60, 60, 60)

#size of hexagons
radius = 15 # outer radius or height

fps = 60

#creating rows and columns based on the screen dimensions
columns = 20
rows = 25
grid_size =(columns, rows)
apothem = radius / (2*tan(pi/6)) #inner radius or width

def main():
    #I use pygame to visualize everything based on the array.
    # It also allows me to click on hexagons to turn them on or off
    # left click = ON; right click = OFF
    # *quick footnote is I couldn't get the mapping to work so if you
    # want to draw on the board you need to play around with it
    # and sometimes it goes out of bounds...

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

        #checking for buttons clicks or if exit button is clicked
        pygame.time.delay(200)
        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                run = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_p:
                    pause = not pause
            if pygame.mouse.get_pressed()[0]:
                pos = []
                x,y = pygame.mouse.get_pos()
                # x = x//radius
                # y = y//radius
                pos = find_hexagon(x, y)
                print(pos)


                # x= x//radius%rows
                # y= y//radius%columns
                array[pos[0]][pos[1]] = 1
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

# function to get the co-ordinates for the hexagons and draw them
# with colours and includes the offsets
def game_of_life(surface, array):
    for x in range(columns):
        for y in range(rows):
            hex_x = (0.5 + x + y * 0.5  ) * (apothem * 2) #(x + z * 0.5f - z / 2) * (HexMetrics.innerRadius * 2f)
            hex_y = ((y+0.86)  * radius * 1.5) #position.z = z * (HexMetrics.outerRadius * 1.5f);
            if array[x][y] == 1:
                draw_hexagram(surface, hex_x, hex_y, radius - 2, ON_COLOUR)
            else:
                draw_hexagram(surface, hex_x, hex_y, radius - 2, OFF_COLOUR)

# This function returns the new array based on the neighbours
def next_array(array, pause):
    if pause == True:      
        next = deepcopy(array)
        for x in range(columns):
            for y in range(rows):
                state = array[x][y]
                neighbours = get_neighbours(array, x, y)
                if state == 1 and neighbours < 2:
                    next[x][y] = 0
                elif state == 1 and neighbours > 2:
                    next[x][y] = 0
                elif state == 0 and neighbours == 2:# and random.randint(1,12) != 2:
                    next[x][y] = 1
                else: next[x][y] = state
        array = next
        return array  
    else:
        return array    

# function to calculate the neighbours depending on the co-ordinates
# I believe you said this was a periodic method? if you are on the 
# first or last column/row you look at the other side of the grid to 
# calculate neighbours (that's why you see the mod(%) here)
def get_neighbours(next, x,y):
    # x, y = offset_to_axial(x, y)
    total = 0

    # co-ordinates of neighbours for even and odd row (my_row is even)
    my_row = [[-1, -1], [-1, +1], [0, +1], [+1, 0], [0, -1], [-1, 0]]
    my_row_odd = [[1, 1], [-1, 0], [0, -1], [+1, 0], [0, +1], [+1, -1]]
    
    #axial co-ordinates
    axial_neighbours = [[0, -1], [-1, 0], [0, +1], [+1, 0], [+1, -1], [-1, 1]]

    # axial coordinates
    for i in range(6):
        total += next[(x +axial_neighbours[i][0] + columns)%columns][(y + axial_neighbours[i][1] +rows)%rows]

    # looks at even and odd row.
    # if y%2 == 0:
        #for i in range(6):
            #total += next[(x +my_row[i][0] + columns)%columns][(y + my_row[i][1] +rows)%rows]
    #     total += next[(x +my_row[0][0] + columns)%columns][(y + my_row[0][1] +rows)%rows]
    #     total += next[(x +my_row[1][0] + columns)%columns][(y + my_row[1][1] +rows)%rows]
    #     total += next[(x +my_row[2][0] + columns)%columns][(y + my_row[2][1] +rows)%rows]
    #     total += next[(x +my_row[3][0] + columns)%columns][(y + my_row[3][1] +rows)%rows]
    #     total += next[(x +my_row[4][0] + columns)%columns][(y + my_row[4][1] +rows)%rows]
    #     total += next[(x +my_row[5][0] + columns)%columns][(y + my_row[5][1] +rows)%rows]
    # else:
        #for i in range(6):
            #total += next[(x +my_row_odd[i][0] + columns)%columns][(y + my_row_odd[i][1] +rows)%rows]
    #     total += next[(x +my_row_odd[0][0] + columns)%columns][(y+ my_row_odd[0][1] +rows)%rows]
    #     total += next[(x +my_row_odd[1][0] + columns)%columns][(y+ my_row_odd[1][1] +rows)%rows]
    #     total += next[(x +my_row_odd[2][0] + columns)%columns][(y+ my_row_odd[2][1] +rows)%rows]
    #     total += next[(x +my_row_odd[3][0] + columns)%columns][(y+ my_row_odd[3][1] +rows)%rows]
    #     total += next[(x +my_row_odd[4][0] + columns)%columns][(y+ my_row_odd[4][1] +rows)%rows]
    #     total += next[(x +my_row_odd[5][0] + columns)%columns][(y+ my_row_odd[5][1] +rows)%rows]

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

    # axial coordinates
    
    x = 7
    y = 7
    x, y 
    horizontal_row = [[0, 3], [1, 3], [2, 3], [3, 3], [4, 3], [5, 3], [6, 3], [7, 3], [8, 3], [9, 3]]
    vertical_row =   [[4 + floor(0/2), 0], [4 + floor(1/2), 1], [4 + floor(2/2), 2], [4 + floor(3/2), 3], [4 + floor(4/2), 4], [4 + floor(5/2), 5], [4 + floor(6/2), 6], [4 + floor(7/2), 7], [4 + floor(8/2), 8], [4 + floor(9/2), 9]]
    axial_neighbours = [[0, -1], [-1, 0], [0, +1], [+1, 0], [+1, -1], [-1, 1]]

    for i in range(6):
        array[x + axial_neighbours[i][0]][y + axial_neighbours[i][1]] = 1
    array[x][y] = 1


    # for i in range(len(horizontal_row)):
    #     array[(horizontal_row[i][0] + columns)%columns][(horizontal_row[i][1] +rows)%rows] = 1
    #     array[(vertical_row[i][0] + columns)%columns][(vertical_row[i][1] +rows)%rows] = 1


    return array

def offset_to_axial(offset_x, offset_y):
    axial_x = offset_x - (floor(offset_y/2))
    axial_y = offset_y #- (floor(offset_x/2))
    return axial_x, axial_y

def cubic_z_coordinate(x, y):
    z = -x -y
    return z

def find_hexagon(x, y):
    # this all doesn't work. I still need to figure out how to map it correctly
    x-=columns
    y-=rows
    xVal = floor((x/apothem))
    yVal = floor((y/(radius*(3/4))))
    dX = x%apothem
    dY = y%(radius*(3/4))
    slope = (radius/4)/(apothem /2)
    caldY = dX*slope
    delta = (radius/4) - caldY

    if yVal%2 == 0:
        if abs(delta) > dY:
            if delta > 0:
                xVal -= 1
                yVal -= 1
            else:
                yVal -= 1
    
    else:
        if dX> (apothem/2):
            if dY < (radius/2) - caldY:
                yVal -= 1
        else:
            if dY>caldY:
                xVal -=1
            else:
                yVal -=1
    x = xVal
    y = yVal

    return x, y



if __name__ == '__main__':
    main()