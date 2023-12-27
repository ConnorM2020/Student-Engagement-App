import unittest
import json
from reverseproxy import app 

class ProxyTest(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 404)

    def test_valid_proxy_request(self):
        response = self.app.get('/?port=81')
        self.assertEqual(response.status_code, 200)

    def test_invalid_proxy_request(self):
        # Test request to an unconfigured port
        response = self.app.get('/?port=9999')
        self.assertEqual(response.status_code, 500)

    def test_configure_service(self):d
        new_url = "http://localhost:9999"
        response = self.app.post('/configure/9999', data=new_url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data['message'], f"Configured service on port 9999 with URL {new_url}")

if __name__ == '__main__':
    unittest.main()
