import os
import helper_function
from flask import Flask, render_template, request, flash, redirect, url_for, session, Markup

app = Flask(__name__)
app.secret_key = 'some_secret'

@app.route('/register', methods = ['GET', 'POST'])
def register():
   if request.method == 'POST':
      if helper_function.username_already_exists(request.form['username']):
          flash(Markup('username: {} already exists, please enter a different value for username to register as a new user or login <a href="/login" class="alert-link">here</a>'.format(request.form["username"])))
          return redirect(url_for('register')) 
      session['username'] = request.form['username']
      session['logged_in'] = True
      flash("Successfully registered as new user and logged in! :)")
      helper_function.update_user_data_file(session['username'])
      return redirect(url_for('index'))
   return render_template("register.html")

@app.route('/login', methods = ['GET', 'POST'])
def login():
   if request.method == 'POST':
      if not helper_function.username_already_exists(request.form['username']):
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
   flash("You were logged out")
   return redirect(url_for('index'))


@app.route('/', methods=["GET", "POST"])
def index():
    """Main page with instructions"""
    current_user_username = ""
    correct_guesses = []
    passes = []
    if 'username' in session:
      current_user_username = session['username']
      helper_function.update_user_data_file(current_user_username)
      correct_guesses = helper_function.get_current_user_game_history(current_user_username, "correctlyGuessed")
      print(correct_guesses)
      passes = helper_function.get_current_user_game_history(current_user_username, "passed")
      print(passes)
      # Handle POST request
      if request.method == "POST":
          return redirect(url_for('game'))
    
    return render_template("index.html", username=current_user_username, correct_guesses=correct_guesses, passes=passes)

    

@app.route('/game', methods=["GET", "POST"])
def game():
    current_user_username = session['username']

            
    if request.method == "GET":
        random_animal = helper_function.get_random_animal()
        print("random animal before:"+random_animal['title'])
        while helper_function.animal_already_asked(current_user_username,random_animal['title']):
            random_animal = helper_function.get_random_animal()
            print("random animal after:"+random_animal['title'])
        score = helper_function.get_current_user_score(current_user_username)
        leaderboard_scores = helper_function.get_leaderboard()
        helper_function.add_to_user_data_file(current_user_username,"animals")
        session['previous_guesses'] = []
        return render_template("game.html", page_title="Game", animal=random_animal, username=current_user_username, score=score, leaderboard_scores=leaderboard_scores)

    elif request.method == "POST":
        guess = request.form['guess'].lower()
        random_animal = session['random_animal']

        session['previous_guesses'].append(guess)

        answer = random_animal['title'].lower()
        if guess == answer or guess+'s' == answer:
            flash("Well done, that's the correct answer! Here's another one :)")
            point_earned = 1
            helper_function.update_user_data_file(current_user_username, point_earned)
            helper_function.add_to_user_data_file(current_user_username,"correctlyGuessed")
            print("updated scores file from game post")
            return redirect(url_for('game'))
        
        elif guess == "pass":
            flash("Previous animal was passed, new animal has been loaded")
            helper_function.add_to_user_data_file(current_user_username,"passed")
            return redirect(url_for('game'))
            
    
        else:
            flash("Try again, that's an incorrect answer!")
            point_earned = 0
            previous_guesses = session['previous_guesses']
            score = helper_function.get_current_user_score(current_user_username)
            leaderboard_scores = helper_function.get_leaderboard()
            random_animal = session['random_animal']
            return render_template("game.html", page_title="Game", animal=random_animal, username=current_user_username, previous_guesses=previous_guesses, score=score, leaderboard_scores=leaderboard_scores, success=point_earned)

#app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)
