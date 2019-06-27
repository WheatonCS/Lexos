# Rolling Window Analysis Test

This function makes a graph that shows the frequency of strings or words por reg-ex

*Test Files:* BeowulfFullLines.txt

*Result Files:* results_rollingAverage.png, results_rollingWords.png, 
results_rollingWords.png, results_Regex.png, results_countByLines.png, 
results_milestones.png, results_blackAndWhite.png, 
results_showIndividualPoints.png


## Test Rolling Average Settings

0. UPLOAD  TEST FILES:
    BeowulfFullLines.txt
    
1. Scrub BeowulfFullLines.txt with default settings

2. Rolling Window
	- Set Search Pattern(s) to "ð, þ"
	- Set Size of Rolling Window to 1000
	- Keep all other settings as Default
	
Results:
- results_rollingAverage.png


## Test Rolling Ratio Settings

0. UPLOAD  TEST FILES:
    BeowulfFullLines.txt
    
1. Scrub BeowulfFullLines.txt with default settings

2. Rolling Window
	- Set Search Pattern(s) to "ð"/ "þ"
	- Set Size of Rolling Window to 1000
	- Keep all other settings as Default
	
Results:
- results_rollingRatio.png


## Test Search Terms Words

0. UPLOAD  TEST FILES:
    BeowulfFullLines.txt
    
1. Scrub BeowulfFullLines.txt with default settings

2. Rolling Window
	- Set Search Pattern(s) to "wæs"
	- Select Word(s)(Tokens)
	- Set Size of Rolling Window to 1000
	- Set Define Window to Count by words (tokens)
	- Keep all other settings as Default
	
Results:
- results_rollingWords.png


## Test Search Terms Words

0. UPLOAD  TEST FILES:
    BeowulfFullLines.txt
    
1. Scrub BeowulfFullLines.txt with default settings

2. Rolling Window
	- Set Search Pattern(s) to "^wear.*"
	- Select Regular Expression(s)
	- Set Size of Rolling Window to 1000
	- Set Define Window to Count by words (tokens)
	- Keep all other settings as Default
	
Results:
- results_Regex.png


## Test Count by Lines

0. UPLOAD  TEST FILES:
    BeowulfFullLines.txt
    
1. Scrub BeowulfFullLines.txt with default settings

2. Rolling Window
	- Set Search Pattern(s) to "ð, þ"
	- Set Size of Rolling Window to 100
	Set Define Window to Count by Lines
	- Keep all other settings as Default
	
Results:
- results_countByLines.png


## Test Document has Milestones

0. UPLOAD  TEST FILES:
    BeowulfFullLines.txt
    
1. Scrub BeowulfFullLines.txt with default settings

2. Rolling Window
	- Set Search Pattern(s) to "ð, þ"
	- Set Size of Rolling Window to 1000
	- Select Document has Milestones
	- Set Milestone Delimiter to "Grendle"
	- Keep all other settings as Default
	
Results:
- results_milestones.png


## Test Black and white only

0. UPLOAD  TEST FILES:
    BeowulfFullLines.txt
    
1. Scrub BeowulfFullLines.txt with default settings

2. Rolling Window
	- Set Search Pattern(s) to "ð, þ"
	- Set Size of Rolling Window to 1000
	- Select Black and White only 
	- Keep all other settings as Default
	
Results:
- results_blackAndWhite.png


## Test Show individual points

0. UPLOAD  TEST FILES:
    BeowulfFullLines.txt
    
1. Scrub BeowulfFullLines.txt with default settings

2. Rolling Window
	- Set Search Pattern(s) to "ð, þ"
	- Set Size of Rolling Window to 1000
	- Select Show individual points
	- Keep all other settings as Default
	
Results:
- results_showIndividualPoints.png
