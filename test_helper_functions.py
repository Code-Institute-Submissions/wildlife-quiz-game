from run import app
from helper_function import (get_random_animal, add_to_user_data_file, animal_already_asked, update_user_data_file, get_current_user_score, get_current_user_game_history, username_already_exists, get_leaderboard)
import unittest
from flask import session

class test_helper_function(unittest.TestCase):

    def setUp(self):
        app.config['SECRET_KEY'] = 'some_secret'
        self.app = app.test_client()
    
    def test_get_random_animal(self):
        # Test if session variable is set (not empty)
        #tester = app.test_client()
        #tester.post(
        #    '/register',
        #    data={
        #    "username": "test"
        #},
        #    follow_redirects=True
        #)
        #tester.get('/game', follow_redirects=True)
        #random_animal = session.get('random_animal')
        #assert session.get("username") == "test"
        #self.assertTrue(random_animal is not None)

        # Test if function returns value in str format #
        with app.test_request_context():
            self.assertIsNotNone(get_random_animal())
        
        

if __name__ == '__main__':
    unittest.main()



