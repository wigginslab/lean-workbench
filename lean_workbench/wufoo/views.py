from flask import Blueprint, render_template, request, session, redirect

app = Blueprint('wufoo', __name__, template_folder='templates')

@app.route('/wufoo', methods=['GET', 'POST'])
def wufoo():
	data = request.args
	field_titles = {}
	field_values = {} 
	field_structure = data['FieldStructure']
	fields = field_structure['Fields']

	# get field titles
	for field in fields:
		field_title = field['Title']
		field_id = field['Id']
		field_titles[field_id] = field_title
		field_values[field_id]= data[field_title]

	# get field values
	for field in field_titles:
		field_model = Wufoo_Field_Model()
	form_structure = data['FormStructure']
	url = form_structure['Url']
	survey = Wufoo_Survey_Model.query.filter_by(url=url)
	if not survey:
		survey = Wufoo_Survey_Model()