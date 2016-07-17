#!/usr/bin/env python3

"""WSGI runner script for the RiveScript Playground."""

import sys
import os

# Add the CWD to the path.
sys.path.append(".")

# Use the 'playground' virtualenv.
activate_this = os.environ['HOME'] + '/.virtualenv/playground/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

def application(environ, start_response):
    from playground.app import create_app
    app = create_app()
    return app(environ, start_response)
