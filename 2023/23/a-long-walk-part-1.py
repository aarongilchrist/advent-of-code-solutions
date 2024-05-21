import os
import networkx as nx

# Define current file location
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + "\\"

# Declare path of input file
input_path = __location__ + "input.txt"

input_strings = []

# Read each line in as a separate list item
with open(input_path) as input_file:
    input_strings = input_file.read().splitlines()

island = [list(input_string) for input_string in input_strings]

get_tile = lambda coord: island[coord[1]][coord[0]]

nodes = [(x,y) for x in range(len(island[0])) for y in range(len(island)) if get_tile((x,y)) != '#']

offset_directions = lambda node: [(-1,0),(1,0),(0,-1),(0,1)] if get_tile(node) == '.' else [(-1,0)] if get_tile(node) == '<' else [(1,0)] if get_tile(node) == '>' else [(0,1)] if get_tile(node) == 'v' else [(0,-1)] if get_tile(node) == '^' else [(0,0)]

directed_node_pairs = [(node,(node[0]+offset[0],node[1]+offset[1])) for node in nodes for offset in offset_directions(node)
                          if node[0]+offset[0] in range(len(island[0])) and node[1]+offset[1] in range(len(island))
                          and get_tile((node[0]+offset[0],node[1]+offset[1])) != '#']

island_graph = nx.DiGraph(directed_node_pairs)

starting_node = (island[0].index('.'),0)
finishing_node = (island[-1].index('.'),len(island)-1)

path_lengths = [len(path) for path in nx.all_simple_paths(island_graph,starting_node,finishing_node)]

# Take 1 from max path lengths as we are counting number of steps
max_num_steps = max(path_lengths) -1

print(max_num_steps)