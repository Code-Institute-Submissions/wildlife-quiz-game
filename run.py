import os
import json
import random
from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)

current_user_username = "username"

def write_to_file(filename, data):
    """Handle the process of writing data to a file"""
    with open(filename, "a") as file:
        file.writelines(data)

@app.route('/', methods=["GET", "POST"])
def index():
    """Main page with instructions"""
    
    # Handle POST request
    if request.method == "POST":
        write_to_file("data/users.txt", request.form["username"] + "\n")
        global current_user_username
        current_user_username = request.form["username"]
        return redirect(url_for('game'))
    return render_template("index.html")

@app.route('/game')
def game():
    username = current_user_username
    data = []
    with open("data/animals.json", "r") as json_data:
        data = json.load(json_data)
        random_animal = random.choice(data)
    return render_template("game.html", page_title="Game", animal=random_animal, username=username)

#app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)