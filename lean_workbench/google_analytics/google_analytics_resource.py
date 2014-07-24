from flask.ext.restful import fields, marshal_with, abort
import sys
import os
from google_analytics_models import *
from google_analytics_client import Google_Analytics_API
from flask.ext.restful import Resource, reqparse
from flask.ext.security import current_user
from flask import session, escape, request, jsonify, make_response
from database import db
from json import dumps

path = os.getenv("path")
sys.path.append(path)

parser = reqparse.RequestParser()
parser.add_argument('start_date', type=str)
parser.add_argument('end_date', type=str)
parser.add_argument('dimension', type=str)
parser.add_argument('metric', type=str)

class Google_Analytics_DAO(object):
    """
    Google Analytics Data Access Object
    used to query the GA models for the Resource

    args:
        username: required
        profile_id: id of specific GA profile to query
    """
    def __init__(self, username, profile_id=None, metric=None, dimension=None):
        self.username = username
        self.profile_id = profile_id
        self.metric = metric
        self.dimension = dimension

    def get_user_profiles(self):
        """
        Retrieve all userprofiles of a user
        """
        g = Google_Analytics_API(self.username)
        if g:
            user_accounts = g.get_user_accounts()
            return user_accounts.get('items')
        else:
            return None

    def get_user_profile_visits(self, username):
        """
	return JSON of user and cohort visits (if available)
        """
	cohorts = current_user.roles
    
        user_visitors = Google_Analytics_Visitors.query.filter_by(username=username).all()
        user_visitors_dict_list = [x.as_dict() for x in user_visitors]
        user_visits = []
        for visit_dict in user_visitors_dict_list:
                date = visit_dict['date']
                count = visit_dict['visitors']
                user_visits.append([date,count])
	if not cohorts:
	    return make_response(dumps([{'key':"Your visitors", 'values':visits}]))
	else:
	    lines = []
	    for cohort in cohorts:
		cohort_name = cohort.name
		cohort_visitors = Google_Analytics_Visitors.query.filter_by(username="cohort:"+cohort_name).all()
		values = []
		cohort_visitors_dict_list = [x.as_dict() for x in cohort_visitors]
	
		for visit_dict in cohort_visitors_dict_list:
		    date = visit_dict['date']
		    count = visit_dict['visitors']
		    values.append([date,count])
		lines.append({'key':cohort_name +'\'s visitors','values':values})
	    lines.append({'key':"Your visitors",'values':user_visits})
	    ex = [{'key':'hi','values':[[1406085474000,0],[1406171874000,0]]},{'key':'hi 2','values':[[1406085474000,0],[1406171874000,5]]}]
	    return make_response(dumps(ex))

class Google_analytics_resource(Resource):
    """
    Handles requests and returns the resources they ask for
    """
    def get(self, **kwargs):
        print 'ga get'
        args =  request.args
        metric = args.get('metric')

        profile = Google_Analytics_User_Model.query.filter_by(username=current_user.email).first()
        profile_id = profile.id
        if profile :
                GA = Google_Analytics_DAO(username = current_user.email)
                if not metric:
                        return GA.get_user_profiles()
                elif metric == "visits":
                        return GA.get_user_profile_visits(username = current_user.email)
        else:
                return jsonify(status=333)

                        
    def post(self, **kwargs):
        """
        Get profile-id
        """
        print 'GA post'
        args = request.json 
        username = current_user.email
        metric = args.get('metric')
        profile_id = args.get('profile_id')
        dimension = args.get('dimension')
        print 'args'    
        print args
        print profile_id
        # if just posting profile id
        if metric == 'profile-id':
            print 'inside profile id'
            ga_cred = Google_Analytics_User_Model.query.filter_by(username=current_user.email).first()
            print ga_cred.profile_id
            ga_cred.profile_id = profile_id
            db.session.add(ga_cred)
            db.session.commit()
            print 'committed data' 
            db.session.close()
            return jsonify(status=200,message="success!")
            if metric == "visits":
                visits =  GA.get_user_profile_visits()
