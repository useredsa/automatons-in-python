


for name in $(ls tests);
do
	echo "Testing $name$"
	echo "tests/$name" | ./objAnalyzer.py
	read
done

