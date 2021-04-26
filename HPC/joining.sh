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

touch corpus_wiki # create new empty file

declare -a wikis # create empty array

for file in *
do
    wikis+=("${File[@]}" "$file") # append every element in folder to array
done

for f in "${wikis[@]}" 
do
    if [[ $f == *clear* ]]; # check to consider only clear files in the folder
    then
        echo "Joining file $f"
	cat $f >> corpus_wiki # concatenate files
    fi    
done

date

echo "FINISH"