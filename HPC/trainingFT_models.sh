#!/bin/bash

#SBATCH --gres=gpu:1
#SBATCH --mem=6g
#SBATCH -p high
#SBATCH -o ./log_cluster/%J.%N.out
#SBATCH -e ./log_cluster/%j.%N.err

module load Miniconda3 

source /homedtic/sbertoldo/project/anaconda3/etc/profile.d/conda.sh # change environment folder

conda activate ftenv # name of the environment

date

# change the window sizes if necessary
# change folders
for i in 1 2 3 5 7 10 20 50
do
   echo "Training model with window size $i"
   fasttext skipgram -input /homedtic/sbertoldo/data/wikimedia/20210419/wikiExtractorOut/AA/clear_wiki_00 -output models/wiki_$i -ws $i
   date
done
