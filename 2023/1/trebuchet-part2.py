import os

# Define current file location
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + "\\"

# Declare path of input file
input_path = __location__ + "input.txt"

# Declare valid "digits" as dictionary corresponding to value represented
digit_strings = {
    '0': '0',
    '1': '1', 'one'   : '1',
    '2': '2', 'two'   : '2',
    '3': '3', 'three' : '3',
    '4': '4', 'four'  : '4',
    '5': '5', 'five'  : '5',
    '6': '6', 'six'   : '6',
    '7': '7', 'seven' : '7',
    '8': '8', 'eight' : '8',
    '9': '9', 'nine'  : '9',
}

calibration_strings = []

# Read each line in as a separate list item
with open(input_path) as input_file:
    calibration_strings = input_file.readlines()

# Function returning dict of the first instance of each substr in a full_str (-1 if not found)
positions_of_substrs = lambda full_string, substrs: {substr: full_string.find(substr) for substr in substrs}

# Returns string digit key corresponding to first substr found (lowest key such that value >= -1)
first_substr_found = lambda positions_dict: min({key: value for (key, value) in positions_dict.items() if value != -1},key=positions_dict.get)

# First digit found in a string
first_digit_found = lambda full_string: digit_strings[first_substr_found(positions_of_substrs(full_string,digit_strings))]

# Reverses dictionary keys
reversed_dict_keys = lambda dict: {key[::-1]: value for (key, value) in dict.items()}

# Last digit found in a string (by matching reversed digit with reversed digit strings dict)
last_digit_found = lambda full_string: reversed_dict_keys(digit_strings)[first_substr_found(positions_of_substrs(full_string[::-1],reversed_dict_keys(digit_strings)))]

# Concatenates result of first and last digit for a given string
calibration_value_string = lambda full_string: first_digit_found(full_string) + last_digit_found(full_string)

# Define a function to concatenate the frst and last digits of a string, and return as an integer
get_calibration_value = lambda int_str: int(int_str[0]+int_str[-1])

# Convert calibration value strings to integers in the way described above and sum the result
sum_of_calibration_values = sum([get_calibration_value(calibration_value_string(calibration_str)) for calibration_str in calibration_strings])

print(sum_of_calibration_values)