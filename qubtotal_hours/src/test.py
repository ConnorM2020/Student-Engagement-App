import unittest
import json
from app import app

class AddNumbersTestCase(unittest.TestCase): 
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_add_numbers(self):

        response = self.app.get(
        '/?item_1=Lecture%20sessions&attendance_1=10'
        '&item_2=Lab%20sessions&attendance_2=20'
        '&item_3=Support%20sessions&attendance_3=30'
        '&item_4=Canvas%20activities&attendance_4=10')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['error'], False)
        self.assertEqual(data['items'], 
        ['Lecture sessions', 'Lab sessions', 'Support sessions', 'Canvas activities'])
        self.assertEqual(data['attendance'], [10, 20, 30, 10])
        self.assertEqual(data['total'], 70) 

    def test_exceeds_max_values(self):
        response = self.app.get(
        '/?item_1=Lecture%20sessions&attendance_1=35' 
        '&item_2=Lab%20sessions&attendance_2=20'
        '&item_3=Support%20sessions&attendance_3=30'
        '&item_4=Canvas%20activities&attendance_4=10')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['error'], True)
        self.assertIn("exceeds maximum limit", data['message'])

    def test_missing_parameters(self):
        # Missing parameters in the query string
        response = self.app.get('/?item_1=Lecture%20sessions&attendance_1=10')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['error'], True)
        self.assertIn("is missing", data['message'])  

    def test_negative_attendance(self):
        response = self.app.get(
        '/?item_1=Lecture%20sessions&attendance_1=-1' 
        '&item_2=Lab%20sessions&attendance_2=20'
        '&item_3=Support%20sessions&attendance_3=30'
        '&item_4=Canvas%20activities&attendance_4=10')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['error'], True)
        self.assertIn("cannot be negative", data['message'])

if __name__ == '__main__':
    unittest.main()
