# RiveScript Playground
#
# This code is released under the GNU General Public License, version 2.
# See the LICENSE file for more information.

from flask import Flask, render_template
import os
from .models import db_session, init_db

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
    init_db()

    # Make a random secret key every time. We don't keep any long term sessions,
    # just when we want to pop up a confirmation after the user was redirected
    # post-share.
    app.secret_key = os.urandom(24)

    # Make the storage directory.
    if not os.path.isdir("./share"):
        os.mkdir("./share")

    from .controllers import controllers
    app.register_blueprint(controllers)

    @app.teardown_request
    def shutdown_session(exception=None):
        db_session.remove()

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("error.html", error="The page you're looking for was not found."), 404

    return app
