from werkzeug import SharedDataMiddleware
import os
from flask import Flask, request, Response, render_template, make_response, session, escape,redirect, url_for
import datetime
import random
import re
import jinja2
from socketio import socketio_manage
from socketio.namespace import BaseNamespace
import redis 
from models.user import *
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('db_url')
db = SQLAlchemy(app)
app.secret_key = os.environ.get('secret_key')

@app.route('/')
def index():
	if 'username' in session:
		username = escape(session['username'])
		return render_template('index.html', username=username)
	else:
		return render_template('public.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
	"""
	user registration endpoint
	"""
	print request.data
	username = request.form['username']
	password = request.form['password']
	email = request.form['email']
	user = User(username, password, email)
	db.session.add(user)
	db.session.commit()
	db.session.close()
	print 'registration success!'
	session['username'] = request.form['username']
	return redirect(url_for('index'))
		
@app.route('/login', methods=['POST'])
def login():
	username = request.form['username']
	password = request.form['password']
	user = User.query.filter_by(username=username).first()
	# if no users by that username
	if not user: 		
		return render_template("error.html", error="This user does not exist yet")
	# if user and password correct
	if user.check_password(password):
		session['username'] = request.form['username']
		return redirect(url_for('index'))
	# password incorrect
	else:
		print 'password is incorrect'
		return render_template("error.html", error="Invalid Password")

@app.route('/user/<user>')
def profile(user):
	# check if user logged in
	if 'username' not in session:
		return redirect(url_for('index'))
	#check is user exists
	user = User.query.filter_by(username=user).first()
	profileUser = user.username
	if user:

		return render_template('profile.html',username=profileUser)
	else:
		return render_template('error.html', error="User does not exist")

@app.route('/logout', methods=['POST', 'GET'])
def logout():
	session.pop('username', None)
	return redirect(url_for('index'))

# store static files on server for now
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
	'/': os.path.join(os.path.dirname(__file__), 'static')
})

if __name__ == '__main__':
	app.run(debug=True)
