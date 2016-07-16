# RiveScript Playground
#
# This code is released under the GNU General Public License, version 2.
# See the LICENSE file for more information.

from playground.app import create_app
import argparse

def main(opts):
    flask_options = dict(
        host='0.0.0.0',
        debug=not opts.prod,
        port=opts.port,
        threaded=True,
    )

    app = create_app()
    app.run(**flask_options)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RiveScript Playground.")
    parser.add_argument("--port", "-p",
        help="The port number to listen on.",
        type=int,
        default=2006,
    )
    parser.add_argument("--prod",
        help="Run the app in production mode (debugging disabled).",
        action="store_true",
    )
    opts = parser.parse_args()
    main(opts)
