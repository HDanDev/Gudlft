import unittest
from server import app, competitions, clubs


class TestBookingSystem(unittest.TestCase):


    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        
        self.first_test_club = clubs[0]
        self.second_test_club = clubs[1]
        self.third_test_club = clubs[2]
        self.first_test_competition = competitions[0]
        self.second_test_competition = competitions[1]
        self.first_test_booking = 5
        self.second_test_booking = 2
        self.third_test_booking = 7


    def test_booking_with_multiple_cases(self):
        test_cases = [
            (self.first_test_club['name'], self.first_test_competition['name'], self.first_test_booking, f"Points available: {int(self.first_test_club['points']) - self.first_test_booking}"),
            (self.second_test_club['name'], self.second_test_competition['name'], self.second_test_booking, f"Points available: {int(self.second_test_club['points']) - self.second_test_booking}"),
            (self.third_test_club['name'], self.first_test_competition['name'], self.third_test_booking, f"Points available: {int(self.third_test_club['points']) - self.third_test_booking}"),
        ]

        for club_name, competition_name, places, expected_message in test_cases:
            with self.subTest(competition=competition_name, club=club_name, places=places):
                response = self.app.post('/purchasePlaces', data={
                    'competition': competition_name,
                    'club': club_name,
                    'places': places
                })
                self.assertIn(expected_message.encode(), response.data)


if __name__ == '__main__':
    unittest.main()