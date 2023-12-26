import os
import itertools
import numpy as np

# Define current file location
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + "\\"

# Declare path of input file
input_path = __location__ + "input.txt"

input_strings = []

# Read each line in as a separate list item
with open(input_path) as input_file:
    input_strings = input_file.read().splitlines()

# Parse definitions of bricks
brick_definitions = {k:[[int(coord_num) for coord_num in coord.split(',')] for coord in input_string.split('~')] for k,input_string in enumerate(input_strings)}

min_component = lambda brick,component: min([cell[component] for cell in brick])
max_component = lambda brick,component: max([cell[component] for cell in brick])

brick_ranges = {k:((min_component(brick,0),max_component(brick,0)),
                   (min_component(brick,1),max_component(brick,1)),
                   (min_component(brick,2),max_component(brick,2)))
                   for k,brick in brick_definitions.items()}

bricks_xy = lambda brick_ranges: {k:set(itertools.product(range(brick_range[0][0],brick_range[0][1]+1),range(brick_range[1][0],brick_range[1][1]+1))) for k,brick_range in brick_ranges.items()}

def intersecting_xy(brick_ranges):
    horizontal_coords = bricks_xy(brick_ranges)
    xy_dict = {}
    for m in brick_ranges.keys():
        xy_ints = []
        for n in brick_ranges.keys():
            if horizontal_coords[m].intersection(horizontal_coords[n]) != set():
                xy_ints.append(n)
        xy_dict.update({m:set(xy_ints)})
    return xy_dict

min_z_key_val = sorted([(k,brick_range[2][0]) for k,brick_range in brick_ranges.items()],key=lambda x: x[1])

intersecting_keys = intersecting_xy(brick_ranges)
occupied_z = lambda brick_ranges,keys: set([x for k in keys for x in range(brick_ranges[k][2][0],brick_ranges[k][2][1]+1)])


# Move bricks down from bottom to top
for key_val in min_z_key_val:
    curr_range = brick_ranges[key_val[0]]
    intersections_xy = intersecting_keys[key_val[0]]
    occupied_in_intersections_xy = occupied_z(brick_ranges,intersections_xy)
    below_z_boundary = max([z if z < key_val[1] else 0 for z in occupied_in_intersections_xy])
    diff = key_val[1] - below_z_boundary - 1
    if key_val[1] != 1:
        brick_ranges.update({key_val[0]:(curr_range[0],curr_range[1],(curr_range[2][0]-diff,curr_range[2][1]-diff))})

# Get all coords in these new ranges
range_to_coords = lambda brick_range: set([tuple(comb) for comb in itertools.product(range(brick_range[0][0],brick_range[0][1]+1),range(brick_range[1][0],brick_range[1][1]+1),range(brick_range[2][0],brick_range[2][1]+1))])
brick_values = {k: range_to_coords(brick_range) for k,brick_range in brick_ranges.items()}

# Find coords below bricks
below_coords  = lambda brick: set([(coord[0],coord[1],coord[2]-1) for coord in brick]).difference(brick)
below_coords_bricks = {k:below_coords(brick) for k,brick in brick_values.items()}

# Find bricks above
above_item_dict = {}
for m,key_val in enumerate(min_z_key_val):
    above_items = []
    for item in intersecting_keys[key_val[0]]:
        if brick_values[key_val[0]].intersection(below_coords_bricks[item]) != set():
            above_items.append(item)
    above_item_dict.update({key_val[0]:set(above_items)})

# Disintegrate bricks
disintegrated_bricks = []
for x in sorted(above_item_dict.keys()):
    above_items = above_item_dict[x]
    held_by_others = set([y for k,v in above_item_dict.items() for y in v if k!=x])
    if np.prod([1 if brick in held_by_others else 0 for brick in above_items]) == 1:
        disintegrated_bricks.append(x)
        
number_which_can_be_disintegrated = len(disintegrated_bricks)

print(number_which_can_be_disintegrated)