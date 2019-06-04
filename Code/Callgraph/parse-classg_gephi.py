import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

columns = ['source','target', 'type', 'weight']
edges_df = pd.DataFrame(columns=columns)

columns = ['label']
nodes_df = pd.DataFrame(columns=columns)
nodes = set()

with open('classgraph.txt') as fp:
    line = fp.readline()
    while line:
        source, target = line.strip()[2:].split()
        edges_df = edges_df.append(pd.Series([source, target, 'directed', 1], index = edges_df.columns), ignore_index = True)

        if source not in nodes:
            nodes_df = nodes_df.append(pd.Series([source], index = nodes_df.columns), ignore_index = True)
            nodes.add(source)
        if target not in nodes:
            nodes.add(target)
            nodes_df = nodes_df.append(pd.Series([target], index = nodes_df.columns), ignore_index=True)

        line = fp.readline()

nodes_df.to_csv('nodes.csv', sep=';', index_label='id')
edges_df.to_csv('edges.csv', sep=';', index=False)

fp.close()
