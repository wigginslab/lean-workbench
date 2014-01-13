from flask import Blueprint, render_template, request, session, redirect, url_for
from flask.ext.security import current_user
import os
from facebook_model import Facebook_model, db

app = Blueprint('facebook', __name__, template_folder='templates')
