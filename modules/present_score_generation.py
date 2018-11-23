import datetime
import pandas as pd
import numpy as np
from similarity import Similarity
from sklearn.metrics.pairwise import cosine_similarity

def getKRecentReviews(review_df, business_id, K,valid_users):
	'''
	params: review_df: The user dataframe
			business_id: The business id for the business being queried
			K: The number of recent reviews to fetch
			valid_users: The set of valid user_ids
	returns: The K most recent reviews of a restaurant provided they are timestamped later than Jan 1st 2012
	'''
	rel_reviews = review_df.loc[(review_df['business_id'] == business_id) & (review_df['user_id'].isin(valid_users))]
	recent_reviews = rel_reviews.sort_values('date', ascending = False).head(K)
	rev=pd.DataFrame(columns=review_df.columns)
	for i in range(len(recent_reviews)):
		d=datetime.datetime.strptime(recent_reviews.iloc[i]['date'],"%Y-%m-%d")
		if(d.year>2010):
			rev=rev.append(recent_reviews.iloc[i],ignore_index=True)
	return (rev,rev.empty)


def calculatePresentScore(user_df, review_df, user_id, business_id, user_sim):
	'''
	params: user_df: The user dataframe
			review_df: The review dataframe
			user_id: The user id of the user for whom a current rating is being computed
			business_id: The id of the business for which the rating is being computed
			user_sim: The similarity object containing the similarity matrix and a mapping between user ids and an integer 
	returns: The current rating for a user-restaurant pair
	'''
	K = 20
	recent_reviews,exists = getKRecentReviews(review_df, business_id, K,user_sim.mapping.keys())
	if(not(exists)):
		sim = []
		ratings = []

		for index, row in recent_reviews.iterrows():
			rating = row['stars'] - user_df.loc[user_df['user_id'] == row['user_id']]['average_stars'].values[0]
			similarity = user_sim.getSimilarity(row['user_id'],user_id)
			sim.append(similarity)
			ratings.append(rating)

		sim.append(1)
		ratings.append(review_df.loc[(review_df.user_id==user_id) & (review_df.business_id==business_id)].stars.values[0])
		pres_rating = sum(list(map(lambda x,y:x*y,sim,ratings)))/sum(sim)
		user_mean=(review_df.loc[review_df.user_id==user_id].stars).mean()
		return(pres_rating+user_mean)

	return(review_df.loc[(review_df.user_id==user_id) & (review_df.business_id==business_id)].stars)

def get_present_score_mat(user_df,review_df,business_df,preference_df,user_id):
	'''
	params: user_df: The user dataframe
			review_df: The review dataframe
			business_df: The business dataframe
			preference_df: The preference dataframe
	returns: An (n_users x n_restaurant) present score matrix 
			(entries are 0 for restaurants that haven't been reviewed by a user)
	'''

	user_map=dict(zip(preference_df.user_id,range(len(preference_df))))
	user_sim=cosine_similarity(preference_df.drop(['user_id'],axis=1))
	user_similarity=Similarity(user_sim,user_map)

	valid_businesses=business_df['business_id'].unique()
	valid_users=user_id

	present_score=np.zeros((len(valid_users),len(valid_businesses)))
	for i in range(len(valid_users)):
		for j in range(len(valid_businesses)):
			check=review_df[(review_df.user_id==valid_users[i])&(review_df.business_id==valid_businesses[j])]
			if(check.empty):
				present_score[i][j]=0
			else:
				present_score[i][j]=calculatePresentScore(user_df,review_df,valid_users[i],valid_businesses[j],user_similarity)
	return(present_score)
