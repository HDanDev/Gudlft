import unittest
from unittest.mock import patch
from server import app
from datetime import datetime, timedelta


class TestBookingSystem(unittest.TestCase):


    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True


    @patch('server.competitions', [
        {'name': 'Test competition', 'date': (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S'), 'numberOfPlaces': 18}
    ])
    @patch('server.clubs', [
        {'name': 'Test club', 'email': 'unittest@email.com', 'points': 9}
    ])
    @patch('server.datetime')
    def test_successful_purchase(self, mock_datetime):
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        mock_datetime.now.return_value = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S')
        mock_datetime.strptime = datetime.strptime

        response = self.app.post('/purchasePlaces', data={
            'competition': 'Test competition',
            'club': 'Test club',
            'places': 5
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Great-booking complete!', response.data)


    @patch('server.competitions', [
        {'name': 'Test competition', 'date': (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S'), 'numberOfPlaces': 18}
    ])
    @patch('server.clubs', [
        {'name': 'Test club', 'email': 'unittest@email.com', 'points': 9}
    ])
    @patch('server.datetime')
    def test_successful_purchase_exact_amount(self, mock_datetime):
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        mock_datetime.now.return_value = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S')
        mock_datetime.strptime = datetime.strptime

        response = self.app.post('/purchasePlaces', data={
            'competition': 'Test competition',
            'club': 'Test club',
            'places': 9
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Great-booking complete!', response.data)


    @patch('server.competitions', [
        {'name': 'Test competition', 'date': (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S'), 'numberOfPlaces': 18}
    ])
    @patch('server.clubs', [
        {'name': 'Test club', 'email': 'unittest@email.com', 'points': 9}
    ])
    @patch('server.datetime')
    def test_insufficient_points(self, mock_datetime):
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        mock_datetime.now.return_value = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S')
        mock_datetime.strptime = datetime.strptime

        response = self.app.post('/purchasePlaces', data={
            'competition': 'Test competition',
            'club': 'Test club',
            'places': 11
        })
        assertion = f"Not enough available points to book the places. You were only able to afford {9}"
        
        self.assertIn(assertion.encode(), response.data)
        
        
if __name__ == '__main__':
    unittest.main()