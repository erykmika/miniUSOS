from flask_login import UserMixin
from flask_login import login_user
from flask_login import LoginManager
from flask_login import current_user
from functools import wraps
from flask_session import Session
from flask import session
from Database import Database

login_manager = LoginManager()

def login_required(role="ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
              return login_manager.unauthorized
            if ((current_user.role != role) and (role != "ANY")):
                return login_manager.unauthorized()
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper


@login_manager.user_loader
def load_user(user_id):
    try:
        con =  Database.connect()
        cur = con.cursor()
        if session.get('user_type') == 'student':
            cur.execute(f"""SELECT imie, nazwisko FROM Studenci WHERE nr_albumu = '{user_id}'""")
        elif session.get('user_type') == 'prowadzacy':
            cur.execute(f"""SELECT imie, nazwisko FROM Prowadzacy WHERE email = '{user_id}'""")
        elif session.get('user_type') == 'admin':
            return User(0, 'admin', 'Administrator', '')
        else:
            return None
        fetched_data = cur.fetchone()
        if fetched_data is None:
            return None
        else:
            return User(user_id, session['user_type'], fetched_data[0], fetched_data[1])
    except:
        return None


# Student's id - nr_albumu
# Prowadzacy's id - email
class User(UserMixin):
    def __init__(self, user_id, role, name, secName):
        self.id = user_id
        self.role = role
        self.name = name
        self.secName = secName

    @property
    def is_student(self):
        return self.role == 'student'

    @property
    def is_prowadzacy(self):
        return self.role == 'prowadzacy'

    @property
    def is_admin(self):
        return self.role == 'admin'
    
    def get_role(self):
        return self.role
