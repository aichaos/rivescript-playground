from flask import current_app, Blueprint, render_template

controllers = Blueprint('controllers', __name__, url_prefix='/')

@controllers.route("")
def index():
    return render_template("index.html")

@controllers.route("about")
def about():
    return render_template("about.html")
