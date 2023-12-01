import os

# Define current file location
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + "\\"

# Declare path of input file
input_path = __location__ + "input.txt"

calibration_strings = []

# Read each line in as a separate list item
with open(input_path) as input_file:
    calibration_strings = input_file.readlines()

# Define a function to strip non digits from strings
remove_non_digits = lambda full_str : ''.join(c for c in full_str if c.isdigit())

# Remove non digits from all strings
calibration_digits = [remove_non_digits(input_str) for input_str in calibration_strings]

# Define a function to concatenate the first and last digits of a string, and return as an integer
get_calibration_value = lambda int_str: int(int_str[0]+int_str[-1])

# Convert filtered strings to integers in the way described above and sum the result
sum_of_calibration_values = sum([get_calibration_value(filtered_str) for filtered_str in calibration_digits])

print(sum_of_calibration_values)