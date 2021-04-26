#!/bin/bash

#SBATCH --gres=gpu:1
#SBATCH --mem=6g
#SBATCH -p high
#SBATCH -o ./log_cluster/%J.%N.out
#SBATCH -e ./log_cluster/%j.%N.err

module load Miniconda3 

source /homedtic/sbertoldo/project/anaconda3/etc/profile.d/conda.sh # change environment folder

conda activate ftenv # name of environment

cd /homedtic/sbertoldo/data/wikimedia/20210419/wikiExtractorOut/AA  # change folder

date

declare -a wikis # create array

for file in *
do
    wikis+=("${File[@]}" "$file") # append element in folder to array
done

# skipping the first element which is the script 
# NB!!! in the array there are ALL the files in the folder, so also the script with the code!!
for f in "${wikis[@]:1}" 
do
    echo "Cleaning file $f"
    python cleaning_wiki.py $f
done

date

echo "FINISH"