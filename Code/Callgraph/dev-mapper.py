from io import open
import pickle

with open('intermediate-files/01-2016-condensedfilegraph.txt', encoding='utf-8') as f:
    content = f.read().splitlines()
f.close()

classes = set()
for line in content:
    class1, class2 = line.split()
    classes.add(class1)
    classes.add(class2)

dev_files =  set()

with open('devfiles.txt', encoding='utf-8') as f:
    content = f.read().splitlines()

    for filename in content:
        filename = filename.split("/")[-1]
        if ".java" in filename:
            filename = filename.split(".java")[0]

            if filename in classes:
                dev_files.add(filename)

with open('intermediate-files/devnodes', 'wb') as fp:
    pickle.dump(dev_files, fp)
