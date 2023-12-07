import os
import math

# Define current file location
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + "\\"

# Declare path of input file
input_path = __location__ + "input.txt"

input_strings = []

# Read each line in as a separate list item
with open(input_path) as input_file:
    input_strings = input_file.read().splitlines()

# Remove non digits from string and parse as int
digits_as_int = lambda input_string: int("".join(character for character in input_string if character.isdigit()))

# Parse time and distance
time = digits_as_int(input_strings[0])
distance = digits_as_int(input_strings[1])

# Get list of scenario speeds
speeds = list(range(0,time))

# Calculate distance travelled
distances_travelled = [speed*(time-speed) for speed in speeds]

# Obtain wins
wins = [speed for n,speed in enumerate(speeds) if distances_travelled[n] > distance]

# Count number of ways to win
ways_to_win = len(wins)

print(ways_to_win)