import pandas as pd
import pickle
import numpy as np
from similarity import Similarity

def make_user_rest_matrix(mat, business_df_v, userids, cosmat):
    """
    Function to make the user-restaurant rating matrix with true and imputed values
    params:
    mat - numpy ndarray of user x restaurant present scores
    buisness_df_v - dataframe of restaurants with only boolean attributes
    userids - list of userids in the group
    cosmat -  Similarity object for restaurant-restaurant similarity

    returns : user-restaurant rating matrix with all imputed values
    """

    for i in range(len(userids)):
        valid_indices = np.nonzero(mat[i])[0]
        to_do = np.where(mat[i]==0)[0]
        for idx in to_do:
            pres_business = [business_df_v.loc[idx].values]
            sum_sims = 0
            imputed_sum = 0
            for vidx in valid_indices:
                imputed_sum += mat[i][vidx]*cosmat.getSimilarity(idx, vidx)
                sum_sims += cosmat.getSimilarity(idx, vidx)
            try:
                mat[i][idx] = imputed_sum/sum_sims
            except:
                print("No valid indices for user", userids[i])

    return mat