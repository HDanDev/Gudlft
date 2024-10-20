import unittest
from server import app, competitions, clubs


class TestBookingSystem(unittest.TestCase):


    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.first_purchase_data = {
            "competition": competitions[0]['name'],
            "club": clubs[0]['name'],
            "places": "3"
        }
        self.second_purchase_data = {
            "competition": competitions[1]['name'],
            "club": clubs[1]['name'],
            "places": clubs[1]['points']
        }
        
        test_failed_club = clubs[2]
        self.test_failed_club_points = test_failed_club['points']
        
        self.test_failed_purchase_data = {
            "competition": competitions[0]['name'],
            "club": test_failed_club['name'],
            "places": "65"
        }


    def test_successful_purchase(self):
        response = self.app.post('/purchasePlaces', data=self.first_purchase_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Great-booking complete!', response.data)


    def test_successful_purchase_exact_amount(self):
        response = self.app.post('/purchasePlaces', data=self.second_purchase_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Great-booking complete!', response.data)


    def test_insufficient_points(self):
        response = self.app.post('/purchasePlaces', data=self.test_failed_purchase_data)
        assertion = f"Not enough available points to book the places. You were only able to afford {self.test_failed_club_points}"
        
        self.assertIn(assertion.encode(), response.data)
        
        
if __name__ == '__main__':
    unittest.main()