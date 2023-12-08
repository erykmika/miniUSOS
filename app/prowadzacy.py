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
