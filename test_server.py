import unittest
from server import app, competitions, clubs


class TestBookingSystem(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        self.club_data = {"email": clubs[0]['email']}
        self.purchase_data = {
            "competition": competitions[0]['name'],
            "club": clubs[0]['name'],
            "places": "1"
        }

    def test_show_summary(self):
        response = self.app.post('/showSummary', data=self.club_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome', response.data)

    def test_successful_purchase(self):
        response = self.app.post('/purchasePlaces', data=self.purchase_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'booking complete', response.data)

    def test_insufficient_points(self):
        self.purchase_data['places'] = '5'  
        response = self.app.post('/purchasePlaces', data=self.purchase_data)
        
        print(response.data.decode())
        
        self.assertIn(b'Not enough points to book the required places.', response.data)


    def test_overbooking(self):
        available_places = int(competitions[0]['numberOfPlaces'])
        self.purchase_data['places'] = str(available_places + 1) 
        response = self.app.post('/purchasePlaces', data=self.purchase_data)
        
        print(response.data.decode())

        self.assertIn(b'Not enough places available for booking.', response.data)


if __name__ == '__main__':
    unittest.main()
