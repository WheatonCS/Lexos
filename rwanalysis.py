from matplotlib import pyplot, pylab
from os import path

def rollingAverageOfWordsByLineOrWord(fileString, windowSize, keyWord, windowType):

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
		words = fileString.split('\n')
		for i in xrange(len(words)):
			words[i] = words[i].split(' ')

		for i in xrange(windowStart, windowEnd):
			j =0
			while len(words[i]) > j:
				print 'kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk' , words[i][j]
				if words[i][j] == keyWord:
					count += 1
				j+=1

		print count, 'keywords in first window'
		
	
		averages = [float(count) / windowSize]

		print averages, 'average'


		while windowEnd < len(words):
			print 'words[windowEnd]: ' , words[windowEnd]
			for i in xrange(len(words[windowEnd])):
				if words[windowEnd][i] == keyWord:
					count += 1
			for i in xrange(len(words[windowStart])):
				if words[windowStart][i] == keyWord:
					count -= 1
	
			windowEnd += 1
			windowStart += 1
			averages.append(float(count) / windowSize)



	else:
		words = fileString.split(' ')
	
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

def rollingAverageOfLetterByWordOrLine(fileString, windowSize, keyLetter, windowType):
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
	average =[]

	SPLITLIST = []

	if windowType == 'lines':
		SPLITLIST = fileString.split('\n')
	else:
		SPLITLIST = fileString.split(' ')

	count = 0
   	
	windowSize = int(windowSize)
	num = 1

	windowStart = 0
	windowEnd = windowStart + windowSize

	for i in xrange(windowStart, windowEnd):
		for char in xrange(len(SPLITLIST[i])):
			if keyLetter == SPLITLIST[i][char]:
		       		count += 1
			
	ReturnRatioList = [float(count) / windowSize]
	while windowEnd < len(SPLITLIST):
		for i in xrange(len(SPLITLIST[windowEnd])):
			if SPLITLIST[windowEnd][i] == keyLetter:
				count += 1
		print 'COUNT AFTER ADDING' , count
		for i in xrange(len(SPLITLIST[windowStart])):
			if SPLITLIST[windowStart][i] == keyLetter:
				count -= 1

		print 'COUNT AFTER SUBTRACTINH', count
			
		windowEnd += 1
		windowStart += 1
		average.append(float(count) / windowSize)
	
	return average



#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def RollingAverageLetterByLetter(fileString, windowSize, keyLetter):
	"""
	computes the rolling average of one letter over a certain window size by characters

	Args:
		fileString: the text from the activated file
		windowSize: the amount of words or lines you want your rolling average window to be
		keyLetter: the letter you are taking the rolling average for
	Returns:
		the list of average for each window
	"""
	average =[]

	count = 0
	num = 0
	windowSize = int(windowSize)
	windowStart = 0
	windowEnd = windowStart + windowSize

	for i in xrange(windowStart, windowEnd):
		print 'FILE STRING AT i: ' , fileString[i]
		if keyLetter == fileString[i]:
	       		count = count + 1
			
	average.append(float(count) / windowSize)
	print '\n\n AVERAGE : ' , average
	while windowEnd < len(fileString):
		print 'window end: ' , windowEnd
		print 'window Start: ' , windowStart
		if fileString[windowEnd] == keyLetter:
			count +=1
		if fileString[windowStart] == keyLetter:
			count -= 1
		windowEnd += 1
		windowStart += 1
		average.append(float(count) / windowSize)

	print 'average: ' , average
	
	return average

def RatioOfLetterByWordsOrLines(filestring, windowSize, firstLetter, secondLetter, windowType):
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
	ReturnRatioList =[]

	SPLITLIST = []

	if windowType == 'lines':
		SPLITLIST = filestring.split('\n')
	else:
		SPLITLIST = filestring.split(' ')

	first = 0
	firstList = []
	second = 0
	secondList = []
   	NumberOfChunks = 0
	Break = 0
	allOccurancesOfBreaksInText = 1
	y = numberInWindow
	num = 1
	allOccurancesOfSecondCounter = 0
	allOccurancesOfFirstCounter = 0

	windowStart = 0
	windowEnd = windowStart + windowSize

	for i in xrange(windowStart, windowEnd):
		for char in SPLITLIST[i]:
			if firstLetter == SPLITLIST[i][char]:
		       		first = first + 1
				print 'first:', first
				allOccurancesOfFirstCounter = allOccurancesOfFirstCounter + 1
			if secondLetter ==  SPLITLIST[i][char]:
				second = second + 1
				print 'second:', second
				allOccurancesOfSecondCounter = allOccurancesOfSecondCounter + 1
	

	ReturnRatioList = [float(first) / second]
	while windowEnd < len(SPLITLIST):
		for i in SPLITLIST[windowEnd]:
			if SPLITLIST[windowEnd][i] == firstLetter:
				first += 1
			if SPLITLIST[windowEnd][i] == secondLetter:
				second += 1
			if SPLITLIST[windowStart][i] == firstLetter:
				first -= 1
			if SPLITLIST[windowStart][i] == secondLetter:
				second -= 1
		
		windowEnd += 1
		windowStart += 1
		ReturnRatioList.append(float(first) / second)

	return ReturnRatioList

def RatioOfLetterByLetter(filestring, windowSize, firstLetter, secondLetter):
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
	ReturnRatioList =[]

	first = 0
	second = 0
	allOccurancesOfSecondCounter = 0
	allOccurancesOfFirstCounter = 0
	num = 0
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
	
	
	ReturnRatioList = [float(first) / second]
	while windowEnd < len(words):
		if SPLITLIST[windowEnd] == firstLetter:
			first += 1
			allOccurancesOfFirstCounter = allOccurancesOfFirstCounter + 1
		if SPLITLIST[windowEnd] == secondLetter:
			second += 1
			allOccurancesOfSecondCounter = allOccurancesOfSecondCounter + 1
		if SPLITLIST[windowStart] == firstLetter:
			first -= 1
		if SPLITLIST[windowStart] == secondLetter:
			second += 1
		
		windowEnd += 1
		windowStart += 1
		ReturnRatioList.append(float(first) / second)
	
	return ReturnRatioList


def RatioOfWordsByWordsOrLines(filestring, windowSize, firstWord, secondWord, windowType):
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
	ReturnRatioList =[]

	SPLITLIST = []
	if windowType == 'lines':
		SPLITLIST = filestring.split('\n')
	else:
		SPLITLIST = filestring.split(' ')

	windowStart = 0
	windowEnd = windowStart + windowSize

	first = 0
	second = 0
	NumberOfChunks = 0
	allOccurancesOfBreaksInText = 1
	allOccurancesOfSecondCounter = 0
	allOccurancesOfFirstCounter = 0
	num = 0

	for i in xrange(windowStart, windowEnd):
		if firstWord == SPLITLIST[i]:
	       		first = first + 1
			print 'first:', first
			allOccurancesOfFirstCounter = allOccurancesOfFirstCounter + 1
		if secondWord == SPLITLIST[i]:
			second = second + 1
			print 'second', second
			allOccurancesOfSecondCounter = allOccurancesOfSecondCounter + 1

	ReturnRatioList = [float(first) / second]
	while windowEnd < len(SPLITLIST):
		if SPLITLIST[windowEnd] == firstWord:
			first += 1
			allOccurancesOfFirstCounter = allOccurancesOfFirstCounter + 1
		if SPLITLIST[windowEnd] == secondWord:
			second += 1
			allOccurancesOfSecondCounter = allOccurancesOfSecondCounter + 1
		if SPLITLIST[windowStart] == firstWord:
			first -= 1
		if SPLITLIST[windowStart] == secondWord:
			second += 1
		
		windowEnd += 1
		windowStart += 1
		ReturnRatioList.append(float(first) / second)

	return ReturnRatioList


def rollinganalyze(fileString, analysisType, inputType, windowType, keyWord, secondKeyWord, windowSize, folder, widthWarp=100, average=True, ratio=False):
	if average:
		widthWarp = float(widthWarp.strip('%'))

		if inputType == 'letter':
			if windowType =='letter':
				averageList = RollingAverageLetterByLetter(fileString=fileString, keyLetter=keyWord, windowSize=windowSize)

			else: #by word or line
				if windowType == 'line':
					averageList = rollingAverageOfLetterByWordOrLine(fileString=fileString, keyLetter=keyWord, windowSize=windowSize, windowType=windowType)
				else: #by word
					averageList = rollingAverageOfLetterByWordOrLine(fileString=fileString, keyLetter=keyWord, windowSize=windowSize, windowType=windowType)
		
		else: #by word
			if windowType =='line':
				averageList =  rollingAverageOfWordsByLineOrWord(fileString=fileString, keyWord=keyWord, windowSize=windowSize, windowType = windowType)

			else: #by word 
				averageList =  rollingAverageOfWordsByLineOrWord(fileString=fileString, keyWord=keyWord, windowSize=windowSize, windowType=windowType)



		fig = pyplot.figure(figsize=(10*widthWarp/100, 10))

		pyplot.plot(averageList)
		pyplot.axis([0, len(averageList), 0, max(averageList)])

		rollanafilepath = path.join(folder, 'rollingaverage.png')
		pyplot.savefig(open(rollanafilepath, 'w'), format='png')


	if ratio:
		widthWarp = float(widthWarp.strip('%'))


		if inputType == 'letter':
			if windowType =='letter':
				RatioList = RatioOfLetterByLetter(fileString=fileString, windowSize=windowSize, keyWord=firstLetter, secondKeyWord=secondLetter)

			else: #by word or line
				if windowType == 'line':
					RatioList =  RatioOfLetterByWordsOrLines(fileString=fileString, windowSize=windowSize, windowType=windowType, keyWord = firstLetter, secondKeyWord=secondLetter)

				else: #by word
					RatioList = RatioOfLetterByWordsOrLines(fileString=fileString, windowSize=windowSize, windowType=windowType, keyWord = firstLetter, secondKeyWord=secondLetter)


		else: #by word or line
			if windowType == 'line':
				RatioList =  RatioOfWordsByWordsOrLines(fileString=fileString, windowSize=windowSize, windowType=windowType, keyWord=firstWord, secondKey=WordsecondWord)

			else: #by word
				RatioList = RatioOfWordsByWordsOrLines(fileString=fileString, windowSize=windowSize, windowType=windowType, keyWord=firstWord, secondKeyWord=secondWord)

		fig = pyplot.figure(figsize=(10*widthWarp/100, 10))

		pyplot.plot(RatioList)
		pyplot.axis([0, len(RatioList), 0, max(RatioList)])

		rollanafilepath = path.join(folder, 'rollingaverage.png')
		pyplot.savefig(open(rollanafilepath, 'w'), format='png')


	return rollanafilepath






