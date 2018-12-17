import json
import random
from flask import Flask, session

def mock_data_setup(username='test_username',score=0,animal='test_animal',correctlyGuessed='test_correctly_guessed',passed='test_passed'):
    '''utility function for populating the user data file with test data during automated tests'''
    with open("data/user_data.json", "r", encoding='utf-8') as jsonFile: # Open the JSON file for reading
        try: 
            data = json.load(jsonFile) # Read the JSON into the buffer
        except ValueError: 
            data = []
        
    ## Save our changes to JSON file
    with open("data/user_data.json", "w", encoding='utf-8') as jsonFile:
        
        score = 0
        entry = {'username': username, 'score': score, "animals":[animal], "correctlyGuessed":[correctlyGuessed], "passed":[passed]}
        data.append(entry)
        
        json.dump(data, jsonFile)

def open_user_data_json():
    '''utility function for opening and reading the user data file'''
    with open("data/user_data.json", "r", encoding='utf-8') as jsonFile: # Open the JSON file for reading
        try: 
            data = json.load(jsonFile) # Read the JSON into the buffer
            print(data)
        except ValueError: 
            data = []#set dummy data to avoid value error later on caused by empty json file
    # # Open the JSON file for reading
    # with open("data/user_data.json", "r", encoding='utf-8') as jsonFile: 
    #     # Read the JSON into the buffer
    #     data = json.load(jsonFile)
        return data

def clear_user_data_json():
    '''utility function for emptying the user data file during automated tests'''
    
    with open("data/user_data.json", "w", encoding='utf-8') as jsonFile:
        jsonFile.close()

def get_random_animal():
    """function to get a random animal from the json file of animal data"""
    data = []
    with open("data/animals.json", "r") as json_data:
        data = json.load(json_data)
        random_animal = random.choice(data)
        session['random_animal'] = random_animal
    return random_animal

def add_to_user_data_file(username,option):
    """function to add the title (name) of randomly chosen animal to user's animals/correctlyGuessed/passed list in user data file"""
    data = open_user_data_json()
    
    ## Save our changes to JSON file
    with open("data/user_data.json", "w", encoding='utf-8') as jsonFile:
        for i in data:
            #if entry is found matching current username then add to animals or correctlyGuessed or passed list depending on option parameter that is passed
            if(i['username'] == username):
                random_animal = session['random_animal']
                if (option == "animals"):
                    i['animals'].append(random_animal['title'])
                elif (option == "correctlyGuessed"):
                    i['correctlyGuessed'].append(random_animal['title'])
                elif (option == "passed"):
                    i['passed'].append(random_animal['title'])
                
        json.dump(data, jsonFile)


def animal_already_asked(username,animal):
    """function to check if the randomly chosen animal has already been asked for the logged in user"""
    # with open("data/user_data.json", "r", encoding='utf-8') as jsonFile: # Open the JSON file for reading 
    #     data = json.load(jsonFile) # Read the JSON into the buffer
    data = open_user_data_json()
        
    for i in data:
        if(i['username'] == username):
            ## check if animal already exists in animals list for this user in the user data file
            if animal in i['animals']:
                return True
            else:
                return False


def update_user_score(username):
    """function to update score if user exists and score is not zero"""
    data = open_user_data_json()
            
    ## Save our changes to JSON file
    with open("data/user_data.json", "w", encoding='utf-8') as jsonFile:
        
        for i in data:
            #if entry is found matching current username then update score by 1 for correct answer
            if(i['username'] == username):
                i['score'] += 1
        
        json.dump(data, jsonFile)

def add_new_user(username):
    """function to insert new user entry into file if user does not exist yet"""
    with open("data/user_data.json", "r", encoding='utf-8') as jsonFile: # Open the JSON file for reading
        try: 
            data = json.load(jsonFile) # Read the JSON into the buffer
            print(data)
        except ValueError: 
            data = [{"username": "test_username","score": 0, "animals":[], "correctlyGuessed":[], "passed":[]}]#set dummy data to avoid value error later on caused by empty json file
            
    ## Save our changes to JSON file
    with open("data/user_data.json", "w", encoding='utf-8') as jsonFile:

        #if username does not exist then create entry in scores file
        if not any(d['username'] == username for d in data):
            score = 0
            print(username,score)
            entry = {'username': username, 'score': score, "animals":[], "correctlyGuessed":[], "passed":[]}
            data.append(entry)
        
        json.dump(data, jsonFile)


"""function to get the user's score value"""
def get_current_user_score(username):
    data = open_user_data_json()
    score = 0
    ## if username already exists in scores file then get the score value
    for i in data:
            if(i['username'] == username):
                score = i['score']
            
    return score


def get_current_user_game_history(username, option):
    """function to get the user's game history (already asked animal list, correctly guessed list and passed list)"""
    data = open_user_data_json()
    game_history = []
    ## if username already exists in scores file then get the history values
    for i in data:
            if(i['username'] == username):
                if (option == "passed"):
                    game_history = i['passed']
                elif (option == "correctlyGuessed"):
                    game_history = i['correctlyGuessed']
                elif (option == "animals"):
                    game_history = i['animals']

    return game_history

def username_already_exists(username):
    """function to check if the username entered already exists in the user data file"""
    data = open_user_data_json()    
    ## check if username already exists in file
    if any(d['username'] == username for d in data):
        return True
    else:
        return False

def get_leaderboard():
    """function to get the top user scores, sorts by score in descending order"""
    data = open_user_data_json()

    leaderboard = sorted(data, key = lambda i: i['score'],reverse=True)
    return leaderboard