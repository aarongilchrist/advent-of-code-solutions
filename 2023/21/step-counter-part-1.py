import os

# Define current file location
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + "\\"

# Declare path of input file
input_path = __location__ + "input.txt"

input_strings = []

# Read each line in as a separate list item
with open(input_path) as input_file:
    input_strings = input_file.read().splitlines()

garden = input_strings

# Get location of S
starting_position = [(row.index('S'),y) for y, row in enumerate(garden) if 'S' in row][0]

number_of_steps_allowed = 64

visited_coords = [set([starting_position])]
# Count number of steps
for n in range(number_of_steps_allowed):
    newly_visited = set()
    for visited_coord in visited_coords[-1]:
        for adjacent in [(visited_coord[0]+direction[0],visited_coord[1]+direction[1]) for direction in [(-1,0),(1,0),(0,-1),(0,1)]]:
            if adjacent not in newly_visited and adjacent[0] in range(len(garden[0])) and adjacent[1] in range(len(garden)) and garden[adjacent[1]][adjacent[0]] != '#':
                newly_visited = newly_visited.union([adjacent])
    visited_coords.append(newly_visited)

#print(visited_coords)

#for y, row in enumerate(garden):
#    print(''.join([step if ((x,y)) not in visited_coords[-1] else 'O' for x,step in enumerate(row)]))

print(len(visited_coords[-1]))
