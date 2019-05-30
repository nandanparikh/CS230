'''
Compute developer stats for each author for particular repo

Usage : python developerStats.py repoName folderNameForResults

repoName is the output directory from authorCommitsPerMonth.sh

@author Nandan
'''

import os
import sys

#Dict for author -> List of files worked upon in entire duration
developerWork = {}

#Dict for author -> Month -> new file count per month
developerMonthlyNewWork = {}

#Dict for author -> Month -> { List of files worked upon in that month}
developerMonthlyStat = {}


shellStatsFolder = sys.argv[1];

resultsFolder = sys.argv[2];

#All directories in given location. This corresponds to each author we intend to work upon
dirlist = []
for root, dirs, files in os.walk(shellStatsFolder):
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
	monthlyCount = {}

	file = open(shellStatsFolder+"/"+author+"/monthlyCommits.txt", "r");
	month = 0
	newFiles = 0
	# Iterating every line from file
	for line in file:
		if "Current month" not in line:
			if len(line.strip()) != 0:

				if line.strip() not in allFilesForAuthor:
					newFiles += 1
					allFilesForAuthor.append(line.strip())
					
				currList.append(line.strip())
		else: 
			monthlyDict[month] = currList
			monthlyCount[month] = newFiles
			month += 1
			currList = []
			newFiles = 0

	developerMonthlyStat[author] = monthlyDict
	developerMonthlyNewWork[author] = monthlyCount
	developerWork[author] = set(allFilesForAuthor)
	file.close()

sys.stdout = open(resultsFolder+'/MonthlyWorkPerAuthor', 'w')
#sys.stdout = sys.__stdout__

for author, monthlyData in developerMonthlyStat.items():
	print("\n****************")
	print("Developer is ", author)
	for month, filesWorked in monthlyData.items():
		print("\nMonth is ", month)
		for file in filesWorked:
			print(file)

sys.stdout = open(resultsFolder+'/AllFilesWorkPerAuthor', 'w')

for author,files in developerWork.items():
	print("\n****************")
	print("Developer is ", author)

	for file in files:
		print(file)


sys.stdout = open(resultsFolder+'/CountOfFilesWorked', 'w')

for author,files in developerWork.items():
	print("Developer is ", author)
	print(len(files))

#sys.stdout = sys.__stdout__
for author, monthlyData in developerMonthlyNewWork.items():
	print("\n****************")
	print("Developer is ", author)
	count = 0
	for month, filesWorked in monthlyData.items():
		print("\nMonth is : ", month, " with new files : ", filesWorked )
		count += filesWorked
	#print("Count printed for test : ", count)