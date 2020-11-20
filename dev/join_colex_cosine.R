#This script creates a data frame of colexifications based on the raw CLICS data.
#It then joins this data with d_cosines, a dataframe containing two columns of words/glosses and another one with their cosine_similarity
#Rows for which there is no cosine_sim value are dropped  (e.g., multi-word expressions or those that are OOV)
library(dplyr)
library(readr)
library(tidyr)


if (!file.exists("../data//local/df_colexifications.csv")){ #if the file doesnt exist: compute it
  df <- read_csv('../data/local/df_all_raw.csv') #original raw CLICS file
  d_colex <- df %>%
    select(clics_form,Concepticon_ID,Glottocode,Concepticon_Gloss) %>%
    drop_na() %>%
    unique()

  dd <- inner_join(d_colex,d_colex,by=c("clics_form","Glottocode")) %>%
    filter(Concepticon_ID.x != Concepticon_ID.y) %>%
    unique()
  
  d_colex <- dd[!duplicated(lapply(as.data.frame(t(dd), stringsAsFactors=FALSE), sort)),]  #remove rows where Concepticon_ID1 and Concepticon_ID2 are permutations of each other 

  #Code colefixications with 1
  d_colex$colex <- rep(1,nrow((d_colex)))

  write_csv(d_colex,'../data//local/df_colexifications.csv')
} else { #if it exists: load it
  print('Loading pre-processed colexification df')
  d_colex <- read_csv('../data/local/df_colexifications.csv')
}

d_cosines <- read_csv('../data/local/cosines.csv')

d_colex <- d_colex %>%
      mutate(Concepticon_Gloss.x = tolower(Concepticon_Gloss.x), #lowering glosses to match to pre-processing done for fasttext
      	     Concepticon_Gloss.y = tolower(Concepticon_Gloss.y)) %>%
      left_join(d_cosines, by=c('Concepticon_Gloss.x' = 'Concepticon_Gloss', #matching to fasttext
      	                       'Concepticon_Gloss.y' = 'Concepticon_Gloss_2')) %>%
      drop_na() #drop rows for which there is no cosine similarity (e.g., multi-word expressions or those that are OOV)

write_csv(d_colex,'../data/local/df_colex_and_cosine.csv')