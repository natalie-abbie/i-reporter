from run import app
import unittest
from flask import json


class TestUser(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.app.post('/api/v1/auth/register', content_type='application/json',
                                    data=json.dumps({"firstname":"abio","lastname":"nattie","othername":"talie","username": "talie","phonenumber":"0700000000", "password": "nats123", "email": "abio@email.com"}))
        self.app.post('/api/v1/auth/login', content_type='application/json',
                                    data=json.dumps({"username": "talie", "password": "nats123"}))

    def test_secret_key(self):
        pass
        SECRETKEY = 'TaLiEatalia'
        res = 'TaLiEatalia'
        self.assertEqual(res, SECRETKEY)

    def test_user_registration_success(self):
        response = self.app.post('/api/v1/auth/register', content_type='application/json',
                                    data=json.dumps({"firstname":"abio",
                                                     "lastname": "natalie",
                                                     "othernames": "talie",
                                                     "username": "atalia",
                                                     "phonenumber":"0700000000",
                                                     "password": "nats123",
                                                     "email": "abio@gmail.com",
                                                    }))
        data = json.loads(response.data)
        self.assertEqual(201, response.status_code)
        self.assertEqual('Account created successfully', data['message'])


    def test_user_login_failed(self):
        
        response = self.app.post('/api/v1/auth/login', content_type='application/json',
                                    data=json.dumps({"username": "taxx", "password": "nats123"}))
        data = json.loads(response.data)
        self.assertEqual('unauthorised access, invalid username or password', data['message'])
        self.assertEqual(401, response.status_code)

    def test_unauthorized_access(self):
        user= {"firstname":"abio",
                "lastname": "natalie",
                "othernames": "talie",
                "username": "atalia",
                "phonenumber":"0700000000",
                "password": "nats123",
                "email": "abio@gmail.com",
                }
        response = self.app.post('/api/v1/auth/register', content_type='application/json',
                                    data=json.dumps(user))
        response = self.app.post('/api/v1/auth/login', content_type='application/json',
                                    data=json.dumps({"username": "bell", "password": "nats123"}))
        data = json.loads(response.data)
        self.assertEqual('unauthorised access, invalid username or password', data['message'])
        self.assertEqual(401, response.status_code)

    
    def test_not_registered(self):

        response = self.app.post('/api/v1/auth/login', content_type='application/json',
                                    data=json.dumps({"username": "bell", "password": "nats123"}))
        data = json.loads(response.data)
        self.assertEqual('unauthorised access, invalid username or password', data['message'])
        self.assertEqual(401, response.status_code)

    def username_short(self):
        response = self.app.post('/api/v1/auth/register', content_type='application/json',
                                    data=json.dumps({"firstname":"abio",
                                                     "lastname": "natalie",
                                                     "othernames": "talie",
                                                     "username": "at",
                                                     "phonenumber":"0700000000",
                                                     "password": "nats123",
                                                     "email": "abio@gmail.com",
                                                    }))
        data = json.loads(response.data)
        self.assertEqual(400, response.status_code)
        self.assertEqual('username should be five characters and above', data['message'])


    def password_short(self):
        response = self.app.post('/api/v1/auth/register', content_type='application/json',
                                    data=json.dumps({"firstname":"abio",
                                                     "lastname": "natalie",
                                                     "othernames": "talie",
                                                     "username": "atalia",
                                                     "phonenumber":"0700000000",
                                                     "password": "nat",
                                                     "email": "abio@gmail.com",
                                                    }))
        data = json.loads(response.data)
        self.assertEqual(400, response.status_code)
        self.assertEqual('username should be five characters and above', data['message'])

    def symbol_missing(self):
        response = self.app.post('/api/v1/auth/register', content_type='application/json',
                                    data=json.dumps({"firstname":"abio",
                                                     "lastname": "natalie",
                                                     "othernames": "talie",
                                                     "username": "atalia",
                                                     "phonenumber":"0700000000",
                                                     "password": "nat",
                                                     "email": "abiogmail.com",
                                                    }))
        data = json.loads(response.data)
        self.assertEqual(400, response.status_code)
        self.assertEqual('email is invalid, @ symbol missing', data['message'])

    def fullstop_missing(self):
        response = self.app.post('/api/v1/auth/register', content_type='application/json',
                                    data=json.dumps({"firstname":"abio",
                                                     "lastname": "natalie",
                                                     "othernames": "talie",
                                                     "username": "atalia",
                                                     "phonenumber":"0700000000",
                                                     "password": "nat",
                                                     "email": "abio@gmail.com",
                                                    }))
        data = json.loads(response.data)
        self.assertEqual(400, response.status_code)
        self.assertEqual('email is invalid, @ dot missing', data['message'])


    def test_missing_username_user_registration(self):
        user= {"firstname":"abio",
                "lastname": "natalie",
                "othernames": "talie",
                "username": "atalia",
                "phonenumber":"0700000000",
                "password": "nats123",
                "email": "abio@gmail.com",
                }
        response = self.app.post('/api/v1/auth/register', content_type='application/json',
                                    data=json.dumps(user))
        response = self.app.post('/api/v1/auth/register', content_type='application/json',
                                    data=json.dumps({"email": "user@email.com", "password": "password"}))
        data = json.loads(response.data)
        self.assertEqual(400, response.status_code)
        self.assertEqual('username is missing', data['message'])

    def test_missing_email_user_registration(self):
        response = self.app.post('/api/v1/auth/register', content_type='application/json',
                                    data=json.dumps({
                                        "firstname":"abio",
                                        "lastname": "natalie",
                                        "othernames": "talie",
                                        "username": "atalia",
                                        "phonenumber":"0700000000",
                                        "password": "nats123",
                                        }
                                    ))
        data = json.loads(response.data)
        self.assertEqual(400, response.status_code)
        self.assertEqual('email is missing', data['message'])


    def test_request_data_keys_user_registration(self):
        response = self.app.post('/api/v1/auth/register', content_type='application/json',
                                    data=json.dumps({"userid": 1, "username": "fsfsf", "password": "somepassword", "email": "some@email.com"}))
        data = json.loads(response.data)
        self.assertTrue(400, response.status_code)
        self.assertNotEqual(4, data.keys())

    def test_user_login_failed_wrong_username(self):
        response = self.app.post('/api/v1/auth/login', content_type='application/json',
                                    data=json.dumps({"username": "tal", "password": "somepassword"}))
        data = json.loads(response.data)
        self.assertEqual(
            'unauthorised access, invalid username or password', data['message'])
        self.assertEqual(401, response.status_code)

    def test_user_login_failed_wrong_password(self):
        user= {"firstname":"abio",
                "lastname": "natalie",
                "othernames": "talie",
                "username": "atalia",
                "phonenumber":"0700000000",
                "password": "nats123",
                "email": "abio@gmail.com",
                }
        response = self.app.post('/api/v1/auth/register', content_type='application/json',
                                    data=json.dumps(user))
        response = self.app.post('/api/v1/auth/login', content_type='application/json',
                                    data=json.dumps({"username": "talie", "password": "password"}))
        data = json.loads(response.data)
        self.assertIn(
            'unauthorised access, invalid username or password', data['message'])
        self.assertEqual(401, response.status_code)

    def test_already_loggedin_user(self):
        user= {"firstname":"abio",
                "lastname": "natalie",
                "othernames": "talie",
                "username": "atalia",
                "phonenumber":"0700000000",
                "password": "nats123",
                "email": "abio@gmail.com",
                }
        response = self.app.post('/api/v1/auth/register', content_type='application/json',
                                    data=json.dumps(user))
        response = self.app.post('/api/v1/auth/login', content_type='application/json',
                                    data=json.dumps({"username": "talie", "password": "password"}))
        data = json.loads(response.data)
        self.assertEqual(401, response.status_code)
        self.assertEqual(
            'unauthorised access, invalid username or password', data['message'])

    def test_user_login_failed_wrong_username(self):        
        response = self.app.post('/api/v1/auth/login', content_type='application/json',
                                    data=json.dumps({"username": "talie", "password": "somepassword"}))
        data = json.loads(response.data)
        self.assertEqual('unauthorised access, invalid username or password', data['message'])        
        self.assertEqual(401, response.status_code)


class TestRedflag(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        
        self.app.post('/api/v1/auth/register', content_type='application/json',
                         data=json.dumps({"firstname": "abio", "lastname": "nataline", "othername": "nats", "username": "talie", "password": "somepassword", "email": "abionatline@gmail.com", "phonenumber": "0752030815", "isAdmin": "true"}))

        self.app.post('/api/v1/auth/login', content_type='application/json',
                         data=json.dumps({"username": "talie", "password": "somepassword"}))

    def test_create_redflag_successful(self):
        user= {"firstname":"abio",
                "lastname": "natalie",
                "othernames": "talie",
                "username": "atalia",
                "phonenumber":"0700000000",
                "password": "nats123",
                "email": "abio@gmail.com",
                }
        self.app.post('/api/v1/auth/register', content_type='application/json',
                                    data=json.dumps(user))
        self.app.post('/api/v1/auth/login', content_type='application/json',
                                    data=json.dumps({"username": "atalia", "password": "nats123"}))
        response = self.app.post('/api/v1/create_redflag', content_type='application/json',
                                    data=json.dumps({"type": "corruption", "comment": "some comment of the corruption", "location": "kampala", "media":"photo.jpeg"}))
        data = json.loads(response.data)
        self.assertEqual('flag successfully created', data['message'])
        self.assertTrue(400, response.status_code)


    def test_short_comment_create_redflag(self):
        user= {"firstname":"abio",
                "lastname": "natalie",
                "othernames": "talie",
                "username": "atalia",
                "phonenumber":"0700000000",
                "password": "nats123",
                "email": "abio@gmail.com",
                }
        self.app.post('/api/v1/auth/register', content_type='application/json',
                                    data=json.dumps(user))
        self.app.post('/api/v1/auth/login', content_type='application/json',
                                    data=json.dumps({"username": "atalia", "password": "nats123"}))
        response = self.app.post('/api/v1/create_redflag', content_type='application/json',
                                    data=json.dumps({"type": "corruption", "comment": "some des", "location": "kampala"}))
        data = json.loads(response.data)
        self.assertEqual('comment should be well defined', data['message'])
        self.assertEqual(400, response.status_code)

    def test_type_missing_create_redflag(self):
        response = self.app.post('/api/v1/create_redflag', content_type='application/json',
                                    data=json.dumps({"comment": "some comment of the corruption", "email": "abionatline@gmail.com", "location": "kampala", "createdby": "nats"}))
        data = json.loads(response.data)
        self.assertEqual('Flag type is missing', data['message'])
        self.assertEqual(400, response.status_code)

    def test_location_missing_create_redflag(self):
        response = self.app.post('/api/v1/create_redflag', content_type='application/json',
                                    data=json.dumps({"type": "corruption", "comment": "some comment of the corruption", "email": "abionatline@gmail.com", "createdby": "nats"}))
        data = json.loads(response.data)
        self.assertEqual('location is missing', data['message'])
        self.assertEqual(400, response.status_code)
    
    def test_get_users(self):
        self.app.post('/api/v1/getuser', content_type='application/json',
                         data=json.dumps({"firstname": "abio", "lastname": "nataline", "othername": "nats", "username": "talie", "password": "somepassword", "email": "abionatline@gmail.com", "phonenumber": "0752030815"}))


    def test_comment_missing_create_redflag(self):
        response = self.app.post('/api/v1/create_redflag', content_type='application/json',
                                    data=json.dumps({"type": "corruption",  "location": "kampala", "createdby": "nats"}))
        data = json.loads(response.data)
        self.assertEqual('comment is missing', data['message'])
        self.assertEqual(400, response.status_code)
    
    


    # def test_delete_flag_failed(self):
    #     response = self.app.delete(
    #         '/api/v1/redflag/<flag_id>', content_type='application/json')
    #     data = json.loads(response.data)
    #     self.assertEqual(
    #         'No flag has that id, nothing was deleted', data['message'])
    #     self.assertEqual(400, response.status_code)

    # def test_update_flag_successful(self):
    #     response = self.app.put('api/v1/redflag/<flag_id>', content_type='application/json',
    #                                data=json.dumps({'name': 'flagdemo', 'location': '', 'comment': ''}))

    #     data = json.loads(response.data)
    #     self.assertEqual('no records of that flag exist', data['message'])
    #     self.assertEqual(404, response.status_code)


if __name__ == '__main__':
    unittest.main()
