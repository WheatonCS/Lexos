from matplotlib import pyplot, pylab
from os import path

def rollingAverage(fileString, windowSize, keyWord):
	windowSize = int(windowSize)
	words = fileString.split()
	windowStart = 0
	windowEnd = windowStart + windowSize
	
	count = 0
	for i in xrange(windowStart, windowEnd):
		if words[i] == keyWord:
			count += 1

	print count, 'keywords in first window'
		
	averages = [float(count) / windowSize]
	while windowEnd < len(words):
		if words[windowEnd] == keyWord:
			count += 1
		if words[windowStart] == keyWord:
			count -= 1
		
		windowEnd += 1
		windowStart += 1
		averages.append(float(count) / windowSize)

	return averages

def rollinganalyze(fileString, analysisType, inputType, windowType, keyWord, windowSize, folder, widthWarp=100, average=True, ratio=False):
	if average:
		widthWarp = float(widthWarp.strip('%'))
		averageList = rollingAverage(fileString=fileString, keyWord=keyWord, windowSize=windowSize)
		fig = pyplot.figure(figsize=(10*widthWarp/100, 10))

		pyplot.plot(averageList)
		pyplot.axis([0, len(averageList), 0, max(averageList)])

		rollanafilepath = path.join(folder, 'rollingaverage.png')
		pyplot.savefig(open(rollanafilepath, 'w'), format='png')
		
	# if ratio:
		# averageList = rollingRatio(fileString=fileString, keyWord=keyWord, windowSize=windowSize)
	return rollanafilepath