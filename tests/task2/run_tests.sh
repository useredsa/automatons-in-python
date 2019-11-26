


for name in $(ls .);
do
	echo "Testing $name$"
	echo $name | ./objAnalyzer.py
	read
done

