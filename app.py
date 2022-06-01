from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension

from surveys import *

app = Flask(__name__)

app.config['SECRET_KEY'] = 'keeta'
app.debug=True
debug = DebugToolbarExtension(app)


survey_responses = []
active_survey = 0

@app.route('/pick_survey')
def do_pick_survey():
    return render_template('surveyselect.html',surveys = surveys)

@app.route('/')
def do_main():
    global survey_responses
    survey_responses = []
    global active_survey
    active_survey = surveys[request.args['choose_survey']]
    return render_template('survey.html', survey = active_survey)

@app.route('/questions/<int:q>')
def do_q(q):
    if len(survey_responses) == q:
        return render_template('/question.html',question_num = q, survey = active_survey)
    elif len(survey_responses) == len(active_survey.questions):
        flash("You tried to access an invalid question or a question out of order.  You've been redirected to the correct place")
        return redirect('/thankyou')
    else:
        flash("You tried to access an invalid question or a question out of order.  You've been redirected to the correct place")
        return render_template('/question.html', question_num = len(survey_responses), survey = satisfaction_survey)

@app.route('/answer', methods=['POST'])
def do_answer():
    
    survey_responses.append(request.form.get('answer'))
    questions_answered = len(survey_responses)

    if questions_answered < len(active_survey.questions):
        return redirect(f'/questions/{questions_answered}')
    return redirect('/thankyou')

    return render_template('answer.html')

@app.route('/thankyou')
def do_thankyou():
    return render_template('thankyou.html', data=survey_responses)