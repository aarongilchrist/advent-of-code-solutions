import os

# Define current file location
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + "\\"

# Declare path of input file
input_path = __location__ + "input.txt"

input_strings = []

# Read each line in as a separate list item
with open(input_path) as input_file:
    input_strings = input_file.read().splitlines()

# Delimit by ','
initialisation_seq = input_strings[0].split(',')

# Hash algorithm
hash_string = lambda hash_str: (hash_string(hash_str[:-1]) + ord(hash_str[-1]))*17 % 256 if len(hash_str) > 1 else ord(hash_str[-1])*17 % 256

# Hash all the strings
hashed_sequence = [hash_string(init_string) for init_string in initialisation_seq]

# Sum hashes
sum_hashes = sum([hashed_str for hashed_str in hashed_sequence])

print(sum_hashes)