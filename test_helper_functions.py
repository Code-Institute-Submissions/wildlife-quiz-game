import json
import unittest
from run import app
from helper_function import (mock_data_setup, open_user_data_json, clear_user_data_json, get_random_animal, add_to_user_data_file, animal_already_asked, update_user_score, add_new_user, get_current_user_score, get_current_user_game_history, username_already_exists, get_leaderboard)
from flask import session

class test_helper_function(unittest.TestCase):

    def setUp(self):
        app.config['SECRET_KEY'] = 'some_secret'
        self.app = app.test_client()

    
    def test_get_random_animal(self):
        ''' Test if function returns any value '''
        with app.test_request_context():
            self.assertIsNotNone(get_random_animal())
            '''Test if session variable is set (not empty)'''
            with app.test_client() as client:
                with client.session_transaction():
                    get_random_animal()
                    random_animal = session.get('random_animal')
                    self.assertIsNotNone(random_animal)

    
    def test_add_to_user_data_file(self):
        ''' Test if entry in file is added to user_data file based on arguments passed'''
        with app.test_request_context():
            add_new_user('username')
            with app.test_client() as client:
                with client.session_transaction():
                    session['random_animal'] = {"title": "test_animal_title"}
                    #clear_user_data_json()
                    add_to_user_data_file('username','animals')
                    add_to_user_data_file('username','correctlyGuessed')
                    add_to_user_data_file('username','passed')
                    
                    self.assertIn("test_animal_title",open_user_data_json()[0]["animals"])
                    self.assertIn("test_animal_title",open_user_data_json()[0]["correctlyGuessed"])
                    self.assertIn("test_animal_title",open_user_data_json()[0]["passed"])

    def test_animal_already_asked(self):
        '''Test if function detects value in user_data.json exists already when given username and animal arguments '''
        clear_user_data_json()
        mock_data_setup()
        self.assertTrue(animal_already_asked("test_username","test_animal"))
        self.assertFalse(animal_already_asked("test_username","other_animal"))

    def test_update_user_score(self):
        '''function to update score (increase by 1) if user exists'''
        clear_user_data_json()
        mock_data_setup()
        update_user_score("test_username")
        self.assertEqual(open_user_data_json()[0]["score"], 1)

        
        

if __name__ == '__main__':
    unittest.main()



