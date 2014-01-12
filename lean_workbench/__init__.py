"""
import os
import json
from flask import Flask, request, Response
from flask import render_template, send_from_directory, url_for
from flask.ext.mail import Mail
from forms.registration_form import ExtendedRegisterForm
from flask_wtf.csrf import CsrfProtect
from flask.ext import restful


class SecuredStaticFlask(Flask):
    def send_static_file(self, filename):
    	protected_templates = ['partials/dashboard.html', 'partials/onboarding/stick.html']
        # Get user from session
        if current_user.is_authenticated() or filename not in protected_templates:
            return super(SecuredStaticFlask, self).send_static_file(filename)
        else:
            return redirect('/static/partials/login.html')

app = SecuredStaticFlask(__name__,static_folder="static", static_path="/static")

app.config.from_object('lean_workbench.settings')

app.url_map.strict_slashes = False

# flask-security
CsrfProtect(app)
mail = Mail(app)

#flask-restful
api = restful.Api(app)

import lean_workbench.core
import lean_workbench.models
import lean_workbench.controllers
"""