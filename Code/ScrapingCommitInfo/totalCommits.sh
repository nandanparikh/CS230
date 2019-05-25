#!/bin/sh

#First argument : Folder of git repo
#Second argument : Year to start search with
#Third argument : Year to end on
#Last argument : Output folder

FROM=$2
TO=$3
FOLDER=$4

((TO++))

echo $TO
#Go to git code folder
echo "Path provided to execute fetch git logs is : " $1;
cd $1;

#Find all authors for the git project. Stores only email
AUTHORS=`git log --all --format='%ae' | sort -u | grep -o '^\S*'`
echo $AUTHORS


#Exit if no authors in repo
if [ ${#AUTHORS[@]} == 0 ]
then
	echo "No authors found"
	exit;
fi

#echo "Commits per author : " > $FOLDER/commitCount.txt;
 
totalCount=0

for author in $AUTHORS
do
	counter=`git log --all --after=$FROM"-01-01" --until=$TO"-01-01" --author=$author\
	| grep -E "^commit" | sed -e 's/commit //g' | wc -l`;
	totalCount=$(( $totalCount + $counter ))
	echo $author ":" $counter >> $FOLDER/commitCountPerAuthor.txt;
done

echo $totalCount

some=`git log --all --after=$FROM"-01-01" --until=$TO"-01-01" \
	| grep -E "^commit" | sed -e 's/commit //g' | wc -l`;
echo $some