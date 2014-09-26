from flask.ext.restful import fields, marshal_with, abort
import sys
import os
from google_analytics_models import *
from google_analytics_client import GoogleAnalyticsAPI
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

class GoogleAnalyticsDAO(object):
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
        print 'inside get user profiles'
        print 'self.username :' + self.username
        g = GoogleAnalyticsAPI(self.username)
        if g:
            print 'GA client exists'
            user_accounts = g.get_user_accounts()
            return user_accounts.get('items')
        else:
            return []

    def get_user_profile_visits(self, username):
        """
	return JSON of user and cohort visits (if available)
        """
	cohorts = current_user.roles
        print 'cohorts'
        print cohorts
        user_visitors = GoogleAnalyticsVisitors.query.filter_by(username=username).all()
	
        user_visitors_dict_list = [x.as_dict() for x in user_visitors]
        user_visits = []
        for visit_dict in user_visitors_dict_list:
                date = visit_dict['date']
                count = visit_dict['visitors']
                user_visits.append([date,count])
	if cohorts:
	    return make_response(dumps([{'key':"Your visitors", 'values':user_visits}]))
	else:
	    start = user_visitors[-1].date
	    end = user_visitors[0].date
	    lines = []
	    for cohort in cohorts:
		cohort_name = cohort.name
		cohort_visitors = GoogleAnalyticsVisitors.query.filter(GoogleAnalyticsVisitors.date >= start, GoogleAnalyticsVisitors.date <= end).filter_by(username="cohort:"+cohort_name).all() 
		values = []
		cohort_visitors_dict_list = [x.as_dict() for x in cohort_visitors]
	
		for visit_dict in cohort_visitors_dict_list:
		    date = visit_dict['date']
		    count = visit_dict['visitors']
		    values = [[date,count]] + values
		if values:
		    lines.append({'key':cohort_name +'\'s visitors','values':values})
	    lines.append({'key':"Your visitors",'values':user_visits})

	    return make_response(dumps(lines))

    def get_user_referrals(self, username, metric='source', start_date=None, end_date=None):
	"""
	Calculate page views per source, session view per source, and quantity per medium 
	"""
	if not start_date and not end_date:
	    if metric == 'source':
		unique_sources = db.session.query(GoogleAnalyticsReferralsModel.source.distinct().label('source')).all()
		sources = [GoogleAnalyticsReferralsModel.query.filter_by(username=username, source=source).all() for source in unique_sources]
		source_counts = []
		for source in sources:
		    counts = [s.sessions for s in source]
		    count = sum(counts)
		    source_counts.append(count)
		source_names = [source[0].source for source in sources]
		print source_counts
		print source_names
		source_count_list = []
		for i in range(len(source_counts)):
		    source_count_dict = {}
		    source = source_names[i]
		    source_count = source_counts[i]
		    source_count_dict['key'] = source
		    source_count_dict['y'] = source_count
		    source_count_list.append(source_count_dict)
		return make_response(dumps(source_count_list))

	    elif metric == "mediums":
		unique_mediums = db.session.query(GoogleAnalyticsReferralsModel.medium.distinct().label('medium')).all()
		mediums = [GoogleAnalyticsReferralsModel.query.filter_by(username=username, medium=medium).all() for medium in unique_mediums]
		medium_counts = []
		for medium in mediums:
		    counts = [m.sessions for m in medium]
		    count = sum(counts)
		    medium_counts.append(count)
		medium_names = [medium[0].medium for medium in mediums]
		print medium_counts
		print medium_names
		return ''

class GoogleAnalyticsResource(Resource):
    """
    Handles requests and returns the resources they ask for
    """
    def get(self, **kwargs):
        print 'ga get'
        args =  request.args
        metric = args.get('metric')
        print 'metric %s' %(metric)
        profile = GoogleAnalyticsUserModel.query.filter_by(username=current_user.email).first()
        print 'profile:'
        print profile
        if not profile:
            return jsonify(authed='no')
        profile_id = profile.profile_id
        print 'profile_id:'
        print profile_id
        if profile and profile_id:
                print 'there is profile'
                GA = GoogleAnalyticsDAO(username = current_user.email)
                if not metric:
                    if profile:
                        print 'get user profiles'
                        profiles = GA.get_user_profiles()
                        return make_response(dumps(profiles))
                    else:
                        
                        return jsonify(status=666)
                elif metric == "visits":
                        return GA.get_user_profile_visits(username = current_user.email)
		elif metric == "referrals":
			return GA.get_user_referrals(username = current_user.email)
        else:
                if profile:
                    GA = GoogleAnalyticsDAO(username = current_user.email)
                    print 'trying to get user profiles'
                    try:
                        
                        print 'attempting to get user profiles'
                        profiles = GA.get_user_profiles()
                        return make_response(dumps(profiles))
                    except:
                        return jsonify(status=111)

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
            ga_cred = GoogleAnalyticsUserModel.query.filter_by(username=current_user.email).first()
            print ga_cred.profile_id
            ga_cred.profile_id = profile_id
            db.session.add(ga_cred)
            db.session.commit()
            print 'committed data' 
            db.session.close()
            return jsonify(status=200,message="success!")
	if metric == "visits":
            visits =  GA.get_user_profile_visits()
