from run import app
import unittest
from flask import session



class FlaskTestCase(unittest.TestCase):

    # Ensure that flask was set up correctly
    def test_a_index(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Ensure that the register page loads correctly
    def test_b_register_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/register')
        self.assertIn(b'Please enter your username into the box and click the register button', response.data)

    # Ensure register behaves correctly with username that does not exist (not already registered)
    def test_c_correct_register(self):
        tester = app.test_client()
        response = tester.post(
            '/register',
            data=dict(username="admin"),
            follow_redirects=True
        )
        self.assertIn(b'Successfully registered as new user and logged in', response.data)

    # Ensure register behaves correctly with username that exists (already registered)
    def test_d_incorrect_register(self):
        tester = app.test_client()
        response = tester.post(
            '/register',
            data=dict(username="admin"),
            follow_redirects=True
        )
        self.assertIn(b'username: admin already exists, please enter a different value for username to register as a new user or login', response.data)

    # Ensure that the login page loads correctly
    def test_e_login_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/login')
        self.assertIn(b'Please enter your username into the box and click the login button', response.data)

    # Ensure login behaves correctly with username that does exist (registered already)
    def test_f_correct_login(self):
        tester = app.test_client()
        response = tester.post(
            '/login',
            data=dict(username="admin"),
            follow_redirects=True
        )
        self.assertIn(b'Successfully logged in as existing user', response.data)

    # Ensure login behaves correctly with username that does not exist (not yet registered)
    def test_g_incorrect_login(self):
        tester = app.test_client()
        response = tester.post(
            '/login',
            data=dict(username="wrong"),
            follow_redirects=True
        )
        self.assertIn(b'username: wrong does not exist yet, please register', response.data)

    # Ensure logout behaves correctly
    def test_h_logout(self):
        tester = app.test_client()
        tester.post(
            '/login',
            data=dict(username="admin"),
            follow_redirects=True
        )
        response = tester.get('/logout', follow_redirects=True)
        self.assertIn(b'You were logged out', response.data)

    # Ensure game route loads correctly
    def test_i_game(self):
        tester = app.test_client()
        tester.post(
            '/login',
            data=dict(username="admin"),
            follow_redirects=True
        )
        response = tester.get('/game', follow_redirects=True)
        self.assertIn(b'Welcome, you are logged in as admin your current score is 0', response.data)

    # Ensure game route behaves correctly when you give an incorrect guess
    def test_k_game_incorrect_guess(self):
        tester = app.test_client()
        tester.post(
            '/login',
            data=dict(username="admin"),
            follow_redirects=True
        )
        tester.get('/game', follow_redirects=True)
        response = tester.post(
            '/game',
            data=dict(guess="animal"),
            follow_redirects=True
        )
        self.assertIn(b'Try again, that&#39;s an incorrect answer!', response.data)

        # Ensure game route behaves correctly when you "pass" (skip to next)
    def test_l_game_pass_guess(self):
        tester = app.test_client()
        tester.post(
            '/login',
            data=dict(username="admin"),
            follow_redirects=True
        )
        tester.get('/game', follow_redirects=True)
        response = tester.post(
            '/game',
            data=dict(guess="pass"),
            follow_redirects=True
        )
        self.assertIn(b'Previous animal was passed, new animal has been loaded', response.data)

    # Ensure game route behaves correctly when you give a correct guess
    """def test_m_game_correct_guess(self):
        tester = app.test_client()
        tester.post(
            '/login',
            data=dict(username="admin"),
            follow_redirects=True
        )
        tester.get('/game', follow_redirects=True)
        with app.test_client() as c:
            with c.session_transaction() as sess:
                sess['random_animal'] = "guess"
        #with app.test_request_context():
        response = tester.post(
        '/game',
        data=dict(guess="guess"),
        follow_redirects=True
        )
        self.assertIn(b'Well done, that&#39;s the correct answer! Here&#39;s another one', response.data)"""
        

if __name__ == '__main__':
    unittest.main()