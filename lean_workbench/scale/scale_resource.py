import sys
import os
from scale_model import Startup_data_model, VC_model
from flask.ext.restful import Resource, reqparse
from flask import Flask, jsonify, request, make_response
import os
from database import db
from flask.ext.security import current_user
from json import dumps

class Scale_DAO(object):

    def __init__(self):
        self.user_scale = Startup_data_model.query.filter_by(username=current_user.email).first()
        print self.user_scale

    #def as_dict(self):
     #   return self.user_twitter.as_dict()


class Scale_resource(Resource):
    def get(self, **kwargs):
        metric = request.args.get('metric')
        if current_user.is_anonymous():
            return jsonify(status=400)
        scale = Scale_DAO()
        if scale.user_scale:
            return make_response(dumps([{'values':values, key:"Twitter series"}]))

        else:
            return jsonify(scale_authed=False)

    def post(self):

        if current_user.is_anonymous():
            return jsonify(msg="You are no longer logged in",status=400)
        try:
            data = request.json
            cb_url = data.get('crunchbase_url')
            al_url = data.get('angellist_url')
            description = data.get('description')
            new_data = Startup_data_model(username=current_user.email, crunchbase_url=cb_url, angellist_url=al_url, description=description)
            db.session.add(new_data)
            db.session.commit()
            return jsonify(status=200,msg="Data added successfully!")
    except:
        jsonify(msg="Error adding your data.")
