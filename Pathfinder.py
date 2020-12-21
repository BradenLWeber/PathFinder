import pygame
import os, sys
from pygame.locals import *

pygame.init()

size = width, height = 1010, 794
box_size = 24
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Pathfinder')

font_button = pygame.font.SysFont('arial', box_size - 3)

shading = 1
clicked = []
# Placeholder so that while loop can be broken when this is changed to a 1
found_path = [0] 
no_solution = [0]
illustrate_process = [0]

loading_icon = pygame.image.load('Loading Icon.png')
pygame.transform.scale(loading_icon, (15, 15))
# This increments to turn the loading icon
angle = [0]
# These are the boxes that are behind the loading icon
draw = []
for i in range(0, box_size*6 + 1, box_size):
    for j in range(size[1] - box_size*6 - 2, size[1], box_size):
        draw.append([i, j])

def drawscreen(solve = False, illustrate = False):
    if not solve:
        if shading == 1:
            screen.fill((180 ,180, 180))
        for column in range(0, size[0], box_size):
            pygame.draw.rect(screen, (30, 30, 30), (column, 0, 2, size[1]))
        for row in range(0, size[1], box_size):
            pygame.draw.rect(screen, (30, 30, 30), (0, row, size[0], 2))

        for column in range(0, size[0], box_size):
            for row in range(0, size[1], box_size):
                drawshading((column, row), 1)

        for box in clicked:
            drawclick(box, clicked = True)
        
        if sequence[0] == 2:
            drawclick(starter, start = True)
        if not initiation[0]:
            drawclick(ender, end = True)
        
        if found_solution[0]:
            for spot in path:
                drawclick(spot, solution = True)
                
        pygame.draw.rect(screen, (110, 110, 110), (size[0] - box_size * 3 + 1, 2, box_size * 3 - 3, box_size - 2))
        drawshading([size[0] - box_size*3 - 2, 0], 3, rect = True)
        text_reset = font_button.render('Reset', 1, (0, 0, 0))
        screen.blit(text_reset, (size[0] - int((box_size * 3 + text_reset.get_width()) / 2), 1))

        pygame.draw.rect(screen, (110, 110, 110), (size[0] - box_size * 3 + 1, 2 + box_size, box_size * 3 - 3, box_size - 2))
        drawshading([size[0] - box_size*3 - 2, box_size], 3, rect = True)
        text_clear = font_button.render('Clear', 1, (0, 0, 0))
        screen.blit(text_clear, (size[0] -  int((box_size * 3 + text_clear.get_width()) / 2), 1 + box_size))

        pygame.draw.rect(screen, (110, 110, 110), (size[0] - box_size * 3 + 1, 2 + box_size*2, box_size * 3 - 3, box_size - 2))
        drawshading([size[0] - box_size*3 - 2, box_size*2], 3, rect = True)
        text_start = font_button.render('Start', 1, (0, 0, 0))
        screen.blit(text_start, (size[0] -  int((box_size * 3 + text_start.get_width()) / 2), 1 + box_size*2))

        if illustrate_process[0]:
            color = (45, 193, 34)
            shade = 4
        else:
            color = (247, 10, 15)
            shade = 5
        pygame.draw.rect(screen, color, (size[0] - box_size * 3 + 1, 2 + box_size * 3, box_size * 3 - 3, box_size - 2))
        drawshading([size[0] - box_size*3 - 2, box_size*3], shade, rect = True)
        text_illustrate = font_button.render('Illustrate', 1, (0, 0, 0))
        screen.blit(text_illustrate, (size[0] -  int((box_size * 3 + text_illustrate.get_width()) / 2), 1 + box_size*3))

    else:
        for spot in draw:
            if spot in clicked:
                drawclick(spot, clicked = True)
            elif spot == starter:
                drawclick(spot, start = True)
            elif spot == ender:
                drawclick(spot, end = True)
            else:
                drawclick(spot, background = True)
        angle[0] += .3
        screen.blit(pygame.transform.rotate(loading_icon, angle[0]), (15, size[1] - 55))

    if illustrate:
        for box in checked:
            drawclick(box, check = True)
        for box in explored:
            drawclick(box, explore = True) 

    pygame.display.update()

def drawshading(spot, shading, rect = False):
    ''' spot is upper left coordinate, shading is number to determine color, and rect is True or False for shading rectangular buttons'''
    # Clicked box
    if shading == 1:
        color1 = 140, 140, 140
        color2 = 195, 195, 195
    # Uncliked box
    elif shading == 2:
        color1 = 20, 20, 20
        color2 = 50, 50, 50
    # Reset button
    elif shading == 3:
        color1 = 90, 90, 90
        color2 = 130, 130, 130
    # Start position
    elif shading == 4:
        color1 = 41, 158, 32
        color2 = 58, 213, 37 
    # End position
    elif shading == 5:
        color1 = 205, 20, 20
        color2 = 255, 56, 51
    # Found path
    elif shading == 6:
        color1 = 40, 81 , 178
        color2 = 67, 116, 229
    # Spots that have been explored
    elif shading == 7:
        color1 = 90, 181, 83
        color2 = 127, 229, 120
    # spots that have been checked
    elif shading == 8:
        color1 = 252, 103, 103
        color2 = 243, 153, 153
    
    pygame.draw.polygon(screen, color1, [(spot[0] + 2, spot[1] + 2), (spot[0] + 2, spot[1] + box_size - 1), (spot[0] + 4, spot[1] + box_size - 2), (spot[0] + 4, spot[1]  + 4)])
    if not rect:
        pygame.draw.polygon(screen, color2, [(spot[0] + 2, spot[1] + 2), (spot[0] + 4, spot[1]  + 4), (spot[0] + box_size - 3, spot[1] + 4), (spot[0] + box_size - 1, spot[1] + 2)])
    else:
        pygame.draw.polygon(screen, color2, [(spot[0] + 2, spot[1] + 2), (spot[0] + 4, spot[1]  + 4), (spot[0] + box_size*3 - 2, spot[1] + 4), (spot[0] + box_size*3, spot[1] + 2)])

def drawclick(spot, clicked = False, start = False, end = False, solution = False, explore = False, check = False, background = False):
    '''This is to color a box that has been clicked'''
    location = (spot[0] + 2, spot[1] + 2, box_size - 2, box_size - 2)
    if clicked:
        pygame.draw.rect(screen, (0,0,0), location)
        drawshading(spot, 2)
    elif start:
        pygame.draw.rect(screen, (45, 193, 34), location)
        drawshading(spot, 4)
    elif end:
        pygame.draw.rect(screen, (247, 10, 15), location)
        drawshading(spot, 5)
    elif solution:
        pygame.draw.rect(screen, (46, 96, 213), location)
        drawshading(spot, 6)
    elif explore:
        pygame.draw.rect(screen, (104, 203, 97), location)
        drawshading(spot, 7)
    elif check:
        pygame.draw.rect(screen, (240, 116, 116), location)
        drawshading(spot, 8)
    elif background:
        pygame.draw.rect(screen, (180, 180, 180), location)
        drawshading(spot, 1)


def findmouselocation(position):
    '''Finds the coordinate of the box the mouse is in rather than the true coordinate of the mouse'''
    for column in range(0, size[0], box_size):
        for row in range(0, size[1], box_size):
            if position[0] > column and position[0] < column + box_size and position[1] > row and position[1] < row + box_size:
                if (column, row) in [(size[0]-box_size*3-2, 0), (size[0]-box_size*2-2, 0), (size[0]-box_size-2, 0)]:
                    return (2, 2)
                elif (column, row) in [(size[0]-box_size*3-2, box_size), (size[0]-box_size*2-2, box_size), (size[0]-box_size-2, box_size)]:
                    return (3, 3)
                elif (column, row) in [(size[0]-box_size*3-2, box_size*2), (size[0]-box_size*2-2, box_size*2), (size[0]-box_size-2, box_size*2)]:
                    return (4, 4)
                elif (column, row) in [(size[0]-box_size*3-2, box_size*3), (size[0]-box_size*2-2, box_size*3), (size[0]-box_size-2, box_size*3)]:
                    return (5, 5)
                else:
                    return (column, row)
    # If mouse is on line between boxes (1, 1) is returned
    return (1, 1)

def finddistance(box1, box2):
    '''diagonal jumps are 14 and normal jumps are 10'''
    distance = 0
    # Changing from tuple to list so it can be editted
    box1 = [box1[0], box1[1]]
    box2 = [box2[0], box2[1]]
    while box1 != box2:
        if box2[0] < box1[0] and box2[1] < box1[1]:
            box1[0] -= box_size
            box1[1] -= box_size
            distance += 14
        elif box2[0] > box1[0] and box2[1] > box1[1]:
            box1[0] += box_size
            box1[1] += box_size
            distance += 14
        elif box2[0] > box1[0] and box2[1] < box1[1]:
            box1[0] += box_size
            box1[1] -= box_size
            distance += 14
        elif box2[0] < box1[0] and box2[1] > box1[1]:
            box1[0] -= box_size
            box2[1] += box_size
            distance += 14
        else:
            if box2[0] > box1[0]:
                box1[0] += box_size
            elif box2[0] < box1[0]:
                box1[0] -= box_size
            elif box2[1] > box1[1]:
                box1[1] += box_size
            elif box2[1] < box1[1]:
                box1[1] -= box_size
            distance += 10
    return distance

# These are ones I've calculated the values of
checked = []
# These are ones that inherit other boxes
explored = []
# This stores distance to reach the explored box
exp_dist = [0]
# Starts with zero because the first spot is explored and it's parent is itself
parent = [0]
# This is only accumulated distance from the start
accum_dist = []
# This is accumulated distance from the start plus red distance
total_dist = []
# This stores the box the begot the current box
inheritance = []
# This will store the resulting path once the end has been reached
path = []

def reset(walls = True):
    for collection in [checked, explored, exp_dist, parent, accum_dist, total_dist, inheritance, path, starter, ender]:
        collection.clear()
    if walls:
        clicked.clear()
    else:
        try:
            addedges(reverse = True)
        except:
            pass
    exp_dist.append(0)
    parent.append(0)
    found_solution[0] = 0
    found_path[0] = 0
    sequence[0] = 1
    initiation[0] = 1
    timer[0] = 0
    clock_speed[0] = 40
    break_path[0] = 1
    no_solution[0] = 0


def addedges(reverse = False):
    '''adds the edges of the screen and buttons to the list of walls (clicked)'''
    add = []
    for i in range(0, size[1], box_size):
        add.append([-box_size, i])
        add.append([size[0] - 2, i])
    for i in range(0, size[0], box_size):
        add.append([i, -box_size])
        add.append([i, size[1] - 2])
    add.append([-box_size, -box_size])
    add.append([-box_size, size[1]])
    add.append([size[0], -box_size])
    add.append([size[0], size[1]])
    for i in range(size[0] - box_size* 3 - 2, size[0], box_size):
        for j in [0, box_size, box_size*2, box_size * 3]:
            add.append([i, j])
    if not reverse:
        clicked.extend(add)
    else:
        for box in add:
            clicked.remove(box)


def explore(spot, dist):
    '''Starts at a spot and works outward one layer
    Dist is total accumulated distance up to that point'''
    if illustrate_process[0]:
        drawscreen(illustrate = True)
    else:
        drawscreen(solve = True)
    if illustrate_process[0]:
        timer[0] += 1
        if timer[0] > 50:
            if timer[0] % 5 == 0:
                clock_speed[0] += 1
        clock.tick(clock_speed[0])

    explored.append(spot)
    # If spot is in checked, must pop out all existing things for it
    if spot != starter:
        exp_dist.append(dist)
        index = checked.index(spot)
        parent.append(inheritance[checked.index(spot)])
        for group in [checked, total_dist, accum_dist, inheritance]:
            group.pop(index)

    if finddistance(spot, ender) in [10,14]:
        findpath(spot)
        return
    for column in [-box_size, 0, box_size]:
        for row in [-box_size, 0, box_size]:
            box = [spot[0] + column, spot[1] + row]
            if [column, row] == [0, 0] or box in clicked:
                continue
            if column == 0 or row == 0:
                distance = 10
            else:
                distance = 14

            if box in checked:
                if dist + distance < accum_dist[checked.index(box)]:
                    index = checked.index(box)
                    for collection in [checked, accum_dist, total_dist, inheritance]:
                        collection.pop(index)
                    checked.append(box)
                    accum_dist.append(dist + distance)
                    total_dist.append(dist + distance + finddistance(box, ender))
                    inheritance.append(spot)
            elif box in explored:
                if dist + distance < exp_dist[explored.index(box)]:
                    index = explored.index(box)
                    for collection in [explored, exp_dist, parent]:
                        collection.pop(index)
                    explored.append(box)
                    exp_dist.append(dist + distance)
                    parent.append(spot)
            else:
                checked.append(box)
                accum_dist.append(dist + distance)
                total_dist.append(dist + distance + finddistance(box, ender))
                inheritance.append(spot)


def searching():
    '''starts sequence of finding a path'''
    addedges()

    explore(starter, 0)
    while found_path[0] == 0 and no_solution[0] == 0:
        # Total dist stores all the distances of checked boxes, but checked boxes are deleted as they are explored
        # If there is no solution, every checked box will be explored until total_dist is just an empty set
        try:
            best = min(total_dist)
        except:
            no_solution[0] = 1
            continue
        if total_dist.count(best) == 1:
            index = total_dist.index(best)
            explore(checked[index], accum_dist[index])
        else:
            indeces = []
            indeces_red_dist = []
            for value in total_dist:
                if value == best:
                    indeces.append(total_dist.index(value))
                    indeces_red_dist.append(total_dist[total_dist.index(value)] - accum_dist[total_dist.index(value)])
            bestest = min(indeces_red_dist)
            for i in range(len(checked)):
                # This is a try because when you explore, some things might get deleted from checked
                try:
                    if total_dist[i] == best and total_dist[i] - accum_dist[i] == bestest:
                        explore(checked[i], accum_dist[i])
                except:
                    pass
    if no_solution[0] == 1:
        reset(walls = False)
            
found_solution = [0]
# Breaks the loop that calculates the ending path
break_path = [1]

def findpath(spot):
    found_path[0] += 1
    path.append(ender)
    path.append(spot)
    while break_path[0]:
        for box in explored:
            if box == spot:
                index = explored.index(box)
                if parent[index] == 0:
                    break_path[0] = 0
                else:
                    path.append(parent[index])
                    spot = parent[index]

    found_solution[0] = 1

# This stores the previous box a mouse has entered so that if you hold click while in the same box, it will only run the code for coloring it once and not over and over
previous = 0
# This is so once you start a long click, if you are adding boxes they can only keep being added and not taken away
add = False
# This is to know if the starting sequence is happening
initiation = [1]
sequence = [1]
# Locations of starting and ending blocks
starter = []
ender = []
# this is so a wall can be clicked multiple times and changed without moving mouse out of the box first
change = False
# This is so that if you hold down click while you lay the red block, it won't automatically turn to black blocks
delay = False
# This tracks how long the program has been running so that it can run slightly faster the longer it goes
timer = [0]
# this is number that goes in clock.tick
clock_speed = [40]


clock = pygame.time.Clock()

# ------------------ Main loop -----------------------

while True:

    for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                if event.key in [K_1, K_2, K_3, K_4]:
                    if event.key == K_1:
                        box_size = 12
                        clock_speed[0] = 80
                    elif event.key == K_2:
                        box_size = 24
                        clock_speed[0] = 45
                    elif event.key == K_3:
                        box_size = 36
                        clock_speed[0] = 30
                    elif event.key == K_4:
                        box_size = 72
                        clock_speed[0] = 20
                    
                    draw = []
                    for i in range(0, box_size*6 + 1, box_size):
                        for j in range(size[1] - box_size*6 - 2, size[1], box_size):
                            draw.append([i, j])

                    font_button = pygame.font.SysFont('arial', box_size - 3)
                    reset()

            if event.type == MOUSEBUTTONDOWN:
                change = True
                if delay:
                    delay = False
                pos = findmouselocation(pygame.mouse.get_pos())
                box = [pos[0], pos[1]]
                if box not in [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5]]:
                    if initiation[0]:
                        if sequence[0] == 1:
                            starter = box
                            sequence[0] = 2
                        elif sequence[0] == 2:
                            ender = box
                            initiation[0] = 0
                            delay = True
                    else:
                        if box not in clicked:
                            add = True
                        else:
                            add = False
                elif box == [2, 2]:
                    reset()

                elif box == [3, 3]:
                    path.clear()
                    reset(walls = False)

                elif box == [4, 4]:
                    if not initiation[0]:
                        searching()
                
                elif box == [5, 5]:
                    if illustrate_process[0] == 0:
                        illustrate_process[0] = 1
                    elif illustrate_process[0] == 1:
                        illustrate_process[0] = 0
            else: 
                change = False

    if not initiation[0] and not delay:         
        mouse_keys = pygame.mouse.get_pressed()
        if mouse_keys[0]:
            pos = findmouselocation(pygame.mouse.get_pos())
            box = [pos[0], pos[1]]
            if box != previous or change == True:
                previous = box
                if box not in [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5]]:
                    if box not in clicked and add:
                        clicked.append(box)
                    elif box in clicked and not add:
                        clicked.remove(box)

    drawscreen()


# Optimize options: drawing walls behind buttons is unnecessary
# Add more comments
# unneccessary to put edges of screen in clicked because then it draws that out when it clearly doesn't need to be drawn
