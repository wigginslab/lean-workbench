from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask
import os

# At top of file
from flask_mail import Mail


# Create app
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'super-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('db_url')
app.config['SECURITY_PASSWORD_HASH'] = 'sha512_crypt'
#TODO: replace with envs when ready
app.config['MAIL_SERVER'] = 'smtp.example.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'username' 
app.config['MAIL_PASSWORD'] = 'password'

mail = Mail(app)

# Create database connection object
db = SQLAlchemy(app)




