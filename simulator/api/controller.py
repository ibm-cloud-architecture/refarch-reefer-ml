

from flask import Blueprint
from flask_restful import Resource, Api

"""
 created a new instance of the Blueprint class and bound the Controller resource to it.
"""

control_blueprint = Blueprint("controller", __name__)
api = Api(control_blueprint)


class SimulationController(Resource):
    def get(self):
        return {"status": "success", "message": "pong!"}


api.add_resource(SimulationController, "/control")