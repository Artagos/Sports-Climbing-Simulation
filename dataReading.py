import os
import json
import sys
import numpy as np




def get_athletes_points(data):
    """
    Reads the athletes' points from the json data.

    Returns:
        dict: A dictionary containing the athletes' points.
    """
    athletes_points = {'men':{},'women':{} , None:{}}
    
    for event in data:
        category = event['category']
        if category == 'boulder':
            get_boulder_points(event['data'], athletes_points[event['sex']])
        elif category == 'speed':
            get_speed_points(event['data'], athletes_points[event['sex']])
    
    
    return athletes_points

def read_json_files_in_directory(main_folder):
    json_data = []
    
    # Traverse the directory tree
    for root, dirs, files in os.walk(main_folder):
        
        category = category_by_path(root)
        
        
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                sex = sex_by_filename(file)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                        
                        data = json.load(f)
                        
                        data_with_category ={
                            'data':data,
                            'category':category,
                            'sex': sex
                        }
                        
                        json_data.append(data_with_category)
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    
    return json_data



def category_by_path(path):
    aux=path.lower()
    categories=['boulder','speed','lead']
    for category in categories:
        if category in aux:
            return category
    return None
def sex_by_filename(file):
    aux=file.lower()
    if('women' in aux):
        return 'women'
    elif('men' in aux):
        return 'men'
    else:
        return None


def get_boulder_points(ranking, athletes_points):
    
    for player in ranking:
        raw_score=player['score']
        if(raw_score.isalpha()):
            continue;
        real_score=string_to_vector(raw_score)
        player_name=player['name'].lower()
        if player_name in athletes_points:
            athletes_points[player_name]['boulder'].append(real_score)
        else:
            athletes_points[player_name]={'boulder':[real_score],'speed':[],'lead':[]}
        

def get_speed_points(ranking_event, athletes_points):
    
    if ('athletes' in ranking_event[0]):
        
        for stage in ranking_event:
            for player in stage['athletes']:
                real_score=player['time']
                try:
                    real_score=float(real_score)
                except:
                    continue;
                
                player_name=player['name'].lower()
                if player_name in athletes_points:
                    athletes_points[player_name]['speed'].append(real_score)
                else:
                    athletes_points[player_name]={'boulder':[],'speed':[real_score],'lead':[]}
    else:
        for player in ranking_event:
            brute_scores=player['scores']
            player_name=player['name'].lower()

            if player_name not in athletes_points:
                athletes_points[player_name]={'boulder':[],'speed':[],'lead':[]}
                
            for score in brute_scores:
                try:
                    real_score=float(score)
                    athletes_points[player_name]['speed'].append(real_score)
                except:
                    continue;
            

        
def string_to_vector(initial_s):
    # Split the string by spaces
    s=initial_s.lower()
    components = s.split()

    # Extract the relevant values
    first_component = int(components[0].split('t')[0])
    second_component = int(components[0].split('t')[1].split('z')[0])
    third_component = int(components[1])
    fourth_component = int(components[2])

    # Create the 4-dimensional vector
    vector = np.array([first_component, second_component, third_component, fourth_component])
    return vector


json_data = read_json_files_in_directory('data')
athletes_points = get_athletes_points(json_data)

