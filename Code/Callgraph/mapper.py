from io import open

classes = set()

with open('output.txt', encoding='utf-8') as f:
    content = f.readlines()

for line in content:
    if line[0] == 'C':
        class1, class2 = line.split()
        class1, class2 = str(class1), str(class2)

        class1 = class1.replace('okhttp3', 'okhttp')
        class2 = class2.replace('okhttp3', 'okhttp')
        class1 = class1.replace('.', '/')[2:]
        class2 = class2.replace('.', '/')

        if '/' in class1:
            classes.add(class1)
        if '/' in class2:
            classes.add(class2)

mapping = {}
with open('allCommitsForGraph.txt', encoding='utf-8') as f:
    content = f.readlines()

    for c in classes:
        for line in content:
            if c + '.' in line:
                mapping[line] = c

for key, value in mapping.items():
    print(value + '->' + key)
