from flask import Blueprint, render_template, request, session, redirect

app = Blueprint('hypotheses', __name__, template_folder='templates')