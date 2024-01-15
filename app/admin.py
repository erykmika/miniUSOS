from flask import *
from User import *
from jinja2 import TemplateNotFound
from markupsafe import escape
from flask_wtf import *
from wtforms import *
from wtforms.validators import *
from datetime import datetime
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