# Colexification
### Traineeship Erasmus

In this repository you can find the code of the Colexification project implemented with COLT group of University of Barcelona.

**List of files:**

00_DataCollection: writes a CSV with the data from CLICS3 (out df_all_raw.csv) <br/>
01_DataUnderstanding: inspect the CSV file <br/>
02_DataCleaning: remove diachronic varieties, multiword concepticons, lowercase all (out df_all_ok.csv) <br/>
03_CreateColex: creates a dataframe of colexifications (out df_colexifications.csv) <br/>
04_BootstrapProbabilities does a bootstrapping (100 cycles) and for every cycle it calculates the probability of finding a specific colexification in any of the families (out statistics_time.txt, listBoot.txt) <br/>
06_AnalysisBootCosine: analyze the distribution of probabilities calculated from the bootstrapped code, and the cosine values for every pair of that bootstrapped cycle

**DATA**

The Data can be downloaded running 00_DataCollection

In every file there is a link to download the file from Google Drive folder. Change that link (if necessary) with correct one.

**CODE**

The files are in notebook format, compiled with Google Colab.

