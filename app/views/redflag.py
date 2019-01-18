""" endpoints for redflag operations"""
import datetime
from flask import Blueprint, jsonify, request
from app.models import Redflag
from .users import loggedinuser

flags = Blueprint('flag', __name__)

FLAGS =[]
redflag_list = []

@flags.route("/api/v1/create_redflag", methods=['POST'])
def create_redflag():

    """endpoint for creating a redflag"""
    try:

        request_data = request.get_json()

        if not request_data:
            return jsonify({"Failed": "Request can't be empty"}), 400

        # if len(loggedinuser) == 0:
        #     # unauthorized access
        #     return jsonify({'message': 'please login to create a flag'}), 401

        if 'type' not in request_data.keys():
            return jsonify({'message': 'Flag type is missing'}), 400
        type = request_data['type']

        if 'location' not in request_data.keys():
            return jsonify({'message': 'location is missing'}), 400
        location = request_data['location']

        if 'comment' not in request_data.keys():
            return jsonify({'message': 'comment is missing'}), 400          
        if len(request_data['comment']) < 20:
            return jsonify({'message':'comment should be well defined'}), 400
        comment = request_data['comment']
         
        if 'media' not in request_data.keys():
            return jsonify({'message': 'media is missing'}), 400
        media = request_data['media']

        data = {
            "flag_id": len(redflag_list)+1,
            "type":type,
            "location":location,
            "comment":comment,
            "media": media,
            "createdBy":1,
            "status":"draft",
            "createdOn":str(datetime.datetime.now())
        }
        redflag_list.append(data)
        return jsonify({'message':'flag successfully created', 'flags-posted':redflag_list,'status':201}), 201

    except KeyError as item:
        return jsonify({'message': str(item) + 'missing'}), 400
    return jsonify({'message': 'flag was not created, try again'}), 400

# only viewed by admin through the admin accesselse:


@flags.route('/api/v1/redflag', methods=['GET'])
def get():
    """"Function that returns all registered flags"""

    if len(loggedinuser) == 0:
        # anauthorized access
        return jsonify({'message': 'you are not logged in, please login or create account'}), 401

    if not redflag_list:
        return jsonify({'message': 'No records found'}), 404  # not found
    
    return jsonify({'flags': redflag_list,"status":200}), 200

@flags.route('/api/v1/redflag/<int:flag_id>', methods=['GET'])
def get_specific_flag(flag_id):
    """ function to retrieve a single flag by id""" 

    if not redflag_list:
        return jsonify({'message':'no records of any flag exist.'}), 404 #not found
    for data in redflag_list:
        if flag_id == data['flag_id']:
            return jsonify({'flags':data}), 200 #ok
    
        return jsonify({'message':'no flag of that exists'}), 400 #bad request
    
@flags.route("/api/v1/redflag/<flag_id>", methods=['DELETE'])
def delete_flag(flag_id):
    """Function is responsible for deleting a flag on parameter passed as id"""

    for data in loggedinuser:
        if flag_id == flag_id: 
            loggedinuser.remove(data)          
            return jsonify({'message': 'flag has been successfully deleted'}), 200      
        return jsonify({'message': 'No flag has that id, nothing was deleted'}), 400
