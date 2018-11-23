def least_satisfaction(preferences,rec):
    score=0
    for i in range(len(preferences)):
        attrs=preferences.iloc[i]
        score=min(score,attrs.dot(rec))
    return(score)

def avg_satisfaction(preferences,rec):
    score=0
    for i in range(len(preferences)):
        attrs=preferences.iloc[i]
        score+=attrs.dot(rec)
    return(score/len(preferences))