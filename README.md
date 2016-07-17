# RiveScript Playground

![02-rivescript.py](https://raw.github.com/aichaos/rivescript-playground/master/screenshot.png)

The RiveScript Playground is a web app where bot makers can develop, test, and
share code snippets for RiveScript bots. It uses the JavaScript edition of
RiveScript, so the bot runs on the user's own web browser, and provides a way
to share code snippets with others (for example, to demonstrate how to do
something or reproduce a bug).

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
