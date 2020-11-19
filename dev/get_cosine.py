import pandas as pd
import fasttext.util
from gensim.models.wrappers import FastText

from aux_functions import add_cosine_sim, add_combinations #Sara's functions to process the data


### Load data ###
df = pd.read_csv('../data/local/df_all_raw.csv') #raw data with single column of concepts


### Manage data ###
# keep only relevant columns
df = df[['Concepticon_ID','Concepticon_Gloss']].copy()
# remove duplicates
df = df.drop_duplicates()

# create column with word count
df['totalwords'] = df['Concepticon_Gloss'].str.count(' ') + 1
# delete columns with more than one word
df = df.drop(df[df.totalwords > 1].index)
# delete column with word count
del df['totalwords']

# reset index
df = df.reset_index(drop=True)

# lowercase
df['Concepticon_Gloss'] = df['Concepticon_Gloss'].str.lower()

#df=df[:20] #remove comment to reduce size of df 


### Load model ###
fasttext.util.download_model('en', if_exists='ignore')  # English
model = FastText.load_fasttext_format('cc.en.300') #load crawl corpus from fasttext


### Process data ###
comb_df = add_combinations(df,'Concepticon_Gloss','Concepticon_Gloss_2')
# comb_df['Concepticon_Gloss'][0]='kjhh' # remove comment to insert oov word
cosine_df = add_cosine_sim(comb_df,'Concepticon_Gloss','Concepticon_Gloss_2',model)


### Write new data frame ###
#df.to_csv('../data/nw/freqs_and_sims_analysis2_clics.csv',index=False,index_label=False)
