import networkx as nx
import matplotlib.pyplot as plt
import re
import gc

graph_edges = []
graph_nodes = set()
with open('classgraph.txt') as fp:
    line = fp.readline()
    #while(re.search("java.*",line) != None):
    while line:
	    graph_edges.append(line.strip()[2:].split())
	    graph_nodes.add(graph_edges[-1][0])
	    graph_nodes.add(graph_edges[-1][1])
	    line = fp.readline()

callgraph = nx.DiGraph()
callgraph.add_nodes_from(graph_nodes)
callgraph.add_edges_from(graph_edges)
#print(callgraph.nodes())
#print(callgraph.edges())

gc.collect()
pos = nx.spring_layout(callgraph)
nx.draw(callgraph, pos, nodes_size = 100, with_labels = True, font_size=10)

# show graph
plt.savefig('callgraph_library.png')
