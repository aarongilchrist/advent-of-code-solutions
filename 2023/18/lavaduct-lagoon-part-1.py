import os
import numpy as np
from PIL import Image, ImageDraw, ImageColor

# Define current file location
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + "\\"

# Declare path of input file
input_path = __location__ + "input.txt"

input_strings = []

# Read each line in as a separate list item
with open(input_path) as input_file:
    input_strings = input_file.read().splitlines()

# Parse dig plan
dig_plan = [(step[0],int(step[1]),step[2][1:-1]) for step in [input_string.split(' ') for input_string in input_strings]]

terrain = [['#']]
curr_coord = (0,0)

# Follow dig plan
for num, item in enumerate(dig_plan):
    item_colour = ImageColor.getcolor(item[2],'RGB')
    # First extend size of terrain, then move coord and paint in
    if item[0] == 'R':
        if len(terrain[0])-1 < curr_coord[0] + item[1]:
            for k in range(len(terrain)):
                terrain[k] = terrain[k] + ['.'] * (curr_coord[0] + item[1] +1 -len(terrain[k]))
        curr_coord = (curr_coord[0]+item[1],curr_coord[1])
        terrain[curr_coord[1]] = terrain[curr_coord[1]][0:curr_coord[0]-item[1]+1] + [item_colour] * item[1] + terrain[curr_coord[1]][curr_coord[0]+1:]
    elif item[0] == 'L':
        if curr_coord[0] < item[1]:
            for k in range(len(terrain)):
                terrain[k] = ['.'] * ((item[1])-curr_coord[0]) + terrain[k]
        curr_coord = (max(curr_coord[0]-item[1],0),curr_coord[1])
        terrain[curr_coord[1]] = terrain[curr_coord[1]][:curr_coord[0]] + [item_colour] * item[1] + terrain[curr_coord[1]][curr_coord[0]+item[1]:]
    elif item[0] == 'D':
        if len(terrain) < curr_coord[1] + item[1]:
            for k in range(curr_coord[1] + item[1] - (len(terrain)-1)):
                terrain.append(['.']*len(terrain[0]))
        curr_coord = (curr_coord[0],curr_coord[1]+item[1])
        for k in range(curr_coord[1]-item[1],curr_coord[1]+1):
            terrain[k][curr_coord[0]] = item_colour
    elif item[0] == 'U':
        if curr_coord[1] < item[1]:
            for k in range(item[1] - curr_coord[1]):
                terrain.insert(0,['.']*len(terrain[0]))
        curr_coord = (curr_coord[0],max(curr_coord[1]-item[1],0))
        for k in range(curr_coord[1],curr_coord[1] + item[1]):
            terrain[k][curr_coord[0]] = item_colour
output_to_file = True

# Turn diagram into image by first putting as numpy array
terrain_image_matrix = np.zeros((len(terrain[0]), len(terrain), 3), dtype=np.uint8)
for y,row in enumerate(terrain):
    for x, item in enumerate(row):
        if(item != '.'):
            terrain_image_matrix[x,y] = item
        else:
            terrain_image_matrix[x,y] = [0,0,0]

# Create image
terrain_image = Image.fromarray(terrain_image_matrix,'RGB')

# Use floodfill algorithm on matrix
ImageDraw.floodfill(terrain_image,(len(terrain[0])/2,len(terrain)/2),(255,255,255))

#Save image
terrain_image.save(__location__ + "part-1.jpg")

# Convert back to array
filled_in_image = np.asarray(terrain_image)

# Count #s
for y,row in enumerate(terrain):
    for x, item in enumerate(row):
        if not np.array_equiv(filled_in_image[x,y],np.array([0,0,0])):
            terrain[y][x] = '#'

# Sum result  
lava_held = sum([row.count('#') for row in terrain])

print(lava_held)

