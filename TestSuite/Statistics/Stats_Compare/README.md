# STATS COMPARE

We want to check whether the counting on STATS page work for large files and whether the data come out are correct, thus we used other two tools to compare the result.

The other two are: 
- Voyant(search it and use it online;
- Intelligent Archive(need download to use, try on mac since it was written in JAVA, need whatever operating systems that supports java)

Need to know:
- Voyant does not do scrubbing stuff, it count the words as how it apperas in the original uploading files
- Intelligent Archive provides a space to let users edit the words to exclude from process after uploading files and click "Word Frequencies", only tried a few punctuations but not sure whether those are all or not


Test files:
- catCaterpillar:original one

- DreamCH1:original one
- DreamCH1(no_punc):removed punctuations using Lexos
- DreamCH1(no_punc&white_spaces):removed punctuations and white spaces using Lexos

- Fog(beginning):original one
- Fog(beginning_no_space):removed spaces
- Fog(beginning_one_line):removed all the white spaces

- Heart_of_Darkness:original one
- Heart_of_Darkness(no_punc&lowercase&no_digits):removed punctuations and made all in lowercase and removed digits using Lexos

- OnetoTen:original one
- OnetoTen(no_space):removed spaces
- OnetoTen(one_line_with_no_space):removed all the white spaces
- OnetoTen(one_line_with_space):removed new line characters

- War and Peace:original one
- War and Peace(no_punc):removed punctuations using Lexos
- War and Peace(no_punc&lowercase):removed punctuations and made all in lowercase using Lexos
- War and Peace(no_punc&lowercase&no_digits):removed punctuations and made all in lowercase and removed digits using Lexos
- War and Peace(no_punc&lowercase&no_digits):removed punctuations and made all in lowercase and removed digits using Lexos on June 28th, 2016(scrubbing has been edited since the last txt version)


Go to "STATS_Compare.ods" in folder ResultsToExpect for results.




