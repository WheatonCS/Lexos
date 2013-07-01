from matplotlib import pyplot, pylab
from os import path



def RollingAverageA(fileString, keyLetter, windowSize):
	"""

	Computes the rolling average of one letter over a certain window size by characters.

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

	#determines the number of letters in the initial window
	for i in xrange(windowStart, windowEnd):
		if keyLetter == fileString[i]:
	       		count += 1
			
	averages = [float(count) / windowSize]
	while windowEnd < len(fileString):
		#To avoid recounting through the entire window, checks the first and last character in the window.
		if fileString[windowEnd] == keyLetter:
			count +=1
		if fileString[windowStart] == keyLetter:
			count -= 1
		windowEnd += 1
		windowStart += 1
		averages.append(float(count) / windowSize)
	print averages
	return averages

def RollingAverageB(splitList, keyLetter, windowSize):
	"""

	Computes the rolling average of one letter over a certain window size of lines or words.
	
	Args:
		fileString: the text from the activated file
		windowSize: the amount of words or lines you want your rolling average window to be
		keyLetter: the letter you are taking the rolling average for
		windowType: determines whether it is by line or word 

	Returns:
		the list of average for each window
	"""
	count = 0
   	
	windowSize = int(windowSize)
	windowStart = 0
	windowEnd = windowStart + windowSize
	#force at least one point to be plotted
	if windowEnd <= 0:
		windowEnd = 1

	amountOfCharsInWindowSize = 0
	for i in xrange(windowStart, windowEnd):
		for each_char in splitList[i]:
			amountOfCharsInWindowSize +=1
			if keyLetter == each_char:
				count += 1
	averages = [float(count) / amountOfCharsInWindowSize]
	
	while windowEnd < len(splitList):
		x = 0
		y = 0
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



def RollingAverageC(splitList, keyWord, windowSize, windowType):
	"""

	Computes the rolling average of a word over a certain window size.

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
	#force at least one point to be plotted
	if windowEnd <= 0:
		windowEnd = 1

	count = 0
	
	if windowType == 'line': #by lines
		lengthOfLines = 0
		lines = splitList
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
	
		while windowEnd < len(lines):
			x=0
			y=0
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

	else: #by words
		words = splitList
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
	Computes the rolling ratio of one letter to another over a certain window size either by word or line.

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
	Computes the rolling ratio of one letter to another over a certain window size by characters.

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
	Computes the rolling ratio of one word to another over a certain window size either by word or line.

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
	"""

	"""
	Y_AXIS_LABEL = ''
	windowSize = int(windowSize)
	widthWarp = float(widthWarp.strip('%'))
	if analysisType == 'average':
		if inputType == 'letter':
			if windowType =='letter':
				#force plot to have at least two points.
				if windowSize >= len(fileString):
					windowSize = len(fileString) - 1
				Y_AXIS_LABEL = "Average number of " + keyWord + "'s per window size of " + str(windowSize) + " characters."
				averageList = RollingAverageA(fileString, keyWord, windowSize)
			else: # by word or line
				if windowType == 'word':
					splitList = fileString.split()
					countUnit = ' words'
				else:
					#note: should handle "\r"
					splitList = fileString.split('\n')
					countUnit = ' lines'
				#force plot to have at least two points.
				listLength = len(splitList)
			
				if listLength < windowSize:
					windowSize = listLength - 1

				Y_AXIS_LABEL = "Average number of " + keyWord + "'s in a window size of " + str(windowSize) + countUnit + "."
				averageList = RollingAverageB(splitList, keyWord, windowSize)
		
		else: # inputType == 'word'
			#handles window sizes in lines and words
			if windowType == 'word':
					splitList = fileString.split()
					countUnit = ' words'
			else:
				#note: should handle "\r"
				splitList = fileString.split('\n')
				countUnit = ' lines'
			#force plot to have at least two points.
			listLength = len(splitList)
		
			if listLength < windowSize:
				windowSize = listLength - 1
			Y_AXIS_LABEL = "Average number of " + keyWord + "'s in a window size of " + str(windowSize) + countUnit + "."		
			averageList = RollingAverageC(splitList, keyWord, windowSize, windowType)

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
	ax.set_xlabel('Window number (left-most point in each window)')
	ax.set_ylabel(Y_AXIS_LABEL)
	pyplot.axis([0, len(plotList)-1, -0.1, max(plotList)+.1])
	rollanafilepath = path.join(folder, 'rollingaverage.png')
	pyplot.savefig(open(rollanafilepath, 'w'), format='png')


	return rollanafilepath
