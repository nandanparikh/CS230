from io import open
import pickle

classes = set()
op = '01-2016-exo.txt'

filegraph = open('intermediate-files/01-2016-filegraph.txt', "w")
condensed_filegraph = open('intermediate-files/01-2016-condensedfilegraph.txt', "w")
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

with open('intermediate-files/edges', 'wb') as fp:
    pickle.dump(edges, fp)

f.close()
filegraph.close()
condensed_filegraph.close()
