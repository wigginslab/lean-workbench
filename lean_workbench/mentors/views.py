from flask import Blueprint, Response, render_template, request, session, redirect, jsonify,\
url_for, make_response, current_app
from flask.ext.security import current_user
import os

app = Blueprint('mentors', __name__, template_folder='templates')


@app.route('/mentors')
def mentors():
	return render_template('mentors.html')

@app.route('/connect/linkedin')
def connect_linkedin():
	return render_template('connect_linkedin.html')