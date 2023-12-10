from flask import *
from User import *
from jinja2 import TemplateNotFound

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
    cur.execute(f"""SELECT Studenci.nr_albumu, Kursy.nazwa, Oceny.ocena
                    FROM Studenci
                    INNER JOIN Oceny ON Studenci.nr_albumu = Oceny.nr_albumu
                    INNER JOIN Kursy ON Kursy.id = Oceny.id_kursu
                    GROUP BY Studenci.nr_albumu, Kursy.nazwa, Oceny.ocena
                    ORDER BY Studenci.nr_albumu ASC;""")
    result = cur.fetchall()
    #for row in result:
    #    print(row)
    try:
        return render_template("prowadzacy_oceny.html",
                               name=current_user.name+" "+current_user.secName+"["+current_user.id+"]",
                               grades=result)
    except TemplateNotFound:
        abort(404)