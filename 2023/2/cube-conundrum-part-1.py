import os

# Define current file location
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + "\\"

# Declare path of input file
input_path = __location__ + "input.txt"

input_strings = []

# Read each line in as a separate list item
with open(input_path) as input_file:
    input_strings = input_file.read().splitlines()

# Declare valid cube colours
cube_colours = ['red','green','blue']

# Remove non digits from string and return as int
digits_to_int = lambda input_string: int(''.join(c for c in input_string if c.isdigit()))

# Get game number
game_number = lambda input_string: digits_to_int(input_string.split(':')[0])

# Remove "Game x:" from beginning of each line
remove_title = lambda input_string: input_string[input_string.find(":")+1:]

# Separate game string by semicolons into sets of cubes after removing title
delimit_game = lambda input_string: remove_title(input_string).split(';')

# Separate set of cubes by commas
delimit_set = lambda input_string: input_string.split(',')

# Match colour of set of cubes
# First get location of colour names in the string
colour_strings_location = lambda input_string: [input_string.find(colour) for colour in cube_colours]
# Get the colour present (only valid if just one colour in string)
cube_colour = lambda input_string: cube_colours[colour_strings_location(input_string).index(max(colour_strings_location(input_string)))]

# Convert a set of cubes into a dict
parse_cube_set = lambda input_string: {cube_colour(cubes): digits_to_int(cubes) for cubes in delimit_set(input_string)}

# Convert games into list of list of dicts
parse_games = lambda input_string: {cube_set[0]: list(map(parse_cube_set,cube_set[1])) for cube_set in {game_number(game): delimit_game(game) for game in input_string}.items()}

# Get maximum number of cubes of a colour in a game, treating empty keys as 0
max_colour = lambda colour_list_dicts,colour: max(item.get(colour) or 0 for item in colour_list_dicts)

# Reduce list of dicts into dict of max
max_colour_dict = lambda colour_list_dicts: {colour: max_colour(colour_list_dicts,colour) for colour in cube_colours}

# Get max cubes for each game
max_colour_games = {game[0]: max_colour_dict(game[1]) for game in parse_games(input_strings).items()}

# Return game ids where there are <= 12 red cubes, 13 green cubes, and 14 blue cubes.
valid_games = [game[0] for game in max_colour_games.items() if game[1]['red'] <= 12 and game[1]['green'] <= 13 and game[1]['blue'] <= 14]

print(sum(valid_games))