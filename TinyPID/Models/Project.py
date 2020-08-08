# coding: utf-8
""" This is projects module """

import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, SMALLINT, BIGINT, String, DateTime

# 매핑 선언
Base = declarative_base()


class Project(Base):
    __tablename__ = 'Projects'

    id = Column(String(37), primary_key=True)
    name = Column(String)
    desc = Column(String)
    prj_unit = Column(String)
    path = Column(String)
    create_date = Column(DateTime, default=datetime.datetime.utcnow)
    update_date = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, id, name, desc, prj_unit, path, create_date, update_date):
        self.id = id
        self.name = name
        self.desc = desc
        self.prj_unit = prj_unit
        self.path = path
        self.create_date = create_date
        self.update_date = update_date

    def __repr__(self):
        return f"<Project({self.name}, {self.desc}, {self.prj_unit})>"

