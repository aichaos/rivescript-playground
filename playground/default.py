# RiveScript Playground
#
# This code is released under the GNU General Public License, version 2.
# See the LICENSE file for more information.

"""The default RiveScript source code shown to new users of the app."""

DEFAULT_SOURCE = """! version = 2.0

+ hello bot
- Hello human.

+ my name is *
- <set name=<formal>>Nice to meet you, <get name>.

+ (what is my name|who am i)
- You're <get name>, right?

+ *
- I don't have a reply for that.
- Try asking that a different way."""
