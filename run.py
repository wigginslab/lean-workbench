from werkzeug import SharedDataMiddleware
import os
from views.user import index, login, register, profile, logout
from app import app
#from resources.user import UserResource
import os
from flask import Flask, request, Response, render_template, make_response, session, escape,redirect, url_for, jsonify
import datetime
import random
import re
from models.user import User
from datetime import datetime
from app import db, app

@app.route('/')
def index():
	print 'in index'
	if 'username' in session:
		username = escape(session['username'])
		return render_template('index.html', username=username)
	else:
		return render_template('public.html')

@app.errorhandler(401)
def user_already_exists(error):
	return render_template("error.html", error = "This user already exists.")

@app.route('/register', methods=['POST','GET'])
def register():
	"""
	user registration endpoint
	"""
	print 'in register'
	username = request.form['username']
	print username
	password = request.form['password']
	email = request.form['email']
	user = User(username, password, email)
	if user == "Error":
		return render_template("error.html", error="Error: user already exists")
	print user
	print db
	db.session.add(user)
	db.session.commit()
	db.session.close()
	print 'registration success!'
	session['username'] = request.form['username']
	return render_template('index.html', username=username)
	
@app.route('/login', methods=['POST','GET'])
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

@app.route('/logout', methods=["GET","POST"])
def logout():
	session.pop('username', None)
	return redirect(url_for('index'))

"""
app.add_url_rule('/', 'index', index)

app.add_url_rule('/register', 'register', register, methods=['POST', 'GET'])
app.add_url_rule('/login', 'login', login, methods=['POST'])

app.add_url_rule('/logout', 'logout', logout, methods=['POST', 'GET'])

app.add_url_rule('/user/<user>', 'profile', profile)
"""
# store static files on server for now
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
	'/': os.path.join(os.path.dirname(__file__), 'static')
})

if __name__ == '__main__':
	app.run(debug=True)
