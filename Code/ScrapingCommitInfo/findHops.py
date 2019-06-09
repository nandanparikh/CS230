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
import networkx as nx
#import matplotlib.pyplot as plt
import bellmanford as bf


G = nx.Graph()

dirlist = []
callGraphFiles = []
authorHopInfo = {}

shellStatsFolder = sys.argv[1];
callGraphFolder = sys.argv[2];

print(shellStatsFolder)
print(callGraphFolder)

def createCallGraph(monthFile):

	try:
		G.clear()

		file = open(callGraphFolder+"/"+monthFile, "r");

		for line in file:
			path = line.split(" ")
			from_path = path[0].strip()
			to_path = path[1].strip()

			if not G.has_node(from_path):
				G.add_node(from_path)
			if not G.has_node(to_path):
				G.add_node(to_path)

			e = (from_path, to_path)

			if G.has_edge(*e):
				continue;

			G.add_edge(from_path, to_path)
			G.add_edge(to_path, from_path)

		#create Graph
		#print(G.number_of_nodes())
		#print(G.number_of_edges())
		#print(G.edges.data())
		file.close()
	except:
		print("Exception in creating graph")

'''
Return total hops to reach to the file
Returns -1 if no way to reach the path
Returns -2 if the graph does not have the file
'''
def findHops(filesList, currentFile):

	maxHop = 50000;

	if not G.has_node(currentFile):
		#print("Node not found in graph : ", currentFile)
		return -2;

	for file in filesList:

		if G.has_node(file):
			try:
				#print("Path for bellman " ,file, " " , currentFile)

				#path_length, path_nodes, negative_cycle = bf.bellman_ford(G, source=file,target=currentFile, weight="length")
				
				path_length = nx.shortest_path_length(G,
                         source=currentFile,
                         target=file,
                         weight=None,
                         method='dijkstra')
				# print("PATH LENGTH ", path_length)
				#print("PATH NODES ", path_nodes)
				#print("NEG_CYCLE ", negative_cycle)
				if maxHop > path_length:
					maxHop = path_length
			except Exception as e:
				print("Exception in finding distance ",e)

	if maxHop == 50000:
		return -1
	return maxHop;

for root, dirs, files in os.walk(shellStatsFolder):
    dirlist += dirs

callGraphFilesTemp = []
for root, dirs, files in os.walk(callGraphFolder):
    callGraphFilesTemp += files

print(callGraphFilesTemp)

for file in callGraphFilesTemp:
	if '.DS' not in file:
		callGraphFiles.append(file)

print(callGraphFiles)

callGraphFiles.sort();
monthLen = len(callGraphFiles)

#For each author find his files worked
for author in dirlist:

	# Temporary lists for each author

	allFilesByAuthor = []
	month = 0
	hopsPerFile = {}
	file = open(shellStatsFolder+"/"+author+"/monthlyCommits.txt", "r");
	print(author)
	bufferTimeForAuthor = 0

	#MAKE GRAPH HERE
	#createCallGraph(callGraphFiles[month]);
	monthlyFiles = []

	for line in file:
		if "Current month" not in line:
			line = line.strip()

			if len(line) != 0 and 'java' in line:

				line = line.strip(".java")
				line = line.rsplit('/')[-1]

				if line not in allFilesByAuthor:
					if bufferTimeForAuthor > 2:
						hopsPerFile[line] = findHops(allFilesByAuthor, line)
						print("Hops for file ", line, " " , hopsPerFile[line])
					else :
						hopsPerFile[line] = 0

					monthlyFiles.append(line)

		else: 
			#MAKE GRAPH AGAIN
			if month == monthLen:
				break;

			print(callGraphFiles[month])
			createCallGraph(callGraphFiles[month])
			allFilesByAuthor += monthlyFiles
			#print(allFilesByAuthor)

			monthlyFiles = []
			bufferTimeForAuthor += 1
			month += 1

	authorHopInfo[author] = hopsPerFile;
	file.close()

#sys.stdout = open(shellStatsFolder+'/HopInformation', 'w')
#sys.stdout = sys.__stdout__
hopStatistics = {}
for author, hopInfo in authorHopInfo.items():
	print("\n****************")
	print("Developer is ", author)

	fileNotFoundInGraph = 0
	fileIndependent = 0
	filesWithHops = 0
	totalHops = 0

	for file, hopCount in hopInfo.items():
		if(hopCount == -1):
			fileIndependent += 1

		if(hopCount == -2):
			fileNotFoundInGraph += 1

		if(hopCount >= 0):
			totalHops += hopCount + 1
			filesWithHops += 1

	print("\nTotal Hops : ", totalHops," fileIndependent : ", fileIndependent, 
		"fileNotFoundInGraph ", fileNotFoundInGraph);
	print("Total files with hops ", filesWithHops)

	someData = {}

	if filesWithHops == 0:
		someData['Total Average Hops'] = 0
	else:
		someData['Total Average Hops'] = totalHops/filesWithHops

	someData['Independent files in Graph'] = fileIndependent
	someData['Files not found in Graph'] = fileNotFoundInGraph

	hopStatistics[author] = someData;
	print(someData)

df = pd.DataFrame(hopStatistics)
df = df.transpose()
df.to_csv(shellStatsFolder+'/hopStatistics.csv')
#def plotGraph():
#	nx.draw(G, with_labels=True, font_weight='bold')
#	plt.subplot(122)