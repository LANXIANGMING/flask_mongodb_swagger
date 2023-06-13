import unittest
import json

from app import app
from test.integration.test_base_logger import BaseTestLogger

class LoginTest(unittest.TestCase,BaseTestLogger):

    def setUp(self):
        self.app = app.test_client()

    def test_successful_login(self):
        # Given
        payload = json.dumps({
            "user_email": "user1@ihpc.a-star.edu.sg",
            "user_id": "user1",
            "password": "mypassword"
        })

        # When
        response = self.app.post('/api/v0/login/', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        
        self.assertEqual(str, type(response.json['data']['token']))
        self.assertEqual(200, response.status_code)

    def test_failed_login(self):
        #Given
        payload=json.dumps({
            "user_email":"non_exist_user@mail.com",
            "user_id": "nonexistuser",
            "password": "mypassword"
        })

        # When
        response = self.app.post('/api/v0/login/', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        
        self.assertEqual(dict, type(response.json['data']))
        self.assertEqual(400, response.status_code)
        self.logger.info('Pass test case --Failed login')

    def tearDown(self):
        self.logger.info('TODO: to delete the new created user')
        #Delete Database collections after the test is complete
        #for collection in self.db.list_collection_names():
        #self.db.drop_collection(collection)
