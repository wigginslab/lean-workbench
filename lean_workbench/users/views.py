from flask import Blueprint, jsonify, render_template, redirect, request, session, redirect, current_app
import urllib
import json
import calendar
import time
import oauth2 as oauth

app = Blueprint('users', __name__, template_folder='templates')