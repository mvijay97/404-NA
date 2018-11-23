import numpy as np
def aggregate_scores(business_ratings):
    scores=np.sum(business_ratings,axis=0)
    scores=scores/business_ratings.shape[0]
    return(np.argsort(scores)[-1])

def get_ideal_restaurant(constraints, top_pick):
    for key in constraints.keys():
        top_pick[key]=constraints[key]
    return(top_pick)