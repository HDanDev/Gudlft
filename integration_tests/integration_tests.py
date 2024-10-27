import unittest
from unittest.mock import patch
from server import app, maxBookingPlaces
from datetime import datetime, timedelta


class IntegrationTestBookingSystem(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        self.mock_clubs = [
            {'name': 'Test Club 1', 'email': 'club1@test.com', 'points': 15},
            {'name': 'Test Club 2', 'email': 'club2@test.com', 'points': 8}
        ]
        self.mock_competitions = [
            {
                'name': 'Test Competition Future',
                'date': (
                    datetime.now() + timedelta(days=10)
                    ).strftime('%Y-%m-%d %H:%M:%S'),
                'numberOfPlaces': 20
                },
            {
                'name': 'Test Competition Past',
                'date': (
                    datetime.now() - timedelta(days=10)
                    ).strftime('%Y-%m-%d %H:%M:%S'),
                'numberOfPlaces': 20
                }
        ]

    @patch('server.clubs', new_callable=lambda: [])
    @patch('server.competitions', new_callable=lambda: [])
    def test_show_summary_with_valid_email(self, mock_competitions, mock_clubs):
        mock_clubs.extend(self.mock_clubs)
        mock_competitions.extend(self.mock_competitions)

        response = self.app.post(
            '/showSummary',
            data={'email': 'club1@test.com'}
            )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome', response.data)

    @patch('server.clubs', new_callable=lambda: [])
    @patch('server.competitions', new_callable=lambda: [])
    def test_booking_places_successful(self, mock_competitions, mock_clubs):
        mock_clubs.extend(self.mock_clubs)
        mock_competitions.extend(self.mock_competitions)

        self.app.post('/showSummary', data={'email': 'club1@test.com'})

        response = self.app.post('/purchasePlaces', data={
            'competition': 'Test Competition Future',
            'club': 'Test Club 1',
            'places': '5'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Great-booking complete!', response.data)
        self.assertIn(b'Points available: 10', response.data)

    @patch('server.clubs', new_callable=lambda: [])
    @patch('server.competitions', new_callable=lambda: [])
    def test_booking_with_insufficient_points(self, mock_competitions, mock_clubs):
        mock_clubs.extend(self.mock_clubs)
        mock_competitions.extend(self.mock_competitions)

        self.app.post('/showSummary', data={'email': 'club2@test.com'})

        response = self.app.post('/purchasePlaces', data={
            'competition': 'Test Competition Future',
            'club': 'Test Club 2',
            'places': '10'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b"Not enough available points to book the places.",
            response.data
            )

    @patch('server.clubs', new_callable=lambda: [])
    @patch('server.competitions', new_callable=lambda: [])
    def test_booking_more_than_max_allowed(self, mock_competitions, mock_clubs):
        mock_clubs.extend(self.mock_clubs)
        mock_competitions.extend(self.mock_competitions)

        self.app.post('/showSummary', data={'email': 'club1@test.com'})

        response = self.app.post('/purchasePlaces', data={
            'competition': 'Test Competition Future',
            'club': 'Test Club 1',
            'places': str(maxBookingPlaces + 1)
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            f"Unfortunately, it is not authorized to book more than "
            f"{maxBookingPlaces} places".encode(),
            response.data
            )

    @patch('server.clubs', new_callable=lambda: [])
    @patch('server.competitions', new_callable=lambda: [])
    def test_booking_past_competition(self, mock_competitions, mock_clubs):
        mock_clubs.extend(self.mock_clubs)
        mock_competitions.extend(self.mock_competitions)

        self.app.post('/showSummary', data={'email': 'club1@test.com'})

        response = self.app.post('/purchasePlaces', data={
            'competition': 'Test Competition Past',
            'club': 'Test Club 1',
            'places': '3'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b'Error: Cannot book a place on a past competition.',
            response.data
            )

    @patch('server.clubs', new_callable=lambda: [])
    @patch('server.competitions', new_callable=lambda: [])
    def test_display_other_clubs_on_booking_page(self, mock_competitions, mock_clubs):
        mock_clubs.extend(self.mock_clubs)
        mock_competitions.extend(self.mock_competitions)

        response = self.app.post(
            '/showSummary',
            data={'email': 'club1@test.com'}
            )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Points available: 8', response.data)
        self.assertNotIn(b'Test Club 1', response.data)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
