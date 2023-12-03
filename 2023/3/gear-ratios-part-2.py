import os
import itertools

# Define current file location
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + "\\"

# Declare path of input file
input_path = __location__ + "input.txt"

input_strings = []

# Read each line in as a separate list item
with open(input_path) as input_file:
    input_strings = input_file.read().splitlines()

# Turn characters into a tuple of tuples
char_matrix = tuple([tuple(input_line) for input_line in input_strings])

# Get location of symbols (non digit / "." characters) in matrix
symbol_indices = [(row[0],rowitem[0]) for row in enumerate(char_matrix) for rowitem in enumerate(row[1]) if not rowitem[1].isdigit() and rowitem[1] != '.']

# Get indices of adjacents to symbols as tuple (symbol_index,{symbol_adjacent_indices})
symbol_and_adjacents = [(index,set([(index[0] + adjacent_relative_index[0],index[1] + adjacent_relative_index[1])
                        for adjacent_relative_index in [(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1)]]))
                        for index in symbol_indices]

# Get position of all digits in matrix
digit_indices = [(row[0],rowitem[0]) for row in enumerate(char_matrix) for rowitem in enumerate(row[1]) if rowitem[1].isdigit()]

# Group indices of digits into sets of adjacents by row
digit_adjacents_by_row = [[item[1] for item in group] for key,group in itertools.groupby(enumerate(digit_indices),lambda x: (x[1][0],x[0]-x[1][1]))]

# Remove lists of adjacent integers, if not adjacent to a symbol
#part_number_indices = [index_list for index_list in digit_adjacents_by_row if set(index_list).intersection(symbol_adjacents) != set()]

#Get integer represented by list of indices from character matrix
get_integer_from_indices = lambda index_list: int(''.join(char_matrix[index[0]][index[1]] for index in index_list))

# Get indices of numbers as tuple (number_as_int,{number_indices})
potential_part_numbers = [(get_integer_from_indices(index_list),set(index_list)) for index_list in digit_adjacents_by_row]

# Get list of lists of integers joined by a symbol
adjacent_integers = [[part_number[0] for part_number in potential_part_numbers if part_number[1].intersection(symbol[1]) != set()]
                     for symbol in symbol_and_adjacents]

# Multiply together part numbers if there are exactly two adjacent to a symbol
gear_ratios = [part_number_set[0] * part_number_set[1] for part_number_set in adjacent_integers if len(part_number_set) == 2]

print(sum(gear_ratios))