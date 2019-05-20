with open('output.txt') as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = "\n".join(x.strip() for x in content if x[0] == 'C' and 'java' not in x)
f.close()

outfile = open("classgraph.txt", "w")
outfile.write(content)
outfile.close()
