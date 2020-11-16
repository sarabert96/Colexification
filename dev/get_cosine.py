import pandas as pd
import fasttext.util
from gensim.models.wrappers import FastText

from aux_functions import add_cosine_sim, add_combinations #Sara's functions to process the data


### Load data ###
df = pd.read_csv('../data/local/df_all_raw.csv') #raw data with single column of concepts


### Load model ###
fasttext.util.download_model('en', if_exists='ignore')  # English
model = FastText.load_fasttext_format('cc.en.300') #load crawl corpus from fasttext


### Process data ###
comb_df = add_combinations(df)
cosine_df = add_cosine_sim(comb_df,'column_1','column_2',model)


### Write new data frame ###
#df.to_csv('../data/nw/freqs_and_sims_analysis2_clics.csv',index=False,index_label=False)
