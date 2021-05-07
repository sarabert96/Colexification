### HPC Files

This folder contains the files used in the High Performing Computing (HPC) of the University Pompeu Fabra.

The phases of work run on the HPC are:
1. download wikipedia dump
2. cleaning wikipedia corpus (various files are created)
3. joining every file of the corpus
4. training the models

The following phases (load the models and apply Logistic Regression models) were not run for a problem in the fasttext package inside the environment (the function get_sentence_vector() returns error. If you are willing to run the code, please first check whether the function works for you.)
