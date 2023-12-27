import unittest
from monitor import app
from unittest.mock import patch
import json

class TestMonitorService(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_check_service_valid(self):
        with patch('monitor.requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = {'some': 'data'}

            response = self.app.get('/check_service?service=http://maxmin:80/')
            self.assertEqual(response.status_code, 200)

    def test_check_service_invalid(self):
        # Test for the check_service route with an invalid service identifier
        response = self.app.get('/check_service?service=invalid_service')
        self.assertEqual(response.status_code, 404)

    def test_monitor(self):
        # Test for the monitor route
        with patch('monitor.monitor_service') as mock_monitor:
            mock_monitor.return_value = ({'some': 'data'}, 0.1)

            response = self.app.get('/monitor')
            self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
