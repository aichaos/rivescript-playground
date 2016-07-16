# RiveScript Playground
#
# This code is released under the GNU General Public License, version 2.
# See the LICENSE file for more information.

from flask import (Flask, g)
import os

def create_app():
    app = Flask(__name__)

    # Make a new session secret key every time. This app keeps no long term
    # session information around.
    app.secret_key = os.urandom(24)

    from .controllers import controllers
    app.register_blueprint(controllers)

    return app
