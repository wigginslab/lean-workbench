from quickbooks_model import *
import sys
import requests
from database import db

def mine_qb_data(quickbooks_server_url, api_token, username=None):
        print quickbooks_server_url
        print api_token
        print username
        if username:
            users = [QuickbooksUser.query.filter_by(username=username)]
        else: 
            users = [x for x in QuickbooksUser.query.all()]
        print users[0].username
        for user in users:
            try:
                username = user.username
                user_quickbooks_server_url = quickbooks_server_url+"?username="+username+"&api_key="+api_token
                print quickbooks_server_url
                #if len(users) != 1:
                 #   today = datetime.datetime.now()
                  #  yesterday = today - datetime.timedelta(days=1)
                   # quickbooks_server_url = quickbooks_server_url
                    #+"&start_date="+yesterday+"&end_date="+today
                r = requests.get(user_quickbooks_server_url)
                data = r.json()
                print data
                for row in data:
                    year,month,day = str(date_tuple(row['date']).date()).split("-")
                    year = int(year)
                    month = int(month)
                    day = int(day)
                    new_date = datetime.date(year,month,day)
                    username = username
                    balance = row['balance']
                    name = row['name']
                    new_daily_account_balance = QuickbooksDailyAccountBalance(username=username, balance=balance, date=new_date,name=name)

                    user.daily_balances.append(new_daily_account_balance)
                    user.active = True
                    db.session.add(user)
                    db.session.commit()
            except Exception,e:
                import traceback
                traceback.print_exc()

def date_tuple(date_string):
        date_tuple = datetime.datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")
        return date_tuple
