import sys
import os
from flask import jsonify, make_response, request
from json import loads
from facebook_model import Facebook_model,Facebook_page_data
from database import db
from flask.ext.restful import Resource, reqparse, fields, marshal_with, abort
from flask.ext.security import current_user
from json import dumps

class Facebook_DAO(object):
    def __init__(self):
        self.user_facebook = Facebook_model.query.filter_by(username=current_user.email).first()

class Facebook_resource(Resource):
    def get(self, **kwargs):
        metric = request.args.get('metric')
        # get Facebook
        facebook_user = Facebook_model.query.filter_by(username=current_user.email).first()
        
        if not facebook_user:
            return jsonify(fb_authed=False)
        else:

            if metric == 'authed':
                return jsonify(authed=True)

            facebook_page = Facebook_page_data.query.filter_by(username=current_user.email).all()

            if hasattr(facebook_page, "__iter__"):
                return make_response(dumps([{'values':[x.as_count() for x in facebook_page]}]))
            
            else:
                return jsonify(facebook_page=facebook_page.as_dict)

    def post(self, **kwargs):
        facebook_user = Facebook_model.query.filter_by(username=current_user.email).first() 
        if facebook_user:
            print facebook_user.username
            return make_response(dumps([{'fb_authed':True}]))
