from flask import Flask, json, jsonify, request, Blueprint
import os
from instance.config import configuration


app = Flask(__name__)

def create_app(configuration_name):
    '''creates the app and registers Blue prints'''
    app.config.from_object(configuration[configuration_name])
    from app.views.users import user
    from app.views.redflag import flags



    app.register_blueprint(user)
    app.register_blueprint(flags)

    return app