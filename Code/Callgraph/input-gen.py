import os
import sys
import pandas as pd

shellStatsFolder = sys.argv[1]
inputfolder = sys.argv[2]

#All directories in given location. This corresponds to each author we intend to work upon
dirlist = []
for root, dirs, files in os.walk(shellStatsFolder):
    dirlist += dirs

authorlist = "\n".join(dirlist)
with open("output/exoplayer/authors.txt", "w+") as f:
	f.write(authorlist)

#print(dirlist)

'''
	For every author as directory, compute statistics
	Reads each line from the file monthlyCommits, and stores the file worked upon info
'''
for author in dirlist:

    try:
        file = open(shellStatsFolder+"/"+author+"/monthlyCommits.txt", "r")
        content = file.read().splitlines()
    except:
        continue;

    to_write = {}
    month_year = "01-2016"

    for line in content:
        if "Current month" in line:
            if month_year in to_write:
                towritemonthyear = to_write[month_year][0] + "\n".join(to_write[month_year][1:])
                try:
                    with open(inputfolder + '/' + month_year + '/' + month_year + "-devfiles-" + author + ".txt", "w+") as f:
                        f.write(towritemonthyear)
                except:
                    pass

            month, year = line.split(":")[-1].split("/")
            month_year = month + "-" + year
            month_year = month_year.strip()
            to_write[month_year] = []
        else:
            to_write[month_year].append(line)


    file.close()
