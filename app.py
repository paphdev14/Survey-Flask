from flask import Flask, render_template, request, redirect
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"

debug = DebugToolbarExtension(app)

"""To store responses to the questions"""
RESPONSES = []

"""To store names of the survey users"""
USERNAMES = {}

@app.route('/')
def survey_intro():
    return render_template('survey.html')