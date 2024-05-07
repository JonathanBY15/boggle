from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


import unittest
from app import app

class TestBoggle(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        # You can add more assertions to check if the response contains expected data

    def test_guess_valid_word(self):
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['board'] = [['A', 'B', 'C', 'D', 'E'],
                                    ['F', 'G', 'H', 'I', 'J'],
                                    ['K', 'L', 'M', 'N', 'O'],
                                    ['P', 'Q', 'R', 'S', 'T'],
                                    ['U', 'V', 'W', 'X', 'Y']]
                
            response = client.post('/guess', json={'guess': 'hi'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['result'], 'ok')

            response = client.post('/guess', json={'guess': 'no'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['result'], 'ok')

            response = client.post('/guess', json={'guess': 'ton'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['result'], 'ok')


    def test_guess_on_board(self):
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['board'] = [['A', 'B', 'C', 'D', 'O'],
                                    ['F', 'G', 'H', 'I', 'J'],
                                    ['K', 'L', 'M', 'N', 'O'],
                                    ['P', 'Q', 'R', 'S', 'T'],
                                    ['U', 'V', 'W', 'X', 'Y']]
                
            response = client.post('/guess', json={'guess': 'abarticulation'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['result'], 'not-on-board')

            response = client.post('/guess', json={'guess': 'shearwaters'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['result'], 'not-on-board')

            response = client.post('/guess', json={'guess': 'pebblehearted'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['result'], 'not-on-board')


    def test_guess_invalid_word(self):
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['board'] = [['A', 'B', 'C', 'D', 'E'],
                                    ['F', 'G', 'H', 'I', 'J'],
                                    ['K', 'L', 'M', 'N', 'O'],
                                    ['P', 'Q', 'R', 'S', 'T'],
                                    ['U', 'V', 'W', 'X', 'Y']]
                
            response = client.post('/guess', json={'guess': 'xyz'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['result'], 'not-word')

            response = client.post('/guess', json={'guess': 'x'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['result'], 'not-word')

            response = client.post('/guess', json={'guess': 'dsaghsad'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['result'], 'not-word')


    def test_case_insensitive(self):
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['board'] = [['A', 'B', 'C', 'D', 'E'],
                                    ['F', 'G', 'H', 'I', 'J'],
                                    ['K', 'L', 'M', 'N', 'O'],
                                    ['P', 'Q', 'R', 'S', 'T'],
                                    ['U', 'V', 'W', 'X', 'Y']]
                
            response = client.post('/guess', json={'guess': 'HI'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['result'], 'ok')

            response = client.post('/guess', json={'guess': 'Hi'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['result'], 'ok')

            response = client.post('/guess', json={'guess': 'hI'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['result'], 'ok')

            response = client.post('/guess', json={'guess': 'hi'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['result'], 'ok')


    def test_high_score(self):
        with app.test_client() as client:
            response = client.post('/high-score', json={'score': 10})
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.json['isHighScore'])

    def test_get_high_score(self):
        with app.test_client() as client:
            response = client.get('/high-score')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['high_score'], 0)  # Assuming default high score is 0

if __name__ == '__main__':
    unittest.main()
