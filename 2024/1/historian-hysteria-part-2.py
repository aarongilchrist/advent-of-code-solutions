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

pairs = [[int(num) for num in input_string.split()]
         for input_string in input_strings]

lists = list(zip(*pairs))

similarity_factors = {x: len([y for y in lists[1] if y == x])
                      for x in set(lists[1])}

similarity_scores = [x * similarity_factors[x]
                     if x in similarity_factors else 0 for x in lists[0]]

similarity_score = sum(similarity_scores)

print(similarity_score)
