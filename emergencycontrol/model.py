from sqlalchemy import *
from sqlalchemy.orm import *
from collections import OrderedDict
from emergencycontrol import db


class Serializer(object):

    def to_dict(self):
        result = OrderedDict()
        for key in self.__mapper__.c.keys():
            value = getattr(self, key, None)
            value = '' if not value else value
            result[key] = str(value)
        return result


class Person(db.Model, Serializer):
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
    is_hero = Column(Boolean, nullable=False, default=False)

    emergencyService_rel = relationship("EmergencyService")

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
            user = Person.query.filter_by(google_id=google_id).one()
            return user
        except:
            return None


class EmergencyService(db.Model, Serializer):
    __tablename__ = 'emergency_services'
    id = Column(Integer, primary_key=True)
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8', 'mysql_collate': 'utf8_general_ci'}
    week_nr = Column(Integer)
    start_date = Column(Date)
    end_date = Column(Date)

    person_id = Column(Integer, ForeignKey('persons.id'))


class CalendarLog(db.Model, Serializer):
    __tablename__ = 'calendar_log'
    id = Column(Integer, primary_key=True)
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8', 'mysql_collate': 'utf8_general_ci'}
    text = Column(Text)
    date = Column(DateTime)
