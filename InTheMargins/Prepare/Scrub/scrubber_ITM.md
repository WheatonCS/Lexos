#Scrubbing Your Documents

Preparing your texts for subsequent tokenization and analysis is a critical but essential step, what we refer to as "scrubbing" your texts. In order to facilitate a conscious consideration of the many small decisions required, scrubbing options are isolated into individual choices. If for no other reason, your careful deliberation and choice of the many options facilitates a replication of your analyses in the future, both by you and others who wish to verify your experiment (Hoover, 2015).

##Directions

1. Removing Gutenberg.org boiler plate material:  Upon entering the Scrubber page, if you have uploaded a file from the Project Gutenberg website without removing the boiler plate material (i.e., text added by the Project Gutenberg site at the top and license material at the end of the text), you will receive the following warning:

>One or more files you uploaded contain Project Gutenberg licensure material. 
>You should remove the beginning and ending material, save, and re-upload the edited version. 
>If you Apply Scrubbing with a text with Gutenberg boiler plate, Lexos will attempt to remove the majority of the Project Gutenberg Licensure, however there may still be some unwanted material left over.

Note that if you select the 'Apply Scrubbing' button without removing this extra text, Lexos will attempt to remove the Gutenberg boiler plate material at the top and end of the file. However, since there are inconsistencies from file to file, we suggest you edit the file and remove the boiler plate material at the top and bottom of the file in order to prevent unwanted text from being included in subsequent analyses, e.g., including Gutenberg licensure material in your word counts. Lexos' attempt to remove start and ending boiler plate material only applies to Gutenberg.org files.

2. Remove All Punctuation: Lexos assumes that an uploaded file may be in any language, thus all files are encoded in Unicode (UTF-8). This requires that Lexos recognize punctuation from all languages. All Unicode characters have an associated set of metadata for classifying its "type", e.g. as a letter, punctuation, or symbol. If this option is selected, any Unicode character in each of the active texts with a "Punctuation Character Property" (that character's property begins with a 'P') or a Symbol Character Property (begins with 'S') is removed. If 'Remove All Punctuation' is selected, three additional suboptions are available:
  1. 




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



###References

Hoover, D. (2015). The Trials of Tokenization. Presented at Digital Humanities 2015, Sydney, Australia. [article](http://dh2015.org/abstracts/xml/HOOVER_David_L__The_Trials_of_Tokenization//HOOVER_David_L__The_Trials_of_Tokenization.html)
