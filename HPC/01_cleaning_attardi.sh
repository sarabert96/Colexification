#!/bin/bash

#SBATCH --gres=gpu:1
#SBATCH --mem=6g
#SBATCH -p high
#SBATCH -o ./log_cluster/%J.%N.out
#SBATCH -e ./log_cluster/%j.%N.err

module load Miniconda3 

source /homedtic/sbertoldo/project/anaconda3/etc/profile.d/conda.sh # change environment folder

conda activate ftenv # name of environment

cd /homedtic/sbertoldo/data/wikimedia/20210419 # change folder where wikipedia dump is

echo Start cleaning WikiExtractor

date

wikiextractor -o wikiExtractorOut -b 1G --no-templates enwiki-latest-pages-articles.xml.bz2

date

echo Finish