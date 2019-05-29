import networkx as nx
import matplotlib.pyplot as plt

graph_edges = []
graph_nodes = set()
graph_nodes_dev = set()

with open('devfiles.txt') as fp:
    line = fp.readline()
    while line:
        graph_nodes_dev.add(line.strip()[2:])
        line = fp.readline()

with open('classgraph.txt') as fp:
    line = fp.readline()
    while line:
        graph_edges.append(line.strip()[2:].split())
        graph_nodes.add(graph_edges[-1][0])
        graph_nodes.add(graph_edges[-1][1])

        line = fp.readline()

fp.close()

color_map = []
for item in graph_nodes:
    if item in graph_nodes_dev:
        color_map.append('green')
    else:
        color_map.append('blue')

callgraph = nx.DiGraph()
callgraph.add_nodes_from(graph_nodes)
callgraph.add_edges_from(graph_edges)
#print(callgraph.nodes())
#print(callgraph.edges())
print(graph_nodes_dev)
print(graph_nodes)

pos = nx.shell_layout(callgraph)
nx.draw(callgraph, pos, node_color = color_map, nodes_size = 100, with_labels = True, font_size=10)

# show graph
plt.savefig('callgraph_library.png')
