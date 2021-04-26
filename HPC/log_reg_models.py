# The file applies the Logistic Regression model on the output of the bootstraps
# To calculate the cosine similarity we use the FastText model --> change the model based on the window size

import fasttext
import itertools
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
import time
import random
import pandas as pd
import numpy as np


def cos_sim(a, b):
	"""Takes 2 vectors a, b and returns the cosine similarity according 
	to the definition of the dot product
	"""
	dot_product = np.dot(a, b)
	norm_a = np.linalg.norm(a)
	norm_b = np.linalg.norm(b)
	return dot_product / (norm_a * norm_b)


# function to write in file
def log(w):
  with open('oov_log.txt', 'a+') as file:
    file.write(w)


# function to handle oov word exception
def trySimilarity(w1, w2, default, model):
  # calculate cosine similarity between two vectors if those exists in the model, else return default --> ft deals with OOV but this avoid errors
  try:
    v1 = model.get_sentence_vector(w1)
  except:
    log(w1)
    return default
  try:
    v2 = model.get_sentence_vector(w2)
  except:
    log(w2)
    return default
  return cos_sim(v1, v2)


def add_cosine_sim(df,col1,col2,ft_model):
  """
  Enriches dataframe with cosine similarity
  Input: a dataframe, two column names, and a fastText mdodel
  Output: The inputted dataframe with a new column with cosine similarities
  """

  #query the model and if there is an oov word write that word to oov_log.txt and move to the next word

  #add column with cosine sims row-wise

  df['Cosine'] = df.apply(lambda row: trySimilarity(row[col1], row[col2], 0, ft_model), axis=1) 

  return df
  
  
  
def timer(start,end):
  hours, rem = divmod(end-start, 3600)
  minutes, seconds = divmod(rem, 60)
  print('TIME: '+"{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))
  print('\n')

def calculate_logreg_bal(nB, ft):  
  
  print ("Running calculate_logreg_bal function")
  start_time = time.time()

  listLogReg = []


  for k in range (nB):
    nBoot = k

    print ("Creating dataframe from bootstrap cicle")
    df = pd.DataFrame(lBoot[nBoot], columns=['Colex_pair','Concept1','Concept2', 'Prob']) # to save in df
    df = df.sort_values(by=['Prob'])
    df = df.reset_index(drop = True)

    # obtain cosine values from model
    print("Obtaining cosine similarity from model")
    add_cosine_sim(df,'Concept1','Concept2', ft)

    # assign 1 to the 2% entries with highest probability
    totN = df.shape[0]
    selected = round(totN * 0.02)
    df ['Colex_bool'] = 0
    df.loc[( totN - selected) : ,'Colex_bool'] = 1

    # select the same number of 0 and 1 pairs --> balance
    g = df.groupby('Colex_bool')
    g = pd.DataFrame(g.apply(lambda x: x.sample(g.size().min()).reset_index(drop=True)))

    X = g[['Cosine']]
    y = g['Colex_bool']

    print("Calculating logistic regression scores")
    for i in range(10):
      X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=i)
      logreg = LogisticRegression()
      logreg.fit(X_train, y_train)
      y_pred = logreg.predict(X_test)
      f1 = round(f1_score(y_test,y_pred, average='macro'), 2)
      newEl = [nBoot, i, f1] # row: number of boot, random_state, f1 result
      listLogReg.append(newEl)

    print("Computation finished for boot number ", k, '\n')
    timer(start_time, time.time())

  return listLogReg


def calculate_logreg_un(nB, ft):  
  
  print ("Running calculate_logreg_un function")
  start_time = time.time()

  listLogReg_un = []


  for k in range (nB):
    nBoot = k

    print ("Creating dataframe from bootstrap cicle")
    df = pd.DataFrame(lBoot[nBoot], columns=['Colex_pair','Concept1','Concept2', 'Prob']) # to save in df
    df['Colex_bool'] = 1 # all the existing colexifications are real

    real_col = set(list(df['Colex_pair'])) # remove duplicates

    # create list with single items
    real_col_l = [item for t in real_col for item in t]
    real_col_l = list(set(real_col_l)) # delete duplicates

    # create unattested colexifications
    print ("Creating unattested colexifications")
    totN = df.shape[0]
    un_col = []
    for i in range (totN):
      while True:
        el1 = random.choice(real_col_l)
        el2 = random.choice(real_col_l)
        while el1 == el2:
          el2 = random.choice(real_col_l)
        supp_t = (el1, el2)
        if supp_t not in real_col: # fail condition
          un_col.append(supp_t) # append only tuple that is not in real ones
          break

    # create dataframe with 0 values: unattested colexifications
    df_un = pd.DataFrame(un_col, columns =['Concept1', 'Concept2'])
    df_un['Colex_pair'] = un_col
    df_un['Colex_bool'] = 0

    # join two dataframes
    print ("Ultimated dataframe with 0 and 1 values")
    df = df.append(df_un)

    # obtain cosine values from model
    print("Obtaining cosine similarity from model")
    add_cosine_sim(df,'Concept1','Concept2', ft)

    # Logistic Regression
    X = df[['Cosine']]
    y = df['Colex_bool']

    print("Calculating logistic regression scores")
    for i in range(10):
      X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=i)
      logreg = LogisticRegression()
      logreg.fit(X_train, y_train)
      y_pred = logreg.predict(X_test)
      f1 = round(f1_score(y_test,y_pred, average='macro'), 2)
      newEl = [nBoot, i, f1] # row: number of boot, random_state, f1 result
      listLogReg_un.append(newEl)

    print("Computation finished for boot number ", k, '\n')
    timer(start_time, time.time())

  return listLogReg_un

model_names = ["result/wiki_standard.bin", "result/wiki_3.bin", "result/wiki_10.bin"] # names of models

for m in model_names:

  ft = fasttext.load_model(m) # name of the model
  with open("listBoot.txt", "rb") as fp:   # Unpickling from the txt
    lBoot = pickle.load(fp)

  random.seed(70)

  #values = calculate_logreg_bal(len(lBoot), ft) # calling the function
  values = calculate_logreg_bal(3, ft) # or change number

  df_logreg_bal = pd.DataFrame(values, columns=['boot_df', 'random_state', 'f1_score'])
  name_df_bal = "df_logreg/df_logreg_bal_" + m[7:-4] + ".csv"
  df_logreg_bal.to_csv(name_df_bal, index = False)

  #values_un = calculate_logreg_un(len(lBoot), ft) # calling the function
  values_un = calculate_logreg_un(3, ft) # or change number

  df_logreg_un = pd.DataFrame(values_un, columns=['boot_df', 'random_state', 'f1_score'])
  name_df_un = "df_logreg/df_logreg_un_" + m[7:-4] + ".csv"

  df_logreg_un.to_csv(name_df_un, index = False)