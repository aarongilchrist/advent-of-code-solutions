# This method yields 293, not 291 which is the answer. I am unsure why this does not work perfectly.
# Instead of using Pick's theorem, we fill in Os on the outside and follow them through

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
valid_routes = [route for route in routes if route[-1] != 'terminated']

# We obtain the same complete loop forwards and backwards, so it is okay to just work with the first elt of valid_routes
selected_route = valid_routes[0]

# Replace all route elements with an @ and others with I
tile_grid = [['@' if (x,y) in selected_route else 'I' for x in range(len(row))] for y, row in enumerate(tile_grid)]

# Mark all non @ elements on the outside with O
tile_grid = [['O' if grid_elt((x,y)) != "@" and (x in [0,grid_cols-1] or y in [0,grid_rows-1]) else grid_elt((x,y)) for x in range(len(row))] for y, row in enumerate(tile_grid)]

# Now mark one cell to the right of each route item with O
# Loop through route again and select tiles to the left of the direction of motion before the next @
perp_direction = lambda prev_tile,curr_tile: (-1,0) if in_direction(prev_tile,curr_tile) == (0,-1) else (0,-1) if in_direction(prev_tile,curr_tile) == (1,0) else (1,0) if in_direction(prev_tile,curr_tile) == (0,1) else (0,1)
outside_route = [add_componentwise(perp_direction(selected_route[n-1],selected_route[n]),selected_route[n]) for n in range(1,len(selected_route))]
outside_route = [outside_tile for outside_tile in outside_route if outside_tile[0] < grid_rows and outside_tile[1] < grid_cols and grid_elt(outside_tile) != "@"]

# Mark all outside values with O
tile_grid = [['O' if (x,y) in outside_route else grid_elt((x,y)) for x in range(len(row))] for y, row in enumerate(tile_grid)]

# Now loop through all Is and delete them if adjacent to Os
# Select all tiles with I present
selected_tiles = {(x,y) for y in range(grid_rows) for x in range(grid_cols) if grid_elt((x,y)) == "I"}

# Finally remove all Is adjacent to O
# Define function to check if adjacent to O
adjacent_to_O = lambda selected_tile: 0 if 'O' in [grid_elt(adjacent) for adjacent in [add_componentwise(direction,selected_tile) for direction in [(-1,0),(0,1),(1,0),(0,-1)]] if adjacent[0] in range(0,grid_cols) and adjacent[1] in range(0,grid_rows)] else 1 #,(-1,-1),(-1,1),(1,-1),(1,1)

# Loop over selected tiles and replace those next to O with O
deselected_tiles = set()
while sum(list(map(adjacent_to_O,selected_tiles.difference(deselected_tiles)))) != len(selected_tiles.difference(deselected_tiles)):
    for selected_tile in selected_tiles:
        if adjacent_to_O(selected_tile) == 0:
            tile_grid[selected_tile[1]][selected_tile[0]] = 'O'
            deselected_tiles.add(selected_tile)

selected_tiles = selected_tiles.difference(deselected_tiles)

# Print out grid for debugging purposes
for row in tile_grid:
    print(''.join(row))

number_inside = len(selected_tiles)

print(number_inside)