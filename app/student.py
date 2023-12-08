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
