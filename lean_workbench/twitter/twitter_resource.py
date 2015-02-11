import sys
import os
from twitter_model import TwitterModel, CohortTweetCountModel
from flask.ext.restful import Resource, reqparse
from flask import Flask, jsonify, request, make_response, Response
import os
from database import db
from flask.ext.security import current_user
from json import dumps
import time
import datetime

class TwitterDAO(object):

    def __init__(self):
        self.user_twitter = TwitterModel.query.filter_by(username=current_user.email).first()
        print self.user_twitter
        try:
            self.twitter_handle = self.user_twitter.twitter_handle
        except:
            self.twitter_handle = None

    def as_dict(self):
        return self.user_twitter.as_dict()

class TwitterResource(Resource):
    def get(self, **kwargs):
        metric = request.args.get('metric')
        if current_user.is_anonymous():
            error = dumps({'error':'The user is not logged in.'})
            resp = Response(response=error,status=400,mimetype="application/json")
            return resp

        twitter = TwitterDAO()
        if not twitter.user_twitter:
            error = dumps({'error':'No Twitter account is associated with this user.'})
            resp = Response(response=error,status=400,mimetype="application/json")
            return resp
        else:
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

            if not values:
                
                values = [[time.mktime(datetime.datetime.timetuple(datetime.datetime.now())) * 100, 0]]

    	    if not cohorts:
                return make_response(dumps([{'values':values, key:"Tweets"}]))
    	    else:
        		cohort_objs = []
        		for cohort in cohorts:
        		    cohort_name = cohort.name
        		    cohort_tweet_counts = CohortTweetCountModel.query.filter_by(cohort_name=cohort_name).all()
        		    cohort_values = [x.as_count() for x in cohort_tweet_counts]
                            if not cohort_values:
                                cohort_values = [[time.mktime(datetime.datetime.timetuple(datetime.datetime.now())) * 100, 0] for i in range(len(values))]

        		    cohort_obj = {'values':cohort_values, 'key': cohort_name+'\'s average tweets'}
        		    cohort_objs.append(cohort_obj)

        		cohort_objs.append({'values':values, 'key':"Your Tweets"})
        		return make_response(dumps(cohort_objs))

        
            

    def post(self):
        print 'inside twitter post\n'
        twitter = TwitterDAO()
        print request.form
        metric = request.args.get('metric')
        print 'metric %s' %(metric)
        if twitter.user_twitter:
            if metric == "authed":
                return make_response(dumps([{'twitter_authed':True}]))
