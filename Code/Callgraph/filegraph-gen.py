from io import open
import pickle
import sys
import os
import pandas as pd

#USAGE: python3 filegraph-gen.py exoplayer 01-2016 dev_id

classes = set()
project_name = sys.argv[1]
op = 'input/' + sys.argv[2] + '/' + sys.argv[2] + '-' + sys.argv[1] + '-callgraph.txt'

output_dir = 'output/' + sys.argv[2]
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

int_dir = output_dir + '/' + 'intermediate-files'
if not os.path.exists(int_dir):
    os.mkdir(int_dir)

csv_dir = output_dir + '/' + 'csv-files' + sys.argv[3]
if not os.path.exists(csv_dir):
    os.mkdir(csv_dir)

filegraph = open(int_dir + '/' + sys.argv[2] + '-filegraph.txt', "w")
condensed_filegraph = open(int_dir + '/' + sys.argv[2] + '-condensedfilegraph.txt', "w")
edges = {}

with open(op, encoding='utf-8') as f:
    content = f.readlines()

for line in content:
    if line[0] == 'C' and 'java.' not in line:
        class1, class2 = line.split()
        class1, class2 = str(class1), str(class2)

        class1 = class1.split("$")[0]

        class1 = class1.replace('.', '/')[2:]
        class2 = class2.replace('.', '/')

        class1 = class1.replace('exoplayer2', 'exoplayer')
        class2 = class2.replace('exoplayer2', 'exoplayer')

        classes.add(class1)
        classes.add(class2)

        #print("{} {}".format(class1, class2))
        filegraph.write("{} {}\n".format(class1, class2))
        condensed_filegraph.write("{} {}\n".format(class1.split("/")[-1], class2.split("/")[-1]))

        class1 = class1.split("/")[-1]
        class2 = class2.split("/")[-1]

        if class1 in edges:
            edges[class1].append(class2)
        else:
            edges[class1] = [class2]

with open(int_dir + '/edges', 'wb') as fp:
    pickle.dump(edges, fp)

f.close()
filegraph.close()
condensed_filegraph.close()


with open(int_dir + '/' + sys.argv[2] + '-condensedfilegraph.txt', encoding='utf-8') as f:
    content = f.read().splitlines()
f.close()

classes = set()
for line in content:
    class1, class2 = line.split()
    classes.add(class1)
    classes.add(class2)

dev_files =  set()

with open('input/' + sys.argv[2] + '/' + sys.argv[2] + '-' + sys.argv[1] + '-devfiles-' + sys.argv[3] + '.txt', encoding='utf-8') as f:
    content = f.read().splitlines()

    for filename in content:
        filename = filename.split("/")[-1]
        if ".java" in filename:
            filename = filename.split(".java")[0]

            if filename in classes:
                dev_files.add(filename)

with open(int_dir + '/devnodes', 'wb') as fp:
    pickle.dump(dev_files, fp)

columns = ['Source','Target', 'type', 'weight']
edges_df = pd.DataFrame(columns=columns)

columns = ['label', 'dev']
nodes_df = pd.DataFrame(columns=columns)

with open(int_dir + '/devnodes', 'rb') as f:
	dev_nodes = pickle.load(f)

with open(int_dir + '/edges', 'rb') as f:
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

edges_df.to_csv(csv_dir + '/edges.csv', index=False)
nodes_df.to_csv(csv_dir + '/nodes.csv', index_label='id')
