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

# Slice patterns into lists of the rows / columns considered if the mirror is at point n
slices = lambda pattern: {x:(pattern[:2*x] if x < (len(pattern))/2 else pattern[len(pattern)-2*(len(pattern)-x):]) for x in range(1,len(pattern))}

# Check where the mirror line is
mirrored_slices = lambda slices: [n for n,slice in slices.items() if list(reversed(slice)) == slice]

# Use above functions and constructs to find vertical mirror lines
horizontal_reflection = [mirrored_slices(slices(pattern)) for pattern in patterns]

# Use above functions and constructs to find horizontal mirror lines
vertical_reflection = [mirrored_slices(slices(pattern)) for pattern in patterns_transposed]

# Finally, summarise result into integer as described
result = sum([sum(mirror) for mirror in vertical_reflection]) + 100 * sum([sum(mirror) for mirror in horizontal_reflection])

print(result)