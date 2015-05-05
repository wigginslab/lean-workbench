import sys
import os
from quickbooks_model import * 
from flask.ext.restful import Resource, reqparse
from flask import Flask, jsonify, request, make_response
import os
from database import db
from flask.ext.security import current_user
from json import dumps
import requests
import datetime
import time
from sqlalchemy.sql import func

class Quickbooks_DAO(object):

    def __init__(self):
        self.user_qb = QuickbooksUser.query.filter_by(username=current_user.email).first()
        print self.user_qb
    def as_dict(self):
	   return self.user_qb.as_dict()

class Quickbooks_resource(Resource):
    def get(self, **kwargs):
        print 'getting qb'
        args = request.args
        if current_user.is_anonymous():
            print 'anon user'
            return jsonify(qb_authed=False)
        qb = Quickbooks_DAO()
       # if qb.user_qb:
        # get sum of balance for every day
        base_query = db.session.query(
            QuickbooksDailyAccountBalance.date,
                func.sum(QuickbooksDailyAccountBalance.balance).label('total')
           # ).filter(QuickbooksDailyAccountBalance.quickbooks_user_id == current_user.id).group_by(QuickbooksDailyAccountBalance.date)
        ).filter(QuickbooksDailyAccountBalance.quickbooks_user_id == 1).group_by(QuickbooksDailyAccountBalance.date)
        balances =  [(time.mktime(datetime.datetime.timetuple(x[0]))*1000,x[1]) for x in base_query.all()]
        d3_data = [{"key":"Runway", "values":balances, "username":current_user.email}]
        return make_response(dumps(d3_data))
        #else:
         #   return make_response(dumps([{'qb_authed':False, 'username':current_user.email}]))

    def post(self):
        args = request.args
        new_user = args.get('new_user')
        if new_user:
            new_qb_user = QuickbooksUser(username=new_user)
            db.session.add(new_qb_user)
            db.session.commit()
            return jsonify(status=200)
	return jsonify(qb_authed=True)

    def return_date_in_ms(self,date_string):
        """
        For D3 to parse

        args:
            date_string - ruby on rails date string output
        returns:
            date_ms - date in milliseconds
        """
        date_tuple = datetime.datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")
        date_ms = time.mktime(date_tuple)*1000
        return date_ms
