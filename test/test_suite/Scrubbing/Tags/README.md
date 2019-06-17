# Tags

***

#### Test Scrub Tags

*Test files:* tags.txt, tags_attributes.txt

*Result files:* tags_DefaultResults.txt, tags_RemoveTagAndContentResults.txt

1. Upload Files

2. Scrub: 
    - Remove Punctuation
    - Make Lowercase
    - Remove Digits
    - Scrub Tags
        * to obtain tags_DefaultResults.txt, leave default scrub tags settings
        * to obtain tags_RemoveTagAndContentResults.txt, in settings, set all
        to Remove All

3. Results
    - a file (tags_DefaultResults.txt) containing
        * lowercase letters
        * no digits
        * no punctuation
        * all tags removed, but their contents left alone
        
    - a file (tags_RemoveTagAndContentResults.txt) containing
        * lowercase letters
        * no digits
        * no punctuation
        * all tags and their contents removed
