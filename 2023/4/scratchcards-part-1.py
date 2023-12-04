import os

# Define current file location
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + "\\"

# Declare path of input file
input_path = __location__ + "input.txt"

input_strings = []

# Read each line in as a separate list item
with open(input_path) as input_file:
    input_strings = input_file.read().splitlines()
    
# Split card string into (winning numbers,selected numbers)
parse_game = lambda input_string: (input_string[input_string.find(':')+1:input_string.find('|')],input_string[input_string.find('|')+1:])

# Transform string of integers delimited by spaces into set of integers
string_to_int_set = lambda input_string: set([int(number) for number in input_string.split(' ') if number not in ['',' ']])

# Get winning numbers for card
winners = lambda input_string: set.intersection(*list(map(string_to_int_set,parse_game(input_string))))

# Count winners per card
card_winners = list(map(len,list(map(winners,input_strings))))

# Sum up score
final_score = sum(2**(num-1) for num in card_winners if num > 0)

print(final_score)