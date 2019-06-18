# XML

***

#### Test Remove XML Tags

*Test files:* book.xml, george.xml, small.xml, test.xml

*Result files:* bookRemoveTags.txt, georgeAttributes.txt, smallContents.txt,
testLeaveTags.txt

### Test book.xml

1. Upload book.xml

2. Under "Prepare" go to "Scrub" and use the following settings: 
    - Remove Punctuation
    - Make Lowercase
    - Remove Digits
    
3. Select "Scrub Tags" and click "Options"
    - Select "Remove Tag" for all tags
    
4. Click "Ok" and "Apply"

Results:
    - bookRemoveTags.txt remove tags only
    
### Test small.xml

1. Upload small.xml

2. Under "Prepare" go to "Scrub" and use the following settings: 
    - Remove Punctuation
    - Make Lowercase
    - Remove Digits
    
3. Select "Scrub Tags" and click "Options"
    - Select "Remove All" for all tags
    
4. Click "Ok" and "Apply"

Results:
    - smallContents.txt remove element and all its contents
    - testLeaveTags.txt leave tags alone
     
### Test test.xml

1. Upload test.xml

2. Under "Prepare" go to "Scrub" and use the following settings: 
    - Remove Punctuation
    - Make Lowercase
    - Remove Digits
    
3. Select "Scrub Tags" and click "Options"
    - Select "None" for all tags
    
4. Click "Ok" and "Apply"

Results:
    - testLeaveTags.txt leave tags alone
