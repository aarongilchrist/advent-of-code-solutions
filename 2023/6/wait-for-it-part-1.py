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

# Parse numbers from line
input_numbers = lambda input_string: [int(value) for value in input_string.split(" ") if value.isdigit()]

# Parse times and distances
times = input_numbers(input_strings[0])
distances = input_numbers(input_strings[1])

# Get each race as a tuple
races = list(zip(times,distances))

# Get scenarios speeds where button is held down
scenario_speeds = [list(range(time)) for time in times]

# Calculate time to complete the race at scenario speed
scenario_distances = [[(times[n]-speed)*speed  for speed in scenario] for n, scenario in enumerate(scenario_speeds)]

# Calculate number of wins
wins = [[scenario_speeds[x][y] for y, distance in enumerate(scenario) if distance > distances[x]] for x, scenario in enumerate(scenario_distances)]

# Numbers of ways to win
ways_to_win = [len(win_list) for win_list in wins]

# Multiply together number of ways to win
mult_of_ways = math.prod(ways_to_win)

print(mult_of_ways)