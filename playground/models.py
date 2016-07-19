# RiveScript Playground
#
# This code is released under the GNU General Public License, version 2.
# See the LICENSE file for more information.

# Length of unique IDs. This should definitely probably be made configurable
# at some point.
UUID_LENGTH = 10

import hashlib
import os
from sqlalchemy import create_engine, Column, String, Text, DateTime
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime

engine = create_engine('sqlite:///database.sqlite', convert_unicode=True)
db_session = scoped_session(sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    if not os.path.isfile("./database.sqlite"):
        Base.metadata.create_all(bind=engine)

class Snippet(Base):
    __tablename__ = 'snippet'

    id       = Column(String(UUID_LENGTH), primary_key=True)
    source   = Column(Text, nullable=False)
    sha1sum  = Column(String(40), nullable=False)
    ip       = Column(String(50), nullable=False)
    created  = Column(DateTime, default=datetime.datetime.utcnow)
    accessed = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, id, ip, source):
        self.id = id
        self.ip = ip
        self.source = source
        self.sha1sum = Snippet.make_checksum(source)

    def __repr__(self):
        return '<Snippet %r>' % self.id

    @classmethod
    def make_checksum(cls, source):
        s = hashlib.sha1()
        s.update(source.encode())
        return s.hexdigest()
