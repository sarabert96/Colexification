def add_cosine_sim(df,col1,col2,ft_model):
	"""
	Enriches dataframe with cosine similarity
	Input: a dataframe, two column names, and a fastText mdodel
	Output: The inputted dataframe with a new column with cosine similarities
	"""
	
	with open('logs/oov_log.txt', 'a+'):
		#query the model and if there is an oov word write that word to oov_log.txt and move to the next word
		df['cosine_sim'] = df.apply(lambda row: model.similarity(row.concept1, row.concept2), axis=1) #add column with cosine sims row-wise

	return df

def add_combinations(df,col1,new_col_name):
	"""
	Enriches dataframe by adding all combinations of col1 as new_col_name
	Input: a dataframe, a existing column name, and a new column name to which to add all combinations
	Output: The inputted dataframe with a new column with all combinations to col 1
	"""

	return new_dataframe