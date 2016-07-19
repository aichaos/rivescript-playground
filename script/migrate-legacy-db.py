#!/usr/bin/env python

"""Migrate the JSON files from /share into the new DB format."""

import os
import sys
import json
import dateutil.parser
pardir = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
sys.path.append(pardir)
os.chdir(pardir)

from playground.models import db_session, Snippet

for filename in os.listdir("./share"):
    if not filename.endswith(".json"):
        continue

    uuid = filename.replace(".json", "")

    with open("./share/"+filename, "r") as fh:
        data = json.loads(fh.read())
        print("Convert %s to SQLite" % uuid)

        # Make sure its checksum isn't already there.
        exist = db_session.query(Snippet).filter(Snippet.sha1sum == Snippet.make_checksum(data["source"])).first()
        if exist:
            print("   Skip: checksum already in DB.")
            continue

        snippet = Snippet(
            id=uuid,
            source=data["source"],
            ip=data["ip"],
        )
        snippet.created = dateutil.parser.parse(data["timeCreated"])
        db_session.add(snippet)
        db_session.commit()
