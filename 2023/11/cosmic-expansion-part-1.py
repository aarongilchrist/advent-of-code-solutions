import os

# Define current file location
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + "\\"

# Declare path of input file
input_path = __location__ + "input.txt"

input_strings = []

# Read each line in as a separate list item
with open(input_path) as input_file:
    input_strings = input_file.read().splitlines()

# Record dimensions
image_width = len(input_strings[0])
image_height = len(input_strings)

# Turn input into matrix
image = [list(input_string) for input_string in input_strings]

# Create function to translate between working in rows and columns
transpose_matrix = lambda matrix: [[matrix[y][x] for y in range(len(matrix))] for x in range(len(matrix[0]))]

# Transpose image so we can ascertain empty columns
image_transposed = transpose_matrix(image)

# Record indices of empty rows and columns
empty_rows = [n for n,row in enumerate(image) if '#' not in row]
empty_cols = [n for n,col in enumerate(image_transposed) if '#' not in col]

# Add empty columns adjacent to empty columns. We work backwards so indices of empty columns do not change
for n in reversed(empty_cols):
    image_transposed.insert(n,['.' for x in range(image_height)])
    image_width += 1

image = transpose_matrix(image_transposed)

# Add empty rows adjacent to empty rows. We work backwards so indices of empty rows do not change
for n in reversed(empty_rows):
    image.insert(n,['.' for x in range(image_width)])
    image_height += 1

# Ensure that the transposed version is updated
image_transposed = transpose_matrix(image)

# Count number of galaxies
number_of_galaxies = sum([row.count('#') for row in image])

# Number galaxies and record locations in dict
galaxies_numbered = 0
curr_row = 0
galaxy_dict = {}
while galaxies_numbered < number_of_galaxies:
    for n in range(image[curr_row].count("#")):
        galaxies_numbered += 1
        galaxy_dict[galaxies_numbered] = (curr_row,image[curr_row].index("#"))
        image[curr_row][image[curr_row].index("#")] = str(galaxies_numbered)
    curr_row += 1

# Given n galaxies, there are 1/2 (n-1)n pairs. We create list of pairs
pairs = [(x,y) for x in range(1,number_of_galaxies+1) for y in range(1,number_of_galaxies+1) if y>x]

# Distance between pairs is sum of absolute value of differences between component coordinates
coord_distance = lambda coord_1, coord_2: abs(coord_1[0]-coord_2[0]) + abs(coord_1[1]-coord_2[1])

# Get shortest distance between all pairs
shortest_distance = [coord_distance(galaxy_dict[pair[0]],galaxy_dict[pair[1]]) for pair in pairs]

# Sum lengths
sum_of_distances = sum(shortest_distance)

print(sum_of_distances)

# Print out image for debugging purposes
#for row in image:
    #print(row)