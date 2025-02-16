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

reports = [[int(num) for num in input_string.split()]
           for input_string in input_strings]

level_diffs = [[report[i+1] - report[i]
                for i in range(0, len(report)-1)] for report in reports]


def all_same_polarity(int_list): return True if sum(
    [1 if x > 0 else 0 for x in int_list]) in (0, len(int_list)) else False


safe_reports = [1 if set(diff).issubset(
    {-3, -2, -1, 1, 2, 3}) and all_same_polarity(diff) else 0 for diff in level_diffs]

number_safe = sum(safe_reports)

print(number_safe)
