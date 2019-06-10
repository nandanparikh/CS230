from io import open
import pickle
import sys
import os
import pandas as pd
import shutil


#USAGE: python3 filegraph-gen.py exoplayer dev_id
time_year = ["01-2016", "02-2016", "03-2016", "04-2016", "05-2016", "06-2016", "07-2016", "08-2016", "09-2016", "10-2016", "11-2016", "12-2016"]
totalnodes = []

for t in time_year:
    classes = set()
    project_name = sys.argv[1]
    op = 'input/' + sys.argv[1] + '/' + t + '/' + t + '-' + sys.argv[1] + '.txt'

    output_dir = 'output/' + sys.argv[1] + '/' + t
    condensed_dir = 'output/' + sys.argv[1] + '/' + t + '/condensed'
    author_dir = 'output/' + sys.argv[1]  + '/' + sys.argv[2]

    if not os.path.exists(author_dir):
        os.makedirs(author_dir)

    if not os.path.exists(condensed_dir):
        os.makedirs(condensed_dir)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    int_dir = output_dir + '/' + 'intermediate-files' + '-' + sys.argv[2]
    if not os.path.exists(int_dir):
        os.mkdir(int_dir)

    filegraph = open(int_dir + '/' + t + '-filegraph.txt', "w")
    condensed_filegraph = open(int_dir + '/' + t + '-condensedfilegraph.txt', "w")
    condensed_filegraph_alt = open(condensed_dir + '/' + t + '-condensedfilegraph.txt', "w+")
    edges = {}

    with open(op, encoding='utf-16') as f:
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
            condensed_filegraph_alt.write("{} {}\n".format(class1.split("/")[-1], class2.split("/")[-1]))

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


    with open(int_dir + '/' + t + '-condensedfilegraph.txt', encoding='utf-8') as f:
        content = f.read().splitlines()
    f.close()

    classes = set()
    for line in content:
        class1, class2 = line.split()
        classes.add(class1)
        classes.add(class2)

    dev_files =  set()

    with open('input/' + sys.argv[1] + '/' + t + '/' + t + '-devfiles-' + sys.argv[2] + '.txt', encoding='utf-8') as f:
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
        src = src.replace(";", "")
        for dep in deps:
            dep = dep.replace(";", "")
            dep = dep.split("$")[0]
            if src != dep and (src, dep) not in already_added:
                if src not in already_added_nodes:
                    if src in totalnodes:
                        nodes_df = nodes_df.append(pd.Series([src, 1], index=nodes_df.columns), ignore_index=True)
                    elif src in dev_nodes:
                        nodes_df = nodes_df.append(pd.Series([src, 2], index=nodes_df.columns), ignore_index=True)
                    else:
                        nodes_df = nodes_df.append(pd.Series([src, 0], index=nodes_df.columns), ignore_index=True)

                    already_added_nodes.append(src)

                if dep not in already_added_nodes:
                    if dep in dev_nodes:
                        nodes_df = nodes_df.append(pd.Series([dep, 2], index=nodes_df.columns), ignore_index=True)
                    elif src in totalnodes:
                        nodes_df = nodes_df.append(pd.Series([dep, 1], index=nodes_df.columns), ignore_index=True)
                    else:
                        nodes_df = nodes_df.append(pd.Series([dep, 0], index=nodes_df.columns), ignore_index=True)
                    already_added_nodes.append(dep)

                edges_df = edges_df.append(pd.Series([src, dep, 'directed', 1], index=edges_df.columns), ignore_index=True)
                already_added.add((src, dep))

    for node in already_added_nodes:
        if node not in totalnodes:
            totalnodes.append(node)

    edges_df["Source"] = edges_df["Source"].apply(lambda s: totalnodes.index(s))
    edges_df["Target"] = edges_df["Target"].apply(lambda s: totalnodes.index(s))

    nodes_df['id'] = nodes_df['label'].apply(lambda l: totalnodes.index(l))
    nodes_df = nodes_df.drop_duplicates(subset='label', keep='first')
    nodes_df = nodes_df.set_index('id')

    edges_df.to_csv(author_dir + '/' + t + 'edges.csv', index=False)
    nodes_df.to_csv(author_dir + '/' + t + 'nodes.csv', sep=';', columns=["label", "dev"])
    shutil.rmtree(output_dir)
