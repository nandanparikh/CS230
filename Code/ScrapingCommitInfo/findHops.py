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
		print(G.edges.data())
		file.close()
	except:
		print("Exception in creating graph")

def findHops(filesList, currentFile):

	maxHop = 50000;

	if not G.has_node(currentFile):
		#print("Node not found in graph : ", currentFile)
		return maxHop;

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
				print("PATH LENGTH ", path_length)
				#print("PATH NODES ", path_nodes)
				#print("NEG_CYCLE ", negative_cycle)
				if maxHop > path_length:
					maxHop = path_length
			except Exception as e:
				print("Exception in finding distance ",e)

	if maxHop == 50000:
		return 0
	return maxHop;

for root, dirs, files in os.walk(shellStatsFolder):
    dirlist += dirs

callGraphFilesTemp = []
for root, dirs, files in os.walk(callGraphFolder):
    callGraphFilesTemp += files


for file in callGraphFilesTemp:
	if '.DS' not in file:
		callGraphFiles.append(file)

callGraphFiles.sort();


#For each author find his files worked
for author in dirlist:

	# Temporary lists for each author

	allFilesByAuthor = []
	month = 0
	hopsPerFile = {}
	file = open(shellStatsFolder+"/"+author+"/monthlyCommits.txt", "r");

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
			createCallGraph(callGraphFiles[month])
			allFilesByAuthor += monthlyFiles
			print(allFilesByAuthor)

			monthlyFiles = []
			bufferTimeForAuthor += 1
			month += 1

		if month > 100:
			break;

	print("BUFF",bufferTimeForAuthor)

	authorHopInfo[author] = hopsPerFile;
	file.close()

#sys.stdout = open(shellStatsFolder+'/HopInformation', 'w')
#sys.stdout = sys.__stdout__

for author, hopInfo in authorHopInfo.items():
	print("\n****************")
	print("Developer is ", author)
	for file, hopCount in hopInfo.items():
		print("\nFile : ", month," hops : ", hops);
		#FIND AVERAGE?!

#def plotGraph():
#	nx.draw(G, with_labels=True, font_weight='bold')
#	plt.subplot(122)