import sys
import os
from wufoo_model import WufooSurveyModel, WufooFieldModel, WufooEntryModel, WufooValueModel, WufooSubfieldModel, WufooTextareaSentiment
from flask.ext.restful import Resource
from flask import Flask, request, make_response, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from database import db
from json import dumps, loads
from flask.ext.security import current_user
import traceback
from alchemyapi_python.alchemyapi import AlchemyAPI

"""
class WufooDAO(object):
    def __init__(self, username):
        self.username = username
"""
class WufooResource(Resource):

    def get(self, **kwargs):
        print 'inside get'
        data = request.args
        survey_id = data.get('survey_id')
        username = current_user.email
        d3_json = []
        if username:
            if survey_id:
                return make_response(dumps({'status':500}))
            else:
                surveys = WufooSurveyModel.query.filter_by(username=username)
                for survey in surveys:
                    sentiment = survey.textareas.all()
                    positive = len([x for x in sentiment if x.sentiment_type == "positive"])
                    negative = len([x for x in sentiment if x.sentiment_type == "negative"])
                    neutral = len([x for x in sentiment if x.sentiment_type == "neutral"])
                    sent_dict = []
                    if positive:
                        sent_dict.append({"key":"Positive","y":positive})
                    if negative:
                        sent_dict.append({"key":"Negative","y":negative})
                    if neutral:
                       sent_dict.appen({"key":"Neutral", "y":neutral})
                    d3_json.append({"name":survey.name,"values":sent_dict}) 
                return make_response(dumps(d3_json))
        else:
            pass 

    def post(self):
        """
        Get wufoo data from webhook
        """
        # potential data coming in from wufoo.com
        data = request.form
        # potential data coming in from leanworkbench.com
        if request.data:
            lwb_data = loads(request.data)
            create = lwb_data.get("create")
        else:
            create = False

        # if creating/registering survey to user
        if create:
            if current_user.is_anonymous():
                return dumps([{"status":400}])
            else:
                url = lwb_data.get("url")
                handshake = lwb_data.get("handshake")
                if not url:
                    return jsonify(emsg="No url given")
                else:
                    print 'attempting to add survey'
                    try:
                        name = url.split('/')[-2]
                        new_survey = WufooSurveyModel(username=current_user.email, url=url, name=name, handshake=handshake)
                        db.session.add(new_survey)
                        db.session.commit()
                        return make_response(dumps({"status":200, "msg":"Survey successfully added"}))
                    except:
                        traceback.print_exc()
                        return jsonify(status=500)
        # if webhook and not the user registering the survey for the first time
        else:
            # parse json load
            entry_id = data.get("EntryId")
            form_structure = data.get("FormStructure")
            form_structure_dict =  loads(form_structure)
            created_by = form_structure_dict.get('Email')
            url = form_structure_dict.get("Url")
            field_structure = data.get("FieldStructure")
            field_structure_dict = loads(field_structure)
            fields = field_structure_dict.get("Fields")
            handshake = data.get("HandshakeKey")
            # get survey
            survey = WufooSurveyModel.query.filter_by(wufoo_email=created_by,name=url).all()
            if not survey:
                print 'survey does not exist yet'
                # if survey doesn't exist yet, pass
                return jsonify(status="This survey does not exist yet.")
            survey = survey[-1]
            survey_handshake = survey.handshake
            if handshake == "":
                handshake = None
            if survey_handshake != handshake:
                print 'handshake not equal'
                return jsonify(status="Handshake invalid")

            # get textareas
            textareas = [] 
            for field in fields:
                print field
                field_type = field.get("Type")
                if field_type == "textarea":
                    textareas.append(field.get("ID"))

            alchemyapi = AlchemyAPI(os.getenv("ALCHEMYAPI_KEY"))
            for key in data:
                if key in textareas:
                    text = data[key]
                    response = alchemyapi.sentiment('text', text)
                    if response['status'] == 'OK':
                        docsentiment = response.get("docSentiment")
                        score = docsentiment.get("score")
                        sent_type = docsentiment.get("type")
                        new_sentiment = WufooTextareaSentiment(score=score, 
                            sentiment_type= sent_type, text=text)
                        survey.textareas.append(new_sentiment)
                        db.session.add(survey)
                        db.session.add(new_sentiment)
                        db.session.commit()
                        
                    else:
                        print 'alchemy failed'
