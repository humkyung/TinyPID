# coding: utf-8
""" This is AppDatabase module """

from enum import Enum
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import sqlalchemy.sql.default_comparator

import sqlite3
# import pymssql


class DBType(Enum):
    SQLITE = 1,
    MSSQL = 2


class AppDatabase(object):
    """ This is AppDatabase class """

    DB_ENGINE = {
        DBType.SQLITE: 'sqlite:///{DB}'
    }

    def __init__(self, db_type, host, user, password, db_path):
        if db_type == DBType.SQLITE:
            self.engine_url = self.DB_ENGINE[db_type].format(DB=db_path)
        elif db_type == DBType.MSSQL:
            pass
        else:
            print(f"DBType({db_type}) is not found in DB_ENGINE")

        self._DBType = type
        self._host = host
        self._user = user
        self._password = password
        self._db_path = db_path

    def __enter__(self):
        """with구문 진입시에 db와 connection을 하고 ORM을 사용하기 위한 session을 만들어준다."""
        self.engine = create_engine(self.engine_url)
        self.session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=self.engine))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """with구문을 빠져나오기 전 session 종료한다."""
        self.session.close()

    @property
    def db_type(self):
        """ return database type """
        return self._DBType

    @db_type.setter
    def db_type(self, value):
        self._DBType = value

    @property
    def host(self):
        """ return host for mssql """
        return self._host

    @host.setter
    def host(self, value):
        self._host = value

    @property
    def user(self):
        """ return user for mssql """
        return self._user

    @user.setter
    def user(self, value):
        self._user = value

    @property
    def password(self):
        """ return password for mssql """
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

    @property
    def db_name(self):
        """ return database name """
        return self._db_path

    @property
    def file_path(self):
        """ return sqlite database file path """
        return self._db_path

    @file_path.setter
    def file_path(self, value):
        self._db_path = value 

    @property
    def place_holder(self):
        """ return database placeholder """
        return '?' if self.db_type == 'SQLite' else '%s' if self.db_type == 'MSSQL' else None

    def connect(self):
        """ return database connection depends on database type """
        conn = None
        if self._DBType == 'SQLite':
            conn = sqlite3.connect(self.file_path, isolation_level=None)
            conn.row_factory = sqlite3.Row
        elif self._DBType == 'MSSQL':
            conn = pymssql.connect(host=self._host, user=self._user, password=self._password, database=self.db_name,
                                   charset='utf8', autocommit=False, as_dict=True)

        return conn

    def to_sql(self, sql):
        """ convert given sql string for database """

        return sql.replace('?', '%s') if self.db_type == "MSSQL" else sql