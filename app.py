from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

# TODO: prevent error, make variable for session key and access

SESSION_KEY = 'responses'

@app.get('/')
def get_root():
    """
    renders a page that shows user the title, instructions, and
    button to start survey
    TODO: no need to be TOO specific for doc string
    """

    reset_session = []
    session[SESSION_KEY] = reset_session

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


@app.get('/question/<int:number>')
def show_question(number):
    """
    handles GET request and renders questions html template

    """

    survey_progress = len(session[SESSION_KEY])

    if survey_progress == len(survey.questions):

        flash("Hey! You! Don't do that! You're already done! Get out!")
        return redirect(f"/completion")
    elif survey_progress != number:

        flash("Hey! You! Don't do that! You're trying to access an invalid question!")
        return redirect(f"/question/{survey_progress}")
    else:

        question = survey.questions[number]
        return render_template("question.html",
                            question=question,
                            question_index = number)


@app.post('/answer')
def handle_response():
    """
    receives answer from previous question and appends it to responses list, then
    redirects to the next question if there is one. otherwise, redirects to
    completion page

    """

    survey_response = request.form["answer"]
    current_responses = session[SESSION_KEY]
    current_responses.append(survey_response)
    session[SESSION_KEY] = current_responses #add previous question answer to responses

    survey_progress = len(session[SESSION_KEY])

    if survey_progress >= len(survey.questions):
        flash("yay!")
        return redirect("/completion")
    else:
        return redirect(f"/question/{str(survey_progress)}")


@app.get('/completion')
def get_completion():
    """
    renders completion page

    """

    return render_template("completion.html",
                           responses = session[SESSION_KEY],
                           questions = survey.questions)