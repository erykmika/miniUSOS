from flask import *
from logowanie import *

app = Flask(__name__,'/static')
app.config.update(dict(SECRET_KEY="1"))

@app.route("/")
def start():
    return render_template("start.html")


@app.route("/login",methods = ['GET','POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        if form.login.data == '1' and form.password.data == '1':
            return redirect(url_for('student_main'))
    return render_template("login.html",form = form)


@app.route("/student")
def student_main():
    return render_template("student_main.html")