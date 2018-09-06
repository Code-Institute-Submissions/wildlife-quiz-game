# Wildlife Quiz Game | Flask & JSON File Practical Python Project
This is a guessing game written in Python using the Flask web application micro framework. The purpose of this project is to take data from a JSON file and use it to create a wildlife themed guessing game.

## UX Design

Details of the UX design is available in the 'PP project design' folder. This document outlines how I approached the design of this site.

## Game Logic Design

Details of the game logic design is available in the
'Game Logic' folder. This document outlines how I approached the design of the Game Logic.

## Features

### Existing Features

This game will present an animal at random from the JSON file and the user must try to guess the name correctly from the clues in the picture and the text information. It has a frontend and a backend (banckend is the server but the data does not persist in a database) and is hosted in the cloud on Heroku platform as a service.
1.  Users are identified by a unique username, but note that no authentication features such as a password are required. A user will register a unique username and then log in with just that username.
2.  Game History displays the animals that have been guessed correctly and the animals that have been passed.
3.	The player is presented with a random animal (image and text info) and the game has 12 rounds in total but the same animal will not be chosen twice.
4.	Players enter their answer into a textarea and submit their answer using a form.
5.  If a player guesses correctly, they are redirected to the next animal and they earn a point and their score is updated.
5.	If a player chooses to Pass, they are redirected to the next animal and they do not earn a point and their score is not updated.
6.	If a player guesses incorrectly, their incorrect guess is stored and printed below the riddle. The textarea is cleared so they can guess again. After 3 incorrect guesses the round is forfeited and they are redirected to the next animal and they do not earn a point and their score is not updated.
7.  Multiple players can play an instance of the game at the same time, each in their own browser. User data is restricted to a browser session.
8.  There is a leaderboard that ranks top scores for all users. This is presented at the end of the game after all 12 rounds are completed.

### Features Left to Implement

## Demo

A demo of this web application is available [here](https://wildlife-quiz-game..herokuapp.com/).


## Getting started /

1. Clone the repo and cd into the project directory.
2. Ensure you have Python 3 installed and create a virtual environment and activate it.
3. Install dependencies: `pip install -r requirements.txt`.


## Technologies Used

**HTML, CSS, JavaScript (Front End Framework Bootstrap)  Python, Full Stack Micro Framework Flask :**

## Testing

Manual testing was undertaken for this application and satisfactorily passed. A sample of the tests conducted are as follows:
1.	Testing navigation buttons and hyperlinks throughout the page
2.	Testing the logic of the game by comparing expected behaviour against the JSON file data.
3.	Testing the responsiveness of the application on different browsers and then using different devices.

## Deployment
1. Make sure requirements.txt and Procfile exist
⋅⋅* pip3 freeze --local requirements.txt
⋅⋅* echo web: python app.py > Procfile
2. Create Heroku App, Select Postgres add-on, download Heroku CLI toolbelt, login to heroku (Heroku login), git init, connect git to heroku (heroku git remote -a <project>), git add ., git commit, git push heroku master.
3. heroku ps:scale web=1
4. In heroku app settings set the config vars to add IP and PORT

## Credits

**Jordan Daly** - This project was completed as part of Code Institute’s Mentored Online Full Stack Web Development course in 2018.

### Content

### Media

### Acknowledgements
