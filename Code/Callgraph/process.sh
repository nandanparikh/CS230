authors=(cdrolle@google.com aquilescanta@google.com tonihei@google.com olly@google.com julian.cable@yahoo.com hoangtc@google.com drewhill80@gmail.com vigneshv@google.com andrewlewis@google.com eguven@google.com)

for a in cdrolle@google.com aquilescanta@google.com tonihei@google.com olly@google.com julian.cable@yahoo.com hoangtc@google.com drewhill80@gmail.com vigneshv@google.com andrewlewis@google.com eguven@google.com
do
for y in 01 02 03 04 05 06 07 08 09 10 11 12
do
	echo "For author $a in $y-2016"
	python3 filegraph-gen.py exoplayer $y"-2016" $a
done
done
