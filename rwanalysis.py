from matplotlib import pyplot, pylab
from os import path



def RollingAverageA(fileString, keyLetter, windowSize):
	"""

	computes the rolling average of one letter over a certain window size by characters

	Args:
		fileString: the text from the activated file
		windowSize: the amount of words or lines you want your rolling average window to be
		keyLetter: the letter you are taking the rolling average for
	Returns:
		the list of average for each window
	"""

	count = 0

	windowSize = int(windowSize)
	windowStart = 0
	windowEnd = windowStart + windowSize

	for i in xrange(windowStart, windowEnd):
		if keyLetter == fileString[i]:
	       		count += 1
			
	averages = [float(count) / windowSize]
	while windowEnd < len(fileString):
		if fileString[windowEnd] == keyLetter:
			count +=1
		if fileString[windowStart] == keyLetter:
			count -= 1
		windowEnd += 1
		windowStart += 1
		averages.append(float(count) / windowSize)
	
	return averages

def RollingAverageB(fileString, keyLetter, windowSize, windowType):
	"""

	computes the rolling average of one letter overa certain window size of lines or words
	
	Args:
		fileString: the text from the activated file
		windowSize: the amount of words or lines you want your rolling average window to be
		keyLetter: the letter you are taking the rolling average for
		windowType: determines whether it is by line or word 

	Returns:
		the list of average for each window
	"""

	splitList = []

	if windowType == 'words':
		splitList = fileString.split(' ')
	else:
		splitList = fileString.split('\n')

	count = 0
   	
	windowSize = int(windowSize)
	windowStart = 0
	windowEnd = windowStart + windowSize

	for i in xrange(windowStart, windowEnd):
		for char in splitList[i]:
			if keyLetter == char:
		       		count += 1
			
	averages = [float(count) / windowSize]
	while windowEnd < len(splitList):
		for char in splitList[windowEnd]:
			if char == keyLetter:
				count += 1
		for char in splitList[windowStart]:
			if char == keyLetter:
				count -= 1
			
		windowEnd += 1
		windowStart += 1
		averages.append(float(count) / windowSize)
	
	return averages


def RollingAverageC(fileString, keyWord, windowSize, windowType):
	"""

	computes the rolling average of a word over a certain window size

	Args:
		fileString: the text from the activated file
		windowSize: the amount of words or lines you want your rolling average window to be
		keyWord: the word you want to take the rolling average for
		windowType: determines whether it is by line or word 

	Returns:
		the list of averages for each window
	"""
	windowSize = int(windowSize)
	windowStart = 0
	windowEnd = windowStart + windowSize
	
	count = 0

	if windowType == 'line':
		lines = fileString.split('\n')
		for i in xrange(len(lines)):
			lines[i] = lines[i].split(' ')

		for i in xrange(windowStart, windowEnd):
			for letter in lines[i]:
				if letter == keyWord:
					count += 1
	
		averages = [float(count) / windowSize]

		while windowEnd < len(lines):
			for word in lines[windowEnd]:
				if word == keyWord:
					count += 1
			for word in lines[windowStart]:
				if word == keyWord:
					count -= 1
	
			windowEnd += 1
			windowStart += 1
			averages.append(float(count) / windowSize)

	else:
		words = fileString.split(' ')
	
		for i in xrange(windowStart, windowEnd):
			if words[i] == keyWord:
				count += 1
		
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


def RatioOfLetterByWordsOrLines(filestring, firstLetter, secondLetter, windowSize, windowType):
	"""
	computes the rolling ratio of one letter to another over a certain window size either by 		word or line

	Args:
		fileString: the text from the activated file
		windowSize: the amount of words or lines you want your rolling average window to be
		firstLetter: the letter you would like to be on the numerator of your ratio
		secondLetter: the letter you would like to be on the denominator or your ratio 
		windowType: determines whether it is by line or word 

	Returns:
		the list of ratios for each window
	"""
	returnRatioList =[]

	splitList = []

	if windowType == 'lines':
		splitList = filestring.split('\n')
	else:
		splitList = filestring.split(' ')

	first = 0
	firstList = []
	second = 0
	secondList = []
   	NumberOfChunks = 0
	Break = 0
	allOccurancesOfBreaksInText = 1
	y = numberInWindow
	allOccurancesOfSecondCounter = 0
	allOccurancesOfFirstCounter = 0

	windowStart = 0
	windowEnd = windowStart + windowSize

	for i in xrange(windowStart, windowEnd):
		for char in splitList[i]:
			if firstLetter == splitList[i][char]:
		       		first = first + 1
				print 'first:', first
				allOccurancesOfFirstCounter = allOccurancesOfFirstCounter + 1
			if secondLetter ==  splitList[i][char]:
				second = second + 1
				print 'second:', second
				allOccurancesOfSecondCounter = allOccurancesOfSecondCounter + 1
	

	returnRatioList = [float(first) / second]
	while windowEnd < len(splitList):
		for i in splitList[windowEnd]:
			if splitList[windowEnd][i] == firstLetter:
				first += 1
			if splitList[windowEnd][i] == secondLetter:
				second += 1
			if splitList[windowStart][i] == firstLetter:
				first -= 1
			if splitList[windowStart][i] == secondLetter:
				second -= 1
		
		windowEnd += 1
		windowStart += 1
		returnRatioList.append(float(first) / second)

	return returnRatioList

def RatioOfLetterByLetter(filestring, firstLetter, secondLetter, windowSize):
	"""
	computes the rolling ratio of one letter to another over a certain window size by characters

	Args:
		fileString: the text from the activated file
		windowSize: the amount of words or lines you want your rolling average window to be
		firstLetter: the letter you would like to be on the numerator of your ratio
		secondLetter: the letter you would like to be on the denominator or your ratio 

	Returns:
		the list of ratios for each window
	"""
	returnRatioList =[]

	first = 0
	second = 0
	allOccurancesOfSecondCounter = 0
	allOccurancesOfFirstCounter = 0
	windowSize = int(windowSize)
	windowStart = 0
	windowEnd = windowStart + windowSize

	for i in xrange(windowStart, windowEnd):
		if firstWord == filestring[i]:
	       		first = first + 1
			print 'first:', first
			allOccurancesOfFirstCounter = allOccurancesOfFirstCounter + 1
		if secondWord == filestring[i]:
			second = second + 1
			print 'second', second
			allOccurancesOfSecondCounter = allOccurancesOfSecondCounter + 1
	
	
	returnRatioList = [float(first) / second]
	while windowEnd < len(words):
		if splitList[windowEnd] == firstLetter:
			first += 1
			allOccurancesOfFirstCounter = allOccurancesOfFirstCounter + 1
		if splitList[windowEnd] == secondLetter:
			second += 1
			allOccurancesOfSecondCounter = allOccurancesOfSecondCounter + 1
		if splitList[windowStart] == firstLetter:
			first -= 1
		if splitList[windowStart] == secondLetter:
			second += 1
		
		windowEnd += 1
		windowStart += 1
		returnRatioList.append(float(first) / second)
	
	return returnRatioList


def RatioOfWordsByWordsOrLines(filestring, firstWord, secondWord, windowSize, windowType):
	"""
	computes the rolling ratio of one word to another over a certain window size either by 		word or line

	Args:
		fileString: the text from the activated file
		windowSize: the amount of words or lines you want your rolling average window to be
		firstWord: the word you would like to be on the numerator of your ratio
		secondWord: the word you would like to be on the denominator or your ratio 
		windowType: determines whether it is by line or word 

	Returns:
		the list of ratios for each window
	"""
	returnRatioList =[]

	splitList = []
	if windowType == 'lines':
		splitList = filestring.split('\n')
	else:
		splitList = filestring.split(' ')

	windowStart = 0
	windowEnd = windowStart + windowSize

	first = 0
	second = 0
	NumberOfChunks = 0
	allOccurancesOfBreaksInText = 1
	allOccurancesOfSecondCounter = 0
	allOccurancesOfFirstCounter = 0

	for i in xrange(windowStart, windowEnd):
		if firstWord == splitList[i]:
	       		first = first + 1
			print 'first:', first
			allOccurancesOfFirstCounter = allOccurancesOfFirstCounter + 1
		if secondWord == splitList[i]:
			second = second + 1
			print 'second', second
			allOccurancesOfSecondCounter = allOccurancesOfSecondCounter + 1

	returnRatioList = [float(first) / second]
	while windowEnd < len(splitList):
		if splitList[windowEnd] == firstWord:
			first += 1
			allOccurancesOfFirstCounter = allOccurancesOfFirstCounter + 1
		if splitList[windowEnd] == secondWord:
			second += 1
			allOccurancesOfSecondCounter = allOccurancesOfSecondCounter + 1
		if splitList[windowStart] == firstWord:
			first -= 1
		if splitList[windowStart] == secondWord:
			second += 1
		
		windowEnd += 1
		windowStart += 1
		returnRatioList.append(float(first) / second)

	return returnRatioList


def rollinganalyze(fileString, analysisType, inputType, windowType, keyWord, secondKeyWord, windowSize, folder, widthWarp=100, average=True, ratio=False):
	widthWarp = float(widthWarp.strip('%'))

	if average:
		if inputType == 'letter':
			if windowType =='letter':
				averageList = RollingAverageA(fileString, keyWord, windowSize)
			else: # by word or line
				averageList = RollingAverageB(fileString, keyWord, windowSize, windowType)
		
		else: # inputType == 'word'
			averageList = RollingAverageC(fileString, keyWord, windowSize, windowType)

		plotList = averageList

	elif ratio:
		if inputType == 'letter':
			if windowType =='letter':
				ratioList = RatioOfLetterByLetter(fileString, keyWord, secondKeyWord, windowSize)
			else: # by word or line
				ratioList = RatioOfLetterByWordsOrLines(fileString, keyWord, secondKeyWord, windowSize, windowType)
		else: #by word or line-
			ratioList = RatioOfWordsByWordsOrLines(fileString, keyWord, secondKeyWord, windowSize, windowType)

		plotList = ratioList

	else:
		return False

	fig = pyplot.figure(figsize=(10*widthWarp/100, 10))
	pyplot.plot(plotList)
	pyplot.axis([0, len(plotList)-1, 0, max(plotList)])
	rollanafilepath = path.join(folder, 'rollingaverage.png')
	pyplot.savefig(open(rollanafilepath, 'w'), format='png')


	return rollanafilepath