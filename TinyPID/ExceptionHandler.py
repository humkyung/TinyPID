# coding: utf-8
""" This is exception handler module """

import sys
import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtXml import *
from PyQt5.QtSvg import *
from PyQt5 import QtWidgets
import logging
from App import App


class QExceptionHandler(QObject):
    """ This is exception handler class """

    errorSignal = pyqtSignal()

    def __init__(self):
        super(QExceptionHandler, self).__init__()

        path = os.path.join(os.getenv('ALLUSERSPROFILE'), App.NAME)
        if os.path.exists(path):
            self.log_path = os.path.join(path, App.NAME + '.log')
            self.logger = logging.getLogger(__name__)
            logging.basicConfig(filename=self.log_path , filemode='w', level=logging.CRITICAL)

    def handler(self, exctype, value, traceback):
        """ log exception, file namd and line number """

        message = 'error occurred({}) in {}:{}'.format(value, traceback.tb_frame.f_code.co_filename, traceback.tb_lineno)
        self.errorSignal.emit()
        self.logger.critical('Unhandled exception: {}'.format(message))