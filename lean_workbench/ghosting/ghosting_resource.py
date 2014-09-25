import sys
import os
from ghosting_model import GhostingModel
from flask.ext.restful import Resource, reqparse
from flask import Flask, jsonify, request, make_response
import os
from database import db
from flask.ext.security import current_user
from json import dumps

class Ghosting_resource(Resource):
    def post(self):
        feature = request.args.get('metric')
        username = current_user.email
        new_ghost = GhostingModel(username=username,feature=feature)
        db.session.add(new_ghost)
        db.session.commit()
        return make_response(dumps([{'msg':"Click added."}]))
