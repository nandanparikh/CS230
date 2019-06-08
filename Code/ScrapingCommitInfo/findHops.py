'''

Compute hops for each new file developer works on!
Usage : python findHops.py repoName callGraphFolder

repoName is the output directory from authorCommitsPerMonth.sh
callGraphFolder is the output directory containing all month call-graphs text file

@author Nandan
'''

import os
import sys
import pandas as pd

dirlist = []
callGraphFiles = []
authorHopInfo = {}

shellStatsFolder = sys.argv[1];
callGraphFolder = sys.argv[2];


def createCallGraph(monthFile):
	file = open(shellStatsFolder+"/"+monthFile, "r");

	for line in file:
		path = line.split(" ")
		from_path = path[0]
		to_path = path[1]

	#create Graph
	file.close()


for root, dirs, files in os.walk(shellStatsFolder):
    dirlist += dirs

for root, dirs, files in os.walk(callGraphFolder):
    callGraphFiles += files

callGraphFiles.sort();

#For each author find his files worked
for author in dirlist:

	# Temporary lists for each author

	allFilesByAuthor = []
	month = 0
	hopsPerFile = {}
	file = open(shellStatsFolder+"/"+author+"/monthlyCommits.txt", "r");

	bufferTimeForAuthor = 1

	#MAKE GRAPH HERE
	createCallGraph(callGraphFiles[month]);

	for line in file:
		if "Current month" not in line:
			line = line.strip()

			if len(line) != 0:

				if line not in allFilesByAuthor:
					allFilesByAuthor.append(line)

					if bufferTimeForAuthor > 2:
						print("Find from graph")
						#find hops
						#hopsPerFile[line] = k
					else :
						hopsPerFile[line] = 0
		else: 
			#MAKE GRAPH AGAIN
			createCallGraph(callGraphFiles[month])
			bufferTimeForAuthor += 1
			month += 1

		if month > 100:
			break;

	authorHopInfo[author] = hopsPerFile;
	file.close()

sys.stdout = open(shellStatsFolder+'/HopInformation', 'w')
#sys.stdout = sys.__stdout__

for author, hopInfo in developerMonthlyStat.items():
	print("\n****************")
	print("Developer is ", author)
	for file, hopCount in hopInfo.items():
		print("\nFile : ", month," hops" : hops);
		#FIND AVERAGE?!