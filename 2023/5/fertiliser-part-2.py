import os

# This took over 12 hours to run

# Define current file location
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + "\\"

# Declare path of input file
input_path = __location__ + "input.txt"

input_strings = []

# Read each line in as a separate list item
with open(input_path) as input_file:
    input_strings = input_file.read().splitlines()#

# Get raw list of seed ranges from first line by using ' ' as a delimiter
raw_seed_ranges = list(map(int,input_strings[0].split(" ")[1:]))

# We now know that these seeds are in ranges, so we split them into pairs
seeds = [raw_seed_ranges[2*n] for n in range(0,int(len(raw_seed_ranges)/2))]
ranges = [raw_seed_ranges[2*n+1] for n in range(0,int(len(raw_seed_ranges)/2))]

# Get all seeds as a generator
all_seeds = (seed + n for index,seed in enumerate(seeds) for n in range(0,ranges[index]))

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

# Search through for min location
locations = (final_seed(seed,entry_rows) for seed in all_seeds)

min_loc = min(locations)

print(min_loc)

# Write to a file, as this takes a long time to run
with open(__location__ + "result.txt", "w") as output_file:
    output_file.write(str(min_loc))