import pandas as pd
import numpy as np
def get_preference_score(user_id,user_df,review_df,business_df):
	'''
	params: user_id: The user-id of the user in question
			user_df: The user dataframe
			review_df: The review dataframe
			business_df: The business dataframe
	returns: The preference score for each attribute for the user
	'''
	user_reviews = review_df[review_df.user_id==user_id]
	user_stars = user_reviews.stars    
	user_stars=user_stars.median()    
	user_reviews = user_reviews.loc[user_reviews.stars>=user_stars]
	businesses_reviewed = business_df[business_df.business_id.isin(user_reviews.business_id)]
	preference_scores=businesses_reviewed.mean()
	return(dict(preference_scores))

def get_preferences(user_df,review_df,business_df):
	'''
	params: user_df: The user dataframe
			review_df: The review dataframe
		rb	business_df: The business dataframe
	returns: An n_users x n_attributes matrix containing preferences for each user for each attribute
	'''
	df_pref = pd.DataFrame(columns=list(business_df.columns)+['user_id'])	
	u_id=user_df['user_id']
	
	for i in u_id:
		pref=get_preference_score(i,user_df,review_df,business_df)
		pref['user_id']=i
		df_pref=df_pref.append(pref,ignore_index=True)

	return(df_pref)