import unittest
from server import app, competitions, clubs, maxBookingPlaces


class TestBookingSystem(unittest.TestCase):


    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.first_purchase_data = {
            "competition": competitions[0]['name'],
            "club": clubs[0]['name'],
            "places": "5"
        }
        self.second_purchase_data = {
            "competition": competitions[1]['name'],
            "club": clubs[1]['name'],
            "places": maxBookingPlaces
        }
        
        test_failed_club_points = f"{int(maxBookingPlaces) + int(1)}"          

        self.test_failed_purchase_data = {
            "competition": competitions[0]['name'],
            "club": clubs[2]['name'],
            "places": test_failed_club_points
        }


    def test_successful_purchase(self):
        response = self.app.post('/purchasePlaces', data=self.first_purchase_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Great-booking complete!', response.data)


    def test_successful_purchase_exact_amount(self):
        response = self.app.post('/purchasePlaces', data=self.second_purchase_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Great-booking complete!', response.data)


    def test_exceeding_allowed_points(self):
        response = self.app.post('/purchasePlaces', data=self.test_failed_purchase_data)
        assertion = f"Unfortunately, it is not authorized to book more than {maxBookingPlaces} places"
        
        self.assertIn(assertion.encode(), response.data)
        
        
if __name__ == '__main__':
    unittest.main()