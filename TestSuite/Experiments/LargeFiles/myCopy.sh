newNameCount=0;
for (( i = 0; i < 90; i++ )); do
	#statements
	Name="les_miserables";
	newNameCount=$((newNameCount+1));
	# Name+=i;
	newName="${Name}${newNameCount}.txt";
	ending="$.txt";
	cp les_miserables.txt "${Name}${newNameCount}.txt";
done