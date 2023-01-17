from flask import Flask, session, flash, render_template, request, redirect
#from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config["SECRET_KEY"] = "keeta"

#responses = []

@app.route("/")
def start_survey():
    """START A NEW SURVEY"""
    return render_template("start_survey.html",survey = satisfaction_survey)


@app.route("/question/<int:question_num>")
def show_question(question_num):
    """DISPLAY QUESTION # BASED ON HOW MANY ANSWERS WE'VE ALREADY GOTTEN"""

    if (len(session['responses']) == len(satisfaction_survey.questions)):
        return redirect("/done")
    elif (len(session['responses']) == question_num):
        q_text = satisfaction_survey.questions[question_num].question
        q_choices = satisfaction_survey.questions[question_num].choices
        return render_template("question.html",survey = satisfaction_survey, qid = question_num, txt = q_text, choices = q_choices)
    else:
        flash("You tried to access an incorrect question number.  Redirecting")
        q_text = satisfaction_survey.questions[len(session['responses'])].question
        q_choices = satisfaction_survey.questions[len(session['responses'])].choices
        return render_template("question.html",survey = satisfaction_survey, qid = len(session['responses']), txt = q_text, choices = q_choices)


@app.route("/answer", methods=["POST"])
def handle_question():
    """GET ANSWER VIA POST, AND DECIDE WHETHER TO SHOW THE NEXT QUESTION OR THE THANK YOU PAGE"""
    answer = request.form['ans']
    response_list = session['responses']
    response_list.append(answer)
    session['responses'] = response_list

    #session['responses'].append(answer)

    if (len(session['responses']) == len(satisfaction_survey.questions)):
        return redirect("/done")
    else:
        return redirect("/question/{}".format(len(session['responses'])))
    
@app.route("/done")
def thanks_page():
    """THANK THE USER AND DISPLAY THEIR ANSWERS FOR REVIEW"""
    return render_template("done.html",responses=session['responses'])

@app.route("/start_new_survey",methods=['POST'])
def start_new_survey():
    """START FRESH; CLEAR OUT THE RESPONSES AND MAKE A BLANK LIST"""
    session['responses'] = []
    return redirect("/question/0")