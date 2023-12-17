import os

# Define current file location
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + "\\"

# Declare path of input file
input_path = __location__ + "input.txt"

input_strings = []

# Read each line in as a separate list item
with open(input_path) as input_file:
    input_strings = input_file.read().splitlines()

# Get columns
columns = [[input_string[x] for input_string in input_strings] for x in range(len(input_strings[0]))]

# Move forwards Os to front of list slice
move_forwards = lambda column_slice: ['O']*column_slice[:column_slice.index('#')].count('O') + ['.']*(column_slice.index('#')-column_slice[:column_slice.index('#')].count('O')) + column_slice[column_slice.index('#'):] if '#' in column_slice else ['O']*column_slice.count('O') + ['.']*(len(column_slice) - column_slice.count('O'))

# Tilt northwards, i.e. move forwards if the first element of the column is not # else move to the next character
tilt_northwards = lambda column: column if len(column) == 1 else move_forwards(column) if '#' not in column else move_forwards(column)[:column.index('#')] + tilt_northwards(column[column.index('#'):]) if column[0] != '#' else [column[0]] + tilt_northwards(column[1:])
tilt_all_northwards = lambda columns: [tilt_northwards(column) for column in columns]

# Rotate platform
rotate = lambda columns: [[columns[y][len(columns)-x-1] for y in range(len(columns[0]))] for x in range(len(columns))]

# Cycle through until columns no longer change
cycled_columns = columns #tilt_all_northwards(rotate(tilt_all_northwards(rotate(tilt_all_northwards(rotate(tilt_all_northwards(rotate(columns))))))))
prev_cycles = []
n = 0
while cycled_columns not in prev_cycles:
    prev_cycles.append(cycled_columns)
    cycled_columns = rotate(tilt_all_northwards(rotate(tilt_all_northwards(rotate(tilt_all_northwards(rotate(tilt_all_northwards(cycled_columns))))))))
    n += 1

# It takes n cycles to get back to an earlier case
earlier_case_no = prev_cycles.index(cycled_columns)
# We calculate how many cycles will get us to the same state as 1000000000 using the Euclidean algorithm
cycles_required = (1000000000-earlier_case_no) % (n-earlier_case_no)

for k in range(cycles_required):
    cycled_columns = rotate(tilt_all_northwards(rotate(tilt_all_northwards(rotate(tilt_all_northwards(rotate(tilt_all_northwards(cycled_columns))))))))

# Count number of rounded rocks by row
number_by_row = [sum([1 for column in cycled_columns if column[x] == 'O']) for x in range(len(cycled_columns[0]))]

#n=0
# Print out columns for debugging
#for x in range(len(prev_cycles[n][0])):
#    print(''.join([prev_cycles[n][y][x] for y in range(len(prev_cycles[n]))]))

# Sum load
load = sum([(len(number_by_row)-x)*number_by_row[x] for x in range(len(number_by_row))])

print(load)