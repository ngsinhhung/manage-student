from flask import Flask, render_template

app = Flask(__name__)



@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/teacher/assignment')
def teacher_assignment():
    return render_template("teacher_assignment.html")


@app.route('/class/create')
def create_class():
    return render_template("create_class.html")


@app.route('/class/edit')
def class_edit():
    return render_template("list_class.html")


@app.route('/register')
def register():
    return render_template("register.html")


@app.route('/<class_id>/info')
def info(class_id):
    return render_template("class_info.html", class_id=class_id)


@app.route("/regulations")
def view_regulations():
    return render_template('view_regulations.html')

if __name__ == "__main__":
    with app.app_context():
        app.run(debug=True)
