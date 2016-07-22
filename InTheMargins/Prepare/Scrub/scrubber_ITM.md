#Scrubbing Your Documents

Preparing your texts for subsequent tokenization and analysis is a critical but essential step, what we refer to as "scrubbing" your texts. In order to facilitate a conscious consideration of the many small decisions required, scrubbing options are isolated into individual choices. If for no other reason, your careful deliberation and choice of the many options facilitates a replication of your analyses in the future, both by you and others who wish to verify your experiment.

##Directions

1. Removing Gutenberg.org boiler plate material:  Upon entering the Scrubber page, if you have uploaded a file from the Project Gutenberg website without removing the boiler plate material (i.e., text added by the Project Gutenberg site at the top and license material at the end of the text), you will receive the following warning:

>One or more files you uploaded contain Project Gutenberg licensure material. 
>You should remove the beginning and ending material, save, and re-upload the edited version. 
>If you Apply Scrubbing with a text with Gutenberg boiler plate, Lexos will attempt to remove the majority of the Project Gutenberg Licensure, however there may still be some unwanted material left over.

Note that if you select the 'Apply Scrubbing' button without removing this extra text, Lexos will attempt to remove the Gutenberg boiler plate material at the top and end of the file. However, since there are inconsistencies from file to file, we suggest you edit the file and remove the boiler plate material at the top and bottom of the file in order to prevent unwanted text from being included in subsequent analyses, e.g., including Gutenberg licensure material in your word counts. Lexos' attempt to remove start and ending boiler plate material only applies to Gutenberg.org files.

2. Remove All Punctuation: Lexos assumes that an uploaded file may be in any language, thus all files are encoded in Unicode (UTF-8). This requires that Lexos recognize punctuation from all languages. All Unicode characters have an associated set of metadata for classifying its "type", e.g. as a letter, punctuation, or symbol. If this option is selected, any Unicode character in each of the active texts with a "Punctuation Character Property" (that character's property begins with a 'P') or a Symbol Character Property (begins with 'S') is removed. If 'Remove All Punctuation' is selected, three additional suboptions are available:
  1. Keep Hyphens: Selecting this option will change all variations of Unicode hyphens to a single type of hyphen and leave the hyphens in the text. Hyphenated words (e.g., computer-aided) will be subsequently treated as one token. Further discussion of the limitations can be found [here](link to scrubbing-topic/keep-hyphen).
  2. Keep Word-Internal Apostrophes: Retain apostrophes in contractions (e.g., _can't_) and possessives (_Scott's_), but not those in plural possessives (_students'_ becomes the type _students_) nor those that appear at the start of a token (_'bout_ becomes the type _bout_). Further discussion of the limitations can be found [here](link to scrubbing-topic/keep-word-internal-apostrophes).
  3. Keep Ampersands: Leave all ampersands in the text. Note that HTML or XML entities such as <code>&amp;amp;aelig;</code> (_æ_) are handled separately and prior to the 'Keep Ampersands' option. You can choose how to convert HTML and XML entities to standard Unicode characters using the [Special Characters](link to special character section) option.

3. Make Lowercase:  Convert all uppercase characters to lowercase characters so that the tokens _The_ and _the_ will be considered as the same type. In addition, all contents (whether in uploaded files or entered manually) for Stop Words/Keep Words, Lemmas, Consolidations, or Special Characters options will also have all uppercase characters changed to lowercase. Lowercase is not applied inside any markup tags remaining in the text.

4. Remove Digits: Remove all number characters from the text. Similar to the handling of punctuation marks, any Unicode character in each of the active texts with a "Number Character Property" is removed. For example, this option will remove a Chinese three (㈢) and Eastern Arabic six (۶) from the text. Note: at present, Lexos does not match Real numbers as a unit. For example, for _3.14_, Lexos will remove (only) the 3, 1, and 4 and the decimal point would be removed if punctuation is removed. Remove Digits is not applied inside any markup tags remaining in the text.

5. Remove White Space: Remove whitespace characters (blank spaces, tabs, and line breaks), althought this is not applied inside any markup tags remaining in the text. Removing whitespace characters may be useful when you are working in non-Western languages such as Chinese that do not use whitespace for word boundaries. In addition, this option may be desired when tokenizing by character n-grams if you do not want spaces to be part of your n-grams. See the section on [Tokenization](<link to tokenize page>) for further discussion on tokenizing by character n-grams.
  1. Remove Spaces (if ON): each _blank-space_ will be removed.
  2. Remove Tabs (if ON): each tab-character (_\t_) will be removed.
  3. Remove Line Break (if ON): each _\n_ (newline) and _\r_ (carriage return) will be removed.

6. Scrub Tags: Handle tags such as those used in XML, HTML, or SGML. When this option is selected, a gear appears which once selected allows you to choose one of four options to handle all the tags at once or individually:
  1. Remove Tag Only (default): <tag>content</tag> would be replaced by _content_
  2. Remove Element and All Its Contents: <tag>content</tag> would be entirely removed
  3. Replace Element's Contents with Attribute Value: Assuming you entered _new content_ for your attribute value, <tag>content</tag> would be replaced with _new content_.
  4. Leave Tag Alone: All tags and their contents will remain in the text.


## Scrubbing Topic
1. Gutenberg.org files
2. Remove All Punctuation
Lexos assumes that an uploaded file may be in any language, thus all files are encoded in Unicode (UTF-8). This requires that Lexos recognize punctuation from all languages. All Unicode characters have an associated set of metadata for classifying its "type", e.g. as a letter, punctuation, or symbol. If this option is selected, any Unicode character in each of the active texts with metadata marking it with a "Punctuation Character Property" (that character's property begins with a 'P') or a Symbol Character Property (begins with 'S') is removed. A complete list of Unicode character properties can be found [here](http://www.fileformat.info/info/unicode/category/index.htm).

When the 'Remove All Punctuation' option is selected, the specific Punctuation and Symbols that are removed are listed below:

Punctuation	 
Pc	Connector punctuation	 
Pd	Dash punctuation	 
Pe	Close punctuation	 
Pf	Final punctuation	 
Pi	Initial punctuation	 
Po	Other punctuation	 
Ps	Open punctuation	 
S	Symbol	 
Sc	Currency symbol	 
Sk	Modifier symbol	 
Sm	Mathematical symbol	 
So	Other symbol

These characters are recognized in Python (for punctuation) via the code:
 `unicodedata.category(unichr(i)).startswith('P')`
 
  1. keep-hyphen: Selecting this option will change [all variations of Unicode hyphens](http://www.fileformat.info/info/unicode/category/Pd/list.htm) to a single type of hyphen (hyphen-minus) and leave the hyphens in the text. Hyphenated words (e.g., computer-aided) will be subsequently treated as one token. Yet, as noted by Hoover (2015), this does not address a number of complicated uses of hyphens. At present, Lexos leaves multiple-hyphen dashes in the text (e.g., "d--n" remains the token 'd--n'), runs of multiple hyphens remain in the text, and wrap-around-line-ending hyphens such as those resulting from OCR remain attached to the end of a token.
  2. keep-word-internal-apostrophes:  As noted by Hoover (2015, p4), "the problems caused by apostrophes and single quotation marks probably cannot be correctly solved computationally". At the very least, we wish to be explicit about how we are presently handling the situation using regular expressions (regex), as shown below. In short, Lexos retains apostrophes in contractions (e.g., can't) and possessives (Scott's), but _not_ those in plural possessives (_students'_ becomes the token _students_) nor those that appear at the start of a token (_'bout_ becomes the token _bout_). All strings of text that match the following regex pattern are removed (replaced with the empty string).
  ```python
  pattern = re.compile(ur"""
            (?<=[\w])'+(?=[^\w])     #If apos preceded by any word character and followed by non-word character
            |
            (?<=[^\w])'+(?=[\w])     #If apos preceded by non-word character and followed by any word character
            |
            (?<=[^\w])'+(?=[^\w])    #If apos surrounded by non-word characters
        """, re.VERBOSE | re.UNICODE)
 ```
   3. keep-ampersands: Selecting this option will change a number of variations of Unicode ampersands to a single type of ampersand and leave them in the text. Note that HTML entities (e.g., &t; ) are handled separately and can be converted to standard Unicode characters using the [Special Characters](link to special character section) option. 

3. Make Lowercase:  
4. Remove Digits:
5. Remove White Space:
6. Scrub Tags:  


###References

Hoover, D. (2015). The Trials of Tokenization. Presented at Digital Humanities 2015, Sydney, Australia. [article](http://dh2015.org/abstracts/xml/HOOVER_David_L__The_Trials_of_Tokenization//HOOVER_David_L__The_Trials_of_Tokenization.html)
