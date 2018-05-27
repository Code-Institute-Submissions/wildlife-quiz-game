import json
import random
from flask import Flask, session

"""function to get a random animal from the json file of animal data"""
def get_random_animal():
    data = []
    with open("data/animals.json", "r") as json_data:
        data = json.load(json_data)
        random_animal = random.choice(data)
        session['random_animal'] = random_animal
    return random_animal

"""function to add the title (name) of randomly chosen animal to user's animals/correctlyGuessed/passed list in user data file"""
def add_to_user_data_file(username,option):
    with open("data/user_data.json", "r", encoding='utf-8') as jsonFile: # Open the JSON file for reading
        data = json.load(jsonFile) # Read the JSON into the buffer
    
    ## Save our changes to JSON file
    with open("data/user_data.json", "w", encoding='utf-8') as jsonFile:
        for i in data:
            #if entry is found matching current username then add to animals or correctlyGuessed or passed list
            if(i['username'] == username):
                random_animal = session['random_animal']
                if (option == "animals"):
                    i['animals'].append(random_animal['title'])
                elif (option == "correctlyGuessed"):
                    i['correctlyGuessed'].append(random_animal['title'])
                elif (option == "passed"):
                    i['passed'].append(random_animal['title'])
                
        json.dump(data, jsonFile)

"""function to check if the randomly chosen animal has already been asked for the logged in user"""
def animal_already_asked(username,animal):
    with open("data/user_data.json", "r", encoding='utf-8') as jsonFile: # Open the JSON file for reading 
        data = json.load(jsonFile) # Read the JSON into the buffer
        
        for i in data:
            if(i['username'] == username):
                ## check if animal already exists in animals list for this user in the user data file
                if animal in i['animals']:
                    return True
                else:
                    return False

"""function to update score if user exists and score is not zero or insert user entry into file if user does not exist yet"""
def update_user_data_file(username, score=0):
    with open("data/user_data.json", "r", encoding='utf-8') as jsonFile: # Open the JSON file for reading
        try: 
            data = json.load(jsonFile) # Read the JSON into the buffer
            print(data)
        except ValueError: 
            data = [{"username": "username","score": 0, "animals":[], "correctlyGuessed":[], "passed":[]}]#set dummy data to avoid value error later on caused by empty json file
            
    ## Save our changes to JSON file
    with open("data/user_data.json", "w", encoding='utf-8') as jsonFile:
        
        for i in data:
            #if entry is found matching current username then update score by 1 for correct answer
            if(i['username'] == username and score != 0):
                i['score'] += 1

        #if username does not exist then create entry in scores file
        if not any(d['username'] == username for d in data):
            score = 0
            print(username,score)
            entry = {'username': username, 'score': score, "animals":[], "correctlyGuessed":[], "passed":[]}
            data.append(entry)
        
        json.dump(data, jsonFile)

"""function to get the user's score value"""
def get_current_user_score(username):
    with open("data/user_data.json", "r", encoding='utf-8') as jsonFile: # Open the JSON file for reading
        data = json.load(jsonFile) # Read the JSON into the buffer
        score = 0
    ## if username already exists in scores file then get the score value
    for i in data:
            if(i['username'] == username):
                score = i['score']
            
    return score

"""function to get the user's game history (already asked animal list, correctly guessed list and passed list)"""
def get_current_user_game_history(username, option):
    with open("data/user_data.json", "r", encoding='utf-8') as jsonFile: # Open the JSON file for reading
        data = json.load(jsonFile) # Read the JSON into the buffer
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

"""function to check if the username entered already exists in the user data file"""
def username_already_exists(username):
    with open("data/user_data.json", "r", encoding='utf-8') as jsonFile: # Open the JSON file for reading
        try: 
            data = json.load(jsonFile) # Read the JSON into the buffer
            print(data)
        except ValueError: 
            data = [{"username": "","score": 0}]#set dummy data to avoid value error later on caused by empty json file
        
    ## check if username already exists in file
    if any(d['username'] == username for d in data):
        return True
    else:
        return False

"""function to get the top user scores, sorts by score in descending order"""
def get_leaderboard():
    with open("data/user_data.json", "r", encoding='utf-8') as jsonFile: # Open the JSON file for reading
        try: 
            data = json.load(jsonFile) # Read the JSON into the buffer
            print(data)
        except ValueError: 
            data = [{"username": "","score": 0}]#set dummy data to avoid value error

    leaderboard = sorted(data, key = lambda i: i['score'],reverse=True)
    return leaderboard