import sys
import os
from wufoo_model import WufooSurveyModel, WufooFieldModel, WufooEntryModel, WufooValueModel, WufooSubfieldModel
from flask.ext.restful import Resource
from flask import Flask, request, make_response, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from database import db
from json import dumps, loads
from flask.ext.security import current_user
import traceback

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
        if username:
            if survey_id:
                return make_response(dumps({'status':500}))
            else:
                surveys = WufooSurveyModel.query.filter_by(username=username).all()
                return make_response(dumps([survey.as_dict() for survey in surveys]))
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

            # create new entry
            print 'create new entry for survey'
            new_entry = WufooEntryModel(entry_id=entry_id)
            survey_values = survey.fields.all()
            if survey_values:
                values = True
            else:
                values = False
            field_ids = [field.field_id for field in survey_values]
            for field in fields:
                # keep track if any modifications
                modified_field = True
                new_field = True
                field_id = field.get("ID")
                title = field.get("Title")
                field_type = field.get("Type")
                subfields = field.get("SubFields")
                subfields_list = []
                if subfields:
                    for subfield in subfields:
                        field_id = subfield.get('ID')
                        label = subfield.get('Label')
                        new_sub = WufooSubfieldModel(field_id=field_id,label=label)
                        subfields_list.append(new_sub)
                field_value = data.get(field_id)

                # check if field_id, field_type, and field_title are still the same
                if field_id in field_ids:
                    new_field = False
                    old_field = survey.fields.filter_by(field_id=field_id).first()
                    if old_field.field_id == field_id and old_field.title == title and old_field.field_type == field_type:
                        print 'not modified field'
                        modified_field = False
                    else:
                        print 'Modified field'
                        
                if new_field or modified_field: 
                    new_field = WufooFieldModel(field_id=field_id, title = title, field_type = field_type)
                    survey.fields.append(new_field)
                    db.session.commit()
                value_field = survey.fields.filter_by(field_id=field_id).first()
                for subfield in subfields_list:
                    value_field.subfields.append(subfield)
                    db.session.add(value_field)
                    db.session.add(subfield)
                    db.session.commit()
                    
                # make new value
                new_value = WufooValueModel(field_value)
                value_field.values.append(new_value)
                db.session.add(value_field)
                db.session.add(new_value)
                db.session.commit() 
                # add new value to new entry
                new_entry.values.append(new_value)
            
        db.session.add(new_entry)
        # add new entries to survey
        survey.entries.append(new_entry)
        db.session.commit()
