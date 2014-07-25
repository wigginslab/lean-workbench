import os
import datetime
from database import db
from flask import current_app
from scale_model import Startup_data_model, VC_model
import requests
import traceback

def get_vcs(startup_data_models):
    for user in startup_data_models:
        page = user.vc_matcher_page + 1
        db.session.add(user)
        db.session.commit()
        description = user.description
        payload = {"description":description}
        # TODO: move this to config eventually
        r = requests.get("http://ec2-54-197-83-234.compute-1.amazonaws.com/get/vcs/"+str(page), params=payload)
        print r.text
        data = r.json()
        print data
        try:
            items = data.get("listItems")
            print 'got list items'
            for item in items:
                url = item.get('url')
                name = item.get('name')
                score = item.get('result')
                vc = VC_model(crunchbase_url=url, name=name, score=score)
                db.session.add(vc)
                user.vcs.append(vc)
            

            user.vc_matcher_page = page 
            if page == 8:
                user.vc_matcher_done = True
            db.session.add(user)
            db.session.commit()

        except:
            print 'VC Matcher data error'
            traceback.print_exc()

