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

# Split strings by mul( and ) [removing the characters] and delimit by ,
split_strings = [
    subsegment.split(",")
    for input_string in input_strings
    for segment in input_string.split("mul(")
    for subsegment in segment.split(")")
]

# Remove list items that are not sets of two integers
filtered_strings = [
    [int(digit) for digit in split_string]
    for split_string in split_strings
    if len(split_string) == 2
    and all(substr.isdigit() for substr in split_string)
]

# Compute instructions
sum_of_muls = sum(instr[0]*instr[1] for instr in filtered_strings)

print(sum_of_muls)
