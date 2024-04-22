from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("teacher/teacher_assignment.html")

@app.route("/inputScore")
def input_score():
    return render_template("inputScore.html")
@app.route("/score_subject")
def score_of_subject():
    return render_template("inputScoreSubject.html")


@app.route("/view_score")
def view_score():
    return render_template("viewScore.html")

if __name__ == "__main__":
    app.run(debug=True)
