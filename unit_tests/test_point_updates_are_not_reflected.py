import unittest
from unittest.mock import patch
from server import app


class TestBookingSystem(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('server.clubs', new_callable=lambda: [
        {'name': 'Club One', 'email': 'clubone@email.com', 'points': 10},
        {'name': 'Club Two', 'email': 'clubtwo@email.com', 'points': 8},
        {'name': 'Club Three', 'email': 'clubthree@email.com', 'points': 12}
    ])
    @patch('server.competitions', new_callable=lambda: [
        {
            'name': 'Competition One',
            'date': '2024-12-01 10:00:00',
            'numberOfPlaces': 20
        },
        {
            'name': 'Competition Two',
            'date': '2024-12-02 10:00:00',
            'numberOfPlaces': 15
        }
    ])
    def test_booking_with_multiple_cases(self, mock_competitions, mock_clubs):
        test_cases = [
            (
                mock_clubs[0]['name'],
                mock_competitions[0]['name'],
                5,
                f"Points available: {mock_clubs[0]['points'] - 5}"
            ),
            (
                mock_clubs[1]['name'],
                mock_competitions[1]['name'],
                2,
                f"Points available: {mock_clubs[1]['points'] - 2}"
            ),
            (
                mock_clubs[2]['name'],
                mock_competitions[0]['name'],
                7,
                f"Points available: {mock_clubs[2]['points'] - 7}"
            ),
        ]

        for club_name, comp_name, places, expected_msg in test_cases:
            with self.subTest(competition=comp_name, club=club_name, places=places):
                response = self.app.post('/purchasePlaces', data={
                    'competition': comp_name,
                    'club': club_name,
                    'places': places
                })
                self.assertIn(expected_msg.encode(), response.data)


if __name__ == '__main__':
    unittest.main()
