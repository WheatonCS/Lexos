from os.path import *
from os import makedirs

def cutter(filepath, over, lastprop, folder, size=0, number=0):
	overlap = int(over)
	with open(filepath, 'r') as edit:
		text = edit.read().decode('utf-8')
		splittext = text.split()

		if number:
			chunksize = len(splittext)/(int(number)-1)
		else:
			chunksize = int(size)

		chunkarray = [splittext[i:i+chunksize] for i in xrange(0, len(splittext), chunksize-overlap)]

		lastsize = float(lastprop)/100.0 * chunksize
		
		if len(chunkarray[-1]) < lastsize:
			last = chunkarray.pop()
			if overlap:
				chunkarray[-1] = chunkarray[-1][:-overlap] + last
			else:
				chunkarray[-1] = chunkarray[-1] + last
	try:
		makedirs(folder)
	except:
		print "folder already there"

	chunkpreview = {}
	for index, chunk in enumerate(chunkarray):
		with open(folder + splitext(basename(filepath))[0] + str(index) + '.txt', 'a+') as chunkfile:
			chunkfile.write(''.join(chunk).encode('utf-8'))
			chunkpreview[index] = ' '.join(chunk[:10])
			if len(chunk) > 10:
				chunkpreview[index] += u"\u2026"
	return chunkpreview