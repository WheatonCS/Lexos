# Scrub

* [Overview](#overview)
* [Scrubbing Options](#features)
* [Additional Options](#addition)
* [Issues/Questions](#issues)

## <a name='overview'></a> Overview



## <a name='features'></a> Scrubbing Options

### Project Gutenberg
1. Tool Tip:  
   none
2. Tool Tip Extended:  
   Upon entering the scrub page if you have uploaded a file from the Project Gutenberg website without removing the boiler plates (text added by the Project Gutenberg site) you will receive a warning. If you choose to continue without removing this extra text on your own the text that is a part of every Project Gutenberg file will be removed, but there are inconsistencies from file to file because of additional text added by the contributors. For this reason we suggest you edit the file yourself to prevent extra unwanted text from being included in your word counts and other tests as you continue working with Lexos.
3. Example:  
   
4. Issue/Questions:  
   
### Preview Scrubbing
1. Tool Tip:  
   none
2. Tool Tip Extended:  
   This button will allow you to see the changes you will be making to the text before the file is saved with the changes. If you have a Project Gutenberg file it will still show the boiler plates in the preview.
3. Example:  
   
4. Issue/Questions:  
   
### Apply Scrubbing
1. Tool Tip:  
   none
2. Tool Tip Extended:  
   This button will save the changes you've selected to the active files. If you have a Project Gutenberg file the standard boiler plates will be removed at this point.
3. Example:  
   
4. Issue/Questions:  
   
### Download Scrubbed Files
1. Tool Tip:  
   none
2. Tool Tip Extended:  
   This button allows you to download the files you have scrubbed to your computer.
3. Example:  
   
4. Issue/Questions:  
   
   
### Remove All Punctuation
1. Tool Tip:  
   none
2. Tool Tip Extended:  
   This option will use a map containing all unicode punctuation characters to remove any character classified as punctuation from the selected files. If remove tags is not selected "<" and ">" will be removed as punctuation.
3. Example:  
   
4. Issue/Questions:  
   
#### Keep Hyphens:  
   1. Tool Tip:  
      none
   2. Tool Tip Extended:  
      Selecting this option within the remove punctuation menu will change all variatons of hyphens to a single type of hyphen and remove the one type of hyphen from the map of punctuation to be removed therefore keeping hyphens.
   3. Example:  
   
   4. Issue/Questions:  
   
#### Keep Word-Internal Apostrophes
   1. Tool Tip:  
      Retain apostrophes in contractions and possessives, but not those in plural possessives and other miscellaneous cases.
   2. Tool Tip Extended:  
      Selecting this option within the remove punctuation menu will remove apostrophes that are not in the middle of a word and then remove apostrophe from the map of punctuation to be removed.
   3. Example:  
   
   4. Issue/Questions:  
   
#### Keep Ampersands
   1. Tool Tip:  
      Ampersands are removed by default, but you may want to keep them if you have HTML or XML entities such as &t;. You can convert these entities to standard Unicode characters using the Special Character function below.
   2. Tool Tip Extended:  
      Selecting this option inside the remove punctuation menu will change all variations of ampersands to a single type of ampersand and remove that one type from the map of punctuation to be removed.
   3. Example:  
   
   4. Issue/Questions:  
   
   
### Make Lowercase
1. Tool Tip:  
   none
2. Tool Tip Extended:  
   Selecting this option will change all uppercase characters in the active files into lowercase characters. In addition any files uploaded for Stop Words/Keep Words, Lemmas, Consolidations, or Special characters will also have all uppercase characters changed to lowercase. However if any of the previous options were manually entered they should be written in lowercase as they will not be changed.
3. Example:  
   
4. Issue/Questions:  
   

### Remove Digits
1. Tool Tip:  
   none
2. Tool Tip Extended:  
   This option will use a map of all unicode characters classified as numbers to remove all digits from the selected documents.
3. Example:  
   
4. Issue/Questions:  
   

### Remove White Space
1. Tool Tip:  
   none
2. Tool Tip Extended:  
   Selecting this option will remove all white spaces (space, tab, new line). Selecting this option automatically selects all sub options. If all the sub options are unchecked this button will do nothing.
3. Example:  
   
4. Issue/Questions:  
   
#### Remove Spaces:  
   1. Tool Tip:  
      none
   2. Tool Tip Extended:  
      While this option is selected all single spaces are removed from the text. This can only be selected if Remove White Space is selected.
   3. Example:  
   
   4. Issue/Questions:  
   
#### Remove Tabs
   1. Tool Tip:  
      none
   2. Tool Tip Extended:  
      While this option is selected all tabs (\t) are removed from the active documents.
   3. Example:  
   
   4. Issue/Questions:  
   
#### Remove New Lines
   1. Tool Tip:  
      none
   2. Tool Tip Extended:  
      While this option is selected all new line characters (\n) are removed. This will make the text one long line.
   3. Example:  
   
   4. Issue/Questions:  
   
### Remove Tags
1. Tool Tip:  
   none
2. Tool Tip Extended:  
   When this option is selected anything contained between an opening "<"  and closing ">" angled bracket will be removed from the active documents.
3. Example:  
   
4. Issue/Questions:  
   If this is selected and there are options selected in XML or DOE do those override this?
#### Handle XML Tags
1. Tool Tip:  
   This should link to an ITM article.
2. Tool Tip Extended:  
   When you select this option a pop-up box with a list of all of the types of tags (Elements) is displayed with four different actions to be applied. The default option is Remove Tag Only. Other options:  Remove Element and All Its Contents, Replace Element's Contents with Attribute Value, Leave Tag Alone
3. Example:  
   
4. Issue/Questions:  
   Not sure this actually works yet, so there's no description for what it does.
#### DOE
1. Tool Tip:  
   none
2. Tool Tip Extended:  
   If you have files from the Dictionary of Old English you will have the option to either keep or remove words that appear between "<corr></corr>" and "<foreign></foreign>"
3. Example:  
   
4. Issue/Questions:  
   

## <a name='addition'></a> Additional Options

### Stop Words/Keep Words
1. Tool Tip:  
   Input a list of Stop Words (words to be removed) or Keep Words (words to keep).  
   List format: a list of words separated by commas.
2. Tool Tip Extended:  
   By default this tool is off, but has the functionality to either select specific words to keep (keep words) or to remove (stop words). Stop words will remove all instances of the tokens listed, but will not remove that word within another word. Keep words will remove all tokens except for instances of the words listed. Either a file can be uploaded with these tokens or they can be manually entered in the box separated by commas.
3. Example:  
   Stop Words: your stop word is "cat", your text is "The cat catches the caterpillar on the catwalk.", the text after scrubbing is "The catches the caterpillar on the catwalk."  
   Keep Words: your keep words are "ball, cat", your text is "The cat chased the ball across the street, but got distracted by the balloon.", the text after scrubbing is "cat ball"
   
4. Issue/Questions:  
   I don't believe this works with removed white space. Should this be mentioned and is it an issue?
   
### Lemmas
1. Tool Tip:  
   Input a list of lemmas (word replacements).  
   Lemma list format: one set of replacement words per line (each separated by commas) followed by a colon(:) then the lemma (e.g. <em>cyng,kyng:king</em> will replace every <em>cyng</em> and <em>kyng</em> in the document with <em>king</em>).
2. Tool Tip Extended:  
   Using this tool will replace a token or tokens with a different token (lemma). This can be used to replace words that have variations in spelling throughout the text with one spelling of the word.
3. Example:  
   Lemma: cyng,kyng:king  
   Text: The kyng ruled the cyngdom.  
   Scrubbed text: The king ruled the kingdom.
4. Issue/Questions:  
   From what I can tell it replaces any instance whether it's part of another word or on its own, correct me if this is wrong.
   
### Consolidations
1. Tool Tip:  
   Input a list of consolidations (character replacements).  
   Consolidation list format: one set of replacement characters per line (each separated by commas) followed by a colon(:) then the replacement character (e.g. <em>a,b:c</em> will replace every <em>a</em> and <em>b</em> in the document with <em>c</em>).
2. Tool Tip Extended:  
   
3. Example:  
   
4. Issue/Questions:  
   
   
### Special Characters
1. Tool Tip:  
   Input a list of rules for handling non-unicode characters (e.g. æ).  
   Special Character list format: one set of replacement words or characters per line (each separated by commas) followed by a colon(:) then the replacement word or character (e.g. <em>æ,ae:æ</em> will replace <em>æ</em> and <em>ae</em> with <em>æ</em>).
2. Tool Tip Extended:  
   
3. Example:  
   
4. Issue/Questions:  
   
   
## <a name='issues'></a> General Issues/Questions

