import os

# Define current file location
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + "\\"

# Declare path of input file
input_path = __location__ + "input.txt"

input_strings = []

# Read each line in as a separate list item
with open(input_path) as input_file:
    input_strings = input_file.read().splitlines()

# Parse into grid
grid = [list(input_string) for input_string in input_strings]

# Create list of beam paths
beams = [[(-1,0),(0,0)]]

get_elt = lambda coord: grid[coord[1]][coord[0]]

rel_dir = lambda last_space, curr_space: (curr_space[0]-last_space[0],curr_space[1]-last_space[1])

add_coord = lambda curr_space, vector: (curr_space[0]+vector[0],curr_space[1]+vector[1])

def next_spaces(beam):
    curr_elt = get_elt(beam[-1])
    prev_dir = rel_dir(beam[-2],beam[-1])
    if curr_elt == '.':
        return [add_coord(beam[-1],prev_dir)]
    elif curr_elt == "/":
        return [add_coord(beam[-1],(-1*prev_dir[1],-1*prev_dir[0]))]
    elif curr_elt == "\\":
        return [add_coord(beam[-1],(prev_dir[1],prev_dir[0]))]
    elif curr_elt == "|":
        if prev_dir in [(0,1),(0,-1)]:
            return [add_coord(beam[-1],prev_dir)]
        else:
            return [add_coord(beam[-1],(0,1)),add_coord(beam[-1],(0,-1))]
    elif curr_elt == "-":
        if prev_dir in [(1,0),(-1,0)]:
            return [add_coord(beam[-1],prev_dir)]
        else:
            return [add_coord(beam[-1],(1,0)),add_coord(beam[-1],(-1,0))]

valid_coord = lambda coord: True if coord[0] in range(0,len(grid[0])) and coord[1] in range(0,len(grid)) else False
valid_beam = lambda beam: 1 if valid_coord(beam[-1]) else 0

# We use the last and the current pair as a termination condition, as beams are the same after these
beam_pairs = set()

# Loop through paths, choosing sufficiently high number of steps
while True:
    terminated = 0
    for k, beam in enumerate(beams):
        if valid_beam(beam) != 1:
            terminated += 1
        elif len(next_spaces(beam)) == 1 and (beam[-1],next_spaces(beam)[0]) in beam_pairs:
            terminated += 1
        elif len(next_spaces(beam)) == 1 and (beam[-1],next_spaces(beam)[0]) in beam_pairs and (beam[-1],next_spaces(beam)[1]) in beam_pairs:
            terminated += 1
        else:
            next_coords = next_spaces(beam)
            if len(next_coords) == 1:
                beam_pairs.add((beam[-1],next_coords[0]))
                beam.append(next_coords[0])
            else:
                beams.insert(k,beam + [next_coords[0]])
                beam.append(next_coords[1])
                beam_pairs.add((beam[-1],next_coords[0]))
                beam_pairs.add((beam[-1],next_coords[1]))
    if terminated == len(beams): break

# Get number energised
energised = set([coord for beam in beams for coord in beam if valid_coord(coord)])
num_energised = len(energised)

#print(energised)
print(num_energised)