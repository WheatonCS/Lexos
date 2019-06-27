# Rolling Window Analysis Test

This function makes a graph that shows the frequency of strings or words or reg-ex

*Test Files:* BeowulfFullLines.txt

*Result Files:* results_rollingAverage.png, results_rollingWords.png, 
results_rollingWords.png, results_Regex.png, results_countByLines.png, 
results_milestones.png, results_blackAndWhite.png, 
results_showIndividualPoints.png

Unless otherwise noted, all examples for Rolling Window use calculation type "Rolling Average"

## Test Rolling Average Settings

1. Upload test files:
    - BeowulfFullLines.txt
    
2. Under the "Prepare" menu scrub BeowulfFullLines.txt with default settings and click "Apply"
    - Make Lowercase
    - Remove Digits
    - Remove Punctuation

3. Under the "Visualize" menu select "Rolling Window"

4. Set Search Terms "ð,þ" and select "Strings"

5. Set Size of Window to 1000

6. Keep all other settings as Default

7. Click "Generate"
	
Results:
- results_rollingAverage.png


## Test Rolling Ratio Settings

1. Upload test files:
    - BeowulfFullLines.txt
    
2. Under the "Prepare" menu scrub BeowulfFullLines.txt with default settings and click "Apply"
    - Make Lowercase
    - Remove Digits
    - Remove Punctuation

3. Under the "Visualize" menu select "Rolling Window"

4. Under "Calculation Type" select "Rolling Ratio"

5. Set Search Terms "ð"/"þ" and select "Strings"

5. Set Size of Window to 1000

6. Keep all other settings as Default

7. Click "Generate"
	
Results:
- results_rollingRatio.png

## Test Search Terms Words

1. Upload test files:
    - BeowulfFullLines.txt
    
2. Under the "Prepare" menu scrub BeowulfFullLines.txt with default settings and click "Apply"
    - Make Lowercase
    - Remove Digits
    - Remove Punctuation

3. Under the "Visualize" menu select "Rolling Window"

4. Set Search Terms "wæs"

5. Set Size of Window to 1000

6. Keep all other settings as Default

7. Click "Generate"
	
Results:
- results_rollingWords.png

## Test Search Terms Words

1. Upload test files:
    - BeowulfFullLines.txt
    
2. Under the "Prepare" menu scrub BeowulfFullLines.txt with default settings and click "Apply"
    - Make Lowercase
    - Remove Digits
    - Remove Punctuation

3. Under the "Visualize" menu select "Rolling Window"

4. Set Search Terms  "^wear.*" and select "Regex"

5. Set Size of Window to 1000

6. Keep all other settings as Default

7. Click "Generate"
	
Results:
- results_Regex.png


## Test Count by Lines

1. Upload test files:
    - BeowulfFullLines.txt
    
2. Under the "Prepare" menu scrub BeowulfFullLines.txt with default settings and click "Apply"
    - Make Lowercase
    - Remove Digits
    - Remove Punctuation

3. Under the "Visualize" menu select "Rolling Window"

4. Set Search Terms  "ð,þ" and select "Strings"

5. Set Size of Window to 100 and select "Lines"

6. Keep all other settings as Default

7. Click "Generate"
	
Results:
- results_countByLines.png


## Test Document has Milestones

1. Upload test files:
    - BeowulfFullLines.txt
    
2. Under the "Prepare" menu scrub BeowulfFullLines.txt with default settings and click "Apply"
    - Make Lowercase
    - Remove Digits
    - Remove Punctuation

3. Under the "Visualize" menu select "Rolling Window"

4. Set Search Terms  "ð,þ" and select "Strings"

5. Set Size of Window to 1000

6. Under "Display" select "Milestone" and enter "grendle"

7. Keep all other settings as default

8. Click "Generate"
	
Results:
- results_milestones.png


## Test Black and white only

1. Upload test files:
    - BeowulfFullLines.txt
    
2. Under the "Prepare" menu scrub BeowulfFullLines.txt with default settings and click "Apply"
    - Make Lowercase
    - Remove Digits
    - Remove Punctuation

3. Under the "Visualize" menu select "Rolling Window"

4. Set Search Terms  "ð,þ" and select "Strings"

5. Set Size of Window to 1000

6. Under "Display" select "Black and White"

7. Keep all other settings as default

8. Click "Generate"
	
Results:
- results_blackAndWhite.png


## Test Show individual points

1. Upload test files:
    - BeowulfFullLines.txt
    
2. Under the "Prepare" menu scrub BeowulfFullLines.txt with default settings and click "Apply"
    - Make Lowercase
    - Remove Digits
    - Remove Punctuation

3. Under the "Visualize" menu select "Rolling Window"

4. Set Search Terms  "ð,þ" and select "Strings"

5. Set Size of Window to 1000

6. Under "Display" select "Show Individual Points"

7. Keep all other settings as default

8. Click "Generate"
	
Results:
- results_showIndividualPoints.png
