import os
import json
import random
from datetime import datetime
from flask import Flask, render_template, request, flash, redirect, url_for, session, Markup

app = Flask(__name__)
app.secret_key = 'some_secret'

def write_to_file(filename, data):
    """Handle the process of writing data to a file"""
    with open(filename, "a") as file:
        file.writelines(data)


def clear_file(filename):
    """Handle the process of clearing contents of file"""
    with open(filename, "w") as file:
        file.write("")

def get_random_animal():
    data = []
    with open("data/animals.json", "r") as json_data:
        data = json.load(json_data)
        random_animal = random.choice(data)
        session['random_animal'] = random_animal
    return random_animal

def add_animal_to_user_data_file(username):
    with open("data/scores.json", "r", encoding='utf-8') as jsonFile: # Open the JSON file for reading
        data = json.load(jsonFile) # Read the JSON into the buffer
    
    ## Save our changes to JSON file
    with open("data/scores.json", "w", encoding='utf-8') as jsonFile:
        #json.dump([], jsonFile)
        for i in data:
            #if entry is found matching current username then update score by 1 for correct answer
            if(i['username'] == username):
                random_animal = session['random_animal']
                i['animals'].append(random_animal['title'])
        
        json.dump(data, jsonFile)

def add_correct_guess_to_user_data_file(username):
    with open("data/scores.json", "r", encoding='utf-8') as jsonFile: # Open the JSON file for reading
        data = json.load(jsonFile) # Read the JSON into the buffer
    
    ## Save our changes to JSON file
    with open("data/scores.json", "w", encoding='utf-8') as jsonFile:
        #json.dump([], jsonFile)
        for i in data:
            #if entry is found matching current username then add current random animal to correctlyGuessed
            if(i['username'] == username):
                random_animal = session['random_animal']
                i['correctlyGuessed'].append(random_animal['title'])
        
        json.dump(data, jsonFile)

def add_passed_to_user_data_file(username):
    with open("data/scores.json", "r", encoding='utf-8') as jsonFile: # Open the JSON file for reading
        data = json.load(jsonFile) # Read the JSON into the buffer
    
    ## Save our changes to JSON file
    with open("data/scores.json", "w", encoding='utf-8') as jsonFile:
        #json.dump([], jsonFile)
        for i in data:
            #if entry is found matching current username then add current random animal to passed
            if(i['username'] == username):
                random_animal = session['random_animal']
                i['passed'].append(random_animal['title'])
        
        json.dump(data, jsonFile)

def animal_already_asked(username,animal):
    with open("data/scores.json", "r", encoding='utf-8') as jsonFile: # Open the JSON file for reading 
        data = json.load(jsonFile) # Read the JSON into the buffer
        
        for i in data:
            if(i['username'] == username):
                ## check if animal already exists in user file
                if animal in i['animals']:
                    return True
                else:
                    return False

def update_scores_file(username, score=0):
    with open("data/scores.json", "r", encoding='utf-8') as jsonFile: # Open the JSON file for reading
        try: 
            data = json.load(jsonFile) # Read the JSON into the buffer
            print(data)
        except ValueError: 
            data = [{"username": "","score": 0, "animals":[], "correctlyGuessed":[], "passed":[]}]#set dummy data to avoid value error later on caused by empty json file
            
    ## Save our changes to JSON file
    with open("data/scores.json", "w", encoding='utf-8') as jsonFile:
        
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

def get_current_user_score(username):
    with open("data/scores.json", "r", encoding='utf-8') as jsonFile: # Open the JSON file for reading
        data = json.load(jsonFile) # Read the JSON into the buffer
        score = 0
    ## if username already exists in scores file then get the score value
    for i in data:
            if(i['username'] == username):
                score = i['score']
            
    return score

def get_current_user_correctly_guessed(username):
    with open("data/scores.json", "r", encoding='utf-8') as jsonFile: # Open the JSON file for reading
        data = json.load(jsonFile) # Read the JSON into the buffer
        correctlyGuessed = []
    ## if username already exists in scores file then get the history values
    for i in data:
            if(i['username'] == username):
                correctlyGuessed = i['correctlyGuessed']
            
    return correctlyGuessed

def get_current_user_passed(username):
    with open("data/scores.json", "r", encoding='utf-8') as jsonFile: # Open the JSON file for reading
        data = json.load(jsonFile) # Read the JSON into the buffer
        passed = []
    ## if username already exists in scores file then get the history values
    for i in data:
            if(i['username'] == username):
                passed = i['passed']
            
    return passed

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

def get_leaderboard():
    with open("data/scores.json", "r", encoding='utf-8') as jsonFile: # Open the JSON file for reading
        try: 
            data = json.load(jsonFile) # Read the JSON into the buffer
            print(data)
        except ValueError: 
            data = [{"username": "","score": 0}]#set dummy data to avoid v

    leaderboard = sorted(data, key = lambda i: i['score'],reverse=True)
    return leaderboard

@app.route('/register', methods = ['GET', 'POST'])
def register():
   if request.method == 'POST':
      if username_already_exists(request.form['username']):
          flash(Markup('username: {} already exists, please enter a different value for username to register as a new user or login <a href="/login" class="alert-link">here</a>'.format(request.form["username"])))
          return redirect(url_for('register')) 
      session['username'] = request.form['username']
      session['logged_in'] = True
      flash("Successfully registered as new user and logged in! :)")
      update_scores_file(session['username'])
      return redirect(url_for('index'))
   return render_template("register.html")

@app.route('/login', methods = ['GET', 'POST'])
def login():
   if request.method == 'POST':
      if not username_already_exists(request.form['username']):
          flash(Markup('username: {} does not exist yet, please register <a href="/register" class="alert-link">here</a>'.format(request.form["username"])))
          return redirect(url_for('login')) 
      session['username'] = request.form['username']
      session['logged_in'] = True
      flash("Successfully logged in as existing user! :)")
      return redirect(url_for('index'))
   return render_template("login.html")

@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   session['logged_in'] = False
   return redirect(url_for('index'))


@app.route('/', methods=["GET", "POST"])
def index():
    """Main page with instructions"""
    current_user_username = ""
    correct_guesses = []
    passes = []
    if 'username' in session:
      current_user_username = session['username']
      correct_guesses = get_current_user_correctly_guessed(current_user_username)
      print(correct_guesses)
      passes = get_current_user_passed(current_user_username)
      print(passes)
      # Handle POST request
      if request.method == "POST":
          return redirect(url_for('game'))
    
    return render_template("index.html", username=current_user_username, correct_guesses=correct_guesses, passes=passes)

    

@app.route('/game', methods=["GET", "POST"])
def game():
    current_user_username = session['username']
            
    if request.method == "GET":
        random_animal = get_random_animal()
        print("random animal before:"+random_animal['title'])
        while animal_already_asked(current_user_username,random_animal['title']):
            random_animal = get_random_animal()
            print("random animal after:"+random_animal['title'])
        score = get_current_user_score(current_user_username)
        leaderboard_scores = get_leaderboard()
        add_animal_to_user_data_file(current_user_username)
        return render_template("game.html", page_title="Game", animal=random_animal, username=current_user_username, score=score, leaderboard_scores=leaderboard_scores)

    elif request.method == "POST":
        guess = request.form['guess'].lower()
        random_animal = session['random_animal']
        session['guess'] = guess
        answer = random_animal['title'].lower()
        if guess == answer or guess+'s' == answer:
            flash("Well done, that's the correct answer! Here's another one :)")
            point_earned = 1
            update_scores_file(current_user_username, point_earned)
            add_correct_guess_to_user_data_file(current_user_username)
            print("updated scores file from game post")
            return redirect(url_for('game'))
        
        elif guess == "pass":
            flash("Previous animal was passed, new animal has been loaded")
            add_passed_to_user_data_file(current_user_username)
            return redirect(url_for('game'))
            
    
        else:
            flash("Try again, that's an incorrect answer!")
            point_earned = 0
            previous_guess = session['guess']
            score = get_current_user_score(current_user_username)
            leaderboard_scores = get_leaderboard()
            random_animal = session['random_animal']
            return render_template("game.html", page_title="Game", animal=random_animal, username=current_user_username, previous_guess=previous_guess, score=score, leaderboard_scores=leaderboard_scores, success=point_earned)

app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)
