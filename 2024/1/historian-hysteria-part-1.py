import os

# Define current file location
__location__ = os.path.realpath(os.path.join(
    os.getcwd(), os.path.dirname(__file__))) + "/"

# Declare path of input file
input_path = __location__ + "input.txt"

input_strings = []

# Read each line in as a separate list item
with open(input_path) as input_file:
    input_strings = input_file.read().splitlines()

location_pairs = [[int(num) for num in input_string.split()]
                  for input_string in input_strings]

location_lists = list(zip(*location_pairs))

location_lists_sorted = [sorted(loc_list) for loc_list in location_lists]

pairs = list(zip(*location_lists_sorted))

distances = [abs(pair[1]-pair[0]) for pair in pairs]

total_distance = sum(distances)

print(total_distance)
