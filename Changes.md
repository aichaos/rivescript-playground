# Change Log

* v1.1.0 -- July 19, 2016
  - Switch to SQLAlchemy and an SQLite3 database for storing shared snippets
    instead of storing JSON files to disk in the `./share` folder.
  - Add a script to migrate legacy JSON snippet files to the SQLite database
    (`./scripts/migrate-legacy-db.py`)
  - Keep track of the last accessed time for each snippet and update it any time
    the snippet is visited (may be useful if you ever need to cull old snippets)
  - To avoid duplicate snippets for identical RiveScript code, start keeping a
    SHA1 checksum of each snippet. If the *exact same code* gets shared multiple
    times (for example, this happened to the default code several times) it will
    find and re-use the same URL as the existing one.
  - Don't use Flask's SecureSessionCookie system for storing the temporary
    "I just shared this" cookie, as it was unreliable due to the session secret
    key being cycled on every app reload. Instead, use a plain cookie.

* v1.0.0 -- July 16, 2016
  - Initial release.
