# K-Means Clustering

This function clusters the texts together using K-Means to show 
similarity between texts

*Test Files:* HenryWP_ThePirate.txt, Irving_ripVanWrinkle.txt, 
Lippard_BelOfPrairieEden.txt, Melville_MobyDick.txt, 
Poe_FallOfHouseUsher_1839.txt

*Result Files:* results_defaults.png, results_byCharacters.png, 
results_numberOfClusters.png, results_2D_Scatter.png, results_3D_Scatter.png,
results_rawCounts.png, results_culling.png

***

## Test Default Settings

1. Upload all test files:
    - HenryWP_ThePirate.txt
    - Irving_ripVanWrinkle.txt, 
    - Lippard_BelOfPrairieEden.txt
    - Melville_MobyDick.txt, 
    - Poe_FallOfHouseUsher_1839.txt

2. Under the "Analyze" menu, click "K-Means"

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

2. Under the "Analyze" menu, click "K-Means"

3. Under "Tokenize" select "By Characters"

4. Keep all other settings as default
	
5. Click "Generate"

Results:
- results_byCharacters.png


## Test Number of Clusters

1. Upload all test files:
    - HenryWP_ThePirate.txt
    - Irving_ripVanWrinkle.txt, 
    - Lippard_BelOfPrairieEden.txt
    - Melville_MobyDick.txt, 
    - Poe_FallOfHouseUsher_1839.txt

2. Under the "Analyze" menu, click "K-Means"

3. Under "Options" change "Clusters" (K-Value) to 5

4. Keep all other settings as default

5. Click "Generate"
	
Results:
- results_numberOfClusters.png


## Test 2D scatter

1. Upload all test files:
    - HenryWP_ThePirate.txt
    - Irving_ripVanWrinkle.txt, 
    - Lippard_BelOfPrairieEden.txt
    - Melville_MobyDick.txt, 
    - Poe_FallOfHouseUsher_1839.txt

2. Under the "Analyze" menu, click "K-Means"

3. Under "Options" select "2D Scatter"

4. Keep all other settings as default

5. Click "Generate"
	
Results:
- results_2D_Scatter.png


## Test 3D scatter

1. Upload all test files:
    - HenryWP_ThePirate.txt
    - Irving_ripVanWrinkle.txt, 
    - Lippard_BelOfPrairieEden.txt
    - Melville_MobyDick.txt, 
    - Poe_FallOfHouseUsher_1839.txt

2. Under the "Analyze" menu, click "K-Means"

3. Under "Options" select "3D Scatter"

4. Keep all other settings as default

5. Click "Generate"
	
Results:
- results_3D_Scatter.png


## Test Culling Options, Culling

1. Upload all test files:
    - HenryWP_ThePirate.txt
    - Irving_ripVanWrinkle.txt, 
    - Lippard_BelOfPrairieEden.txt
    - Melville_MobyDick.txt, 
    - Poe_FallOfHouseUsher_1839.txt

2. Under the "Analyze" menu, click "K-Means"

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

2. Under the "Analyze" menu, click "K-Means"

3. Under "Normalize" select "Raw"

4. Keep all other settings as default

5. Click "Generate"
	
Results:
- results_rawCounts.png
