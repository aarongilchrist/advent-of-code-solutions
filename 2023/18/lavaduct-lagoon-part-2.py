import os
from re import A

# Define current file location
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + "\\"

# Declare path of input file
input_path = __location__ + "input.txt"

input_strings = []

# Read each line in as a separate list item
with open(input_path) as input_file:
    input_strings = input_file.read().splitlines()

dir_dict = {'0':'R','1':'D','2':'L','3':'U'}

# Parse dig plan
dig_plan = [(dir_dict[step[2][-2]],int(step[2][2:-2],16)) for step in [input_string.split(' ') for input_string in input_strings]]

path_coords = [(0,0)]

add_coord = lambda curr_space, vector: (curr_space[0]+vector[0],curr_space[1]+vector[1])

#print(sum([step[1] for step in dig_plan]))

for step in dig_plan:
    for x in range(step[1]):
        if step[0] == 'R':
            path_coords.append(add_coord(path_coords[-1],(1,0)))
        elif step[0] == 'D':
            path_coords.append(add_coord(path_coords[-1],(0,1)))
        elif step[0] == 'L':
            path_coords.append(add_coord(path_coords[-1],(-1,0)))
        elif step[0] == 'U':
            path_coords.append(add_coord(path_coords[-1],(0,-1)))



# Use shoelace and Pick's theorem to calculate number inside
area = 0.5 * sum([path_coords[k][0]*path_coords[k+1][1] - path_coords[k][1]*path_coords[k+1][0] for k in range(len(path_coords)-1)])
boundary_length = len(set(path_coords))
number_inside = int(len(path_coords)/2 + area)+1

print(number_inside)