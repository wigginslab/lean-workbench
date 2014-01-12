from flask import Blueprint, render_template, request, session, redirect

app = Blueprint('quickbooks', __name__, template_folder='templates')

@app.route('/connect/quickbooks/callback')
def quickbooks_callback():
	print 'inside quickbooks callback'
	print request.args