from os.path import *
from os import makedirs

def cutter(filepath, size, over, lastprop, folder):
	chunksize = int(size)
	overlap = int(over)
	with open(filepath, 'r') as edit:
		text = edit.read()
		start = 0
		chunkarray = []
		end = chunksize

		while end < len(text):
			chunkarray.append(text[start:end])
			if overlap:
				end -= overlap
			start = end
			end += chunksize

		lastsize = float(lastprop)/100.0 * chunksize
		if len(chunkarray[-1]) < lastsize:
			if overlap:
				chunkarray[-1] = chunkarray[-1][:-overlap] + chunkarray.pop()
			else:
				chunkarray[-1] += chunkarray.pop()
	try:
		makedirs(folder)
	except:
		print "folder already there"
	chunkpreview = {}
	for index, chunk in enumerate(chunkarray):
		with open(folder + splitext(basename(filepath))[0] + str(index) + '.txt', 'a+') as chunkfile:
			chunkfile.write(chunk)
			chunkpreview[index] = chunk[:50]

	return chunkpreview