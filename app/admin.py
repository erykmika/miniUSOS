from flask import *
from User import *
from jinja2 import TemplateNotFound
from markupsafe import escape
from flask_wtf import *
from wtforms import *
from wtforms.validators import *
from Database import Database

admin = Blueprint('admin', __name__,
                        template_folder='templates')

@admin.route('/admin')
@login_required(role="admin")
def index():
    try:
        return render_template("admin_main.html", name=current_user.name+" "+current_user.secName)
    except TemplateNotFound:
        abort(404)

@admin.route('/admin/komunikaty')
@login_required(role="admin")
def oceny():
    con =  Database.connect()
    cur = con.cursor()
    cur.execute(f"""SELECT Komunikaty.tytul, Komunikaty.data, Komunikaty.id
                    FROM Komunikaty
                    ORDER BY Komunikaty.data ASC;""")
    result = cur.fetchall()
    try:
        return render_template("admin_komunikaty.html",
                               name=current_user.name+" "+current_user.secName,
                               messages=result)
    except TemplateNotFound:
        abort(404)


@admin.route('/admin/komunikaty/<id>', methods=['GET'])
@login_required(role="admin")
def edytuj_oceny(id):
    con =  Database.connect()
    cur = con.cursor()
    cur.execute(f"""SELECT Komunikaty.Tytul, Komunikaty.Tresc
                    FROM Komunikaty
                    WHERE Komunikaty.id = '{escape(id)}';""")
    
    result = cur.fetchall()
    try:
        return render_template("admin_komunikaty_id.html",
                               name=current_user.name+" "+current_user.secName,messages = result)
    except TemplateNotFound:
        abort(404)


@admin.route('/admin/zapisy', methods=['GET'])
@login_required(role='admin')
def zapisy():
    con = Database.connect()
    cur = con.cursor()
    try:
        return render_template("admin_zapisy.html",
                            name=current_user.name+" "+current_user.secName)
    except TemplateNotFound:
        abort(404)


@admin.route('/admin/zapisy/<range>', methods=['GET'])
@login_required(role='admin')
def zapisy_zakres(range):
    if escape(range) not in ('AE', 'FL', 'MS', 'SZ'):
        abort(403)
    con = Database.connect()
    cur = con.cursor()
    query_str = ""
    if range == 'AE':
        query_str = "Studenci.nazwisko >= 'A' and Studenci.nazwisko < 'F'"
    elif range == 'FL':
        query_str = "Studenci.nazwisko >= 'F' and Studenci.nazwisko < 'M'"
    elif range == 'MS':
        query_str = "Studenci.nazwisko >= 'M' and Studenci.nazwisko < 'S'"
    else:
        query_str = "Studenci.nazwisko >= 'S'"
    result = []
    try:
        cur.execute("""SELECT Studenci.nr_albumu, Studenci.imie, Studenci.nazwisko, 
                                Kierunki_studiow.nazwa, Kierunki_studiow.stopien, Kierunki_studiow.id
                        FROM Studenci
                        INNER JOIN Kierunki_studiow
                        ON Studenci.id_kierunku = Kierunki_studiow.id
                        WHERE """ + query_str + 
                     """ORDER BY Studenci.nazwisko ASC;""")
        result = [row[:5] for row in cur.fetchall()]
        print(result)
    except:
        abort(403)
    try:
        return render_template("admin_zapisy_zakres.html",
                            name=current_user.name+" "+current_user.secName,
                            students=result)
    except TemplateNotFound:
        abort(404)


@admin.route('/admin/zapisy/student/<id>', methods=['GET', 'POST'])
@login_required(role='admin')
def zapisy_wybrany_student(id):
    con = Database.connect()
    cur = con.cursor()
    if request.method == 'POST':
        try:
            courseId = request.form.get("courseId")
            cur.execute(f"""INSERT INTO Studenci_kursy
                            VALUES ({escape(id)}, '{escape(courseId)}');""")
            return redirect(url_for('admin.zapisy_wybrany_student', id=id))
        except:
            abort(403)
    # 'GET' otherwise - show available courses
    try:
        # Courses that a student can be enrolled in (they are not currently enrolled in)
        cur.execute(f"""SELECT Kursy.id, Kursy.nazwa FROM Kursy
                        INNER JOIN Kierunki_studiow ON Kursy.id_kierunku = Kierunki_studiow.id
                        LEFT JOIN Studenci_kursy on Studenci_kursy.id_kursu = Kursy.id AND Studenci_kursy.nr_albumu = {escape(id)}
                        WHERE Studenci_kursy.nr_albumu is null AND Kursy.id_kierunku = (SELECT id_kierunku FROM Studenci WHERE nr_albumu = {escape(id)})
                        ORDER BY Studenci_kursy.id_kursu ASC;""")
        result_not_enrolled = cur.fetchall()
        # Courses that the student is enrolled in
        cur.execute(f"""SELECT Kursy.id, Kursy.nazwa FROM Kursy
                        INNER JOIN Studenci_kursy ON Kursy.id = Studenci_kursy.id_kursu
                        WHERE Studenci_kursy.nr_albumu = {escape(id)}
                        ORDER BY Kursy.id ASC;""")
        result_enrolled = cur.fetchall()
        return render_template("admin_zapisy_student.html",
                            name=current_user.name+" "+current_user.secName,
                            courses1=result_not_enrolled,
                            courses2=result_enrolled,
                            id=id)
    except TemplateNotFound:
        abort(403)

@admin.route('/admin/zapisy/student/<id>/usun', methods=['POST'])
@login_required(role='admin')
def zapisy_wybrany_student_usun(id):
    con = Database.connect()
    cur = con.cursor()
    if request.method == 'POST':
        try:
            courseId = request.form.get("courseId")
            cur.execute(f"""DELETE FROM Studenci_kursy
                            WHERE nr_albumu = {escape(id)}
                            AND id_kursu = '{escape(courseId)}';
                        """)
            return redirect(url_for('admin.zapisy_wybrany_student', id=id))
        except:
            abort(403)
