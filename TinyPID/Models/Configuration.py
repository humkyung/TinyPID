# coding: utf-8
""" This is projects module """

import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, SMALLINT, BIGINT, String, DateTime, PrimaryKeyConstraint

# 매핑 선언
Base = declarative_base()


class Configuration(Base):
    __tablename__ = 'Configuration'
    __table_args__ = (
        PrimaryKeyConstraint('section', 'key', name='Configuration_PK'),
    )

    section = Column(String(37), primary_key=True)
    key = Column(String)
    value = Column(String)

    def __init__(self, section, key, value):
        self.section = section
        self.key = key
        self.value = value

    def __repr__(self):
        return f"<Configuration({self.section}, {self.key}, {self.value})>"

