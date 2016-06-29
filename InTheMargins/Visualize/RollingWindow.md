# Rolling Window

* [Overview](#overview)
* [Features](#features)
* [Issues/Questions](#issues)

## <a name='overview'></a> Overview



## <a name='features'></a> Features

### 1. Select Active Document
1. __Tool Tip:__  
   none
2. __Tool Tip Extended:__  
   Choose one of your active documents to perform the rolling window analysis on.
3. __Example:__  
   
4. __Issue/Questions:__  
   

### 2. Select Calculation Type
1. __Tool Tip:__  
   *Rolling Average:* Measures the number of times the input appears in the window, divided by the overall size of the window.  
   *Rolling Ratio:* Measures the value of the first input divided by the sum of the first and second inputs.
2. __Tool Tip Extended:__  
   The Rolling Average feature is useful when examining one or two search terms that have relatively similar frequency in
   the text. If one of the terms appears with much more regularity than the other term(s) then the graph may appear skewed, making it more difficult to interpret the data. In this case, if the terms are mutually exclusive, the Rolling Ratio feature can be utilized. This effectively combines two search terms to provide a more comprehensive and concise view of two mutually exclusive terms.  
3. __Example:__  
   ```python
        if countType == "ratio":
            keyWordList2 = secondKeyWord.replace(",", ", ")
            keyWordList2 = keyWordList2.split(", ")
            for i in xrange(len(keyWordList)):
                keyWordList[i] = keyWordList[i] + "/(" + keyWordList[i] + "+" + keyWordList2[i] + ")"
```
4. __Issue/Questions:__  
   What are the inputs?

### 3. Enter Search Terms
1. __Tool Tip:__  
   * Search Pattern(s): Up to six inputs, divided by commas. For rolling ratios, input the numerator and denominator.  
   * Search pattern(s) as:  
      *Strings:* A string can be of any length.  
      *Word(s) (Tokens):* A token is typically a word, but Lexos will use whatever unit you have chosen in Tokenize.
      *Regular Expression(s):* Regular Expressions (RegEx) can be used as the input.
2. __Tool Tip Extended:__  
   Specifying a search term allows rolling window to visually display patterns of strings, words, or RegEx in the text of interest. This can be useful when interested in mapping patterns in the frequency of particular terms in the text.  
3. __Example:__  
   
4. __Issue/Questions:__  
   

### 4. Define Window
1. __Tool Tip:__  
   * Size of Rolling Window: The number of characters, tokens, or lines to increment for each window.  
   * Document has Milestones: Search the file for all instances of a specified string and plot a vertical dividing line at those locations.  
2. __Tool Tip Extended:__  
   The size of rolling window determines the length of each window, a good standard for a typical novel or longer text file is a window of 2,000 words.  
   Sometimes it can be helpful to insert "Milestones" in the text. Essentially, by manually writing the word "Milestone" or any word that is unique to the text file, the user can provide a visual representation on the graph (in the form of a vertical line).  
3. __Example:__  
   If working with a novel or text that includes chapters it is helpful to use the word "chapter" as a milestone in order to visualize the progression of the search term in relation to the chapters. This helps to give the graph added context.  
   ```python
        windowSize = int(windowSize)
        windowSizeStringLines = windowSize  # for when finding strings in window need original value
        minNumOfWindows = 10

        # if windowType is a word or line, splits the list accordingly
        if windowType == 'word':
            splitList = fileString.split()
        elif windowType == 'line':
            if re.search('\r', fileString) is not None:
                splitList = fileString.split('\r')
            else:
                splitList = fileString.split('\n')


        if windowType == 'word' or windowType == 'line':
            splitList = [i for i in splitList if i != '']

            if windowSize > len(splitList) - minNumOfWindows:
                windowSize = len(splitList) - minNumOfWindows
                if (windowSize <= 0):
                    windowSize = 1
        else:
            if windowSize > len(fileString) - minNumOfWindows:
                windowSize = len(fileString) - minNumOfWindows
                if (windowSize <= 0):
                    windowSize = 1
```
   
4. __Issue/Questions:__  
   

### 5. Choose Display Options
1. __Tool Tip:__  
   none
2. __Tool Tip Extended:__  
   * Hide individual points: Individual points allow the user to look at specific data points. However, if there is no need to
   examine specific points it is beneficial to select this option as it can sometimes take longer to produce a graph with individual points and the visual is not as sharp. 
   * Black and White only: By selecting this feature the graph will be generated in only black and white 
3. __Example:__  
   
4. __Issue/Questions:__  
   

### 6. Get Graph
1. __Tool Tip:__  
   none
2. __Tool Tip Extended:__  
   The resulting graph provides a representation of the search term plotted on an X-Axis measured by the number of words and a Y-Axis of the average number of times the term appears within the specified window. If milestones were indicated then the graph will have additional vertical lines that display the occurrences. 
3. __Example:__  
   ```python
        # Call the correct analysis function to get plot data
            if countType == 'average':
                if tokenType == 'string' or tokenType == 'regex':
                    if windowType == 'letter':
                        for i in (xrange(len(splitKeyWords))):
                            plotList.append(aStringLetter(fileString, splitKeyWords[i], windowSize, tokenType))

                    else:  # windowType == 'word' or windowType == 'line'
                        for i in (xrange(len(splitKeyWords))):
                            plotList.append(aStringWordLine(splitList, splitKeyWords[i], windowSize, tokenType))

                else:  # tokenType == 'word'
                    if windowType == 'word':
                        for i in (xrange(len(splitKeyWords))):
                            plotList.append(aWordWord(splitList, splitKeyWords[i], windowSize))
                    else:  # windowType == 'line'
                        for i in (xrange(len(splitKeyWords))):
                            plotList.append(aWordLine(splitList, splitKeyWords[i], windowSize))

            elif countType == 'ratio':
                if tokenType == 'string' or tokenType == 'regex':
                    if windowType == 'letter':
                        for i in (xrange(len(splitKeyWords))):
                            plotList.append(
                        rStringLetter(fileString, splitKeyWords[i], splitKeyWords2[i], windowSize, tokenType))
                    else:  # windowType == 'line' or 'word'
                        for i in (xrange(len(splitKeyWords))):
                            plotList.append(
                                rStringWordLine(splitList, splitKeyWords[i], splitKeyWords2[i], windowSize, tokenType))

                else:  # tokenType == 'word'
                    if windowType == 'word':
                        for i in (xrange(len(splitKeyWords))):
                            plotList.append(rWordWord(splitList, splitKeyWords[i], splitKeyWords2[i], windowSize))
                    else:  # windowType == 'line'
                        for i in (xrange(len(splitKeyWords))):
                            plotList.append(rWordLine(splitList, splitKeyWords[i], splitKeyWords2[i], windowSize))
```
4. __Issue/Questions:__  
   

### Download
1. __Tool Tip:__  
   none
2. __Tool Tip Extended:__  
   * Graph Data:  
   * CSV Matrix:  
   * PDF/PNG:  
   * SVG (Chrome):  
   * SVG (other browser):  
3. __Example:__  
   
4. __Issue/Questions:__  
   

## <a name='issues'></a> General Issues/Questions
