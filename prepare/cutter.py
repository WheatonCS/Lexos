from math import ceil


def cut(text, overlap, lastProp='50%', cuttingValue=2, cuttingBySize=True):
	"""
	Cuts each text file into various segments according to the options chosen by the user.

	*Called in cut() in lexos.py

	Args:
		filepath: A string representing the path to the file.
		over: A unicode string representing the number of words to be overlapped by each text segment.
		folder: A string representing the path to the folder where the cut files will be stored.
		lastProp: A unicode string representing the percentage for the last proportion.
		cuttingValue: A unicode string representing the value at which the file are cut.
		cuttingBySize: A boolean distinguishing whether the files are cut by size or number.

	Returns:
		A dictionary where the integer keys represent the various segments that have been cut,
		and the string values represent the actual text for each corresponding text segment.
	"""
	overlap = int(overlap)
	lastProp = lastProp.strip('%')

	splittext = text.split()

	if cuttingBySize:
		chunksize = int(cuttingValue)
	else:
		chunksize = int(ceil(len(splittext) / float(cuttingValue)))
		lastProp = 0

	print 'Chunksize:', chunksize

	chunkarray = [splittext[i:i + chunksize] for i in xrange(0, len(splittext), chunksize - overlap)]

	print chunkarray

	lastsize = float(lastProp) / 100.0 * chunksize

	if len(chunkarray) > 1 and len(chunkarray[-1]) < lastsize:
		last = chunkarray.pop()
		if overlap:
			chunkarray[-1] = chunkarray[-1][:-overlap] + last
		else:
			chunkarray[-1] = chunkarray[-1] + last

	return chunkarray
