#!/bin/sh

#First argument : Folder of git repo
#Second argument : Year to start search with
#Third argument : Year to end on
#Last argument : Output folder

#Usage : sh Code/sortCommitByAuthor.sh . 2018 2020 $PWD

#References
#Sample codes : authors and date
#git log --all --after=$2"-01-31" --until="2019-05-19" --author="N"

#git diff-tree --no-commit-id --name-only -r bd61ad98
#git show --pretty="" --name-only bd61ad98

#https://stackoverflow.com/questions/37311494/how-to-get-git-to-show-commits-in-a-specified-date-range-for-author-date
#https://www.commandlinefu.com/commands/view/4519/list-all-authors-of-a-particular-git-project

MONTH=(01 02 03 04 05 06 07 08 09 10 11 12)
DATE=(31 28 31 30 31 30 31 31 30 31 30 31)
FROM=$2
TO=$3
FOLDER=$4

#Go to git code folder
echo "Path provided to execute fetch git logs is : " $1;
cd $1;

#Find all authors for the git project. Stores only firstname
AUTHORS=`git log --all --format='%aN' | sort -u | grep -o '^\S*'`
echo $AUTHORS


#Exit if no authors
if [ ${#AUTHORS[@]} == 0 ]
then
	echo "No authors found"
	exit;
fi

#For each author, for each month, find his commits
for author in $AUTHORS
do
	echo "Author is : " $author
	echo "Author is : " $author >> sorted.txt
	from=$FROM
	while [ $from -lt $TO ]
	do
		index=0
		while [ $index -lt 12 ]
		do
			echo ${MONTH[$index]};
			commits=`git log --all --after=$from"-"${MONTH[$index]}"-01" --until=$from"-"${MONTH[$index]}"-"${DATE[$index]} --author=$author\
			| grep -E "^commit" | sed -e 's/commit //g'`;
			echo "" > $FOLDER/tempForAuthor.txt
			for commit in $commits
			do
				git show --pretty="" --name-only $commit >> $FOLDER/tempForAuthor.txt
			done
			echo "Current month/year : " ${MONTH[$index]}/$from >> $FOLDER/sorted.txt
			sort -u $FOLDER/tempForAuthor.txt >> $FOLDER/sorted.txt 
			((index++))
		done
		((from++))
	done
done