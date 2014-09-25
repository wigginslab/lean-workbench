import sys
import os
from flask import jsonify, make_response, request
from json import loads
from facebook_model import FacebookModel, FacebookPageData, CohortFacebookLikesModel
from database import db
from flask.ext.restful import Resource, reqparse, fields, marshal_with, abort
from flask.ext.security import current_user
from json import dumps

class FacebookDAO(object):
    def __init__(self):
        self.user_facebook = FacebookModel.query.filter_by(username=current_user.email).first()

class FacebookResource(Resource):
    def get(self, **kwargs):
        metric = request.args.get('metric')
        # get Facebook
        facebook_user = FacebookModel.query.filter_by(username=current_user.email).first()
        
        if not facebook_user:
            return jsonify(fb_authed=False)
        else:

            if metric == 'authed':
                return jsonify(authed=True)

            facebook_page = FacebookPageData.query.filter_by(username=current_user.email).all()

            if hasattr(facebook_page, "__iter__"):
                roles = current_user.roles
                if not roles:
                    return make_response(dumps([{'values':[x.as_count() for x in facebook_page]}]))
                else:
                    series = [{'values':[x.as_count() for x in facebook_page], 'key':"Your Likes"}]
                    for role in roles:
                        role_name = role.name
                        cohort_data = Cohort_Facebook_Likes_Model.query.filter_by(cohort_name=role_name).all()
                        series_values = [x.as_count() for x in cohort_data]
                        series_dict = {"key": role_name+ "'s Average Likes", 'values': series_values}
                    series.append(series_dict)
                    return make_response(dumps(series))
            
            else:
                return jsonify(facebook_page=facebook_page.as_dict)

    def post(self, **kwargs):
        facebook_user = FacebookModel.query.filter_by(username=current_user.email).first() 
        if facebook_user:
            print facebook_user.username
            return make_response(dumps([{'fb_authed':True}]))