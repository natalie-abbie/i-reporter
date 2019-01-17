from flask import Flask, Blueprint, jsonify, json, request
from datetime import datetime
from functools import wraps
from app.models import User,USERS,FLAGS,Redflag
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash
from .users import loggedinuser

flags = Blueprint('flag', __name__)


@flags.route("/api/v1/create_redflag", methods=['POST'])
def create_redflag():

    try:
        if request.content_type != 'application/json':
            return jsonify({'Bad request': 'Content-type must be in json'}), 400

        request_data = request.get_json()

        if not request_data:
            return jsonify({"Failed": "Request can't be empty"}), 400

        global loggedinuser
        global FLAGS

        if len(loggedinuser) == 0:
            # unauthorized access
            return jsonify({'message': 'please login to create a flag'}), 401

        if 'type' not in request_data.keys():
            # bad request
            return jsonify({'message': 'Flag type is missing'}), 400
        else:
            type = request_data['type']

        if 'location' not in request_data.keys():
            # bad request
            return jsonify({'message': 'location is missing'}), 400
        else:
            location = request_data['location']

        if 'description' not in request_data.keys():
            # bad request
            return jsonify({'message': 'description is missing'}), 400
        if len(request_data['description']) < 20:
            # bad request
            return jsonify({'message': 'description should be well defined'}), 400

        else:
            description = request_data['description']
            
        data={
              "flag_id": str(uuid4()),
              "type":type,
              "location":location,
              "description":description
        }
        loggedinuser.append(data)
        return jsonify({'message': 'flag successfully created', 'flags':loggedinuser}), 201

    except KeyError as item:
        return jsonify({'message': str(item) + 'missing'}), 400
    return jsonify({'message': 'flag was not created, try again'}), 400

# only viewed by admin through the admin accesselse:


@flags.route('/api/v1/redflag', methods=['GET'])
def get():
    """"Function that returns all registered flags"""
    global loggedinuser
    global FLAGS

    if not loggedinuser:
        return jsonify({'message': 'No records found','flags':FLAGS}), 404  # not found
    else:
        return jsonify({'flags': loggedinuser}), 200


@flags.route('/api/v1/redflag/<flag_id>', methods=['GET'])
def get_specific_flag(flag_id):
    """ function to retrieve a single flag by id"""
    global loggedinuser

    for flag_id in loggedinuser:
        if flag_id == flag_id:
            return jsonify({'flag': loggedinuser}), 200  # ok
        else:
            # bad request
            return jsonify({'flag': 'no records of that flag exist'}), 400


@flags.route("/api/v1/redflag/<flag_id>/update", methods=['PATCH'])
def update(flag_id):
    """Function to update flag using the id passed from parameter"""
    global FLAGS
    global loggedinuser

    if len(loggedinuser) == 0:
        # anauthorized access
        return jsonify({'message': 'you are logged out, please login'}), 401

    for data in FLAGS:
        if flag_id == flag_id:
            data[2] = request.get_json()
            return jsonify({"message":"redflag updated", "update":FLAGS}), 200
            
        else:
            # not found
            return jsonify({'message': 'no records of that flag exist'}), 404


@flags.route("/api/v1/redflag/<flag_id>/description", methods=['PATCH'])
def update1(flag_id):
    """Function to update flag description using the id passed from parameter"""
    global FLAGS
    global loggedinuser

    if len(loggedinuser) == 0:
        # anauthorized access
        return jsonify({'message': 'you are logged out, please login'}), 401

    if FLAGS:

        request_data = request.get_json()

        exists = Redflag.get_specific_flag(id)
        flag_id = ''

        if len(request_data.keys()) != 4:
            # bad request
            return jsonify({'message': 'some fields are missing, try again'}), 400

        if request_data['description']:
            description = request_data['description']
        else:
            description = ''

        if exists or exists == 0:
            result = FLAGS[exists]
            for k in result.items():
                flag_id = k
                FLAGS[exists] = {flag_id: [loggedinuser[0], description]}
                # ok
                return jsonify({'message': 'flag description has been updated successfully'}), 200
        else:
            # not found
            return jsonify({'message': 'no records of that flag exist'}), 404


@flags.route("/api/v1/redflag/<flag_id>", methods=['DELETE'])
def delete_flag(flag_id):
    """Function is responsible for deleting a flag on parameter passed as id"""
    global loggedinuser

    for data in loggedinuser:
                if flag_id == flag_id: 
                    loggedinuser.remove(data)            
                    return jsonify({'message': 'flag has been successfully deleted'}), 200
                else:
                    # bad request
                    return jsonify({'message': 'No flag has that id, nothing was deleted'}), 400

# @flags.route("/api/v1/redflag/getlocation", methods=['GET'])
# def location():
#     url = 'https://maps.googleapis.com/maps/api/geocode/json'
#     params = {'sensor': 'false', 'address': 'kampala,bwaise'}
#     r = requests.get(url, params=params)
#     results = r.json()['results']
#     location = results[0]['geometry']['location']
#     location['lat'], location['lng']
    
#     return jsonify({"message":"location created","details":location})
