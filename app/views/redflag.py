""" endpoints for redflag operations"""
import datetime
from uuid import uuid4
from flask import Blueprint, jsonify, request
from .users import loggedinuser
from app.models import FLAGS, Redflag

flags = Blueprint('flag', __name__)


@flags.route("/api/v1/create_redflag", methods=['POST'])
def create_redflag():

    """endpoint for creating a redflag"""
    try:

        request_data = request.get_json()

        if not request_data:
            return jsonify({"Failed": "Request can't be empty"}), 400

        global loggedinuser

        if len(loggedinuser) == 0:
            # unauthorized access
            return jsonify({'message': 'please login to create a flag'}), 401

        if 'type' not in request_data.keys():
            # bad request
            return jsonify({'message': 'Flag type is missing'}), 400
        type = request_data['type']

        if 'location' not in request_data.keys():
            # bad request
            return jsonify({'message': 'location is missing'}), 400
        location = request_data['location']

        if 'comment' not in request_data.keys():
            # bad request
            return jsonify({'message': 'comment is missing'}), 400
        if len(request_data['comment']) < 20:
            # bad request
            return jsonify({'message': 'comment should be well defined'}), 400
        comment = request_data['comment']  

        if 'media' not in request_data.keys():
            # bad request
            return jsonify({'message': 'media is missing'}), 400
        # if request_data['media'] != mp3 and request_data['media'] != mp4:
        #     return jsonify({'message':'media format not supported'}),400
        media = request_data['media']

        data = {
            "flag_id": str(uuid4()),
            "type":type,
            "location":location,
            "comment":comment,
            "media": media,
            "createdOn":str(datetime.datetime.now())
        }
        loggedinuser.append(data)
        return jsonify({'message':'flag successfully created', 'flags-posted':loggedinuser}), 201

    except KeyError as item:
        return jsonify({'message': str(item) + 'missing'}), 400
    return jsonify({'message': 'flag was not created, try again'}), 400

# only viewed by admin through the admin accesselse:


@flags.route('/api/v1/redflag', methods=['GET'])
def get():
    """"Function that returns all registered flags"""
    global loggedinuser
    global FLAGS

    if len(loggedinuser) == 0:
        # anauthorized access
        return jsonify({'message': 'you are not logged in, please login or create account'}), 401

    if not loggedinuser:
        return jsonify({'message': 'No records found'}), 404  # not found
    
    return jsonify({'flags': loggedinuser}), 200

@flags.route('/api/v1/redflag/<string:flag_id>', methods=['GET'])
def get_specific_flag(flag_id):
    """ function to retrieve a single flag by id"""
    global loggedinuser   

    if not loggedinuser:
        return jsonify({'message':'no records of any flag exist.'}), 404 #not found
    else:
        result = Redflag.get_one_flag(flag_id)
        if result or result == 0:
            return jsonify({'flags2':loggedinuser[result]}), 200 #ok
    
        return jsonify({'flag':loggedinuser[1]}), 400 #bad request
    
@flags.route("/api/v1/redflag/<flag_id>", methods=['DELETE'])
def delete_flag(flag_id):
    """Function is responsible for deleting a flag on parameter passed as id"""
    global loggedinuser

    for data in loggedinuser:
        if flag_id == flag_id: 
            loggedinuser.remove(data)          
            return jsonify({'message': 'flag has been successfully deleted'}), 200
      
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
