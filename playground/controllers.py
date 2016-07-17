# RiveScript Playground
#
# This code is released under the GNU General Public License, version 2.
# See the LICENSE file for more information.

from flask import Blueprint, request, session, jsonify, render_template
import codecs
import datetime
import json
import os
import random
import re
import string

from .default import DEFAULT_SOURCE

controllers = Blueprint('controllers', __name__, url_prefix='/')

# 64 KB max source size sounds quite generous, but this might be useful to
# make it a configurable option in the future.
MAX_SOURCE_SIZE = 64000

# Length of unique IDs. This should definitely probably be made configurable
# at some point.
UUID_LENGTH = 10

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

    # Generate a unique ID.
    uuid  = make_unique_id(UUID_LENGTH)
    retry = 0
    while os.path.isfile("./share/{}.json".format(uuid)):
        retry += 1
        if retry > 20:
            return jsonify(error="Couldn't allocate a unique ID for you. Try your request again."), 500
        uuid = make_unique_id(UUID_LENGTH)

    # User's IP address, is it behind X-Forwarded-For?
    ip = request.remote_addr
    if os.environ.get("USE_X_FORWARDED_FOR"):
        ip = request.access_route[0]

    # Payload to save to disk.
    payload = {
        "source": source,
        "timeCreated": datetime.datetime.utcnow().isoformat(),
        "ip": ip,
    }

    # Save their code snippet.
    with codecs.open("./share/{}.json".format(uuid), "w", "utf-8") as fh:
        fh.write(json.dumps(payload, sort_keys=True, indent=4))

    session["sharing"] = True
    return jsonify(uuid=uuid)

@controllers.route("s/<uuid>")
def saved_code(uuid):
    """User is visiting a saved, shared link to RiveScript code."""

    # Validate the tag isn't suspicious.
    if re.match(r'[^A-Za-z0-9]+$', uuid):
        return error("Improperly formatted UUID.")

    # Exists?
    db = "./share/{}.json".format(uuid)
    if not os.path.isfile(db):
        return error("The RiveScript snippet you're looking for was not found. "
            "It may have been deleted; otherwise double check the URL.")

    # Read it!
    data = dict()
    with codecs.open(db, "r", "utf-8") as fh:
        try:
            data = json.loads(fh.read())
        except Exception as e:
            return error("Failed to parse JSON from stored file: {}".format(e))

    return render_template("index.html",
        source=data["source"],
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
