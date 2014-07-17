import sys
import os
from wufoo_model import Wufoo_Survey_Model
from flask.ext.restful import Resource, reqparse
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from database import db
from json import dumps
from flask.ext.security import current_user

class Wufoo_DAO(object):
    def __init__(self, username):
        self.username = username

class Wufoo_resource(Resource):

    def get(self, **kwargs):
        if current_user.is_anonymous():
            return dumps([{"status":400}])

    def post(self, **kwargs):
        """
        Get wufoo data from webhook
        """
        # get json data
        data = request.args
        create = data.get("create")
        # if creating/registering survey to user
        if create:
            if current_user.is_anonymous():
                return dumps([{"status":400}])
            else:
                url = data.get("url")
                if not url:
                    return jsonify(error="No url given")
                else:
                    new_survey = Wufoo_Survey_Model(username=current_user.email, url=url)
                    db.session.add(new_survey)
                    db.session.commit()
        # if webhook and not the user registering the survey for the first time
        if not create:
            # parse json load
            created_by = data.get("CreatedBy")
            entry_id = data.get("EntryId")
            form_structure = data.get("FormStructure")
            url = form_structure.get("Url")
            field_structure = data.get("FieldStructure")
            fields = field_structure.get("Fields")
            form_url = "%s.wufoo.com/forms/%surl" %(created_by, url)
            # get survey
            survey = Wufoo_Survey_Model.query.filter_by(url=form_url).last()
            if not survey:
                # if survey doesn't exist yet, pass
                return jsonify(status="This survey does not exist yet.")
            # create new entry
            new_entry = Wufoo_Entry_Model(entry_id=entry_id)
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
                        new_field = Wufoo_Field_Model(field_id=field_id, title = title, field_type = field_type)
                        survey.fields.append(new_field)
                # make new value
                new_value = Wufoo_Value(field_value)
                db.session.add(new_value)
                # add new value to new entry
                new_entry.values.append(new_value)
            
        db.session.add(new_entry)
        # add new entries to survey
        survey.entries.append(new_entry)
        db.session.add(survey)
        db.session.commit()
