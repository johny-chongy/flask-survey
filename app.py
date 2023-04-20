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
    responses.clear()

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
                           question=survey.questions[question_index],
                           question_index = question_index)


@app.post('/answer/<number>')
def redirect_next_question(number):
    """
    redirects to the next question if there is one. otherwise, redirects to
    completion page

    """

    survey_response = request.form["answer"]

    responses.append(survey_response)

    if int(number) >= len(survey.questions):
        flash("yay!")

        return redirect("/completion")
    else:
        return redirect(f"/question/{number}")


@app.get('/completion')
def get_completion():
    """
    renders completion page

    """

    return render_template("completion.html",
                           responses = responses,
                           questions = survey.questions,
                           range = range(len(survey.questions)))