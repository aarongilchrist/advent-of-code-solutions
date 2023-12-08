import os

# Define current file location
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + "\\"

# Declare path of input file
input_path = __location__ + "input.txt"

input_strings = []

# Read each line in as a separate list item
with open(input_path) as input_file:
    input_strings = input_file.read().splitlines()

# Split directional instructions into list
directions = list(input_strings[0])

# Parse network node into dict
network = {input_string[0:3]:(input_string[7:10],input_string[12:15]) for input_string in input_strings[2:]}

# Find next node based on current node and direction
next_node = lambda current_node, direction: network[current_node][0] if direction == 'L' else network[current_node][1]

# Create list of nodes
nodes_list = ['AAA']

# Create counter of steps
step_number = 0

# Loop through nodes
while nodes_list[-1] != 'ZZZ':
    curr_direction = directions[step_number%len(directions)]
    nodes_list += [next_node(nodes_list[-1],curr_direction)]
    step_number += 1

# Return number of steps
print(step_number)