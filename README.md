CS230 Spring 2019 Project
========================

A Study on Developer Growth in Open Source Software Systems

Contributors :
  Nandan Parikh,
  Prateek Malhotra,
  Tanmay Chinchore


Project 
---------
Get developer statistics for each repository, which includes new files work upon across months <br />
Generate tabular information of files worked every month <br />
Generate tabular information of new files and its minimum distance to any previous work by developer <br />
Get static call-graph text files <br />
Visualization of call-graphs for every author every month using Gephi <br />

Requirements 
-------------

Java and javac installed <br />
java-callgraph installed <br />
shell scripts work on bin/sh<br />
python 3.x<br />
Gephi Application<br />

How to run
------------ 

Download git repo using git clone <br />
Execute "Integration script for all scraping information"<br />
	sh findAllInformationForRepo.sh gitRepoFolder yearFrom yearTo resultsDirectory<br /><br />
Generate jars for the specific repo. Might require specific java cmnds to generate jar </br>
Execute "call-graph" on this using process.sh <br /><br />

Use this output to generate hops information  <br />
	python findHops.py callGraphFolder resultsDirectory <br />

Generate visualization using the Gephi.jar file
