# Content Analysis Tool
### How to test Organizational Hardiness

*Files to use:*  JP Morgan2000.txt, JP Morgan2001.txt, JP Morgan2002.txt, JP Morgan2003.txt, 
JP Morgan2004.txt, JP Morgan2005.txt, JP Morgan2006.txt, JP Morgan2007.txt, JP Morgan2008.txt, 
JP Morgan2009.txt, Enactment.txt, Opportunity.txt, Org_Identity.txt, Threat.txt

*Expected Results:* Result.csv

****

**Follow the steps provided below to determine the Organizational Hardiness of J.P. Morgan Chase & Co.**

*Organizational hardiness is the probability of a company to recover from an issue or set back.*

1. Upload all JP Morgan files

2. These files have already been prepared or "scrubbed" with the following default settings:
    - Remove Punctuation
    - Make Lowercase
    - Remove Digits

3. Under the "Analyze" menu, select "Content Analysis"

4. Select "Upload Files" under Dictionaries and select the 4 provided dictionary 
files: Enactment.txt, Opportunity.txt, Org_Identity.txt, Threat.txt

5. Using the calculator under Formula, set formula to **[Enactment] + [Opportunity] + [Org_Identity] + [Threat]**

6. To get your results, click "Analyze". The first table you see should be what 
is shown in the ResultsToExpect folder
