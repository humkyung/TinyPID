# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import os
from Project import Project
from AppDocData import AppDocData
from UI.Project_UI import Ui_ProjectDialog


class ProjectDialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        _translate = QtCore.QCoreApplication.translate

        self.ui = Ui_ProjectDialog()
        self.ui.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint &
                            ~QtCore.Qt.WindowContextHelpButtonHint)

        self.init_combobox()
        """
        self.ui.comboBox.currentIndexChanged.connect(self.changeProject)
        self.ui.radioButtonSQLite.clicked.connect(self.on_sqlite_selected)
        self.ui.radioButtonMSSQL.clicked.connect(self.on_mssql_selected)
        self.ui.lineEditPassword.setEchoMode(QLineEdit.Password)
        self.ui.pushButtonTestConnection.clicked.connect(self.on_test_connection_clicked)
        self.changeProject()  # force fill project's properties
        """
        self.ui.toolButtonAdd.clicked.connect(self.add_project_click)
        self.ui.toolButtonDelete.clicked.connect(self.delete_project_click)
        self.setWindowTitle(_translate('Project Dialog', 'Project'))

        # unit setting move into configuration
        self.ui.comboBoxProjectUnit.setHidden(True)
        self.ui.label_3.setHidden(True)

        self._selected = None

    @property
    def selected(self):
        return self._selected

    def init_combobox(self):
        from AppDocData import AppDocData

        self.ui.comboBox.clear()
        projects = AppDocData.instance().get_projects()
        # ComboBox setting
        for project in projects:
            self.ui.comboBox.addItem(project.name, project)

        if projects:
            self.ui.comboBox.setCurrentIndex(0)

        self.ui.comboBoxProjectUnit.clear()
        self.ui.comboBoxProjectUnit.addItem('Metric')
        self.ui.comboBoxProjectUnit.addItem('Imperial')
        self.ui.comboBoxProjectUnit.setCurrentIndex(0)

    def accept(self):
        """accept project"""
        from AppDatabase import AppDatabase, DBType

        index = self.ui.comboBox.currentIndex()
        self._selected = self.ui.comboBox.itemData(index)
        prj_desc = self.ui.lineEditProjectDesc.text()
        prj_unit = self.ui.comboBoxProjectUnit.currentText()
        if self._selected:
            self._selected.desc = prj_desc
            self._selected.prj_unit = prj_unit
            db_type = DBType.SQLITE if self.ui.radioButtonSQLite.isChecked() else DBType.MSSQL
            if db_type == DBType.MSSQL:
                self._selected.database = AppDatabase(db_type=DBType.MSSQL,
                                                      host=self.ui.lineEditServer.text(),
                                                      user=self.ui.lineEditUser.text(),
                                                      password=self.ui.lineEditPassword.text(),
                                                      db_path=self._selected.name)
            else:
                self._selected.database = AppDatabase(db_type=DBType.SQLITE,
                                                      host=None,
                                                      user=None,
                                                      password=None,
                                                      db_path=os.path.join(self._selected.get_database_file_path(),
                                                                           Project.DATABASE))

            AppDocData.instance().update_project_updated_date(self._selected)

        QDialog.accept(self)

    def reject(self):
        QDialog.reject(self)

    def add_project_click(self):
        _translate = QtCore.QCoreApplication.translate

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        options |= QFileDialog.ShowDirsOnly
        selected_dir = QFileDialog.getExistingDirectory(None, _translate('Project Dialog', "Select Project Path"),
                                                       os.getcwd(), options=options)
        if selected_dir:
            if selected_dir and not any(c.isspace() for c in selected_dir):
                prj_unit = self.ui.comboBoxProjectUnit.currentText()
                self.insert_project_info(dir=selected_dir, desc=self.ui.lineEditProjectDesc.text(), prj_unit=prj_unit)
            else:
                QMessageBox.warning(self, self.tr('Message'), self.tr('Folder name should not contains space'))

    def delete_project_click(self):
        """remove selected project"""
        selected = self.ui.comboBox.currentData()
        if selected:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(self.tr('Are you sure you want to delete project "{}" ?\nData can not be restored! '.format(
                selected.name)))
            msg.setWindowTitle(self.tr('Delete Project'))
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            if QMessageBox.Ok == msg.exec_():
                #AppDocData.instance().removeProjectInfo(self.selectedProject)
                self.init_combobox()

    '''
        @brief      display project desc,unit and database information when change project
        @author     humkyung
        @date       2019.04.09
    '''

    def change_project(self):
        index = self.ui.comboBox.currentIndex()
        project = self.ui.comboBox.itemData(index)
        if project:
            self.ui.lineEditProjectDesc.setText(project.desc)
            self.ui.comboBoxProjectUnit.setCurrentText(project.prj_unit)

            self.ui.radioButtonSQLite.setChecked(project.database.db_type == 'SQLite')
            self.ui.radioButtonMSSQL.setChecked(project.database.db_type == 'MSSQL')
            self.ui.lineEditServer.setEnabled(project.database.db_type == 'MSSQL')
            self.ui.lineEditUser.setEnabled(project.database.db_type == 'MSSQL')
            self.ui.lineEditPassword.setEnabled(project.database.db_type == 'MSSQL')
            self.ui.pushButtonTestConnection.setEnabled(project.database.db_type == 'MSSQL')
            if project.database.db_type == 'MSSQL':
                self.ui.lineEditServer.setText(project.database.host)
                self.ui.lineEditUser.setText(project.database.user)
                self.ui.lineEditPassword.setText(project.database.password)

    def on_sqlite_selected(self):
        """ call when user select sqlite """

        self.ui.lineEditServer.setEnabled(False)
        self.ui.lineEditUser.setEnabled(False)
        self.ui.lineEditPassword.setEnabled(False)
        self.ui.pushButtonTestConnection.setEnabled(False)

    def on_mssql_selected(self):
        """ called when user select mssql """

        self.ui.lineEditServer.setEnabled(True)
        self.ui.lineEditUser.setEnabled(True)
        self.ui.lineEditPassword.setEnabled(True)
        self.ui.pushButtonTestConnection.setEnabled(True)

    def on_test_connection_clicked(self):
        from AppDatabase import AppDatabase

        index = self.ui.comboBox.currentIndex()
        project = self.ui.comboBox.itemData(index)
        database = AppDatabase('MSSQL', self.ui.lineEditServer.text(), self.ui.lineEditUser.text(),
                               self.ui.lineEditPassword.text(), db_path=project.name)
        try:
            conn = database.connect()
            with conn:
                QMessageBox.information(self, self.tr('Information'), self.tr('Test connection is success'))
        except Exception as ex:
            mb = QMessageBox()
            mb.setIcon(QMessageBox.Critical)
            mb.setWindowTitle(self.tr('Error'))
            mb.setText(f"{ex}")
            mb.exec_()

    def insert_project_info(self, desc, prj_unit, dir):
        AppDocData.instance().insert_project_info(dir=dir, desc=desc, prj_unit=prj_unit)
        self.init_combobox()

# if __name__ == "__main__":
#    import sys
#    app = QtWidgets.QApplication(sys.argv)
#    Dialog = QtWidgets.QDialog()
#    Dialog.show()
#    sys.exit(app.exec_())
