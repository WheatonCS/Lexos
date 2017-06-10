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
  pattern = re.compile(r"""
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

Hoover, D. (2015). The Trials of Tokenization. Presented at Digital Humanities 2015, Sydney, Australia. [article](http://dh2015.org/abstracts/xml/HOOVER_David_L__The_Trials_of_Tokenization//HOOVER_David_L__The_Trials_of_Token
