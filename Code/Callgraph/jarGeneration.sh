#@author : Tanmay
#First argument : Folder of git repo
#Second argument : Year to start search with
#Third argument : Year to end on
#Last argument : Output folder

#Usage: sh Code/downloadingHash.sh . 2018 2020 $PWD

MONTH=(01 02 03 04 05 06 07 08 09 10 11 12)
DATE=(31 28 31 30 31 30 31 31 30 31 30 31)
FROM=$2
TO=$3
FOLDER=$4

mkdir $FOLDER

#move to the directory
cd $1

while [ $FROM -lt $TO ]
do
	index=0
	while [ $index -lt 12 ]
	do
		name1="$FROM"-"${MONTH[$index]}"-01""
		name2="$FROM"-"${MONTH[$index]}"-"${DATE[$index]}"

		echo $name1" "$name2
		HASH=`git log --all --pretty=format:'%h' --after=$FROM"-"${MONTH[$index]}"-01" --until=$FROM"-"${MONTH[$index]}"-"${DATE[$index]} -n 1`

		hashValue=$HASH
		echo $hashValue
		#SHOW=`git show $hashValue`
		#echo $SHOW
		CHECKOUT=`git checkout $hashValue`
		echo $CHECKOUT

		JAR=`jar -cvf $FOLDER/okhttp"_"${MONTH[$index]}"_"$FROM".jar" .`
		echo $JAR  > /dev/null
	
		((index++))
	done
	((FROM++))
done

cd ~/jarStorage/
ls -l

#Get the Hashes
