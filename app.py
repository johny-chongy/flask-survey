from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = [] # initialize responses list

@app.get('/')
def get_root():
    """
    renders a page that shows user the title, instructions, and
    button to start survey

    """

    return render_template("survey_start.html",
                           survey_title=survey.title,
                           survey_instructions=survey.instructions)

@app.post('/begin')
def begin_survey():
    """
    takes in /begin POST request after clicking 'start' button
    and redirect user to Question 0

    """

    return redirect("/question/0")


@app.get('/question/<number>')
def show_question(number):
    """
    handles GET request and renders questions html template

    """

    question_index = int(number)

    return render_template("question.html",
                           question=survey.questions[question_index])
