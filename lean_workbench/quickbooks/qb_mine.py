from quickbooks_model import *
import sys
import requests
from database import db

def mine_qb_data(quickbooks_server_url, api_token, username=None):
        if username:
            users = [QuickbooksUserModel.query.filter_by(username=username)]
        else: 
            users = [x for x in QuickbooksUser.query.all()]
        for user in users:
            username = user.username
            quickbooks_server_url = quickbooks_server_url+"?username="+username+"&api_key="+api_token
            if len(users) != 1:
                today = datetime.datetime.now()
                yesterday = today - datetime.timedelta(days=1)
                quickbooks_server_url = quickbooks_server_url+"&start_date="+yesterday+"&end_date="+today
            r = requests.get(quickbooks_server_url)
            data = r.json()
            print data
            for row in data:
                date = date_tuple(row['date'])
                username = username
                balance = row['balance']
                name = row['name']
                new_daily_balance = QuickbooksDailyBalance(username=username, balance=balance, date=date,name=name)
                user.balances.append(new_daily_balance)
                db.session.add(user)
                db.session.commit()

def date_tuple(date_string):
        date_tuple = datetime.datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")
        return date_tuple
