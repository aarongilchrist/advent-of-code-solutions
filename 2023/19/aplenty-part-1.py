import os

# This uses eval, so check the input before running

# Define current file location
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + "\\"

# Declare path of input file
input_path = __location__ + "input.txt"

input_strings = []

# Read each line in as a separate list item
with open(input_path) as input_file:
    input_strings = input_file.read().splitlines()

# Split workflows from part ratings
workflows = input_strings[:input_strings.index('')]
part_ratings = input_strings[input_strings.index('')+1:]

# Create dict of workflows
workflow_dict = {workflow[:workflow.index('{')]:[(condition[:condition.index(':')],condition[condition.index(':')+1:]) if condition.count(':') != 0 else ('1==1',condition) for condition in workflow[workflow.index('{')+1:workflow.index('}')].split(',')] for workflow in workflows}

# Create list of expressions to evaluate
parsed_part_ratings = [{entry[0]:int(entry[2:]) for entry in part_rating[1:-1].split(',')} for part_rating in part_ratings]

# List accepted ratings
ratings = []

# Evaluate statements in workflows
evaluate_workflow = lambda curr_node: [condition[1] for condition in workflow_dict[curr_node] if eval(condition[0])][0]

# Follow workflows to A or R
follow_workflows = lambda curr_node: curr_node if curr_node in ['A','R'] else follow_workflows(evaluate_workflow(curr_node))

# Follow workflows for all part ratings
for part_rating in parsed_part_ratings:
    x = part_rating['x']
    m = part_rating['m']
    a = part_rating['a']
    s = part_rating['s']
    if follow_workflows('in') == 'A':
        ratings.append(x + m + a + s)
    
# Sum accepted workflows:
sum_rating_numbers = sum(ratings)

print(sum_rating_numbers)