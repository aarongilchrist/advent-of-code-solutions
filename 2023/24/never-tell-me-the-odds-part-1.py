import os

# Define current file location
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + "\\"

# Declare path of input file
input_path = __location__ + "input.txt"

input_strings = []

# Read each line in as a separate list item
with open(input_path) as input_file:
    input_strings = input_file.read().splitlines()

# Parse hailstones as (position,velocity)
hailstones = [tuple([tuple([int(num) for num in coord.split(',')]) for coord in input_string.split('@')]) for input_string in input_strings]

# First we get directions by considering vel_y / vel_x
xy_directions = [hailstone[1][1]/hailstone[1][0] for hailstone in hailstones]

# Set out test zone
lower_bound = 200000000000000
upper_bound = 400000000000000

# Count intersections
valid_intersections = 0

# Compare hailstones and look for intersections
for m, hailstone in enumerate(hailstones):
    # Iterate over all pairs of hailstones efficiently
    for n, other_hailstone in enumerate(hailstones[:m]):
        # Remove parallel directions
        if xy_directions[n] == xy_directions[m]:
            continue
        # Get x intersection
        x = ((other_hailstone[0][1] - xy_directions[n]*other_hailstone[0][0]) - (hailstone[0][1] - xy_directions[m]*hailstone[0][0]))/(xy_directions[m]-xy_directions[n])
        # Get y intersection
        y = xy_directions[m]*(x - hailstone[0][0]) + hailstone[0][1]
        # Check that time of intersection in future is at a positive time
        t1 = (x-hailstone[0][0])/hailstone[1][0]
        t2 = (x-other_hailstone[0][0])/other_hailstone[1][0]
        if t1 < 0 or t2 < 0:
            continue
        # Finally check that intersection is in the valid range
        if x >= lower_bound and x <= upper_bound and y >= lower_bound and y <= upper_bound:
            valid_intersections +=1

# Basic mathematics used above
#y - y1 = m(x-x1)
#y = mx - mx1 + y1
#y - y2 = n(x-x2)
#y = nx - nx2 + y2
# mx - mx1 + y1 = nx - nx2 + y2
# (m-n)x = y2 - nx2 - y1 + mx1

#for hailstone in hailstones:
#    print(hailstone)

#print(xy_directions)

print(valid_intersections)