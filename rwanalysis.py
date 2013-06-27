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

	if windowSize > len(fileString):
		windowEnd = len(fileString)

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
	

	if windowType == 'word':
		splitList = fileString.split()
	else:
		splitList = fileString.split('\n')
	
	count = 0
   	
	windowSize = int(windowSize)
	windowStart = 0
	windowEnd = windowStart + windowSize

	amountOfCharsInWindowSize = 0
	if windowSize > len(splitList):
		windowEnd = len(splitList)

	for i in xrange(windowStart, windowEnd):
		for char in splitList[i]:
			amountOfCharsInWindowSize +=1
			if keyLetter == char:
		       		count += 1
	averages = [float(count) / amountOfCharsInWindowSize]
	x = 0
	y = 0
	
	while windowEnd < len(splitList):
		for char in splitList[windowEnd]:
			x+=1
			if char == keyLetter:
				count += 1
		for char in splitList[windowStart]:
			y+=1
			if char == keyLetter:
				count -= 1
		windowEnd += 1
		windowStart += 1
		amountOfCharsInWindowSize +=x
		amountOfCharsInWindowSize-=y	
		averages.append(float(count) / amountOfCharsInWindowSize)
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

		lengthOfLines = 0
		lines = fileString.split('\n')
		if windowSize > len(lines):
			windowEnd = len(lines)
		for i in lines:
			if i == '':
				lines.remove(i)

		for i in xrange(len(lines)):
			lines[i] = lines[i].split()

		for i in xrange(windowStart, windowEnd):
			lengthOfLines += len(lines[i])
			for letter in lines[i]:
				if letter == keyWord:
					count += 1
		averages = [float(count) / lengthOfLines]
		x=0
		y=0
		while windowEnd < len(lines):
			x = x+len(lines[windowEnd])
			y = y+len(lines[windowStart])
			for word in lines[windowEnd]:
				if word == keyWord:
					count += 1
			for word in lines[windowStart]:
				if word == keyWord:
					count -= 1
	
			windowEnd += 1
			windowStart += 1
			lengthOfLines = ((lengthOfLines+x)-y)
			averages.append(float(count) / lengthOfLines)

	else:
		words = fileString.split(' ')
		if windowSize > len(words):
			windowEnd = len(words)
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
	windowSize = int(windowSize)
	if windowType == 'line':
		splitList = filestring.split('\n')
	else:
		splitList = filestring.split()

	first = 0
	
	second = 0
	
	allOccurancesOfSecondCounter = 0
	allOccurancesOfFirstCounter = 0

	windowStart = 0
	windowEnd = windowStart + windowSize
	if windowSize > len(splitList):
		windowEnd = len(splitList)
	for i in xrange(windowStart, windowEnd):		
		for char in xrange(len(splitList[i])):
			if firstLetter == splitList[i][char]:
		       		first = first + 1
				allOccurancesOfFirstCounter = allOccurancesOfFirstCounter + 1
			if secondLetter ==  splitList[i][char]:
				second = second + 1
				allOccurancesOfSecondCounter = allOccurancesOfSecondCounter + 1
	

	if second == 0 and first ==0:
		returnRatioList.append(0)

	else:
		returnRatioList.append(float(first) / (first+second))
	while windowEnd < len(splitList):
		for i in xrange(len(splitList[windowEnd])):
			if splitList[windowEnd][i] == firstLetter:
				first += 1
			if splitList[windowEnd][i] == secondLetter:
				second += 1
		for i in xrange(len(splitList[windowStart])):	
			if splitList[windowStart][i] == firstLetter:
				first -= 1
			if splitList[windowStart][i] == secondLetter:
				second -= 1
				
		
		windowEnd += 1
		windowStart += 1
		
		if second == 0 and first ==0:
			returnRatioList.append(0)

		else:
			returnRatioList.append(float(first) / (first+second))
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
	if windowSize > len(filestring):
		windowEnd = len(filestring)
	for i in xrange(windowStart, windowEnd):
		if firstLetter == filestring[i]:
	       		first = first + 1
			
			allOccurancesOfFirstCounter = allOccurancesOfFirstCounter + 1
		if secondLetter == filestring[i]:
			second = second + 1
		
			allOccurancesOfSecondCounter = allOccurancesOfSecondCounter + 1
	
	
	if second == 0 and first ==0:
		returnRatioList.append(0)

	else:
		returnRatioList.append(float(first) / (first+second))
	while windowEnd < len(filestring):
		if filestring[windowEnd] == firstLetter:
			first += 1
			allOccurancesOfFirstCounter = allOccurancesOfFirstCounter + 1
		if filestring[windowEnd] == secondLetter:
			second += 1
			allOccurancesOfSecondCounter = allOccurancesOfSecondCounter + 1
		if filestring[windowStart] == firstLetter:
			first -= 1
		if filestring[windowStart] == secondLetter:
			second += 1
		
		windowEnd += 1
		windowStart += 1
				
		if second == 0 and first ==0:
			returnRatioList.append(0)

		else:
			returnRatioList.append(float(first) / (first+second))
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
	windowSize = int(windowSize)

	splitList = []
	if windowType == 'lines':
		splitList = filestring.split('\n')
	else:
		splitList = filestring.split()

	windowStart = 0
	windowEnd = windowStart + windowSize

	first = 0
	second = 0
	NumberOfChunks = 0
	allOccurancesOfBreaksInText = 1
	allOccurancesOfSecondCounter = 0
	allOccurancesOfFirstCounter = 0
	if windowSize > len(splitList):
		windowEnd = len(splitList)
	for i in xrange(windowStart, windowEnd):
		if firstWord == splitList[i]:
	       		first = first + 1

			allOccurancesOfFirstCounter = allOccurancesOfFirstCounter + 1
		if secondWord == splitList[i]:
			second = second + 1

			allOccurancesOfSecondCounter = allOccurancesOfSecondCounter + 1

	if second == 0 and first ==0:
		returnRatioList.append(0)

	else:
		returnRatioList.append(float(first) / (first+second))
		
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
				
		if second == 0 and first ==0:
			returnRatioList.append(0)

		else:
			returnRatioList.append(float(first) / (first+second))

	return returnRatioList


def rollinganalyze(fileString, analysisType, inputType, windowType, keyWord, secondKeyWord, windowSize, folder, widthWarp=100):
	Y_AXIS_LABEL = ''
	widthWarp = float(widthWarp.strip('%'))

	if analysisType == 'average':
		Y_AXIS_LABEL = Y_AXIS_LABEL + 'average of '
		if inputType == 'letter':
			Y_AXIS_LABEL = Y_AXIS_LABEL + 'letter '
			if windowType =='letter':
				Y_AXIS_LABEL = Y_AXIS_LABEL + 'by letter'
				averageList = RollingAverageA(fileString, keyWord, windowSize)
			else: # by word or line
				Y_AXIS_LABEL = Y_AXIS_LABEL + 'by ' + str(windowType)
				averageList = RollingAverageB(fileString, keyWord, windowSize, windowType)
		
		else: # inputType == 'word'
			Y_AXIS_LABEL = Y_AXIS_LABEL +'of ' + str(inputType) + ' by ' + str(windowType)
			averageList = RollingAverageC(fileString, keyWord, windowSize, windowType)

		plotList = averageList

	elif analysisType == 'ratio':
		Y_AXIS_LABEL = Y_AXIS_LABEL + 'ratio of '
		if inputType == 'letter':
			Y_AXIS_LABEL = Y_AXIS_LABEL + 'letter '
			if windowType =='letter':
				Y_AXIS_LABEL = Y_AXIS_LABEL + 'by rollletter '
				ratioList = RatioOfLetterByLetter(fileString, keyWord, secondKeyWord, windowSize)
			else: # by word or line
				Y_AXIS_LABEL = Y_AXIS_LABEL + 'by ' + str(windowType)
				ratioList = RatioOfLetterByWordsOrLines(fileString, keyWord, secondKeyWord, windowSize, windowType)
		else: #by word or line-
			Y_AXIS_LABEL = Y_AXIS_LABEL +'of ' + str(inputType) + ' by ' + str(windowType)
			ratioList = RatioOfWordsByWordsOrLines(fileString, keyWord, secondKeyWord, windowSize, windowType)

		plotList = ratioList

	else:
		return False

	fig = pyplot.figure(figsize=(10*widthWarp/100, 10))
	pyplot.plot(plotList)
	ax= pyplot.subplot(111)
	ax.set_xlabel('window number')
	ax.set_ylabel(Y_AXIS_LABEL)
	pyplot.axis([0, len(plotList)-1, 0, max(plotList)])
	rollanafilepath = path.join(folder, 'rollingaverage.png')
	pyplot.savefig(open(rollanafilepath, 'w'), format='png')


	return rollanafilepath
