from flask import Flask, render_template, request, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config["SECRET_KEY"] = "oh-so-secret"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

debug = DebugToolbarExtension(app)

"""To store responses to the questions"""
RESPONSES = []


@app.route("/")
def survey_intro():
    """Enter username, and show title, instructions, button to start survey"""
    return render_template("starter.html", survey=survey)


@app.route("/begin", methods=["POST"])
def begin_survey():
    return redirect("questions/0")


@app.route("/answer", methods=["POST"])
def handle_question():

    choice = request.form["answer"]
    RESPONSES.append(choice)
    if len(RESPONSES) != len(survey.questions):
        return redirect(f"/questions/{len(RESPONSES)}")
    else:
        return redirect("/complete")


@app.route("/questions/<int:qestId>")
def show_question(qestId):
    question = survey.questions[qestId]

    if RESPONSES is None:
        # trying to access question page too soon
        return redirect("/")

    if len(RESPONSES) == len(survey.questions):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    if len(RESPONSES) != qestId:
        # Trying to access questions out of order.
        flash(f"Invalid question id: {qestId}.")
        return redirect(f"/questions/{len(RESPONSES)}")

    return render_template("question.html", question_num=qestId, question=question)


@app.route("/complete")
def complete():
    return render_template("complete.html")
