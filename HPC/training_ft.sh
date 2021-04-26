#!/bin/bash

#SBATCH --gres=gpu:1
#SBATCH --mem=6g
#SBATCH -p high
#SBATCH -o ./log_cluster/%J.%N.out
#SBATCH -e ./log_cluster/%j.%N.err

module load Miniconda3 

source /homedtic/sbertoldo/project/anaconda3/etc/profile.d/conda.sh # change environment folder

conda activate ftenv # name of environment

date

fasttext skipgram -input /homedtic/sbertoldo/data/wikimedia/20210419/wikiExtractorOut/AA/corpus_wiki -output result/wiki_standard
# change name and parameters for training

date