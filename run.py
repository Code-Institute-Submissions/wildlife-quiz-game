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


@app.route('/', methods=["GET", "POST"])
def index():
    """Main page with instructions"""
    
    # Handle POST request
    if request.method == "POST":
        write_to_file("data/users.txt", request.form["username"] + "\n")
        clear_file("data/guesses.txt")
        global current_user_username
        current_user_username = request.form["username"]
        return redirect(url_for('game'))
    return render_template("index.html")

@app.route('/game', methods=["GET", "POST"])
def game():
    username = current_user_username
            
    if request.method == "GET":
        guesses = get_all_guesses()
        data = []
        with open("data/animals.json", "r") as json_data:
            data = json.load(json_data)
            global random_animal
            random_animal = random.choice(data)
        return render_template("game.html", page_title="Game", animal=random_animal, username=username, guesses=guesses)

    elif request.method == "POST":
        guess = request.form['guess'].lower()
        answer = random_animal['title'].lower()
        if guess == answer:
            flash("Well done, that's the correct answer! Here's another one :)")
            clear_file("data/guesses.txt")
            return redirect(url_for('game'))
    
        else:
            flash("Try again, that's an incorrect answer!")
            add_guesses(username, request.form["guess"] + "\n")
            guesses = get_all_guesses()
            return render_template("game.html", page_title="Game", animal=random_animal, username=username, guesses=guesses)
            
        

#app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)
