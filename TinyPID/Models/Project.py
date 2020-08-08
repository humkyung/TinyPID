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
    create_date = Column(DateTime, default=datetime.datetime.now())
    update_date = Column(DateTime, default=datetime.datetime.now())

    def __init__(self, id, name, desc, prj_unit, path, create_date=datetime.datetime.now(),
                 update_date=datetime.datetime.now()):
        self.id = id
        self.name = name
        self.desc = desc
        self.prj_unit = prj_unit
        self.path = path
        self.create_date = create_date
        self.update_date = update_date

    def __repr__(self):
        return f"<Project({self.name}, {self.desc}, {self.prj_unit})>"

    def get_database_file_path(self):
        """return database file path"""
        import os

        return os.path.join(self.path, 'db')

