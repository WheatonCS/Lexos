# Hierarchical Clustering

This function clusters the texts together using a distance metric to show 
similarity between texts

*Test Files:* HenryWP_ThePirate.txt, Irving_ripVanWrinkle.txt, 
Lippard_BelOfPrairieEden.txt, Melville_MobyDick.txt, 
Poe_FallOfHouseUsher_1839.txt

*Result Files:* results_defaults.png, results_byCharacters.png, 
results_braycurtis.png, results_leftOrientation.png, results_culling.png,
results_rawCounts.png



## Test Default Settings

0. UPLOAD ALL TEST FILES:
    - HenryWP_ThePirate.txt
    - Irving_ripVanWrinkle.txt, 
    - Lippard_BelOfPrairieEden.txt
    - Melville_MobyDick.txt, 
    - Poe_FallOfHouseUsher_1839.txt

1. Hierarchical Clustering 
	- Change **NO** settings  
	
Results:
- results_defaults.png


## Test Tokenize by Characters

0. UPLOAD ALL TEST FILES:
    - HenryWP_ThePirate.txt
    - Irving_ripVanWrinkle.txt, 
    - Lippard_BelOfPrairieEden.txt
    - Melville_MobyDick.txt, 
    - Poe_FallOfHouseUsher_1839.txt

1. Hierarchical Clustering 
	- Change Tokenize to "by Characters"
	- Keep all other settings as default
	
Results:
- results_byCharacters.png


## Test different Distance Metric

0. UPLOAD ALL TEST FILES:
    - HenryWP_ThePirate.txt
    - Irving_ripVanWrinkle.txt, 
    - Lippard_BelOfPrairieEden.txt
    - Melville_MobyDick.txt, 
    - Poe_FallOfHouseUsher_1839.txt

1. Hierarchical Clustering 
	- Change Distance Metric to Braycurtis 
	- Keep all other settings as default
	
Results:
- results_braycurtis.png


## Test different Leaves Orientation

0. UPLOAD ALL TEST FILES:
    - HenryWP_ThePirate.txt
    - Irving_ripVanWrinkle.txt, 
    - Lippard_BelOfPrairieEden.txt
    - Melville_MobyDick.txt, 
    - Poe_FallOfHouseUsher_1839.txt

1. Hierarchical Clustering 
	- Change Dendrogram Leaves Orientation to Left
	- Keep all other settings as default
	
Results:
- results_leftOrientation.png


## Test Culling Options, Culling

0. UPLOAD ALL TEST FILES:
    - HenryWP_ThePirate.txt
    - Irving_ripVanWrinkle.txt, 
    - Lippard_BelOfPrairieEden.txt
    - Melville_MobyDick.txt, 
    - Poe_FallOfHouseUsher_1839.txt

1. Hierarchical Clustering 
	- Select Culling Options, Culling
	- Change Must be in Documents to 5
	- Keep all other settings as default
	
Results:
- results_culling.png


## Test Normalize, Raw Counts

0. UPLOAD ALL TEST FILES:
    - HenryWP_ThePirate.txt
    - Irving_ripVanWrinkle.txt, 
    - Lippard_BelOfPrairieEden.txt
    - Melville_MobyDick.txt, 
    - Poe_FallOfHouseUsher_1839.txt

1. Hierarchical Clustering 
    - Select Normalize, Raw Counts
	- Keep all other settings as default
	
Results:
- results_rawCounts.png
