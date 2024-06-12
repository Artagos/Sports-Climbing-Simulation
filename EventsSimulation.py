import numpy as np
from heapImplementation import Item,PriorityArray,MaxHeap
from KDE_calculations import KDE_for_athlete,modify_scores_based_on_cuantity,CalcKde;
from functools import cmp_to_key
from dataReading import athletes_points;
import sys
import io



def simulate_event(athletes_kde, heap, discipline, comparison_function):
    
    athletes_sorted_per_score=[]
    
    for athlete in athletes_kde:
        if discipline not in athletes_kde[athlete]:
            continue;
        function = athletes_kde[athlete][discipline];
        score= function.sample(1)[0]
        if(discipline=='boulder'):
            score=np.clip(np.rint(score), 0, None).astype(int)
            if(score[0]>score[1]):
                score[1]=score[0]
            if(score[0]>score[2]):
                score[2]=score[0]
            if(score[1]>score[3]):
                score[3]=score[1]
        athletes_sorted_per_score.append({'name': athlete,'score': score})
    
    
    #qualifications fase
    athletes_sorted_per_score.sort(key=comparison_function);
    

    
    for index,athlete in enumerate(athletes_sorted_per_score):
        if(index==10):
            break
        function = athletes_kde[athlete['name']][discipline];
        score = function.sample(1)[0];
        if(discipline=='boulder'):
            score=np.clip(np.rint(score), 0, None).astype(int)
            if(score[0]>score[1]):
                score[1]=score[0]
            if(score[0]>score[2]):
                score[2]=score[0]
            if(score[1]>score[3]):
                score[3]=score[1]
        athlete['score']=score;
    
    #final athletes
    finals_athletes=sorted(athletes_sorted_per_score[:10], key=comparison_function)
    
    athletes_sorted_per_score[:10]=finals_athletes

        
    for index,athlete in enumerate(athletes_sorted_per_score):
        heap.increment_rank(athlete['name'], index, len(athletes_sorted_per_score))
    


        
    


def compare_vectors(player1, player2):
    """
    Compares two vectors of length 4 based on the specified rules: 
    *Boulder Criteria
    
    1. Compare first components.
    2. If equal, compare second components.
    3. If still equal, compare third components.
    4. If still equal, compare fourth components.

    Args:
        vec1 (np.ndarray): First vector of length 4.
        vec2 (np.ndarray): Second vector of length 4.

    Returns:
        int: -1 if vec1 is smaller, 1 if vec1 is larger, 0 if equal.
    """
    vec1=player1['score'];
    vec2=player2['score'];
    
    for i in range(2):
        if vec1[i] < vec2[i]:
            return 1
        elif vec1[i] > vec2[i]:
            return -1
    for i in range(2):    
        if vec1[i+2] < vec2[i+2]:
            return -1
        elif vec1[i+2] > vec2[i+2]:
            return 1
    return 0
    

# max_heap_boulder_men = MaxHeap()

# max_heap_boulder_women = MaxHeap()

# max_heap_speed_men = MaxHeap()

# max_heap_speed_women = MaxHeap()

# # print(athletes_points['men']['aiden yanev']['boulder'])
# # modify_scores_based_on_cuantity(athletes_points['men']['aiden yanev']['boulder'],'boulder')
# # print(athletes_points['men']['aiden yanev']['boulder'])
# # func=CalcKde(athletes_points['men']['aiden yanev']['boulder'],'boulder')
# # print(func)
# # print(func.sample(4))


# men_athletes_kde = KDE_for_athlete(athletes_points['men'])


# women_athletes_kde = KDE_for_athlete(athletes_points['women'])

# key_function = cmp_to_key(compare_vectors)


# ##simulate_event(men_athletes_kde,max_heap_boulder_men,'boulder',key_function)



# for i in range(0,1000):
#     simulate_event(men_athletes_kde,max_heap_boulder_men,'boulder',key_function)
#     simulate_event(women_athletes_kde,max_heap_boulder_women,'boulder',key_function)
    
#     simulate_event(men_athletes_kde,max_heap_speed_men,'speed',lambda x: x['score'])
#     simulate_event( women_athletes_kde, max_heap_speed_women,'speed',lambda x: x['score'])

# print('Boulder')
# for i in range(0,8):
#     athlete= max_heap_boulder_men.pop()
#     #                   Cantidad de veces en primer lugar
#     print(athlete.name,athlete.ranks[0])    

# print('mujeres')
#     #Top 8 de boulder femenino
# for i in range(0,8):
#     athlete= max_heap_boulder_women.pop()
#     #                   Cantidad de veces en primer lugar
#     print(athlete.name,athlete.ranks[0])
    



# print('Speed')
# for i in range(0,8):
#     athlete= max_heap_speed_men.pop()
#     #                   Cantidad de veces en primer lugar
#     print(athlete.name,athlete.ranks[0])

# print('mujeres')

# #Top 8 de speed femenino
# for i in range(0,8):
#     athlete= max_heap_speed_women.pop()
#     #                   Cantidad de veces en primer lugar
#     print(athlete.name,athlete.ranks[0])    
    
    
    


# for i in range(0,20):
#     score1= men_athletes_kde['sorato anraku']['boulder'].sample(1)[0]
#     score2= men_athletes_kde['hanwool kim']['boulder'].sample(1)[0]
#     score1=np.clip(np.rint(score1), 0, None).astype(int)
#     score2=np.clip(np.rint(score2), 0, None).astype(int)
#     print(score1,'---sorato anraku',score2, '---hanwool kim')
    
