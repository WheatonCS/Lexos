# Top Words

This function finds the Z-score of words in texts

*Test Files:* Melville_MobyDick.txt, Pride_and_Prejudice.txt

*Result Files:* results_defaults.csv, results_topOutliers.csv, 
results_docToClass.csv, results_classToClass.csv


## Test Default Settings

1. Upload all files:
    - Melville_MobyDick.txt, 
    - Pride_and_Prejudice.txt

2. Under the "Analyze" menu, click "Top Words"

3. Change **NO** settings  

4. Click "Generate"
	
Results:
- results_defaults.csv


## Test Tokenize by Characters

1. Upload all files:
    - Melville_MobyDick.txt, 
    - Pride_and_Prejudice.txt

2. Under the "Analyze" menu, click "Top Words"

3. Under "Tokenize" select "By Characters"

4. Keep all other setting as default

5. Click "Generate"
	
Results:
- results_byCharacters.csv


## Test Compare Each Document to Other Classes

1. Upload all files:
    - Melville_MobyDick.txt, 
    - Pride_and_Prejudice.txt

2. Go to the "Manage" page. 

3. Right click on Melville_MobyDick and click "Edit Class". Set the class to "Class1" 

4. Right click on Pride_and_Prejudice and click "Edit Class". Set the class to "Class2" 

5. Under the "Analyze" menu, click "Top Words"
    
6. Select "Each document to other classes"

7. Keep all other settings as default

8. Click "Generate"
	
Results:
- results_docToClass.csv


## Test Compare Class to Other Classes

1. Upload all files:
    - Melville_MobyDick.txt, 
    - Pride_and_Prejudice.txt

2. Go to the "Manage" page. 

3. Right click on Melville_MobyDick and click "Edit Class". Set the class to "Class1" 

4. Right click on Pride_and_Prejudice and click "Edit Class". Set the class to "Class2" 

5. Under the "Analyze" menu, click "Top Words"
    
6. Select "Each class to other classes"

7. Keep all other settings as default

8. Click "Generate"
	
Results:
- results_classToClass.csv
