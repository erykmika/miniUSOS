from flask import *
from flask_login import login_required, logout_user
from logowanie import *
from db import connect
from User import *
from student import student
from prowadzacy import prowadzacy
from admin import admin

app = Flask(__name__,'/static')
app.config['TESTING'] = False
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
login_manager.init_app(app)

# Admin's password
ADMIN_PASS = 'xyz'

app.register_blueprint(student)
app.register_blueprint(prowadzacy)
app.register_blueprint(admin)

con = connect()

# Import routes for particular views
import student
import prowadzacy
import admin

print(app.url_map)

@app.route("/")
def start():
    return render_template("start.html")

@app.route("/login",methods = ['GET','POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        cur = con.cursor()
        if form.role.data == 'student':
            try:
                cur.execute(f"""SELECT haslo, nr_albumu, imie, nazwisko FROM Studenci WHERE email = '{form.login.data}'""")
                fetched_data = cur.fetchone()
                password = fetched_data[0] if fetched_data is not None else None
                if password is not None and form.password.data == password:
                    user = User(fetched_data[1], 'student', fetched_data[2], fetched_data[3])
                    login_user(user)
                    session["user_type"] = "student"
                    return redirect(url_for('student.index'))
            except:
                con.rollback()
        elif form.role.data == 'prowadzący':
            try:
                cur.execute(f"""SELECT haslo, imie, nazwisko FROM Prowadzacy WHERE email = '{form.login.data}'""")
                fetched_data = cur.fetchone()
                password = fetched_data[0] if fetched_data is not None else None
                if password is not None and form.password.data == password:
                    user = User(form.login.data, 'prowadzacy', fetched_data[1], fetched_data[2])
                    login_user(user)
                    session["user_type"] = "prowadzacy"
                    return redirect(url_for('prowadzacy.index'))
            except:
                con.rollback()
        else:
            if form.login.data == 'admin' and form.password.data == ADMIN_PASS:
                user = User(form.login.data, 'admin', "Administrator", "")
                login_user(user)
                session["user_type"] = "admin"
                return redirect(url_for('admin.index'))
    return render_template("login.html",form = form)


@app.route("/logout")
@login_required(role="ANY")
def logout():
    logout_user()
    return redirect(url_for('start'))
