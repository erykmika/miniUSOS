from flask import *
from User import *
from jinja2 import TemplateNotFound

student = Blueprint('student', __name__,
                        template_folder='templates')

@student.route('/student')
@login_required(role="student")
def index():
    try:
        return render_template("student_main.html", name=current_user.name+" "+current_user.secName+"["+current_user.id+"]")
    except TemplateNotFound:
        abort(404)


@student.route('/student/komunikaty')
@login_required(role="student")
def komunikaty():
    try:
        con = connect()
        cur = con.cursor()
        cur.execute(f"""SELECT Komunikaty.tytul, Komunikaty.data, Komunikaty.tresc
                        FROM Komunikaty
                        INNER JOIN Komunikaty_kierunki_studiow
                        ON Komunikaty.id = Komunikaty_kierunki_studiow.id_komunikatu
                        INNER JOIN Studenci
                        ON Studenci.id_kierunku = Komunikaty_kierunki_studiow.id_kierunku
                        WHERE Studenci.nr_albumu = {current_user.id};
                    """)
        result = cur.fetchall()
        return render_template("student_komunikaty.html", name=current_user.name+" "+current_user.secName+"["+current_user.id+"]",
                               messages = result)
    except:
        abort(403)
