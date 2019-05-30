'''
Compute developer stats for each author for particular repo

Usage : python developerStats.py repoName

repoName is the output directory from authorCommitsPerMonth.sh

@author Nandan
'''

import os
import sys

#Dict for author -> List of files worked upon in entire duration
developerWork = {}

#Dict for author -> Month -> { List of files worked upon in that month}
developerMonthlyStat = {}

#All directories in given location. This corresponds to each author we intend to work upon
dirlist = []
for root, dirs, files in os.walk(sys.argv[1]):
    dirlist += dirs

#print(dirlist)

'''
	For every author as directory, compute statistics
	Reads each line from the file monthlyCommits, and stores the file worked upon info
'''
for author in dirlist:

	# Temporary lists for each author
	monthlyDict = {}
	currList = []
	allFilesForAuthor = []

	file = open(sys.argv[1]+"/"+author+"/monthlyCommits.txt", "r");
	month = 0

	# Iterating every line from file
	for line in file:
		if "Current month" not in line:
			if len(line.strip()) != 0:
				allFilesForAuthor.append(line.strip())
				currList.append(line.strip())
		else: 
			monthlyDict[month] = currList
			month += 1
			currList = []

	developerMonthlyStat[author] = monthlyDict
	developerWork[author] = set(allFilesForAuthor)
	file.close()

sys.stdout = open('file', 'w')
#sys.stdout = sys.__stdout__

for author, monthlyData in developerMonthlyStat.items():
	print("\n****************")
	print("Developer is ", author)
	for month, filesWorked in monthlyData.items():
		print("\nMonth is ", month)
		for file in filesWorked:
			print(file)

sys.stdout = open('allFiles', 'w')

for author,files in developerWork.items():
	print("\n****************")
	print("Developer is ", author)

	for file in files:
		print(file)


