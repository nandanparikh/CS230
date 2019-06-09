#!/bin/bash
#Integration script for all scraping information

# Usage : sh findAllInformationForRepo.sh gitRepoFolder yearFrom yearTo resultsDirectory
# @author : nandan

#Steps :
# 1. Find all commits for the repo in given year
# 2. Find relevant top developers and make their commits sorted monthwise in separate folder
# 3. Find developer stats for every new file and total commits
# 4. Create dataframe information for every repo to get a tabular display


gitRepo=$1
yearFrom=$2
yearTo=$3
resultsDir=$4


sh totalCommits.sh $gitRepo $yearFrom $yearTo $resultsDir
sh authorCommitsPerMonth.sh $gitRepo $yearFrom $yearTo $resultsDir
python developerStats.py $resultsDir $resultsDir
python ownershipStats.py $resultsDir $resultsDir
