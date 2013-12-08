from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from collections import OrderedDict

db_engine = None
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False))


def init_engine(db_uri):
    global db_engine
    db_engine = create_engine(db_uri, encoding='utf-8')
    db_session.configure(bind=db_engine)


def init_db():
    Base.metadata.create_all(bind=db_engine)


def clear_db():
    Base.metadata.drop_all(bind=db_engine)


class Base(object):
    id = Column(Integer, primary_key=True)


class HasUniqueName(object):
    name = Column(Text, nullable=False, unique=True)

    def __repr__(self):
        return '<%s(%r, %r)>' % (self.__class__.__name__, self.id, self.name)


Base = declarative_base(cls=Base)
Base.query = db_session.query_property()


class Serializer(object):

    def to_dict(self):
        result = OrderedDict()
        for key in self.__mapper__.c.keys():
            value = getattr(self, key, None)
            value = '' if not value else value
            result[key] = str(value)
        return result


class Person(Base, Serializer):
    __tablename__ = 'persons'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8', 'mysql_collate': 'utf8_general_ci'}
    id = Column(Integer, primary_key=True)
    google_id = Column(String(32))
    name = Column(String(32))
    phone = Column(String(32))
    picture = Column(String(255))
    link = Column(String(255))
    locale = Column(String(4))
    hd = Column(String(255))
    email = Column(String(255))
    active = Column(Boolean, nullable=False, default=True)

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.google_id

    @staticmethod
    def load(google_id):
        try:
            user = db_session.query(Person).filter_by(google_id=google_id).one()
            return user
        except:
            return None


class EmergencyService(Base, Serializer):
    __tablename__ = 'emergency_services'
    id = Column(Integer, primary_key=True)
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8', 'mysql_collate': 'utf8_general_ci'}
    week_nr = Column(Integer)
    start_date = Column(Date)
    end_date = Column(Date)

    person_id = Column(Integer, ForeignKey('persons.id'))
    person_rel = relationship("Person", foreign_keys="[Person.id]", primaryjoin="Person.id==EmergencyService.person_id")
