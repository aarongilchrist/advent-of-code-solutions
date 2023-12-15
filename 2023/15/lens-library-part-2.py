import os

# Define current file location
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + "\\"

# Declare path of input file
input_path = __location__ + "input.txt"

input_strings = []

# Read each line in as a separate list item
with open(input_path) as input_file:
    input_strings = input_file.read().splitlines()

# Delimit by ','
initialisation_seq = input_strings[0].split(',')

# Hash algorithm
hash_string = lambda hash_str: (hash_string(hash_str[:-1]) + ord(hash_str[-1]))*17 % 256 if len(hash_str) > 1 else ord(hash_str[-1])*17 % 256

# Set up boxes
boxes = [[] for i in range(256)]
for str in initialisation_seq:
    operation = ''
    hashmap_item = ''
    focal_length = 0
    if '=' in str:
        operation = '='
        hashmap_item = str[:str.index('=')]
        focal_length = int(str[str.index('=')+1:])
        box_num = hash_string(hashmap_item)
        if hashmap_item in dict(boxes[box_num]).keys():
            # Replace focusing length if box already there
            boxes[box_num][(boxes[box_num]).index((hashmap_item,dict(boxes[box_num])[hashmap_item]))] = (hashmap_item,focal_length)
        else:
            # Add new lens if not already there
            boxes[box_num].append((hashmap_item,focal_length))
    elif '-' in str:
        operation = '-'
        hashmap_item = str[:-1]
        box_num = hash_string(hashmap_item)
        # Remove lens if already there
        if hashmap_item in dict(boxes[box_num]).keys():
            boxes[box_num].remove((hashmap_item,dict(boxes[box_num])[hashmap_item]))

result = 0
# Calculate focusing power
for x,box in enumerate(boxes):
    for y,lens in enumerate(box):
        result += (x+1)*(y+1)*lens[1]

print(result)