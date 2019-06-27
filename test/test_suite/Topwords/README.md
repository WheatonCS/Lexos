# Topwords

This function finds the Z-score of words in texts

*Test Files:* Melville_MobyDick.txt, Pride_and_Prejudice.txt

*Result Files:* results_defaults.csv, results_topOutliers.csv, 
results_docToClass.csv, results_classToClass.csv


## Test Default Settings

0. UPLOAD ALL TEST FILES:
    - Melville_MobyDick.txt, 
    - Pride_and_Prejudice.txt

1. Topwords
	- Change **NO** settings  
	
Results:
- results_defaults.csv


## Test Tokenize by Characters

0. UPLOAD ALL TEST FILES:
    - Melville_MobyDick.txt, 
    - Pride_and_Prejudice.txt

1. Topwords
	- Select by Characters
	- Keep all other settings as default
	
Results:
- results_byCharacters.csv


## Test Compare each doc to other class

0. UPLOAD ALL TEST FILES:
    - Melville_MobyDick.txt, 
    - Pride_and_Prejudice.txt

1. Manage
    - Set class for Melville_MobyDick as "Class1"
    - Set class for Pride_and_Prejudice as "Class2"
    
2. Topwords
	- Select Compare each document to other class(es)
	- Keep all other settings as default
	
Results:
- results_docToClass.csv


## Test Compare class to other class

0. UPLOAD ALL TEST FILES:
    - Melville_MobyDick.txt, 
    - Pride_and_Prejudice.txt

1. Manage
    - Set class for Melville_MobyDick as "Class1"
    - Set class for Pride_and_Prejudice as "Class2"
    
2. Topwords
	- Select Compare each class to other class(es)
	- Keep all other settings as default
	
Results:
- results_classToClass.csv
