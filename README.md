# Colexification
### Traineeship Erasmus

In this repository you can find the code of the Colexification project implemented with COLT group of University of Barcelona.

**List of files:**

00_DataCollection: writes a CSV with the data from CLICS3 (out df_all_raw.csv) <br/>
01_DataUnderstanding: inspect the CSV file <br/>
02_DataCleaning: remove diachronic varieties, multiword concepticons and lowercase every concepticon (out df_all_ok.csv) <br/>
03_CreateColex: creates a dataframe of colexifications (out df_colexifications.csv) <br/>
04_BootstrapProbabilities does a bootstrapping (100 cycles) and for every cycle it calculates the probability of finding a specific colexification in any of the families (out statistics_time.txt, listBoot.txt) <br/>
05_gettingCosines: given the colexifications dataframe (out of 03), it returns another dataframe with the calculation of cosine similarity between a pair of concepts (a colexification). Uses the pre-trained version of FastText. (out df_colex_cosines.csv) <br/>
06_AnalysisBootCosine: analyze the distribution of probabilities calculated from the bootstrapped code, and the cosine values for every pair of that bootstrapped cycle <br/>
07_LogisticRegression_3ver: 3 versions of application of Logistic Regression on the output of only one cycle of the bootstrap <br/>
07b_gettingCosines_support: the file uses the FastText model to calculate the cosine similarity values. Serves as a support for the file 07 <br/>


**DATA**

The Data can be downloaded running 00_DataCollection

In every file there is a link to download the file from Google Drive folder. Change that link (if necessary) with correct one.

**CODE**

The files are in notebook format, compiled with Google Colab.

