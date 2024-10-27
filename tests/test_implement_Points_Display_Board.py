import unittest
from unittest.mock import patch
from server import app


class BookingTestCase(unittest.TestCase):


    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        self.selected_club = None
        self.first_test_club = None
        self.second_test_club = None
        self.other_clubs_number = None


    @patch('server.clubs', new_callable=lambda: [
        {'name': 'Selected Club', 'email': 'selected@club.com', 'points': 10},
        {'name': 'First Test Club', 'email': 'first@test.com', 'points': 8},
        {'name': 'Second Test Club', 'email': 'second@test.com', 'points': 6}
    ])
    def test_booking_displaying_clubs(self, mock_clubs):
        self.selected_club = mock_clubs[0]
        self.first_test_club = mock_clubs[1]
        self.second_test_club = mock_clubs[2]
        self.other_clubs_number = len([c for c in mock_clubs if c != self.selected_club])

        response = self.app.post('/showSummary', data={
            'email': self.selected_club['email']
        })

        first_test_club_name = f"{self.first_test_club['name']}"
        first_test_club_points = f"Points available: {self.first_test_club['points']}"
        second_test_club_name = f"{self.second_test_club['name']}"
        second_test_club_points = f"Points available: {self.second_test_club['points']}"
        selected_club_name = f"{self.selected_club['name']}"

        self.assertIn(first_test_club_name.encode(), response.data)
        self.assertIn(first_test_club_points.encode(), response.data)
        self.assertIn(second_test_club_name.encode(), response.data)
        self.assertIn(second_test_club_points.encode(), response.data)
        self.assertNotIn(selected_club_name.encode(), response.data)

        number_of_club_items_rendered = response.data.count(b'class="club-item"')
        self.assertEqual(number_of_club_items_rendered, self.other_clubs_number)


if __name__ == '__main__':
    unittest.main()
