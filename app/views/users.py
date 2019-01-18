"""endpoints for user operations"""
import datetime
from uuid import uuid4
from flask import Blueprint, jsonify, request, make_response
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import USERS


user = Blueprint('users', __name__)

USERS =[]
loggedinuser = []

specialChars = ['@', '#', '$', '%', '^', '&', '*', '!', '/', '?', '-', '_']

# routes for the api


@user.route('/api/v1/auth/register', methods=['POST'])
def register():
    """ User creates an account.User sign up details are added to the request_data base"""

    try:

        if request.content_type != 'application/json':
            return jsonify({'Bad request': 'Content-type must be json type'}), 400

        request_data = request.get_json()

        if not request_data:
            return jsonify({"message": "Request not made"}), 400

        # validate username
        if 'username' not in request_data.keys():
            # bad request
            return jsonify({'message': 'username is missing'}), 400
        username = request_data['username']

        # valid firstname
        if 'firstname'  not in request_data.keys():
            return jsonify({'Error': 'firstname missing'}), 400
        firstname = request_data['firstname']

        if 'lastname' not in request_data.keys():
            return jsonify({'Error':'lastname missing'}), 400
        lastname = request_data['lastname']

        if 'othernames' not in request_data.keys():
            return jsonify({'Error':'field missing'}), 400   
        othernames = request_data['othernames']      

        if len(request_data['phonenumber']) < 5:
            return jsonify({'Failed':'phonenumber must be 10 characters'}), 400
        phonenumber = request_data['phonenumber']

        # check that email is not missing
        if 'email' not in request_data.keys():
            return jsonify({'message':'email is missing'}), 400  # bad request
        email = request_data['email']

        # valid password
        if 'password' not in request_data.keys():
            # bad request
            return jsonify({'message':'password is missing'}), 400

        if not len(request_data['password']) > 5:
            return jsonify({'Failed': 'password must be atleast 6-8 characters'}), 400
        password = request_data['password']

        if len(request_data['username']) < 5:
            return jsonify({'message':'username should be five characters and above'}), 400 #bad request

        if len(request_data['password']) < 5:
            return jsonify({'message':'password should be five characters and above'}), 400 #bad request
         # check whether username has already been taken.
        for value in username:
            if value in specialChars:
                return jsonify({'message':'username cannot contains special characters'}), 400 #bad request
       #check if the email contains a dot
        if '.' not in request_data['email']:
            return jsonify({'message':'email is invalid, dot missing'}), 400 #bad request

        #check if the email contains an @ symbol
        if '@' not in request_data['email']:
            return jsonify({'message':'email is invalid, @ symbol missing'}), 400 #bad request
        
        #check whether username has already been taken.
        for data in USERS:
            for value in data.items():
                if value == username:            
                    return jsonify({'message':'user already exists'}), 400 #bad request
    
        password = generate_password_hash(password)
        USERS.append({
                      "userid":len(USERS)+1, 
                      "firstname":firstname,
                      "lastname":lastname,
                      "othernames":othernames, 
                      "username":username,
                      "email":email,
                      "password":password, 
                      "phonenumber":phonenumber,
                      "registeredOn":str(datetime.datetime.now())})
        # created
        return jsonify({"message": "Account created successfully", "users":USERS}), 201

    except KeyError as item:
        return jsonify({'Error': str(item) + ' is missing'}), 400


@user.route('/api/v1/getuser', methods=['GET'])
def get_users():
    """ function that returns the users registered"""

    if not USERS:
        return jsonify({'message': 'No users found in the system'})
  
    usersx = USERS
    return jsonify({"USERS": usersx})

# user Login


@user.route('/api/v1/auth/login', methods=['POST'])
def login():
    """
    User login with correct credentials
    token is generated and given to a user
    """

    try:
        # if request.content_type != 'application/json':
        #     return jsonify({'Bad request': 'Content-type must be json type'}), 400

        request_data = request.get_json()

        if not request_data:
            return jsonify({"message": "Request not made"}), 400
        
        auth = request.authorization

        if not USERS:
            # unauthorized access
            return jsonify({'message': 'you are not yet registered'}), 401

        if auth:
            username = auth.username
            password = auth.password
            token = jwt.encode({'user': auth.username, 'exp': datetime.datetime.utcnow(
            ) + datetime.timedelta(minutes=30)}, SECRETKEY)

            if USERS:
                for data in USERS:
                    for key in data:
                        if data['username'] == username and check_password_hash(data['password'], password):
                            loggedinuser.append([data['userid'], data['username']])
                            return jsonify({'token': token.decode('UTF-8'), 'message': 'logged in successfully'}), 200
                        # return jsonify({'message':'Logged in Successfully'}), 200
                        else:
                            return jsonify({'message': 'unauthorised access, invalid username or password'}), 400

        elif request_data:

            if 'username' not in request_data.keys():
                return jsonify({'message': 'username is missing'}), 400

            if 'password' not in request_data.keys():
                return jsonify({'message': 'password is missing'}), 400

            username = request_data['username']
            password = request_data['password']
           
            if USERS:
                for data in USERS:
                    for k in data:
                        if data['username'] == username and check_password_hash(data['password'], password):
                            loggedinuser.append([data['userid'], data['username']])
                            # return jsonify({'token': token.decode('UTF-8'), 'message':'logged in successfully'}), 200
                            return jsonify({'message': 'logged in successfully', 'loggedinusers':loggedinuser}), 200

                        return jsonify({'message': 'unauthorised access, invalid username or password'}), 401

        else:
            # unauthorised access
            return jsonify({"message": "Could not verify authetication"}), 401

        # unauthorised access
        return make_response(jsonify({'message': "couldn't verify login"})), 401

    except KeyError as item:
        return jsonify({'Error': str(item) + ' is missing'}), 400


@user.route('/api/v1/auth/resetpassword', methods=['POST'])
def reset_password():
    """function for a user to reset password"""
   
    request_data = request.get_json()

    if request_data.keys() != 0:
        return jsonify({'message': 'nothing has been provided'}), 400

    if 'password' not in request_data.keys():
        return jsonify({'message': 'password field is missing'}), 400

    new_password = request_data['password']

    # check that we have users registered
    if not USERS:
        # not found
        return jsonify({"message": "no users found, first register"}), 404

    # check if user is already logged in
    if loggedinuser == 0:
        # unauthorized access
        return jsonify({"message": "please first login"}), 401

    # get username for current logged in user
    for user in loggedinuser:
        username = user[1]

    # lets only reset password for currently logged in user.
    for user in USERS:
        for key, value in user.items():
            if key == 'username':
                if value == username:
                    user['password'] = generate_password_hash(new_password)
                    return jsonify({'message': 'password was reset successfully'}), 200

    return jsonify({'message': 'password reset was not successful'}), 400


@user.route('/api/v1/auth/resetpassword', methods=['POST'])
def logout():
    """ function for a user to logout of the platform"""
    global loggedinuser
    global USERS

    if not loggedinuser:
        # bad request
        return jsonify({'message': 'you are already logged out'}), 400

    if len(loggedinuser) < 0:
        del loggedinuser[:]
        request.authorization = None
        # ok
        return jsonify({'message': 'you have successfully logged out'}), 200

    return jsonify({'message': 'something went wrong, please try again'}), 400
