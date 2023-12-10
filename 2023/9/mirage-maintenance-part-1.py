import os

# Define current file location
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + "\\"

# Declare path of input file
input_path = __location__ + "input.txt"

input_strings = []

# Read each line in as a separate list item
with open(input_path) as input_file:
    input_strings = input_file.read().splitlines()

# Parse each line a list of integers delimited by spaces
histories_of_values = [list(map(int,input_string.split(' '))) for input_string in input_strings]

# Get sequence of differences between values in list
differences = lambda history: [history[n+1]-history[n] for n,value in enumerate(history) if n < len(history)-1]

# Get list of lists of differences until every element in list is 0
recursive_diffs = lambda history: [history] + recursive_diffs(differences(history)) if history.count(0) != len(history) else [history]

# Get list of lists of differences for all histories
history_diffs = [recursive_diffs(history) for history in histories_of_values]

# Extrapolate each list to the next value
# Firstly add 0 to the end of each list of 0s
extrapolated_sublists = [[diff_list if n < len(history_sublist)-1 else diff_list + [0] for n,diff_list in enumerate(history_sublist)] for history_sublist in history_diffs]

# Create function to take two sublists and extrapolate one
extrapolate_sublist_pair = lambda original_list,extrapolated_diffs: original_list + [original_list[-1] + extrapolated_diffs[-1]]

# Recursively apply this function to the list of diffs. We do not get the final list of 0s, but for this example this does not matter
extrapolate_sublist = lambda history_sublist: extrapolate_sublist(history_sublist[:-2]+[extrapolate_sublist_pair(history_sublist[-2],history_sublist[-1])]) + [extrapolate_sublist_pair(history_sublist[-2],history_sublist[-1])] if len(history_sublist) != 1 else []

# Apply this function to all of the lists
extrapolated_sublists = [extrapolate_sublist(history_sublist) for history_sublist in extrapolated_sublists]

# We need the extrapolated value for the original list
extrapolated_values = [history_sublist[0][-1] for history_sublist in extrapolated_sublists]

# Finally sum these to obtain results
extrapolated_value_sum = sum(extrapolated_values)

print(extrapolated_value_sum)