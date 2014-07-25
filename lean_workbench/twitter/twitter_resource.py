import sys
import os
from twitter_model import Twitter_model, Cohort_Tweet_Count_Model
from flask.ext.restful import Resource, reqparse
from flask import Flask, jsonify, request, make_response
import os
from database import db
from flask.ext.security import current_user
from json import dumps

class Twitter_DAO(object):

    def __init__(self):
        self.user_twitter = Twitter_model.query.filter_by(username=current_user.email).first()
        print self.user_twitter
        try:
            self.twitter_handle = self.user_twitter.twitter_handle
        except:
            self.twitter_handle = None

    def as_dict(self):
        return self.user_twitter.as_dict()

class Twitter_resource(Resource):
    def get(self, **kwargs):
        metric = request.args.get('metric')
        if current_user.is_anonymous():
            return jsonify(status=400)
        twitter = Twitter_DAO()
        if twitter.user_twitter:
	    cohorts = current_user.roles
            tracked_words = twitter.user_twitter.words
            counts = [x.as_dict() for x in tracked_words]
            date_count = {}

            for word in counts:
                counts_list = word['counts']
                for count in counts_list:
                    date = count['date']
                    count_at_date = count['count']
                    try:
                            date_count[date] = date_count[date] + count_at_date
                    except:
                            date_count[date] = count_at_date

            values = []

            for key in date_count:
                values.append([key,date_count[key]])

	    if not cohorts:
		return make_response(dumps([{'values':values, key:"Tweets"}]))
	    else:
		cohort_objs = []
		for cohort in cohorts:
		    cohort_name = cohort.name
		    cohort_tweet_counts = Cohort_Tweet_Count_Model.query.filter_by(cohort_name=cohort_name).all()
		    values = [x.as_count() for x in cohort_tweet_counts]
		    print values
		    cohort_obj = {'values':values, 'key': cohort_name+'\'s average tweets'}
		    cohort_objs.append(cohort_obj)

		cohort_objs.append({'values':values, 'key':"Your Tweets"})
		return make_response(dumps(cohort_objs))

        else:
            return jsonify(twitter_authed=False)

    def post(self):
        print 'inside twitter post\n'
        twitter = Twitter_DAO()
        print request.form
        metric = request.args.get('metric')
        print 'metric %s' %(metric)
        if twitter.user_twitter:
            if metric == "authed":
                return make_response(dumps([{'twitter_authed':True}]))
