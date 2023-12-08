import os
import math

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

# Create list of lists of nodes
nodes_lists = [[node] for node in network.keys() if node.count('A') > 0]

# Firstly find how many steps it takes to get to the first z for each node
# Create loop failure condition
last_elt_contains_z = lambda lists: [1 if nodes_list[-1].count('Z') > 0 and len(nodes_list) > 1 else 0 for nodes_list in lists]

# Loop through sublists of nodes
step_number = 0
while sum(last_elt_contains_z(nodes_lists)) < len(nodes_lists):
    curr_direction = directions[step_number%len(directions)]
    non_terminated_paths = last_elt_contains_z(nodes_lists)
    nodes_lists = [nodes_list + [next_node(nodes_list[-1],curr_direction)] if non_terminated_paths[n] == 0 else nodes_list for n, nodes_list in enumerate(nodes_lists)]
    step_number += 1

# Find the number of steps to the first z
cycle_length = lambda list: [len(nodes_list)-1 for nodes_list in list]

# Now we calculate the length of a full cycle from the first Z to the next one
nodes_lists_2 = [[nodes_list[-1]] for nodes_list in nodes_lists]

# We create new loop failure criteria, i.e. the first elt is the same as the last
last_elt_same_as_first = lambda lists: [1 if nodes_list[-1] == nodes_list[0] and len(nodes_list) > 1 else 0 for nodes_list in lists]

while sum(last_elt_contains_z(nodes_lists_2)) < len(nodes_lists_2):
    curr_direction = directions[step_number%len(directions)]
    non_terminated_paths = last_elt_contains_z(nodes_lists_2)
    nodes_lists_2 = [nodes_list + [next_node(nodes_list[-1],curr_direction)] if non_terminated_paths[n] == 0 else nodes_list for n, nodes_list in enumerate(nodes_lists_2)]
    step_number += 1


# Find index of first Z and length of cycle to next as tuple
first_z_and_cycle_lengths = [(len(nodes_lists[n])-1,len(nodes_lists_2[n])-1) for n in range(len(nodes_lists))]

# Now we work out the total number of steps by solving simultaneous equations
# Let the index of z in the list x and the cycle length from z to z be y
# The solution is some integer n which solves all equations of the form x + ny

# In this case, by coincidence, each cycle from the first z to the next instance of itself is the same length as the A to the first Z
# We therefore can take a shortcut and calculate the lcm of these cycle lengths as our answer

final_cycle_length = math.lcm(*[item[0] for item in first_z_and_cycle_lengths])

print(final_cycle_length)