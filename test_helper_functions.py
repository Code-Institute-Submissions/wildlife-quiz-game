import json
import unittest
from run import app
from helper_function import (open_user_data_json,get_random_animal, add_to_user_data_file, animal_already_asked, update_user_data_file, get_current_user_score, get_current_user_game_history, username_already_exists, get_leaderboard)
from flask import session

class test_helper_function(unittest.TestCase):

    def setUp(self):
        app.config['SECRET_KEY'] = 'some_secret'
        self.app = app.test_client()

    def mock_data_setup(self,username='test_username',score=0,animal='test_animal',correctlyGuessed='test_correctly_guessed',passed='test_passed'):
        with open("data/user_data.json", "r", encoding='utf-8') as jsonFile: # Open the JSON file for reading
            try: 
                data = json.load(jsonFile) # Read the JSON into the buffer
                print(data)
            except ValueError: 
                data = [{"username": "username","score": 0, "animals":[], "correctlyGuessed":[], "passed":[]}]#set dummy data to avoid value error later on caused by empty json file
            
        ## Save our changes to JSON file
        with open("data/user_data.json", "w", encoding='utf-8') as jsonFile:
            
            score = 0
            entry = {'username': username, 'score': score, "animals":[animal], "correctlyGuessed":[correctlyGuessed], "passed":[passed]}
            data.append(entry)
            
            json.dump(data, jsonFile)

    
    def test_get_random_animal(self):
        #Test if session variable is set (not empty)
        # with app.test_request_context():
        #     tester = app.test_client()
        #     tester.post(
        #     '/register',
        #     data={
        #     "username": "test"
        #     },
        #     follow_redirects=True
        #     )
        #     tester.get('/game', follow_redirects=True)
        #     random_animal = session.get('random_animal')
        #     self.assertTrue(random_animal is not None)

        # Test if function returns anything at all #
        with app.test_request_context():
            self.assertIsNotNone(get_random_animal())

    
    def test_add_to_user_data_file(self):
        # Test if entry in file is added to user_data file based on parameter passed
        with app.test_request_context():
            update_user_data_file('username')
            with app.test_client() as client:
                with client.session_transaction():
                    session['random_animal'] = {"title": "test_animal_title"}
                    add_to_user_data_file('username','animals')
                    add_to_user_data_file('username','correctlyGuessed')
                    add_to_user_data_file('username','passed')
                    
                    # self.assertIn(''.join(open_user_data_json()), 'test_animal_title')
                    self.assertIn("test_animal_title",open_user_data_json()[0]["animals"])
                    self.assertIn("test_animal_title",open_user_data_json()[0]["correctlyGuessed"])
                    self.assertIn("test_animal_title",open_user_data_json()[0]["passed"])

    # def test_animal_already_asked(self,mock_data_setup):
    #     mock_data_setup()
    #     self.assertEquals(animal_already_asked("test_username","test_animal"), True)

        
        

if __name__ == '__main__':
    unittest.main()



