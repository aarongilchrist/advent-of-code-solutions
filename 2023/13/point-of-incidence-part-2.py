import os

# Define current file location
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + "\\"

# Declare path of input file
input_path = __location__ + "input.txt"

input_strings = []

# Read each line in as a separate list item
with open(input_path) as input_file:
    input_strings = input_file.read().splitlines()

# Delimit list of strings into pattern
patterns = []
curr_pattern = []
for input_string in input_strings:
    if input_string != "":
        curr_pattern.append(input_string)
    else:
        patterns.append(curr_pattern)
        curr_pattern = []
patterns.append(curr_pattern)

# Transpose patterns to line by line vertically
patterns_transposed = [[''.join([pattern[x][y] for x in range(len(pattern))]) for y in range(len(pattern[0]))] for pattern in patterns]
transpose_pattern = lambda pattern: [''.join([pattern[x][y] for x in range(len(pattern))]) for y in range(len(pattern[0]))]

# We compare each row with all of the other rows and each column with all of the other columns to find how many elements in order they have in common
compare_same_length_strings = lambda str1,str2: sum([1 if str1[x] == str2[x] else 0 for x in range(len(str1))])
numbers_in_common = lambda pattern: {(x,y): compare_same_length_strings(pattern[x],pattern[y]) for x in range(len(pattern)) for y in range(len(pattern)) if x<y}
different_index = lambda str1,str2: [1 if str1[x] == str2[x] else 0 for x in range(len(str1))].index(0)
nearly_same = lambda pattern: {coord:different_index(pattern[coord[0]],pattern[coord[1]]) for coord,num in numbers_in_common(pattern).items() if num == len(pattern[0])-1}

index_slice = lambda pattern, x: pattern[:2*x] if x < (len(pattern))/2 else pattern[len(pattern)-2*(len(pattern)-x):]

# Compute which coord can be changed to make two rows the same
nearly_same_coords = lambda pattern: {(coord[x],diff) for x in [0,1] for coord, diff in nearly_same(pattern).items()}

# Get these potential coordinates to change
horiz_coords = [nearly_same_coords(pattern) for pattern in patterns]
vert_coords = [{coord[::-1] for coord in nearly_same_coords(pattern)} for pattern in patterns_transposed]

# Create functions to produce alternative slices
swap_symbol = lambda symbol: '#' if symbol == '.' else '.'
altered_pattern = lambda pattern, coord: [pattern[i] if i != coord[0] else pattern[i][:coord[1]] + swap_symbol(pattern[i]) + pattern[i][coord[1]+1:] for i in range(len(pattern))]

# Create a list of alternative slices
new_patterns_horiz = {k:{coord:altered_pattern(patterns[k],coord) for coord in horiz_coords[k]} for k in range(len(patterns))}
new_patterns_vert = {k:{coord:altered_pattern(patterns_transposed[k],coord[::-1]) for coord in vert_coords[k]} for k in range(len(patterns))}

# Slice patterns into lists of the rows / columns considered if the mirror is at point n
slices = lambda pattern: {x:(pattern[:2*x] if x < (len(pattern))/2 else pattern[len(pattern)-2*(len(pattern)-x):]) for x in range(1,len(pattern))}

new_slices_horiz = {k:{coord: slices(new_pattern) for coord, new_pattern in pattern_set.items()} for k,pattern_set in new_patterns_horiz.items()}
new_slices_vert = {k:{coord: slices(new_pattern) for coord, new_pattern in pattern_set.items()} for k,pattern_set in new_patterns_vert.items()}

# Check where the mirror line is
mirrored_slices = lambda slices: [n for n,slice in slices.items() if list(reversed(slice)) == slice]

mirrored_horiz = {k:{key:val for key,val in {coord: mirrored_slices(slice_dict) for coord, slice_dict in pattern_dict.items()}.items() if val != []} for k, pattern_dict in new_slices_horiz.items()}
mirrored_vert = {k:{key:val for key,val in {coord: mirrored_slices(slice_dict) for coord, slice_dict in pattern_dict.items()}.items() if val != []} for k, pattern_dict in new_slices_vert.items()}

# Find conventional mirror_lines
# Use above functions and constructs to find vertical mirror lines
horizontal_reflection = {k:set(mirrored_slices(slices(patterns[k]))) for k in range(len(patterns))}

# Use above functions and constructs to find horizontal mirror lines
vertical_reflection = {k:set(mirrored_slices(slices(patterns_transposed[k]))) for k in range(len(patterns_transposed))}

# Filter mirrror lines to check they make sense with the given coordinates
filtered_mirrored_horiz = {k:{key:val for key,val in {coord:[mirror_line for mirror_line in mirror_lines if mirror_line not in horizontal_reflection[k] and  ((coord[0] < 2*mirror_line and mirror_line <= (len(patterns[k]))/2) or (coord[0] > mirror_line*2 - len(patterns[k])-1 and mirror_line > (len(patterns[k]))/2))] for coord,mirror_lines in mirror_lines_dict.items()}.items() if val != []} for k, mirror_lines_dict in mirrored_horiz.items()}
filtered_mirrored_vert = {k:{key:val for key,val in {coord:[mirror_line for mirror_line in mirror_lines if mirror_line not in vertical_reflection[k] and ((coord[1] < 2*mirror_line and mirror_line <= (len(patterns_transposed[k])-1)/2) or (coord[1] > mirror_line*2 - len(patterns_transposed[k])-1 and mirror_line > (len(patterns_transposed[k]))/2))] for coord,mirror_lines in mirror_lines_dict.items()}.items() if val != []} for k, mirror_lines_dict in mirrored_vert.items()}

# Get list of coordinates
points = {n: set(filtered_mirrored_horiz[n].keys()) if set(filtered_mirrored_vert[n].keys()) == set() else set(filtered_mirrored_vert[n].keys()) if set(filtered_mirrored_horiz[n].keys()) == set() else set.intersection(set(filtered_mirrored_horiz[n].keys()),set(filtered_mirrored_vert[n].keys())) for n in range(len(patterns))}
mirror_lines = {n:(set([mirror for point in points[n] if (filtered_mirrored_horiz.get(n)).get(point) is not None for mirror in (filtered_mirrored_horiz.get(n)).get(point)]),set([mirror for point in points[n] if (filtered_mirrored_vert.get(n)).get(point) is not None for mirror in (filtered_mirrored_vert.get(n)).get(point)])) for n in range(len(patterns))}

horiz_lines = [max(mirror_lines[k][0]) if mirror_lines[k][0] != set() else 0 for k in range(len(patterns))]
vert_lines = [max(mirror_lines[k][1]) if mirror_lines[k][1] != set() else 0 for k in range(len(patterns))]

# Finally, summarise result into integer as described
result = sum(horiz_lines)* 100 + sum(vert_lines)

print(result)