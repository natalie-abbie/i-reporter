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

    if not loggedinuser:
        return jsonify({'message': 'No records found'}), 404  # not found
    else:
        return jsonify({'flags': loggedinuser}), 200


@flags.route('/api/v1/redflag/<flag_id>', methods=['GET'])
def get_specific_flag(flag_id):
    """ function to retrieve a single flag by id"""
    global loggedinuser

    