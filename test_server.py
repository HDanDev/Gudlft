import unittest
from server import app, competitions, clubs


class TestBookingSystem(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        self.valid_club_email = clubs[0]['email']
        self.invalid_club_email = 'unknown@nonexistent.com'
        
        self.app = app.test_client()
        self.app.testing = True
        
        self.selected_club = clubs[0]
        self.first_test_club = clubs[1]
        self.second_test_club = clubs[2]
        self.other_clubs_number = len([c for c in clubs if c != self.selected_club])

    def test_show_summary_with_valid_email(self):
        response = self.app.post('/showSummary', data={'email': self.valid_club_email})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome', response.data)

    def test_show_summary_with_invalid_email(self):
        response = self.app.post('/showSummary', data={'email': self.invalid_club_email}, follow_redirects=True)
        
        self.assertIn(b"Sorry, that email wasn&#39;t found.", response.data)

    def test_flash_message_displayed(self):
        response = self.app.post('/showSummary', data={'email': self.invalid_club_email}, follow_redirects=True)
        
        self.assertIn(b"Sorry, that email wasn&#39;t found.", response.data)
        
    def test_booking_displaying_clubs(self):
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
