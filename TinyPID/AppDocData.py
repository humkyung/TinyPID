# coding: utf-8
""" This is document data(SDI) class """

import sys
import os
import sqlite3
import datetime
from enum import Enum

try:
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    from PyQt5 import QtWidgets
except ImportError:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *

from SingletonInstance import SingletonInstane
from AppDatabase import AppDatabase, DBType
from Models.Project import Project


class Config:
    def __init__(self, section, key, value):
        self.section = section
        self.key = key
        self.value = value


class MessageType(Enum):
    """MessageType class"""
    Normal = 1
    Error = 2
    Information = 3


class AppDocData(SingletonInstane):
    def __init__(self):
        self._current_project = None

    def get_app_db_path(self) -> str:
        """Get application DB file path in ProgramData"""
        from App import App

        path = os.path.join(os.getenv('ALLUSERSPROFILE'), App.NAME)
        app_database = os.path.join(path, 'App.db')
        return app_database

    def build_app_database(self) -> None:
        """build application database"""
        from App import App
        from AppDatabase import AppDatabase, DBType
        from Models.Project import Project
        from Models.Configuration import Configuration

        path = os.path.join(os.getenv('ALLUSERSPROFILE'), App.NAME)
        app_database_filepath = os.path.join(path, 'App.db')

        if os.path.exists(path):
            with AppDatabase(db_type=DBType.SQLITE, host=None, user=None, password=None, db_path=app_database_filepath) as database:
                Project.__table__.create(bind=database.engine, checkfirst=True)
                Configuration.__table__.create(bind=database.engine, checkfirst=True)

    def get_projects(self):
        from App import App
        from AppDatabase import AppDatabase, DBType
        from Models.Project import Project

        path = os.path.join(os.getenv('ALLUSERSPROFILE'), App.NAME)
        app_database_filepath = os.path.join(path, 'App.db')

        with AppDatabase(db_type=DBType.SQLITE, host=None, user=None, password=None, db_path=app_database_filepath) as database:
            return database.session.query(Project).all()

    def insert_project_info(self, dir, desc, prj_unit):
        import uuid
        from App import App
        from AppDatabase import AppDatabase, DBType
        from Models.Project import Project

        path = os.path.join(os.getenv('ALLUSERSPROFILE'), App.NAME)
        app_database_filepath = os.path.join(path, 'App.db')

        with AppDatabase(db_type=DBType.SQLITE, host=None, user=None, password=None, db_path=app_database_filepath) as database:
            database.session.add(Project(id=str(uuid.uuid4()), name=os.path.basename(dir), desc=desc, prj_unit=prj_unit,
                                         path=dir))
            database.session.commit()

    def update_project_updated_date(self, project):
        from App import App
        from AppDatabase import AppDatabase, DBType
        from Models.Project import Project

        path = os.path.join(os.getenv('ALLUSERSPROFILE'), App.NAME)
        app_database_filepath = os.path.join(path, 'App.db')

        with AppDatabase(db_type=DBType.SQLITE, host=None, user=None, password=None,
                         db_path=app_database_filepath) as database:
            database.session.query(Project).filter(Project.id == project.id).update({'update_date': datetime.datetime.now()})
            database.session.commit()

    def load_app_style(self):
        """load app style"""
        style = 'Fusion'
        self.build_app_database()

        return style

    def get_app_configs(self, section, key=None):
        """get application configurations"""

        res = []

        db_path = self.get_app_db_path()
        path = os.path.dirname(db_path)
        if os.path.exists(path):
            with sqlite3.connect(db_path) as conn:
                try:
                    conn.execute('PRAGMA foreign_keys = ON')
                    # Get a cursor object
                    cursor = conn.cursor()

                    if key is not None:
                        sql = "select * from configuration where section=? and key=?"
                        param = (section, key)
                    else:
                        sql = "select * from configuration where section=?"
                        param = (section,)

                    cursor.execute(sql, param)
                    rows = cursor.fetchall()
                    for row in rows:
                        res.append(Config(row[0], row[1], row[2]))
                # Catch the exception
                except Exception as ex:
                    from App import App
                    # Roll back any change if something goes wrong
                    conn.rollback()

                    message = f"error occurred({repr(ex)}) in {sys.exc_info()[-1].tb_frame.f_code.co_filename}:" \
                              f"{sys.exc_info()[-1].tb_lineno}"
                    App.main_wnd().addMessage.emit(MessageType.Error, message)

        return res

    def get_configs(self, section, key=None):
        """get configurations"""

        res = []

        with sqlite3.connect(self.activeDrawing.path) as conn:
            try:
                conn.execute('PRAGMA foreign_keys = ON')
                # Get a cursor object
                cursor = conn.cursor()

                if key is not None:
                    sql = "select Section, Key, Value from configuration where section=? and key=?"
                    param = (section, key)
                else:
                    sql = "select Section, Key, Value from configuration where section=?"
                    param = (section,)

                cursor.execute(sql, param)
                rows = cursor.fetchall()
                for row in rows:
                    res.append(Config(row[0], row[1], row[2]))
            # Catch the exception
            except Exception as ex:
                from App import App

                # Roll back any change if something goes wrong
                conn.rollback()

                message = f"error occurred({repr(ex)}) in {sys.exc_info()[-1].tb_frame.f_code.co_filename}:" \
                          f"{sys.exc_info()[-1].tb_lineno}"
                App.main_wnd().addMessage.emit(MessageType.Error, message)

        return res

    def save_app_configs(self, configs):
        """save application configurations"""
        app_database_filepath = self.get_app_db_path()
        with AppDatabase(db_type=DBType.SQLITE, host=None, user=None, password=None,
                         db_path=app_database_filepath) as database:
            try:
                for config in configs:
                    database.session.merge(config)
                database.session.commit()
            except Exception as ex:
                from App import App
                # Roll back any change if something goes wrong
                database.session.rollback()

                message = f"error occurred({repr(ex)}) in {sys.exc_info()[-1].tb_frame.f_code.co_filename}:" \
                          f"{sys.exc_info()[-1].tb_lineno}"
                App.main_wnd().addMessage.emit(MessageType.Error, message)

    def save_configs(self, configs):
        """save configurations"""

        # Creates or opens a file called mydb with a SQLite3 DB
        with sqlite3.connect(self.activeDrawing.path) as conn:
            try:
                conn.execute('PRAGMA foreign_keys = ON')
                # Get a cursor object
                cursor = conn.cursor()

                for config in configs:
                    value = config.value
                    if type(value) is str and "'" in value:
                        value = value.replace("'", "''")

                    sql = "insert or replace into configuration(Section,Key,Value) values(?,?,?)"
                    param = (config.section, config.key, value)

                    cursor.execute(sql, param)
                conn.commit()
            # Catch the exception
            except Exception as ex:
                from App import App
                # Roll back any change if something goes wrong
                conn.rollback()

                message = 'error occurred({}) in {}:{}'.format(ex, sys.exc_info()[-1].tb_frame.f_code.co_filename,
                                                               sys.exc_info()[-1].tb_lineno)
                App.main_wnd().addMessage.emit(MessageType.Error, message)

    def delete_app_configs(self, section, key=None):
        """delete application configurations"""

        # Creates or opens a file called mydb with a SQLite3 DB
        dbPath = self.get_app_db_path()
        with sqlite3.connect(dbPath) as conn:
            try:
                conn.execute('PRAGMA foreign_keys = ON')
                # Get a cursor object
                cursor = conn.cursor()

                if key is not None:
                    sql = "delete from configuration where section='{}' and key='{}'".format(section, key)
                else:
                    sql = "delete from configuration where section='{}'".format(section)
                cursor.execute(sql)

                conn.commit()
            # Catch the exception
            except Exception as ex:
                from App import App

                # Roll back any change if something goes wrong
                conn.rollback()

                message = 'error occurred({}) in {}:{}'.format(ex, sys.exc_info()[-1].tb_frame.f_code.co_filename,
                                                               sys.exc_info()[-1].tb_lineno)
                App.main_wnd().addMessage.emit(MessageType.Error, message)

    @property
    def current_project(self):
        return self._current_project

    @current_project.setter
    def current_project(self, value):
        self._current_project = value

