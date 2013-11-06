from hashlib import sha1
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from flask.ext.login import UserMixin
from .hash_passwords import check_hash, make_hash
from .auth import login_serializer

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


class User(UserMixin, Base):
    __tablename__ = 'users'
    username = Column(String(255), nullable=False, unique=False)
    email = Column(String(255), nullable=False, unique=True)
    _password = Column('password', String(255), nullable=False)
    active = Column(Boolean, nullable=False, default=True)

    def get_auth_token(self):
        data = (self.id, sha1(self.password).hexdigest())
        return login_serializer.dumps(data)

    def _set_password(self, password):
        self._password = make_hash(password)

    def _get_password(self):
        return self._password

    password = synonym('_password', descriptor=property(_get_password,
                                                        _set_password))

    def valid_password(self, password):
        """Check if provided password is valid."""
        return check_hash(password, self.password)

    def is_active(self):
        return self.active

    def __repr__(self):
        return '<%s(%r, %r)>' % (self.__class__.__name__, self.id,
                                 self.username)


class Person(Base):
    __tablename__ = 'persons'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8', 'mysql_collate': 'utf8_general_ci'}
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    phone = Column(String(32))
    image_url = Column(String(255))


class EmergencyService(Base):
    __tablename__ = 'emergency_services'
    id = Column(Integer, primary_key=True)
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8', 'mysql_collate': 'utf8_general_ci'}
    week_nr = Column(Integer)
    start_date = Column(Date)
    end_date = Column(Date)

    person_id = Column(Integer, ForeignKey('persons.id'))
    person_rel = relationship("Person", foreign_keys="[Person.id]", primaryjoin="Person.id==EmergencyService.person_id")


class Incident(Base):
    __tablename__ = 'incidents'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8', 'mysql_collate': 'utf8_general_ci'}
    id = Column(Integer, primary_key=True)
    text = Column(Text)

    users_id = Column(Integer, ForeignKey('users.id'))
    users_rel = relationship("User", foreign_keys="[User.id]", primaryjoin="User.id==Incident.users_id")

    emergency_service_id = Column(Integer, ForeignKey('emergency_services.id'))
    emergency_service_rel = relationship("EmergencyService", foreign_keys="[EmergencyService.id]", primaryjoin="EmergencyService.id==Incident.emergency_service_id")
