# RiveScript Playground
#
# This code is released under the GNU General Public License, version 2.
# See the LICENSE file for more information.

from flask import Blueprint, request, session, jsonify, render_template
import os
import random
import re
import string

from .default import DEFAULT_SOURCE
from .models import UUID_LENGTH, db_session, Snippet

controllers = Blueprint('controllers', __name__, url_prefix='/')

# 64 KB max source size sounds quite generous, but this might be useful to
# make it a configurable option in the future.
MAX_SOURCE_SIZE = 64000

@controllers.route("")
def index():
    return render_template("index.html", source=DEFAULT_SOURCE)

@controllers.route("share", methods=["POST"])
def share():
    """The POST handler for when the user wants to save/share their code."""

    data = request.json
    if data is None:
        return jsonify(error="Invalid payload."), 400

    source = data.get("source")
    if len(source) > MAX_SOURCE_SIZE:
        return jsonify(error="Your source file is too large."), 400

    # Has somebody already shared this exact code before?
    exist = db_session.query(Snippet).filter(Snippet.sha1sum == Snippet.make_checksum(source)).first()
    if exist is not None:
        session["sharing"] = True
        return jsonify(uuid=exist.id)

    # Generate a unique ID.
    uuid  = make_unique_id(UUID_LENGTH)
    retry = 0
    exist = db_session.query(Snippet).get(uuid)
    while exist is not None:
        retry += 1
        if retry > 20:
            return jsonify(error="Couldn't allocate a unique ID for you. Try your request again."), 500
        uuid = make_unique_id(UUID_LENGTH)
        exist = Snippet.get(uuid)

    # User's IP address, is it behind X-Forwarded-For?
    ip = request.remote_addr
    if os.environ.get("USE_X_FORWARDED_FOR"):
        ip = request.access_route[0]

    # Save their snippet.
    snippet = Snippet(
        id=uuid,
        source=source,
        ip=ip,
    )
    db_session.add(snippet)
    db_session.commit()

    session["sharing"] = True
    return jsonify(uuid=uuid)

@controllers.route("s/<uuid>")
def saved_code(uuid):
    """User is visiting a saved, shared link to RiveScript code."""

    # Validate the tag isn't suspicious.
    if re.match(r'[^A-Za-z0-9]+$', uuid):
        return error("Improperly formatted UUID.")

    # Look up the snippet.
    snippet = db_session.query(Snippet).get(uuid)
    if snippet is None:
        return error("The RiveScript snippet you're looking for was not found. "
            "It may have been deleted; otherwise double check the URL.")

    return render_template("index.html",
        source=snippet.source,
        sharing=session.pop("sharing", False),
        url=request.url,
    )

@controllers.route("about")
def about():
    return render_template("about.html")

def make_unique_id(length):
    """Make a random string of any length."""
    return "".join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(length))

def error(message):
    """Exit with a friendly (HTML) error message."""
    return render_template("error.html", error=message)
