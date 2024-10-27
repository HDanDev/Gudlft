import unittest
from server import app
from unittest.mock import patch


class TestBookingSystem(unittest.TestCase):


    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        self.valid_club_email = 'testclub@valid.com'
        self.invalid_club_email = 'unknown@nonexistent.com'


    @patch('server.clubs', new_callable=lambda: [
        {'name': 'Test Club', 'email': 'testclub@valid.com', 'points': 10},
        {'name': 'Another Club', 'email': 'anotherclub@valid.com', 'points': 15},
    ])
    def test_show_summary_with_valid_email(self, mock_clubs):
        response = self.app.post('/showSummary', data={'email': self.valid_club_email})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome', response.data)


    @patch('server.clubs', new_callable=lambda: [
        {'name': 'Test Club', 'email': 'testclub@valid.com', 'points': 10},
        {'name': 'Another Club', 'email': 'anotherclub@valid.com', 'points': 15},
    ])
    def test_show_summary_with_invalid_email(self, mock_clubs):
        response = self.app.post('/showSummary', data={'email': self.invalid_club_email}, follow_redirects=True)
        
        self.assertIn(b"Sorry, that email wasn&#39;t found.", response.data)


    @patch('server.clubs', new_callable=lambda: [
        {'name': 'Test Club', 'email': 'testclub@valid.com', 'points': 10},
        {'name': 'Another Club', 'email': 'anotherclub@valid.com', 'points': 15},
    ])
    def test_flash_message_displayed(self, mock_clubs):
        response = self.app.post('/showSummary', data={'email': self.invalid_club_email}, follow_redirects=True)
        
        self.assertIn(b"Sorry, that email wasn&#39;t found.", response.data)


if __name__ == '__main__':
    unittest.main()