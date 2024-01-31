from flask import *
from User import *
from jinja2 import TemplateNotFound
from Database import Database
from markupsafe import escape

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
        con =  Database.connect()
        cur = con.cursor()
        cur.execute(f"""SELECT Komunikaty.tytul, Komunikaty.data, Komunikaty.tresc
                        FROM Komunikaty
                        INNER JOIN Komunikaty_kierunki_studiow
                        ON Komunikaty.id = Komunikaty_kierunki_studiow.id_komunikatu
                        INNER JOIN Studenci
                        ON Studenci.id_kierunku = Komunikaty_kierunki_studiow.id_kierunku
                        WHERE Studenci.nr_albumu = {current_user.id}
                        ORDER BY Komunikaty.data DESC;
                    """)
        result = cur.fetchall()
        return render_template("student_komunikaty.html", name=current_user.name+" "+current_user.secName+"["+current_user.id+"]",
                               messages = result)
    except:
        abort(403)


@student.route('/student/profil')
@login_required(role="student")
def profil():
    con = Database.connect()
    cur = con.cursor()
    try:
        cur.execute(f"""SELECT Studenci.email, Studenci.nr_albumu, Studenci.semestr, Studenci.adres,  
                        Kierunki_studiow.nazwa, Kierunki_studiow.stopien
                        FROM Studenci 
                        INNER JOIN Kierunki_studiow 
                        ON Studenci.id_kierunku = Kierunki_studiow.id 
                        WHERE Studenci.nr_albumu = '{current_user.id}';
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

        return render_template("student_profil.html",
                               student=student)
    except TemplateNotFound:
        abort(404)


@student.route('/student/plan_zajec', methods=["GET"])
@login_required(role="student")
def plan_zajec():
    con =  Database.connect()
    cur = con.cursor()
    try:
        cur.execute(f"""SELECT Kursy.dzien_tygodnia, Kursy.nazwa, Kursy.godzina_rozpoczecia, Kursy.godzina_zakonczenia, Kursy.budynek_sala
                        FROM Kursy
                        INNER JOIN Studenci_kursy
                        ON Kursy.id = Studenci_kursy.id_kursu
                        INNER JOIN Studenci
                        ON Studenci.nr_albumu = Studenci_kursy.nr_albumu
                        WHERE Studenci.nr_albumu = '{current_user.id}'
                        ORDER BY Kursy.godzina_rozpoczecia ASC;""")
        fetchedResult = cur.fetchall()
        DAYS_MAPPING = {1: 'Poniedziałek', 2: 'Wtorek', 3: 'Środa', 4: 'Czwartek',
                        5: 'Piątek', 6: 'Sobota', 7: 'Niedziela'}
        weekdays = { day : [] for day in DAYS_MAPPING.values() }
        for row in fetchedResult:
            weekdays[DAYS_MAPPING[row[0]]].append([row[1], row[2], row[3], row[4]])
        return render_template("student_plan_zajec.html", name=current_user.name+" "+current_user.secName+"["+current_user.id+"]",
                                timetable=weekdays)
    except:
        abort(403)

@student.route('/student/oceny')
@login_required(role="student")
def oceny():
    con =  Database.connect()
    cur = con.cursor()
    cur.execute(f"""SELECT Oceny.ocena, kursy.nazwa
                    FROM Oceny
                    INNER JOIN Studenci
                    ON Oceny.nr_albumu = Studenci.nr_albumu
                    INNER JOIN Kursy
                    ON Oceny.id_kursu = Kursy.id
                    WHERE Studenci.nr_albumu = '{current_user.id}' 
                    ORDER BY Oceny.id_kursu ASC;""")
    result = cur.fetchall()
    try:
        return render_template("student_oceny.html",
                               name=current_user.name+" "+current_user.secName+"["+current_user.id+"]",
                               courses=result)
    except TemplateNotFound:
        abort(404)


@student.route('/student/zapisy',methods=['GET', 'POST'])
@login_required(role="student")
def zapisy():
    con =  Database.connect()
    cur = con.cursor()
    if request.method == 'POST':

        courseId = request.form.get("courseId")
        cur.execute(f"""INSERT INTO Studenci_kursy
                            VALUES ('{current_user.id}', '{escape(courseId)}');""")
        con.commit()

    
    cur.execute(f"""SELECT Kursy.id, Kursy.nazwa FROM Kursy
                        INNER JOIN Kierunki_studiow ON Kursy.id_kierunku = Kierunki_studiow.id
                        LEFT JOIN Studenci_kursy on Studenci_kursy.id_kursu = Kursy.id AND Studenci_kursy.nr_albumu = '{current_user.id}'
                        WHERE Studenci_kursy.nr_albumu is null AND Kursy.id_kierunku = (SELECT id_kierunku FROM Studenci WHERE nr_albumu = '{current_user.id}')
                        ORDER BY Studenci_kursy.id_kursu ASC;""")
    result1 = cur.fetchall()

    cur.execute(f"""SELECT Kursy.id, Kursy.nazwa FROM Kursy
                        INNER JOIN Studenci_kursy ON Kursy.id = Studenci_kursy.id_kursu
                        WHERE Studenci_kursy.nr_albumu = '{current_user.id}'
                        ORDER BY Kursy.id ASC;""")
    result2 = cur.fetchall()


    print(result1)
    try:
        return render_template("student_zapisy.html",
                               name=current_user.name+" "+current_user.secName+"["+current_user.id+"]",
                               courses1=result1,courses2=result2)
    except TemplateNotFound:
        abort(404)