import unittest
from unittest.mock import patch
from server import app
from datetime import datetime, timedelta


class BookingTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('server.competitions', [
        {'name': 'Test competition', 'date': (
            datetime.now() + timedelta(days=1)
            ).strftime(
                '%Y-%m-%d %H:%M:%S'
                ), 'numberOfPlaces': 9}
    ])
    @patch('server.clubs', [
        {'name': 'Test club', 'email': 'unittest@email.com', 'points': 12}
    ])
    @patch('server.datetime')
    def test_booking_valid_competition(self, mock_datetime):
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        mock_datetime.now.return_value = datetime.strptime(
            current_time, '%Y-%m-%d %H:%M:%S'
            )
        mock_datetime.strptime = datetime.strptime

        response = self.app.post('/purchasePlaces', data={
            'competition': 'Test competition',
            'club': 'Test club',
            'places': 3
        })
        self.assertIn(b'Great-booking complete!', response.data)

    @patch('server.competitions', [
        {'name': 'Test competition', 'date': (
            datetime.now() - timedelta(days=1)
            ).strftime(
                '%Y-%m-%d %H:%M:%S'
                ), 'numberOfPlaces': 9}
    ])
    @patch('server.clubs', [
        {'name': 'Test club', 'email': 'unittest@email.com', 'points': 12}
    ])
    @patch('server.datetime')
    def test_booking_past_competition(self, mock_datetime):
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        mock_datetime.now.return_value = datetime.strptime(
            current_time, '%Y-%m-%d %H:%M:%S'
            )
        mock_datetime.strptime = datetime.strptime

        response = self.app.post('/purchasePlaces', data={
            'competition': 'Test competition',
            'club': 'Test club',
            'places': 3
        })
        self.assertIn(
            b'Error: Cannot book a place on a past competition.', response.data
            )

    @patch('server.competitions', [
        {'name': 'Test competition', 'date': (
            datetime.now() + timedelta(minutes=1)
            ).strftime(
                '%Y-%m-%d %H:%M:%S'
                ), 'numberOfPlaces': 9}
    ])
    @patch('server.clubs', [
        {'name': 'Test club', 'email': 'unittest@email.com', 'points': 12}
    ])
    @patch('server.datetime')
    def test_booking_just_in_time(self, mock_datetime):
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        mock_datetime.now.return_value = datetime.strptime(
            current_time, '%Y-%m-%d %H:%M:%S'
            )
        mock_datetime.strptime = datetime.strptime

        response = self.app.post('/purchasePlaces', data={
            'competition': 'Test competition',
            'club': 'Test club',
            'places': 3
        })
        self.assertIn(b'Great-booking complete!', response.data)

    @patch('server.competitions', [
        {'name': 'Test competition', 'date': (
            datetime.now() - timedelta(minutes=1)
            ).strftime(
                '%Y-%m-%d %H:%M:%S'
                ), 'numberOfPlaces': 9}
    ])
    @patch('server.clubs', [
        {'name': 'Test club', 'email': 'unittest@email.com', 'points': 12}
    ])
    @patch('server.datetime')
    def test_booking_too_late(self, mock_datetime):
        current_time = datetime.now().strftime(
            '%Y-%m-%d %H:%M:%S'
            )
        mock_datetime.now.return_value = datetime.strptime(
            current_time, '%Y-%m-%d %H:%M:%S'
            )
        mock_datetime.strptime = datetime.strptime

        response = self.app.post('/purchasePlaces', data={
            'competition': 'Test competition',
            'club': 'Test club',
            'places': 3
        })
        self.assertIn(
            b'Error: Cannot book a place on a past competition.', response.data
            )


if __name__ == '__main__':
    unittest.main()
