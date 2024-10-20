import unittest
from server import app, competitions, clubs

class BookingTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        
        self.valid_competition = competitions[2]
        self.invalid_competition = competitions[0]
        self.invalid_competition_current_date = competitions[3]
        self.invalid_competition_current_date_late = competitions[4]
        self.first_test_club = clubs[0]
        self.second_test_club = clubs[1]
        self.first_test_places = 10
        self.second_test_places = 2

    def test_booking_valid_competition(self):
        response = self.app.post('/purchasePlaces', data={
            'competition': self.valid_competition['name'],
            'club': self.first_test_club['name'],
            'places': self.first_test_places
        })
        self.assertIn(b'Great-booking complete!', response.data)

    def test_booking_past_competition(self):
        response = self.app.post('/purchasePlaces', data={
            'competition': self.invalid_competition['name'],
            'club': self.second_test_club['name'],
            'places': self.second_test_places
        })
        self.assertIn(b'Error: Cannot book a place on a past competition.', response.data)

    def test_booking_past_competition_current_date_just_in_time(self):
        response = self.app.post('/purchasePlaces', data={
            'competition': self.invalid_competition_current_date['name'],
            'club': self.first_test_club['name'],
            'places': self.first_test_places
        })
        self.assertIn(b'Great-booking complete!', response.data)

    def test_booking_past_competition_current_date_too_late(self):
        response = self.app.post('/purchasePlaces', data={
            'competition': self.invalid_competition_current_date_late['name'],
            'club': self.second_test_club['name'],
            'places': self.second_test_places
        })
        self.assertIn(b'Error: Cannot book a place on a past competition.', response.data)

if __name__ == '__main__':
    unittest.main()