import os

# Define current file location
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + "\\"

# Declare path of input file
input_path = __location__ + "input.txt"

input_strings = []

# Read each line in as a separate list item
with open(input_path) as input_file:
    input_strings = input_file.read().splitlines()

module_name = lambda module_declaration: module_declaration[1:module_declaration.index('->')-1] if module_declaration[0] in ['%','&'] else module_declaration[:module_declaration.index('->')-1]

module_type = lambda module_declaration: module_declaration[0] if module_declaration[0] in ['%','&'] else 'b'

module_outputs = lambda module_declaration: module_declaration[module_declaration.index('->')+3:].replace(' ','').split(',')

# Set up dict of modules in form {name: (type,outputs,current_state)} for flip flop modules and {name: (type,outputs,inputs)} for conjunction_modules
modules = {module_name(input_string):(module_type(input_string),module_outputs(input_string), 0 if module_type(input_string) == '%' else []) for input_string in input_strings}

for name,module in modules.items():
    if module[0] == '&':
        inputs = {}
        for other_name,other_module in modules.items():
            if name in other_module[1]:
                inputs.update({other_name:0})
        modules.update({name:[module[0],module[1],inputs]})

module_states = lambda module_dict: [module_tuple[2] for module_tuple in module_dict.values() if module_tuple[0] in ['%','&']]

original_states = module_states(modules)

high_pulses = 0
low_pulses = 0

def button_press():
    global low_pulses
    global high_pulses
    
    # Source, dest, high / low
    process_queue = []
    
    # Button to broadcaster
    low_pulses += 1
    
    for output in modules['broadcaster'][1]:
        process_queue.append(('broadcaster',output,'low'))
    
    while len(process_queue) > 0:
        for x in range(len(process_queue)):
            # Remove process from queue after getting the name
            curr_process = process_queue[0]
            process_queue = process_queue[1:]
            #print(curr_process)
            # Iterate the count of pulses
            if curr_process[2] == 'high':
                high_pulses += 1
            elif curr_process[2] == 'low':
                low_pulses += 1
            
            # Process the current queue item
            if curr_process[1] in modules.keys():
                dest_module = modules[curr_process[1]]
                if dest_module[0] == '%':
                    if curr_process[2] == 'low':
                        if dest_module[2] == 0:
                            modules.update({curr_process[1]: (dest_module[0],dest_module[1],1)})
                            for output in dest_module[1]:
                                process_queue.append((curr_process[1],output,'high'))
                        elif dest_module[2] == 1:
                            modules.update({curr_process[1]: (dest_module[0],dest_module[1],0)})
                            for output in dest_module[1]:
                                process_queue.append((curr_process[1],output,'low'))
                    elif curr_process[2] == 'high':
                        pass
                elif dest_module[0] == '&':
                    inputs = dest_module[2]
                    if curr_process[2] == 'low':
                        inputs.update({curr_process[0]:0})
                    elif curr_process[2] == 'high':
                        inputs.update({curr_process[0]:1})
                    modules.update({curr_process[1]: (dest_module[0],dest_module[1],inputs)})
                    if sum(inputs.values()) == len(inputs.values()):
                        for output in dest_module[1]:
                            process_queue.append((curr_process[1],output,'low'))
                    else:
                        for output in dest_module[1]:
                            process_queue.append((curr_process[1],output,'high'))

button_presses = 0
button_press()
button_presses += 1

while button_presses < 1000:
    button_press()
    button_presses += 1
    #print(button_presses)

print(low_pulses*high_pulses)