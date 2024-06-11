import numpy as np
from heapImplementation import Item,PriorityArray,MaxHeap
from KDE_calculations import KDE_for_athlete;
from functools import cmp_to_key
from dataReading import athletes_points;


def simulate_event(athletes_kde, heap, discipline, comparison_function):
    
    athletes_sorted_per_score=[]
    
    for athlete in athletes_kde:
        if discipline not in athletes_kde[athlete]:
            continue;
        function = athletes_kde[athlete][discipline];
        score= function.sample(1)[0]
        if(discipline=='boulder'):
            score=np.clip(np.rint(score), 0, None).astype(int)
        athletes_sorted_per_score.append({'name': athlete,'score': score})
    
    
    #qualifications fase
    athletes_sorted_per_score.sort(key=comparison_function,reverse=(discipline=='boulder'));
    
    for index,athlete in enumerate(athletes_sorted_per_score):
        if(index==10):
            break
        function = athletes_kde[athlete['name']][discipline];
        score = function.sample(1)[0];
        if(discipline=='boulder'):
            score=np.clip(np.rint(score), 0, None).astype(int)
        athlete['score']=score;
    
    #final athletes
    finals_athletes=sorted(athletes_sorted_per_score[:10], key=comparison_function, reverse=(discipline=='boulder'))
    
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
            return -1
        elif vec1[i] > vec2[i]:
            return 1
    for i in range(2):    
        if vec1[i+2] < vec2[i+2]:
            return 1
        elif vec1[i+2] > vec2[i+2]:
            return -1
    return 0



max_heap_boulder_men = MaxHeap()

max_heap_speed_men = MaxHeap()

men_athletes_kde = KDE_for_athlete(athletes_points['men'])



key_function = cmp_to_key(compare_vectors)

for i in range(0,1000):
    simulate_event(men_athletes_kde,max_heap_boulder,'boulder',key_function)
    simulate_event(men_athletes_kde,max_heap_speed,'speed',lambda x: x['score'])

print('BOULDER')

for i in range(0,8):
    athlete= max_heap_boulder.pop()
    
    print(athlete.name,athlete.ranks[0])
    
print('SPEED')
    
for i in range(0,8):
    athlete= max_heap_speed.pop()
    
    print(athlete.name,athlete.ranks[0])

# for i in range(0,20):
#     print(np.clip(np.rint(men_athletes_kde['gefen levi']['boulder'].sample(1)), 0, None).astype(int),'--gefen levi',np.clip(np.rint(men_athletes_kde['sorato anraku']['boulder'].sample(1)), 0, None).astype(int) ,'--sorato anraku' )
    
    
    

    
        