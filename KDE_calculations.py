import pandas as pd
import calendar, datetime
import math
import sys
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.neighbors import KernelDensity
from sklearn.model_selection import GridSearchCV

def CalcKde(points,discipline):

    bandwidths = np.logspace(-1, 1, 20)
    
    param_grid = {'bandwidth': bandwidths}

    # Initialize GridSearchCV
    grid = GridSearchCV(KernelDensity(), param_grid, cv=min(5, len(points)))
    grid.fit(points)

    # Get the best bandwidth
    best_bandwidth = grid.best_estimator_.bandwidth
    

    return KernelDensity(kernel="tophat", bandwidth=best_bandwidth).fit(points)

def KDE_for_athlete(athletes_points):
    athletes_kde={}
    for athlete in athletes_points:
        if athlete not in athletes_kde:
            athletes_kde[athlete]={}
        for discipline in athletes_points[athlete]:
            if(len(athletes_points[athlete][discipline])>1 and discipline != 'lead'):
                modify_scores_based_on_cuantity(athletes_points[athlete][discipline],discipline)
                if discipline == 'speed':
                    athletes_kde[athlete][discipline]=CalcKde(np.array(athletes_points[athlete][discipline]).reshape(-1,1),discipline);
                    continue;
                athletes_kde[athlete][discipline]=CalcKde(athletes_points[athlete][discipline],discipline);
    return athletes_kde

def modify_scores_based_on_cuantity(points,discipline):
    
    
    if discipline=='boulder':
        alpha=2
        pondVal_first_two_comp=(1-alpha/len(points))
        pondVal_last_two_comp=(1+alpha/len(points))
        for vector in points:
            for i in range(2):
                vector[i]= vector[i]*pondVal_first_two_comp
                vector[i+2]= vector[i+2]*pondVal_last_two_comp
    else:
        alpha=4
        pondVal=(1+alpha/len(points))
        for time in points:
            time=time*pondVal
    