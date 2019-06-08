import pandas as pd
from io import open
import pickle

columns = ['Source','Target', 'type', 'weight']
edges_df = pd.DataFrame(columns=columns)

columns = ['label', 'dev']
nodes_df = pd.DataFrame(columns=columns)

with open('intermediate-files/nodes', 'rb') as f:
	nodes = pickle.load(f)

with open('intermediate-files/devnodes', 'rb') as f:
	dev_nodes = pickle.load(f)

with open('intermediate-files/edges', 'rb') as f:
	edges = pickle.load(f)

#CLEAN EDGES TO ONLY INCLUDES ONES WHICH DEVELOPER HAS WORKED ON
to_pop = []

for src, deps in edges.items():
	if src in dev_nodes:
		pass
	else:
		c = 0
		for dep in deps:
			if dep in dev_nodes:
				c = 1
				break
		if c == 0:
			to_pop.append(src)

for src in to_pop:
	edges.pop(src)

already_added = set()
already_added_nodes = []

for src, deps in edges.items():
	for dep in deps:
		dep = dep.split("$")[0]
		if src != dep and (src, dep) not in already_added:

			if src not in already_added_nodes:
				if src in dev_nodes:
					nodes_df = nodes_df.append(pd.Series([src, 1], index=nodes_df.columns), ignore_index=True)
				else:
					nodes_df = nodes_df.append(pd.Series([src, 0], index=nodes_df.columns), ignore_index=True)
				already_added_nodes.append(src)

			if dep not in already_added_nodes:
				if dep in dev_nodes:
					nodes_df = nodes_df.append(pd.Series([dep, 1], index=nodes_df.columns), ignore_index=True)
				else:
					nodes_df = nodes_df.append(pd.Series([dep, 0], index=nodes_df.columns), ignore_index=True)
				already_added_nodes.append(dep)

			edges_df = edges_df.append(pd.Series([already_added_nodes.index(src), already_added_nodes.index(dep), 'directed', 1], index=edges_df.columns), ignore_index=True)
			already_added.add((src, dep))

edges_df.to_csv('csvfiles/edges.csv', index=False)
nodes_df.to_csv('csvfiles/nodes.csv', index_label='id')

'''
with open('inv_dev.txt', encoding='utf-8') as f:
	content = f.readlines()

	for line in content:
		dev_nodes.add(line.replace("\n", ""))

print(dev_nodes)

with open('condensed_filegraph_2016-01.txt') as fp:
	line = fp.readline()
	while line:
		source, target = line.strip().split()
		edges_df = edges_df.append(pd.Series([source, target, 'directed', 1], index = edges_df.columns), ignore_index = True)

		val = 0
		if source not in nodes:
			if source in dev_nodes:
				val = 1
			nodes_df = nodes_df.append(pd.Series([source, val], index = nodes_df.columns), ignore_index = True)
			nodes.add(source)

		val = 0
		if target not in nodes:
			if source in dev_nodes:
				val = 1
			nodes.add(target)
			nodes_df = nodes_df.append(pd.Series([target, val], index = nodes_df.columns), ignore_index=True)

		line = fp.readline()

nodes_df.to_csv('nodes.csv', sep=';', index_label='id')
edges_df.to_csv('edges.csv', sep=';', index=False)
'''
