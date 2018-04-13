import os
import json
import random
from datetime import datetime
from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = 'some_secret'

current_user_username = "username"

def write_to_file(filename, data):
    """Handle the process of writing data to a file"""
    with open(filename, "a") as file:
        file.writelines(data)

def add_guesses(username, guess):
    """Add guesses to the `guesses` text file"""
    write_to_file("data/guesses.txt", "({0}) {1} - {2}\n".format(
            datetime.now().strftime("%H:%M:%S"),
            username.title(),
            guess))

def clear_file(filename):
    """Handle the process of clearing contents of file"""
    with open(filename, "w") as file:
        file.write("")



def get_all_guesses():
    """Get all of the guesses and separate them by a `br`"""
    guesses = []
    with open("data/guesses.txt", "r") as animal_name_guesses:
        guesses = animal_name_guesses.readlines()
    return guesses

def update_scores_file(username):
    with open("data/scores.json", "r", encoding='utf-8') as jsonFile: # Open the JSON file for reading
        try: 
            data = json.load(jsonFile) # Read the JSON into the buffer
            print(data)
        except ValueError: 
            data = [{"username": "","score": 0}]#set dummy data to avoid value error later on caused by empty json file
        

    ## Save our changes to JSON file
    with open("data/scores.json", "w", encoding='utf-8') as jsonFile:
        #json.dump([], jsonFile)
        print(type(data))
        for i in data:
            print(type(i))
            #if entry is found matching current username then update score by 1 for correct answer
            if(i['username'] == username):
                print (i['username'])
                print(username)
                print("score before")
                print (i['score'])
                i['score'] += 1
                print("score after")
                print (i['score'])

        #if username does not exist then create entry in scores file
        if not any(d['username'] == username for d in data):
            score = 0
            print(username,score)
            entry = {'username': username, 'score': score}
            data.append(entry)
        
        json.dump(data, jsonFile)

def get_current_user_score(username):
    with open("data/scores.json", "r", encoding='utf-8') as jsonFile: # Open the JSON file for reading
        data = json.load(jsonFile) # Read the JSON into the buffer
        score = 0
    ## if username already exists in scores file then get the score value
    for i in data:
            if(i['username'] == username):
                score = i['score']
            
    return score

def username_already_exists(username):
    with open("data/scores.json", "r", encoding='utf-8') as jsonFile: # Open the JSON file for reading
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




@app.route('/', methods=["GET", "POST"])
def index():
    """Main page with instructions"""
    
    # Handle POST request
    if request.method == "POST":
        #write_to_file("data/users.txt", request.form["username"] + "\n")
        clear_file("data/guesses.txt")
        global current_user_username
        current_user_username = request.form["username"]
        if username_already_exists(current_user_username):
            flash("username: {} already exists, please enter a different value for username :(".format(request.form["username"]))
            return redirect(url_for('index')) 
        update_scores_file(current_user_username)
        print("updated scores file from index post")
        return redirect(url_for('game'))
    return render_template("index.html")

@app.route('/game', methods=["GET", "POST"])
def game():
    username = current_user_username
            
    if request.method == "GET":
        data = []
        with open("data/animals.json", "r") as json_data:
            data = json.load(json_data)
            global random_animal
            random_animal = random.choice(data)
            score = get_current_user_score(username)
        return render_template("game.html", page_title="Game", animal=random_animal, username=username, score=score)

    elif request.method == "POST":
        guess = request.form['guess'].lower()
        answer = random_animal['title'].lower()
        if guess == answer:
            flash("Well done, that's the correct answer! Here's another one :)")
            clear_file("data/guesses.txt")
            update_scores_file(username)
            print("updated scores file from game post")
            return redirect(url_for('game'))
    
        else:
            flash("Try again, that's an incorrect answer!")
            add_guesses(username, request.form["guess"] + "\n")
            guesses = get_all_guesses()
            score = get_current_user_score(username)
            return render_template("game.html", page_title="Game", animal=random_animal, username=username, guesses=guesses, score=score)

#app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)