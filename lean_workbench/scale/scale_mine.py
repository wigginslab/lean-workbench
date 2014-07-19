import os
import datetime
from twitter_model import Twitter_model, Date_count
from twython import Twython
from database import db
from flask import current_app
from scale_model import Startup_data_model, VC_model
import requests

def get_vcs(startup_data_models):
    for user in startup_data_models:
        page = user.vc_matcher_page
        description = user.description
        payload = {"description":description}
        # TODO: move this to config eventually
        r = request.get("http://ec2-54-197-83-234.compute-1.amazonaws.com/", params=payload)
        data = r.json()
        try:
            items = data.get("listItems")
            for item in items:
                url = item.get('url')
                name = item.get('name')
                score = item.get('result')
                vc = VC_model(url=crunchbase_url, name=name, score=score)
                db.session.add(vc)
                users.vcs.append(vc)
            db.session.add(users)
            db.session.commit()
        except:
            print 'VC Matcher data error"
        
