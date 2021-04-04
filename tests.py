#Unittest cases for the api

import json, requests
import unittest
import flask
from models import User, db
import app
from flask_jwt_extended import create_access_token
from unittest.mock import patch

'''class to mock requests.get'''
def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.data = json_data
            self.status_code = status_code
            self.text = 'access_token=123&scope=user&token_type=bearer'

        def json(self):
            return self.data

    if args[0] == 'https://github.com/login/oauth/access_token':
        return MockResponse({"access_token": "test_access_token"}, 200)
    elif args[0] == 'https://api.github.com/user':
        return MockResponse({"id": 123, "login": "test_username"}, 200)

    return MockResponse(None, 404)

'''Unittests to test the user profile api app'''        
class UserProfileAppTestCase(unittest.TestCase):
    #setup add and create userobj, access token
    def setUp(self):
        self.app = app.app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        with self.app.app_context():
            self.userObj =  User(username = 'test_username', github_id=123, is_active = True)
            db.session.add(self.userObj)
            db.session.commit()
            access_token = create_access_token(self.userObj.id)
            self.headers = {
                'Authorization': 'Bearer {}'.format(access_token)
            }

    #destroy the user object
    def tearDown(self):
         with self.app.app_context():
            self.userObj =  User.query.filter_by(username = 'test_username').first()
            db.session.delete(self.userObj)
            db.session.commit()

    #login callback method
    @patch('requests.get', side_effect = mocked_requests_get)
    @patch('flask.redirect')
    def test_callback(self, mockRedirect, mockRequests):
        mockRedirect.return_value = ''
        response = self.client.get('/login/callback')
        self.assertEqual(response.status_code, 200)

    #access the user api without authorization
    def test_get_user_without_authorization_header(self):
        response = self.client.get('/user/me')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertDictEqual(data, {'msg': 'Missing Authorization Header'})

    #get user success
    def test_get_user(self):
        response = self.client.get('/user/me', headers = self.headers)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(data, {'github_id': 123, 'id': self.userObj.id, 'is_active': True, 'username': 'test_username'})
    
    #get profile without profile data
    def test_get_profile(self):
        response = self.client.get('/profile', headers = self.headers)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(data, {})

    #update profile without the actual profile
    def test_update_profile_not_available(self):
        self.client.delete('/profile', headers = self.headers)
        response = self.client.put('/profile', headers = self.headers, \
                                    json = {"email": "test@gmail.com"})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(data, {"status":"failed", "message":"Profile not available for the current user."})

    #create profile
    def test_create_profile(self):
        response = self.client.post('/profile', headers = self.headers, \
                                    json = {"email": "test@gmail.com"})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(data, {'currentaddress': '','email': 'test@gmail.com','name': '','phone': '','previousaddress': '','user_id': self.userObj.id})

    #create profile - profile already exists for the user
    def test_create_profile_already_exists(self):
        self.client.post('/profile', headers = self.headers, \
                                    json = {"email": "test@gmail.com"})
        response = self.client.post('/profile', headers = self.headers, \
                                    json = {"email": "test@gmail.com"})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(data, {'message': 'Profile already exists', 'status': 'failed'})

    #update profile
    def test_update_profile(self):
        self.client.post('/profile', headers = self.headers, \
                                    json = {"email": "test@gmail.com"})
        response = self.client.put('/profile', headers = self.headers, \
                                    json = {"email": "test@gmail.com"})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(data, {'currentaddress': '','email': 'test@gmail.com','name': '','phone': '','previousaddress': '','user_id': self.userObj.id})

    #delete profile
    def test_delete_profile(self):
        self.client.post('/profile', headers = self.headers, \
                                    json = {"email": "test@gmail.com"})
        response = self.client.delete('/profile', headers = self.headers)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(data, {"status": "success"})

if __name__ == '__main__':
    unittest.main()

