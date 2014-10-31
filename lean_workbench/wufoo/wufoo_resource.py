import sys
import os
from wufoo_model import WufooSurveyModel, WufooFieldModel
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
        data = request.json
        survey_id = data.get('survey_id')
        if not survey_id:
            return make_response(json.dumps({'status':500}))

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
                if not url:
                    return jsonify(emsg="No url given")
                else:
                    print 'attempting to add survey'
                    try:
                        new_survey = WufooSurveyModel(username=current_user.email, url=url)
                        db.session.add(new_survey)
                        db.session.commit()
                        return make_response(dumps({"status":200, "msg":"Survey successfully added"}))
                    except:
                        traceback.print_exc()
                        return jsonify(status=500)
        # if webhook and not the user registering the survey for the first time
        else:
            #TODO: confirm handshake
            print 'not create'
            # parse json load
            created_by = data.get("CreatedBy")
            entry_id = data.get("EntryId")
            form_structure = data.get("FormStructure")
            form_structure_dict =  loads(form_structure)
            url = form_structure_dict.get("Url")
            field_structure = data.get("FieldStructure")
            field_structure_dict = loads(field_structure)
            fields = field_structure_dict.get("Fields")
            form_url = "https://%s.wufoo.com/forms/%s/" %(created_by, url)
            print 'attempt to query for survey'
            # get survey
            survey = WufooSurveyModel.query.filter_by(url=form_url).all()
            if not survey:
                print form_url
                print 'survey does not exist yet'
                # if survey doesn't exist yet, pass
                return jsonify(status="This survey does not exist yet.")
            survey = survey[-1]
            # create new entry
            print 'create new entry for survey'
            new_entry = WufooEntryModel(entry_id=entry_id)
            survey_values = survey.values

            if survey_values:
                values = True
            else:
                values = False
            
            survey_values = []
            new_fields = []
            field_ids = [field.id for field in survey.fields]
            for field in fields:
                # keep track if any modifications
                modified_field = True
                new_field = True
                field_id = field.get("ID")
                title = field.get("Title")
                field_type = field.get("Type")
                subfields = field.get("Subfields")
                field_value = data.get("field_id")

                # check if field_id, field_type, and field_title are still the same
                if field_id in field_ids:
                    new_field = False
                    old_field_index = field_ids.index('field_id')
                    old_field = survey.fields[old_field_index]
                    if old_field.field_id == field_id and old_field.title == title and old_field.field_type == field_type:
                        modified_field = False
                        
                    if new_field or modified_field: 
                        new_field = WufooFieldModel(field_id=field_id, title = title, field_type = field_type)
                        survey.fields.append(new_field)
                # make new value
                new_value = WufooValue(field_value)
                db.session.add(new_value)
                # add new value to new entry
                new_entry.values.append(new_value)
            
        db.session.add(new_entry)
        # add new entries to survey
        survey.entries.append(new_entry)
        db.session.add(survey)
        db.session.commit()
