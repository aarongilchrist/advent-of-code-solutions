import os

# Define current file location
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + "\\"

# Declare path of input file
input_path = __location__ + "input.txt"

input_strings = []

# Read each line in as a separate list item
with open(input_path) as input_file:
    input_strings = input_file.read().splitlines()#

# Get list of seeds from first line by using ' ' as a delimiter
seeds = list(map(int,input_strings[0].split(" ")[1:]))

# Define function to delimiit string of ints by ' '
values = lambda input_string: tuple(map(int,input_string.split(" ")))

# Get list of starting points of almanac entries (entry_name,starting_row)
entries = [(input_string[0:input_string.find(' map:')],index) for index,input_string in enumerate(input_strings) if input_string.find(' map') != -1]

# Get rows for each entry, first adding an indicator of the end of the file
entries.append(('end',len(input_strings)+1))
entry_rows = [(entry[0],list(map(values,input_strings[entry[1]+1:entries[index+1][1]-1]))) for index,entry in enumerate(entries) if index < len(entries)-1]

# Map seed through list of tuples for an entry
seed_map = lambda seed, map_tuple_list: seed + map_tuple_list[0][0] - map_tuple_list[0][1] if map_tuple_list[0][1] <= seed and map_tuple_list[0][1] + map_tuple_list[0][2] > seed else seed_map(seed,map_tuple_list[1:]) if len(map_tuple_list) > 1 else seed

# Map seed through entries
final_seed = lambda seed, entry_row_tuples: seed_map(seed,entry_row_tuples[0][1]) if len(entry_row_tuples) == 1 else final_seed(seed_map(seed,entry_row_tuples[0][1]),entry_row_tuples[1:])

# Create dict of seeds and locations
final_seed_locations = {seed:final_seed(seed,entry_rows) for seed in seeds}

# Get seed with lowest final location
min_location = min(final_seed_locations.values())

print(min_location)