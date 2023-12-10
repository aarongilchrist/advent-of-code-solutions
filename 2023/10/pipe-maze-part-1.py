import os

# Define current file location
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + "\\"

# Declare path of input file
input_path = __location__ + "input.txt"

input_strings = []

# Read each line in as a separate list item
with open(input_path) as input_file:
    input_strings = input_file.read().splitlines()

# We parse the input as a grid of tiles
tile_grid = [list(input_string) for input_string in input_strings]

# Get dimensions of tile_grid
grid_cols = len(tile_grid[0])
grid_rows = len(tile_grid)

# We plan on treating 2 element tuples as coordinates, so create function to add componentwise
add_componentwise = lambda first,second: tuple([sum(sublist) for sublist in zip(first,second)])

# Create function to easily return tile grid elt from tuple
grid_elt = lambda coord_tuple: tile_grid[coord_tuple[1]][coord_tuple[0]]

# Find starting position. We choose the first element we find as there is only one S
s_position = [(x,y) for y, row in enumerate(tile_grid) for x, column in enumerate(row) if tile_grid[y][x] == 'S'][0]

# Determine which directions we can go from the starting position and create sublist for each valid route
routes = [[s_position, start_location] for start_location in [add_componentwise(s_position,direction) for direction in [(1,0),(0,1),(-1,0),(0,-1)]]
          if start_location[0] >= 0 and start_location[1] >= 0 and start_location[0] < grid_rows and start_location[1] < grid_cols
          and grid_elt(start_location) != '.']

# Get next list item by considering current and last tile
# Work out input direction 
in_direction = lambda last_tile, current_tile: add_componentwise(current_tile, (-last_tile[0],-last_tile[1]))

# Create mapping between directions and inputs
tile_mapping = {'|': lambda in_direction: (0,-1) if in_direction == (0,-1) else (0,1) if in_direction == (0,1) else 'invalid',
                '-': lambda in_direction: (1,0) if in_direction == (1,0) else (-1,0) if in_direction == (-1,0) else 'invalid',
                'L': lambda in_direction: (1,0) if in_direction == (0,1) else (0,-1) if in_direction == (-1,0) else 'invalid',
                'J': lambda in_direction: (-1,0) if in_direction == (0,1) else (0,-1) if in_direction == (1,0) else 'invalid',
                '7': lambda in_direction: (0,1) if in_direction == (1,0) else (-1,0) if in_direction == (0,-1) else 'invalid',
                'F': lambda in_direction: (0,1) if in_direction == (-1,0) else (1,0) if in_direction == (0,-1) else 'invalid',
                '.': lambda in_direction: 'invalid',
                'S': lambda in_direction: (0,0)}

# Find next tile. We make sure to map to the S if the next direction is (0,0) to prevent an infinite loop
next_tile = lambda route: add_componentwise(route[-1], tile_mapping[grid_elt(route[-1])](in_direction(route[-2],route[-1]))) if tile_mapping[grid_elt(route[-1])](in_direction(route[-2],route[-1])) != 'invalid' else 'terminated'

# Loop through routes until they reach the end
while sum([1 for route in routes if route[-1] == 'terminated' or route[-1] == s_position]) != len(routes):
    routes = [route + [next_tile(route)] for route in routes if route[-1] != 'terminated']

# Get route lengths, the furthest away element is half the length of the longest route away -1. Exclude routes which terminate wrongly
route_lengths = [len(route) for route in routes if route[-1] != 'terminated']
furthest_elt = int(0.5*(max(route_lengths)-1))

print(furthest_elt)