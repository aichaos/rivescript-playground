# RiveScript Playground

![02-rivescript.py](https://raw.github.com/aichaos/rivescript-playground/master/screenshot.png)

The RiveScript Playground is a web app where bot makers can develop, test, and
share code snippets for RiveScript bots. It uses the JavaScript edition of
RiveScript, so the bot runs on the user's own web browser, and provides a way
to share code snippets with others (for example, to demonstrate how to do
something or reproduce a bug).

You can use the live RiveScript Playground site at <https://play.rivescript.com/>

This is a simple Python Flask web app that requires no database or
configuration at all: not even session secret keys need to be set up.

# Installation

The only dependency for this app is Flask itself (and Flask's dependencies).

Create a virtual environment for **Python 3** and run:

    pip install -r requirements.txt

To launch the server for local debugging and testing:

    python run.py

There is an example `app.wsgi` and `wsgi_gunicorn.py` for running the app in
production using mod_wsgi or gunicorn, respectively. Refer to the Flask
documentation for deployment options.

## Configuration

If you're serving this behind a proxy (so that the "remote address" isn't the
visitor's real IP address), run the app with the environment variable
`USE_X_FORWARDED_FOR` set to a truthy value. Don't do this if you're not running
the app from behind a proxy, though, or users can spoof their own IP addresses!

# Shared Snippets

This app requires no configuration, but the "Share" feature of the app needs to
write JSON files to the hard disk. It writes them into a folder named "share"
relative to the app's current working directory. It will need permission to
create this folder when it doesn't exist and to read and write files in it.

Here is an example Supervisor configuration for running this app:

```ini
[program:rivescript_playground]
command = /home/www/.pyvenv/playground/bin/gunicorn -b 127.0.0.1:9004 -u www -g www wsgi_gunicorn:app
directory = /home/www/git/rivescript-playground
user = www
```

In that configuration it runs as an unprivileged user, `www` and its working
directory is set to the git clone where it has permissions to create and
manage its `share` folder.

# Copyright

```
The RiveScript Playground
Copyright (C) 2016 Noah Petherbridge

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
```
