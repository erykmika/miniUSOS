from flask import *
from User import *
from jinja2 import TemplateNotFound

admin = Blueprint('admin', __name__,
                        template_folder='templates')

@admin.route('/admin')
@login_required(role="admin")
def index():
    try:
        return render_template("admin_main.html", name=current_user.name+" "+current_user.secName)
    except TemplateNotFound:
        abort(404)
