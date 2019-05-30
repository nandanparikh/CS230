with open('output.txt', encoding='utf16') as f:
    content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
content = "\n".join(x.strip() for x in content if x[0] == 'C' and 'java' not in x)
print(content)
f.close()

outfile = open("classgraph.txt", "w")
outfile.write(content)
outfile.close()
