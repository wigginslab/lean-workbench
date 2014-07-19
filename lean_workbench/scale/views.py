from flask import Blueprint, Response, render_template, request, session, redirect, jsonify,\
url_for, make_response, current_app
from flask.ext.security import current_user
import os
import urllib

app = Blueprint('scale', __name__, template_folder='templates')


