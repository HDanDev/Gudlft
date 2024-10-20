import unittest
from server import app, competitions, clubs


class TestBookingSystem(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        self.valid_club_email = clubs[0]['email']
        self.invalid_club_email = 'unknown@nonexistent.com'

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


if __name__ == '__main__':
    unittest.main()