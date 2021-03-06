# coding: utf-8
""" This is application module """
import sys
import os

if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtXml import *
from PyQt5.QtSvg import *
from PyQt5 import QtWidgets
# from PluginScope import PluginScope

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Commands'))
from AppDocData import AppDocData


class App(QApplication):
    """ This is App class inherits from QApplication """

    COMPANY = 'ATOOLS'
    NAME = 'TinyPID'
    THREAD_MAX_WORKER = os.cpu_count()

    def __init__(self, args):
        import locale

        super(App, self).__init__(args)
        self._main_wnd = None

        app_doc_data = AppDocData.instance()
        app_style = app_doc_data.load_app_style()
        self.setStyle(app_style)

        configs = app_doc_data.get_app_configs('app', 'stylesheet')
        if configs and len(configs) == 1:
            self.load_style_sheet(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'stylesheets',
                                             configs[0].value))
            self.stylesheet_name = configs[0].value
        else:
            self.load_style_sheet(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'stylesheets', 'coffee'))
            self.stylesheet_name = 'coffee'

        # load language file
        self._translator = None
        configs = app_doc_data.get_app_configs('app', 'language')
        if configs and len(configs) == 1:
            qm_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'translate', f"{configs[0].value}.qm")
        else:
            locale = locale.getdefaultlocale()
            qm_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'translate', f"{locale[0]}.qm")

        self.load_language(qm_file)
        # up to here

        QtWidgets.qApp = self

    def load_style_sheet(self, sheetName):
        """load application style sheet"""
        try:
            file = QFile('%s.qss' % sheetName.lower())
            file.open(QFile.ReadOnly)

            styleSheet = file.readAll()
            styleSheet = str(styleSheet, encoding='utf8')

            self.setStyleSheet(styleSheet)
        finally:
            file.close()

    def load_language(self, language_file):
        """load translator with given language file"""
        try:
            if self._translator is not None:
                self.removeTranslator(self._translator)

            self.language_name = 'en_us'
            if os.path.isfile(language_file):
                self._translator = QTranslator()  # I18N ??????
                self._translator.load(language_file)
                self.installTranslator(self._translator)
                self.language_name = os.path.splitext(os.path.basename(language_file))[0]
        finally:
            pass

    @staticmethod
    def main_wnd():
        """return main window"""
        app = QApplication.instance()
        if not app._main_wnd:
            for widget in app.topLevelWidgets():
                if isinstance(widget, QMainWindow):
                    app._main_wnd = widget
                    return app._main_wnd
        else:
            return app._main_wnd

        return None


if __name__ == '__main__':
    from ProjectDialog import ProjectDialog
    from MainWindow import MainWindow
    from ExceptionHandler import QExceptionHandler

    app = App(sys.argv)
    
    """ log for unhandled exception """
    app.exception_handler = QExceptionHandler()
    app._excepthook = sys.excepthook
    sys.excepthook = app.exception_handler.handler

    dlg = ProjectDialog()
    if QDialog.Accepted == dlg.exec_():
        if dlg.selected is not None:
            AppDocData.instance().current_project = dlg.selected
            main_wnd = MainWindow.instance()
            main_wnd.show()
            sys.exit(app.exec_())
