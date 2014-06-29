import sys
import os
from twitter_model import Twitter_model
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
        print 'inside twitter get\n'
        metric = request.args.get('metric')
        if current_user.is_anonymous():
            return jsonify(status=400)
        twitter = Twitter_DAO()
        if twitter.user_twitter:
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
            print date_count

            for key in date_count:
                values.append([key,date_count[key]])
            return make_response(dumps([{'values':values, key:"Twitter series"}]))

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
