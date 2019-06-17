# Hierarchical Clustering

This function clusters the texts together using a distance metric to show 
similarity between texts

*Test Files:* HenryWP_ThePirate.txt, Irving_ripVanWrinkle.txt, 
Lippard_BelOfPrairieEden.txt, Melville_MobyDick.txt, 
Poe_FallOfHouseUsher_1839.txt

*Result Files:* results_defaults.png, results_byCharacters.png, 
results_braycurtis.png, results_leftOrientation.png, results_culling.png,
results_rawCounts.png

***

## Test Default Settings

1. Upload all test files:
    - HenryWP_ThePirate.txt
    - Irving_ripVanWrinkle.txt, 
    - Lippard_BelOfPrairieEden.txt
    - Melville_MobyDick.txt, 
    - Poe_FallOfHouseUsher_1839.txt

2. Under the "Analyze" menu, click "Dendrogram"

3. Change **NO** settings.

4. Click "Generate" 
	
Results:
- results_defaults.png


## Test Tokenize by Characters

1. Upload all test files:
    - HenryWP_ThePirate.txt
    - Irving_ripVanWrinkle.txt, 
    - Lippard_BelOfPrairieEden.txt
    - Melville_MobyDick.txt, 
    - Poe_FallOfHouseUsher_1839.txt

2. Under the "Analyze" menu, click "Dendrogram"

3. Under "Tokenize" select "By Characters"

4. Keep all other settings as default
	
5. Click "Generate"

Results:
- results_byCharacters.png


## Test different Distance Metric

1. Upload all test files:
    - HenryWP_ThePirate.txt
    - Irving_ripVanWrinkle.txt, 
    - Lippard_BelOfPrairieEden.txt
    - Melville_MobyDick.txt, 
    - Poe_FallOfHouseUsher_1839.txt

2. Under the "Analyze" menu, click "Dendrogram"

3. Change Distance Metric to Braycurtis 

4. Keep all other settings as default

5. Click "Generate"
	
Results:
- results_braycurtis.png


## Test different Leaves Orientation

1. Upload all test files:
    - HenryWP_ThePirate.txt
    - Irving_ripVanWrinkle.txt, 
    - Lippard_BelOfPrairieEden.txt
    - Melville_MobyDick.txt, 
    - Poe_FallOfHouseUsher_1839.txt

2. Under the "Analyze" menu, click "Dendrogram"

3. Change Orientation to Bottom

4. Keep all other settings as default
	
5. Click "Generate"

Results:
- results_bottomOrientation.png


## Test Culling Options, Culling

1. Upload all test files:
    - HenryWP_ThePirate.txt
    - Irving_ripVanWrinkle.txt, 
    - Lippard_BelOfPrairieEden.txt
    - Melville_MobyDick.txt, 
    - Poe_FallOfHouseUsher_1839.txt

2. Under the "Analyze" menu, click "Dendrogram"

3. Under "Cull", select "Must be in [ ] documents" and change it to 5

4. Keep all other settings as default

5. Click "Generate"
	
Results:
- results_culling.png


## Test Normalize, Raw Counts

1. Upload all test files:
    - HenryWP_ThePirate.txt
    - Irving_ripVanWrinkle.txt, 
    - Lippard_BelOfPrairieEden.txt
    - Melville_MobyDick.txt, 
    - Poe_FallOfHouseUsher_1839.txt

2. Under the "Analyze" menu, click "Dendrogram"

3. Under "Normalize" select "Raw"

4. Keep all other settings as default

5. Click "Generate"
	
Results:
- results_rawCounts.png
