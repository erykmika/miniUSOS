from flask import *
from User import *
from jinja2 import TemplateNotFound
from markupsafe import escape
from flask_wtf import *
from wtforms import *
from wtforms.validators import *
from datetime import datetime


prowadzacy = Blueprint('prowadzacy', __name__,
                        template_folder='templates')

@prowadzacy.route('/prowadzacy')
@login_required(role="prowadzacy")
def index():
    try:
        return render_template("prowadzacy_main.html", name=current_user.name+" "+current_user.secName+"["+current_user.id+"]")
    except TemplateNotFound:
        abort(404)

@prowadzacy.route('/prowadzacy/oceny')
@login_required(role="prowadzacy")
def oceny():
    con = connect()
    cur = con.cursor()
    # Courses led by specific lecturer
    cur.execute(f"""SELECT Kursy.id, Kursy.nazwa
                    FROM Kursy
                    INNER JOIN Prowadzacy ON Kursy.id_prowadzacego = Prowadzacy.id
                    WHERE Prowadzacy.email = '{current_user.id}' 
                    ORDER BY Kursy.nazwa ASC;""")
    result = cur.fetchall()
    try:
        return render_template("prowadzacy_oceny.html",
                               name=current_user.name+" "+current_user.secName+"["+current_user.id+"]",
                               courses=result)
    except TemplateNotFound:
        abort(404)


@prowadzacy.route('/prowadzacy/oceny/<courseId>', methods=['GET'])
@login_required(role="prowadzacy")
def edytuj_oceny(courseId):
    con = connect()
    cur = con.cursor()
    if not verify_prowadzacy_course(escape(courseId)):
        abort(403)
    cur.execute(f"""SELECT Oceny.nr_albumu, Studenci.imie, Studenci.nazwisko, Oceny.ocena, Oceny.data_wpisania, Oceny.id
                    FROM Oceny
                    INNER JOIN Studenci
                    ON Oceny.nr_albumu = Studenci.nr_albumu
                    WHERE Oceny.id_kursu = '{escape(courseId)}'
                    ORDER BY Oceny.id ASC;""")
    
    result = cur.fetchall()
    try:
        return render_template("prowadzacy_oceny_kurs.html",
                               name=current_user.name+" "+current_user.secName+"["+current_user.id+"]",
                               grades_data=result, courseId=escape(courseId))
    except TemplateNotFound:
        abort(404)


@prowadzacy.route('/prowadzacy/oceny/<courseId>/dodaj', methods=['GET', 'POST'])
@login_required(role='prowadzacy')
def dodaj_ocene(courseId):
    con = connect()
    cur = con.cursor()
    if not verify_prowadzacy_course(courseId):
        abort(403)
    form = AddGrade()
    form.student.choices = []
    print(request.method)
    if request.method=="POST":
        try:
            cur.execute(f"""INSERT INTO Oceny (ocena, data_wpisania, nr_albumu, id_kursu)
                            VALUES ('{form.grade.data}', '{datetime.now()}', {form.student.data}, '{courseId}');""")
            con.commit()
            return redirect(url_for('prowadzacy.edytuj_oceny', courseId=courseId))
        except:
            abort(403)
    cur.execute(f"""SELECT Studenci.nr_albumu, Studenci.imie, Studenci.nazwisko
                    FROM Studenci
                    INNER JOIN Studenci_kursy ON Studenci.nr_albumu = Studenci_kursy.nr_albumu
                    INNER JOIN Kursy ON Kursy.id = Studenci_kursy.id_kursu
                    WHERE Kursy.id='{courseId}'; """)
    for row in cur.fetchall():
        form.student.choices.append((row[0], str(row[0]) + " " + row[1] + " " + row[2])) 
    return render_template("prowadzacy_oceny_dodaj.html", form = form, courseId=courseId)


@prowadzacy.route('/prowadzacy/oceny/<courseId>/usun', methods=["POST"])
@login_required(role="prowadzacy")
def usun_ocene(courseId):
    if not verify_prowadzacy_course(courseId) or request.method != "POST":
        abort(403)
    gradeId = request.form.get("gradeId")
    con = connect()
    cur = con.cursor()
    try:
        cur.execute(f"""DELETE FROM
                        Oceny
                        WHERE id = {gradeId};""")
        con.commit()
        return redirect(url_for('prowadzacy.edytuj_oceny', courseId=courseId))

    except:
        abort(403)


@prowadzacy.route('/prowadzacy/oceny/<courseId>/zmien', methods=["POST"])
@login_required(role="prowadzacy")
def zmien_ocene(courseId):
    if not verify_prowadzacy_course(courseId) or request.method != "POST":
        abort(403)
    newGrade = request.form.get("newGrade").lstrip('-+').strip()
    gradeId = request.form.get("gradeId")
    print(newGrade)
    if newGrade not in ("2.0", "3.0", "3.5", "4.0", "4.5", "5.0", "5.5"):
        return redirect(url_for('prowadzacy.edytuj_oceny', courseId=courseId))
    con = connect()
    cur = con.cursor()
    try:
        cur.execute(f"""UPDATE
                        Oceny
                        SET ocena = '{newGrade}', data_wpisania = '{datetime.now()}'
                        WHERE id = {gradeId};""")
        con.commit()
        return redirect(url_for('prowadzacy.edytuj_oceny', courseId=courseId))

    except:
        abort(403)


def verify_prowadzacy_course(courseId):
    con = connect()
    cur = con.cursor()
    cur.execute(f"""SELECT id_prowadzacego
                    FROM Kursy
                    WHERE id = '{courseId}'""")
    idResult = cur.fetchone()
    if idResult is None:
        return False
    lecturerId = idResult[0]
    cur.execute(f"""SELECT email
                    FROM Prowadzacy
                    WHERE id = {lecturerId}""")
    emailResult = cur.fetchone()
    if emailResult is None:
        return False
    email = emailResult[0]
    return current_user.id == email


class AddGrade(FlaskForm):
    student = SelectField('Student', choices=[], validators=[DataRequired()])
    grade = SelectField('Ocena', choices=['2.0', '3.0', '3.5', '4.0', '4.5', '5.0', '5.5'], validators=[DataRequired()])
    submit = SubmitField('Dodaj')
