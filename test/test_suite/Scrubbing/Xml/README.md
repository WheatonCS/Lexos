XML
==========

#### Test Remove XML Tags

*Test files:* book.xml, george.xml, small.xml, test.xml

*Result files:* bookRemoveTags.txt, georgeAttributes.txt, smallContents.txt,
testLeaveTags.txt

1. UPLOAD FILES

2. SCRUB: 
    - Remove All Punctuation
    - Make Lowercase
    - Remove Digits
    - Remove Tags
        * Remove Tag Only
        * Remove Element and All its Contents
        * Replace Element and its Contents with Attribute Value
        * Leave Tag Alone

3. RESULTS:
    - bookRemoveTags.txt remove tags only
    - georgeAttributes.txt replace element's contents with attribute value
    - smallContents.txt remove element and all its contents
    - testLeaveTags.txt leave tags alone
     
