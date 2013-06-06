from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask
import os

# At top of file
from flask_mail import Mail

# Create app
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('db_url')
app.config['SECURITY_PASSWORD_HASH'] = 'sha512_crypt'
app.config['MAIL_SERVER'] = os.getenv('mail_server') 
app.config['MAIL_PORT'] = os.getenv('mail_port')
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.getenv('mail_username') 
app.config['MAIL_PASSWORD'] = os.getenv('mail_password')

mail = Mail(app)

# Create database connection object
db = SQLAlchemy(app)
