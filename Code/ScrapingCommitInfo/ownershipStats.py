'''
Compute ownership stats -> Computes author #commits for every java file 

Usage : python ownershipStats.py repoName folderNameForResults

repoName is the output directory from authorCommitsPerMonth.sh

@author Nandan
'''

import os
import sys
import pandas as pd

shellStatsFolder = sys.argv[1];
resultsFolder = sys.argv[2];

dirlist = []
for root, dirs, files in os.walk(shellStatsFolder):
    dirlist += dirs

#print(dirlist)

authorDict = {}

for author in dirlist:

	fileCount = {}

	file = open(shellStatsFolder+"/"+author+"/allMonthlyCommits.txt", "r");

	for line in file:
		if "Current month" not in line:
			line = line.strip();
			if len(line) != 0 and line.endswith('java'): 
				if line not in fileCount.keys():
					fileCount[line] = 1
				else:
					fileCount[line] += 1

	authorDict[author] = fileCount;
	file.close()

df = pd.DataFrame(authorDict) 
df.to_csv('df.csv')
    
#print("Transpose the dictionary")
    
df1 = df.transpose()
df1.to_csv('df1.csv')