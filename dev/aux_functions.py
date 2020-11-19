import itertools
import pandas as pd

# function to write in file
def log(w):
  with open('logs/oov_log.txt', 'a+') as file:
    file.write(w)

def add_cosine_sim(df,col1,col2,ft_model):
  """
  Enriches dataframe with cosine similarity
  Input: a dataframe, two column names, and a fastText mdodel
  Output: The inputted dataframe with a new column with cosine similarities
  """

  # function to handle oov word exception
  def trySimilarity(w1, w2, default):
    try:
      ft_model[w1]
    except:
      log(w1)
      return 0
    try:
      ft_model[w2]
    except:
      log(w2)
      return default
    return ft_model.similarity(w1, w2)

  #query the model and if there is an oov word write that word to oov_log.txt and move to the next word
  #df['cosine_sim'] = df.apply(lambda row: model.similarity(row.concept1, row.concept2), axis=1) # Thomas baseline

  #add column with cosine sims row-wise

  df['cosine_sim'] = df.apply(lambda row: trySimilarity(row[col1], row[col2], 0), axis=1) 

  return df


def add_combinations(df,col1,new_col_name):
  """
  Enriches dataframe by adding all combinations of col1 as new_col_name
  Input: a dataframe, a existing column name, and a new column name to which to add all combinations
  Output: The inputted dataframe with a new column with all combinations to col 1
  """

  # create list of combinations
  comb=list(itertools.combinations(df[col1], 2))
  # create new df
  new_dataframe=pd.DataFrame()
  new_dataframe[[col1, new_col_name]]= pd.DataFrame(comb)

  # not added ID columns

  return new_dataframe
