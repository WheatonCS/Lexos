newNameCount=0;
for (( i = 0; i < 10000; i++ )); do
	#statements
	Name="les_miserables";
	newNameCount=$((newNameCount+1));
	# Name+=i;
	newName="${Name}${newNameCount}.txt";
	ending="$.txt";
	cp moby_dick.txt "${Name}${newNameCount}.txt";
done