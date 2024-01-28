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


@admin.route('/admin/komunikaty/edytuj/<id>', methods=['GET'])
@login_required(role="admin")
def edytuj_komunikaty(id):
    con =  Database.connect()
    cur = con.cursor()
    cur.execute(f"""SELECT Komunikaty.Tytul, Komunikaty.Tresc, Komunikaty.id
                    FROM Komunikaty
                    WHERE Komunikaty.id = '{escape(id)}';""")
    
    result = cur.fetchall()
    cur.execute(f"""SELECT nazwa
                    FROM Kierunki_studiow
                    INNER JOIN Komunikaty_kierunki_studiow ON Kierunki_studiow.id = Komunikaty_kierunki_studiow.id_kierunku
                    INNER JOIN Komunikaty ON Komunikaty.id = Komunikaty_kierunki_studiow.id_komunikatu
                    WHERE Komunikaty.id = '{escape(id)}';""")
    result += cur.fetchall()
    result = sum(result,())
    result = [result]
    try:
        return render_template("admin_komunikaty_id.html",
                               name=current_user.name+" "+current_user.secName,messages = result,id=escape(id))
    except TemplateNotFound:
        abort(404)

@admin.route('/admin/komunikaty/edytuj/<id>/zmien', methods=["POST"])
@login_required(role="admin")
def zmien_komunikat(id):
    newTitle = request.form.get("newTitle").strip()
    newMessage = request.form.get("newMessage").strip()
    con =  Database.connect()
    cur = con.cursor()
    try:
        cur.execute(f"""UPDATE
                        Komunikaty
                        SET tytul = '{newTitle}', data = '{datetime.now()}', tresc = '{newMessage}'
                        WHERE id = {escape(id)};""")
        con.commit()
        return redirect('/admin/komunikaty')
    except:
        abort(403)
    
@admin.route('/admin/komunikaty/edytuj/<id>/usun', methods=["POST"])
@login_required(role="admin")
def usun_komunikat(id):
    con =  Database.connect()
    cur = con.cursor()

    cur.execute(f"""DELETE FROM
                        Komunikaty_kierunki_studiow
                        WHERE id_komunikatu = {escape(id)};""")
    
    cur.execute(f"""DELETE FROM
                        Komunikaty
                        WHERE id = {escape(id)};""")
    con.commit()
    return redirect('/admin/komunikaty')



@admin.route('/admin/komunikaty/dodaj', methods=['GET'])
@login_required(role="admin")
def dodaj_komunikat():
    con =  Database.connect()
    cur = con.cursor()

    cur.execute(f"""SELECT nazwa FROM
                    Kierunki_studiow;""")
    result = cur.fetchall()
    lenght = len(result)
    result = sum(result,())
    result = [result]
    return render_template("admin_komunikaty_dodaj.html",
                               name=current_user.name+" "+current_user.secName,messages=result , len=lenght)


@admin.route('/admin/komunikaty/dodaj2', methods=['POST','GET'])
@login_required(role="admin")
def dodawanie_komunikat():
    newTitle = request.form.get("newTitle").strip()
    newMessage = request.form.get("newMessage").strip()
    checkbox_values = request.form.getlist('checkbox')
    con =  Database.connect()
    cur = con.cursor()

    cur.execute(f"""INSERT INTO Komunikaty (tytul, data, tresc)
                            VALUES ('{newTitle}', '{datetime.now()}', '{newMessage}');""")
    con.commit()
    
    cur.execute(f"""SELECT id FROM Komunikaty WHERE tytul = '{newTitle}' AND tresc = '{newMessage}';""")
    result = cur.fetchall()
    
    for i in checkbox_values:
        cur.execute(f"""INSERT INTO Komunikaty_kierunki_studiow (id_kierunku, id_komunikatu)
                            VALUES ('{int(i)+1}','{result[0][0]}');""")
        con.commit()
    return redirect('/admin/komunikaty')


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


@admin.route('/admin/plan_zajec')
@login_required(role="admin")
def plan_zajec():
    con = Database.connect()
    cur = con.cursor()
    try:
        cur.execute(f"""SELECT id, nazwa FROM Kierunki_studiow""")
        result = cur.fetchall()
        kierunki = []
        for row in result:
            kierunki.append({"id": row[0], "nazwa": row[1]})
        return render_template("admin_plan_zajec.html",
                               fields=kierunki)
    except TemplateNotFound:
        abort(404)
    except:
        abort(403)


@admin.route('/admin/plan_zajec/<majorId>', methods=['GET'])
@login_required(role="admin")
def edytuj_plan(majorId):
    con = Database.connect()
    cur = con.cursor()
    try:
        cur.execute(f"""SELECT id, imie, nazwisko FROM Prowadzacy""")
        lecturers_result = cur.fetchall()
        all_lecturers = {}
        for row in lecturers_result:
            all_lecturers[row[0]] = ({"id": row[0], "imie": row[1], "nazwisko": row[2]})

        cur.execute(f"""
                    SELECT Kursy.id, Kursy.dzien_tygodnia, Kursy.nazwa, Kursy.godzina_rozpoczecia, Kursy.godzina_zakonczenia, Kursy.budynek_sala, Kursy.id_prowadzacego, COUNT(Studenci_kursy.nr_albumu) AS ilosc_zapisanych_studentow
                    FROM Kursy
                    LEFT JOIN Studenci_kursy ON Kursy.id = Studenci_kursy.id_kursu
                    WHERE Kursy.id_kierunku='{escape(majorId)}'
                    GROUP BY Kursy.id
                    ORDER BY Kursy.godzina_rozpoczecia ASC;
                    """)
        fetchedResult = cur.fetchall()
        DAYS_MAPPING = {1: 'Poniedziałek', 2: 'Wtorek', 3: 'Środa', 4: 'Czwartek',
                        5: 'Piątek', 6: 'Sobota', 7: 'Niedziela'}
        weekdays = {day: [] for day in DAYS_MAPPING.values()}

        for row in fetchedResult:
            weekdays[DAYS_MAPPING[row[1]]].append({
                "id": row[0],
                "dzien_tygodnia": weekdays[DAYS_MAPPING[row[1]]],
                "nazwa": row[2],
                "godzina_rozpoczecia": row[3],
                "godzina_zakonczenia": row[4],
                "budynek_sala": row[5],
                "prowadzacy": row[6],
                "zapisanych": row[7],
                "id_kierunku": majorId
            })
        return render_template("admin_plan_zajec_kierunek.html", lecturers=all_lecturers, timetable=weekdays, majorId=majorId)

    except TemplateNotFound:
        abort(404)


@admin.route('/admin/plan_zajec/<majorId>/usun', methods=["POST"])
@login_required(role="admin")
def usun_kurs(majorId):
    courseId = request.form.get("courseId")
    con = Database.connect()
    cur = con.cursor()
    try:
        cur.execute(f"""DELETE FROM
                        Studenci_kursy
                        WHERE id_kursu = '{escape(courseId)}';""")
        cur.execute(f"""DELETE FROM
                        Kursy
                        WHERE id = '{escape(courseId)}'""")
        con.commit()
        return redirect(url_for('admin.edytuj_plan', majorId=majorId))
    except TemplateNotFound:
        abort(403)


@admin.route('/admin/plan_zajec/<majorId>/dodaj', methods=['GET', 'POST'])
@login_required(role='admin')
def dodaj_kurs(majorId):
    con =  Database.connect()
    cur = con.cursor()
    form = AddCourse()
    form.lecturer.choices = []
    if request.method=="POST":
        try:
            cur.execute(f"""INSERT INTO Kursy (id, nazwa, budynek_sala, dzien_tygodnia, godzina_rozpoczecia, godzina_zakonczenia, id_kierunku, id_prowadzacego)
                            VALUES ('{escape(form.id.data)}', '{escape(form.course_name.data)}', '{escape(form.building_room.data)}', {form.day.data}, '{escape(form.start_time.data)}', '{escape(form.end_time.data)}', {majorId}, {form.lecturer.data});""")
            con.commit()
            return redirect(url_for('admin.edytuj_plan', majorId=majorId))
        except:
            abort(403)

    cur.execute(f"""SELECT Prowadzacy.id, Prowadzacy.imie, Prowadzacy.nazwisko FROM Prowadzacy""")
    for row in cur.fetchall():
        form.lecturer.choices.append((row[0], str(row[0]) + " " + row[1] + " " + row[2]))
    return render_template("admin_plan_zajec_dodaj.html", form = form, majorId=majorId)

class AddCourse(FlaskForm):
    id = StringField('Identyfikator', validators=[DataRequired()])
    course_name = StringField('Nazwa kursu', validators=[DataRequired()])
    lecturer = SelectField('Prowadzący', choices=[], validators=[DataRequired()])
    day = SelectField('Dzień tygodnia', choices=[(1, 'Poniedziałek'), (2, 'Wtorek'), (3, 'Środa'), (4, 'Czwartek'), (5, 'Piątek'), (6, 'Sobota'), (7, 'Niedziela')], validators=[DataRequired()])
    start_time = TimeField('Godzina rozpoczęcia', validators=[DataRequired()])
    end_time = TimeField('Godzina zakończenia', validators=[DataRequired()])
    building_room = StringField('Budynek', validators=[DataRequired()])
    submit = SubmitField('Dodaj')

@admin.route('/admin/studenci', methods=['GET'])
@login_required(role='admin')
def studenci():
    con = Database.connect()
    cur = con.cursor()
    try:
        return render_template("admin_studenci.html",
                            name=current_user.name+" "+current_user.secName)
    except TemplateNotFound:
        abort(404)

@admin.route('/admin/studenci/<range>', methods=['GET'])
@login_required(role='admin')
def studenci_zakres(range):
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
        return render_template("admin_studenci_zakres.html",
                            name=current_user.name+" "+current_user.secName,
                            students=result)
    except TemplateNotFound:
        abort(404)

@admin.route('/admin/studenci/student/<id>', methods=['GET'])
@login_required(role='admin')
def studenci_wybrany_student(id):
    con = Database.connect()
    cur = con.cursor()
    try:
        cur.execute(f"""SELECT Studenci.email, Studenci.nr_albumu, Studenci.semestr, Studenci.adres,  
                        Kierunki_studiow.nazwa, Kierunki_studiow.stopien
                        FROM Studenci 
                        INNER JOIN Kierunki_studiow 
                        ON Studenci.id_kierunku = Kierunki_studiow.id 
                        WHERE Studenci.nr_albumu = {escape(id)};
                        """)
        fetched_data = cur.fetchone()
        DEGREE_MAPPING = {1: 'Inżynierskie', 2: 'Magisterskie'}

        student = {
            'imie': current_user.name,
            'nazwisko': current_user.secName,
            'email': fetched_data[0],
            'nr_albumu': fetched_data[1],
            'semestr': fetched_data[2],
            'adres': fetched_data[3],
            'kierunek': fetched_data[4],
            'stopien': DEGREE_MAPPING[fetched_data[5]]
        }

        return render_template("admin_studenci_profil.html",
                               student=student)
    except TemplateNotFound:
        abort(403)

