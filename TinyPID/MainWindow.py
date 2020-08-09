# coding: utf-8
""" This is MainWindow module """

import sys
import os
import subprocess
from functools import partial
import asyncio

"""
import cv2
import numpy as np
"""
import uuid

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSvg import *

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Commands'))
"""
from CreateCommand import CreateCommand
import CropCommand
import AreaOcrCommand
import CreateSymbolCommand
import AreaZoomCommand
import FenceCommand
import PlaceLineCommand
import PlacePolygonCommand
"""

from UI.MainWindow_UI import Ui_MainWindow
# from QtImageViewer import QtImageViewer
from SingletonInstance import SingletonInstane

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '\\Shapes')
"""
from EngineeringAbstractItem import QEngineeringAbstractItem
from EngineeringPolylineItem import QEngineeringPolylineItem
from EngineeringLineItem import QEngineeringLineItem
from SymbolSvgItem import SymbolSvgItem
from GraphicsBoundingBoxItem import QGraphicsBoundingBoxItem
from EngineeringTextItem import QEngineeringTextItem
from EngineeringLineNoTextItem import QEngineeringLineNoTextItem
from EngineeringNoteItem import QEngineeringNoteItem
from QEngineeringSizeTextItem import QEngineeringSizeTextItem
from EngineeringUnknownItem import QEngineeringUnknownItem
from EngineeringEquipmentItem import QEngineeringEquipmentItem
from EngineeringInstrumentItem import QEngineeringInstrumentItem
from EngineeringSpecBreakItem import QEngineeringSpecBreakItem
from EngineeringErrorItem import QEngineeringErrorItem
from EngineeringVendorItem import QEngineeringVendorItem
from EngineeringEndBreakItem import QEngineeringEndBreakItem
from EngineeringReducerItem import QEngineeringReducerItem
from EngineeringFlowMarkItem import QEngineeringFlowMarkItem
from QEngineeringTrimLineNoTextItem import QEngineeringTrimLineNoTextItem
"""
from AppDocData import *
"""
import SymbolTreeWidget, SymbolPropertyTableWidget
import SymbolEditorDialog
import ItemTreeWidget
import ItemPropertyTableWidget
from UserInputAttribute import UserInputAttribute
from TextItemFactory import TextItemFactory
from TrainingImageListDialog import QTrainingImageListDialog
from TrainingSymbolImageListDialog import QTrainingSymbolImageListDialog
from TextDataListDialog import QTextDataListDialog
from ImportTextFromCADDialog import QImportTextFromCADDialog
from SymbolThicknessDialog import QSymbolThicknessDialog
from DisplayColors import DisplayColors
from DisplayColors import DisplayOptions
"""


class QDisplayWidget(QWidget):
    def __init__(self):
        from PyQt5 import QtWidgets, uic

        QWidget.__init__(self)
        uic.loadUi(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'UI', 'DisplayWidget.ui'), self)


class MainWindow(QMainWindow, Ui_MainWindow, SingletonInstane):
    """ This is MainWindow class """
    addMessage = pyqtSignal(Enum, str)

    def __init__(self):
        """MainWindow constructor"""
        from App import App
        #from QtImageViewerScene import QtImageViewerScene

        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.progress_bar = QProgressBar()
        self._label_mouse = QLabel(self.statusbar)
        self._label_mouse.setText(self.tr('mouse pos : ({},{})'.format(0, 0)))
        self.labelStatus = QLabel(self.statusbar)
        self.labelStatus.setText(self.tr('Unrecognition : '))
        self.labelSymbolStatus = QLabel(self.statusbar)
        self.labelSymbolStatus.setText(self.tr('Symbol : '))
        self.labelLineStatus = QLabel(self.statusbar)
        self.labelLineStatus.setText(self.tr('Line : '))
        self.labelTextStatus = QLabel(self.statusbar)
        self.labelTextStatus.setText(self.tr('Text : '))

        self.statusbar.addWidget(self._label_mouse)
        self.statusbar.addPermanentWidget(self.progress_bar, 1)
        self.statusbar.addPermanentWidget(self.labelSymbolStatus)
        self.statusbar.addPermanentWidget(self.labelLineStatus)
        self.statusbar.addPermanentWidget(self.labelTextStatus)
        self.statusbar.addPermanentWidget(self.labelStatus)

        app_doc_data = AppDocData.instance()
        _translate = QCoreApplication.translate
        version = QCoreApplication.applicationVersion()
        # set title
        self.setWindowTitle(app_doc_data.current_project.name)

        """
        self._scene = QtImageViewerScene(self)

        self.graphicsView = QtImageViewer(self)
        self.graphicsView.setParent(self.centralwidget)
        self.graphicsView.useDefaultCommand()  # USE DEFAULT COMMAND
        self.graphicsView.setMouseTracking(True)
        self.graphicsView.viewport().installEventFilter(self)
        self.graphicsView.setScene(self._scene)

        self.verticalLayout.addWidget(self.graphicsView)
        """

        # connect signals and slots
        self.actionNew.triggered.connect(self.on_new)
        self.actionOpen.triggered.connect(self.open_image_drawing)
        self.actionSave.triggered.connect(self.on_save)

        self.resizeDocks({self.dockWidget}, {self.dockWidgetObjectExplorer.sizeHint().width()}, Qt.Horizontal)

        # load stylesheet file list
        stylesheet_name = QtWidgets.qApp.stylesheet_name
        files = [os.path.splitext(file)[0] for file in
                 os.listdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'stylesheets'))
                 if os.path.splitext(file)[1] == '.qss']
        for file in files:
            action = self.menuTheme.addAction(file)
            action.setCheckable(True)
            action.setChecked(True) if stylesheet_name == file else action.setChecked(False)
            action.triggered.connect(partial(self.load_stylesheet, file))
        # up to here

        # load language files
        language_name = QtWidgets.qApp.language_name
        files = ['en_us']  # english is default language
        files.extend([os.path.splitext(file)[0] for file in
                      os.listdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'translate'))
                      if os.path.splitext(file)[1] == '.qm'])
        for file in files:
            action = self.menuLanguage.addAction(file)
            action.setCheckable(True)
            action.setChecked(True) if language_name.lower() == file.lower() else action.setChecked(False)
            action.triggered.connect(partial(self.load_language, file))
        # up to here

        self.read_settings()

    @property
    def title(self) -> str:
        """return window title"""

        from App import App

        app_doc_data = AppDocData.instance()
        project = app_doc_data.getCurrentProject()
        version = QCoreApplication.applicationVersion()
        title = f"{App.NAME}({version}) - {project.name}:" \
                f"{app_doc_data.activeDrawing.name if app_doc_data.activeDrawing else ''}"
        #title = f"{App.NAME} : ID2 " \
        #        f"{app_doc_data.activeDrawing.name if app_doc_data.activeDrawing else ''}"

        return title

    @property
    def scene(self):
        """getter scene"""
        return self._scene

    def eventFilter(self, source, event):
        """display mouse position of graphics view"""
        try:
            if event.type() == QEvent.MouseMove:
                self.current_pos = self.graphicsView.mapToScene(event.pos())
                self._label_mouse.setText(
                    'mouse pos : ({},{})'.format(round(self.current_pos.x()), round(self.current_pos.y())))
        except Exception as ex:
            message = 'error occurred({}) in {}:{}'.format(ex, sys.exc_info()[-1].tb_frame.f_code.co_filename,
                                                           sys.exc_info()[-1].tb_lineno)
            self.addMessage.emit(MessageType.Error, message)

        return QWidget.eventFilter(self, source, event)

    def closeEvent(self, event):
        """save geometry and state and ask user to save drawing which is modified"""

        self.settings.setValue('geometry', self.saveGeometry())
        self.settings.setValue('windowState', self.saveState())
        # TODO: need to modify
        # self.save_drawing_if_necessary()
        AppDocData.instance().clear()
        event.accept()

    def inconsistencyTableKeyPressEvent(self, event):
        try:
            row = self.tableWidgetInconsistency.selectedIndexes()[0].row()
            col = self.tableWidgetInconsistency.selectedIndexes()[0].column()
            from HighlightCommand import HighlightCommand
            if event.key() == Qt.Key_Up:
                if row != 0:
                    errorItem = self.tableWidgetInconsistency.item(row - 1, 1).tag
                    HighlightCommand(self.graphicsView).execute(errorItem)
            elif event.key() == Qt.Key_Down:
                if row is not self.tableWidgetInconsistency.rowCount() - 1:
                    errorItem = self.tableWidgetInconsistency.item(row + 1, 1).tag
                    HighlightCommand(self.graphicsView).execute(errorItem)
            elif event.key() == Qt.Key_Delete:
                item = self.tableWidgetInconsistency.item(row, 0).tag
                if item and item.scene(): item.scene().removeItem(item)
                self.tableWidgetInconsistency.removeRow(row)

                self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tabInconsistency),
                                            self.tr('Inconsistency') + f"({self.tableWidgetInconsistency.rowCount()})")
        except Exception as ex:
            message = 'error occurred({}) in {}:{}'.format(ex, sys.exc_info()[-1].tb_frame.f_code.co_filename,
                                                           sys.exc_info()[-1].tb_lineno)
            self.addMessage.emit(MessageType.Error, message)
        # finally:
        #    return QTableView.keyPressEvent(self.tableWidgetInconsistency, event)

    def onValidation(self):
        """validation check"""
        from ValidationDialog import QValidationDialog
        from ValidateCommand import ValidateCommand

        if not self.graphicsView.hasImage():
            self.showImageSelectionMessageBox()
            return

        try:
            dlg = QValidationDialog(self)
            if QDialog.Accepted == dlg.exec_():
                # remove error items
                for item in self.graphicsView.scene().items():
                    if type(item) is QEngineeringErrorItem:
                        item.transfer.onRemoved.emit(item)
                # up to here

                self.progress_bar.setMaximum(len(self.graphicsView.scene().items()))
                self.progress_bar.setValue(0)

                cmd = ValidateCommand(self.graphicsView)
                cmd.show_progress.connect(self.progress_bar.setValue)
                errors = cmd.execute(self.graphicsView.scene().items())
                for error in errors:
                    error.transfer.onRemoved.connect(self.itemRemoved)
                    #self.graphicsView.scene().addItem(error)
                    error.addSvgItemToScene(self.graphicsView.scene())

                self.tableWidgetInconsistency.clearContents()
                self.tableWidgetInconsistency.setRowCount(len(errors))
                for index, error in enumerate(errors):
                    self.makeInconsistencyTableRow(index, error)

                self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tabInconsistency),
                                            self.tr('Inconsistency') + f"({len(errors)})")
                if errors:
                    self.tabWidget_2.tabBar().setTabTextColor(self.tabWidget_2.indexOf(self.tabInconsistency), Qt.red)
                else:
                    self.tabWidget_2.tabBar().setTabTextColor(self.tabWidget_2.indexOf(self.tabInconsistency), Qt.black)
        except Exception as ex:
            message = 'error occurred({}) in {}:{}'.format(ex, sys.exc_info()[-1].tb_frame.f_code.co_filename,
                                                           sys.exc_info()[-1].tb_lineno)
            self.addMessage.emit(MessageType.Error, message)
        finally:
            self.progress_bar.setValue(self.progress_bar.maximum())

    def makeInconsistencyTableRow(self, row, errorItem):
        '''
            @brief  make row data for inconsistency widget
            @author euisung
            @date   2019.04.16
        '''

        item = QTableWidgetItem(str(errorItem.parent))
        item.tag = errorItem
        self.tableWidgetInconsistency.setItem(row, 0, item)

        item = QTableWidgetItem(str(type(errorItem.parent)))
        item.tag = errorItem
        self.tableWidgetInconsistency.setItem(row, 1, item)

        item = QTableWidgetItem(errorItem.msg)
        item.tag = errorItem
        self.tableWidgetInconsistency.setItem(row, 2, item)

    def inconsistencyItemClickEvent(self, item):
        """
        @brief  inconsistency table item clicked
        @author euisung
        @date   2019.04.02
        """
        from HighlightCommand import HighlightCommand

        HighlightCommand(self.graphicsView).execute(item.tag)

    def read_settings(self):
        """read geometry and state"""
        from App import App

        try:
            self.settings = QSettings(App.COMPANY, App.NAME)
            self.restoreGeometry(self.settings.value("geometry", ""))
            self.restoreState(self.settings.value("windowState", ""))
        except Exception as ex:
            message = f"error occurred({repr(ex)}) in {sys.exc_info()[-1].tb_frame.f_code.co_filename}:" \
                      f"{sys.exc_info()[-1].tb_lineno}"
            print(message)

    def load_stylesheet(self, file):
        """load stylesheets"""
        from Models.Configuration import Configuration

        QtWidgets.qApp.load_style_sheet(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'stylesheets', file))

        app_doc_data = AppDocData.instance()
        configs = [Configuration('app', 'stylesheet', file)]
        app_doc_data.save_app_configs(configs)

        for action in self.menuTheme.actions():
            if action.text() == file:
                continue
            action.setChecked(False)

    def load_language(self, file):
        """load language file and then apply selected language"""
        from Models.Configuration import Configuration

        try:
            qm_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'translate', '{0}.qm'.format(file))
            QtWidgets.qApp.load_language(qm_file)

            app_doc_data = AppDocData.instance()
            configs = [Configuration('app', 'language', file)]
            app_doc_data.save_app_configs(configs)

            for action in self.menuLanguage.actions():
                if action.text().lower() == file.lower():
                    continue
                action.setChecked(False)
        finally:
            self.retranslateUi(self)
            self.propertyTableWidget.retranslateUi()

    def refresh_item_list(self):
        """refresh item tree"""
        self.itemTreeWidget.InitLineNoItems()

        line_nos = AppDocData.instance().tracerLineNos
        for line_no in line_nos:
            item = self.itemTreeWidget.addTreeItem(self.itemTreeWidget.root, line_no)
            connectedItems = line_no.getConnectedItems()
            for connectedItem in connectedItems:
                if issubclass(type(connectedItem), SymbolSvgItem):
                    self.itemTreeWidget.addTreeItem(item, connectedItem)

    def load_drawing_list(self):
        """load p&id drawing list"""
        from Drawing import Drawing

        try:
            app_doc_data = AppDocData.instance()
            drawings = app_doc_data.getDrawings()

            self.treeWidgetDrawingList.clear()
            self.treeWidgetDrawingList.root = QTreeWidgetItem(self.treeWidgetDrawingList,
                                                              [self.tr('P&ID Drawings'), ''])
            self.treeWidgetDrawingList.root.setFlags(
                self.treeWidgetDrawingList.root.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
            self.treeWidgetDrawingList.root.setCheckState(0, Qt.Unchecked)
            files = app_doc_data.getDrawingFileList()

            # self.progress_bar.setMaximum(len(files))
            count = 0
            # self.progress_bar.setValue(count)
            for file in files:
                x = [drawing for drawing in drawings if drawing.name == file]
                if not x or not x[0].UID:
                    drawing = Drawing(None, file, None)
                    drawings.append(drawing)
                else:
                    drawing = x[0]

                item = QTreeWidgetItem(self.treeWidgetDrawingList.root, [file, drawing.datetime])
                item.setIcon(0, QIcon(':newPrefix/image.png'))
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                item.setCheckState(0, Qt.Unchecked)
                item.setData(Qt.UserRole, 0, drawing)

                count += 1
                # self.progress_bar.setValue(count)
                # QApplication.processEvents()

            self.treeWidgetDrawingList.root.setText(0, self.tr('P&ID Drawings') +
                                                    f"({self.treeWidgetDrawingList.root.childCount()})")
            self.treeWidgetDrawingList.expandItem(self.treeWidgetDrawingList.root)
            self.treeWidgetDrawingList.root.sortChildren(0, Qt.AscendingOrder)
            self.treeWidgetDrawingList.resizeColumnToContents(0)

            app_doc_data.saveDrawings(drawings)
        except Exception as ex:
            message = 'error occurred({}) in {}:{}'.format(repr(ex), sys.exc_info()[-1].tb_frame.f_code.co_filename,
                                                           sys.exc_info()[-1].tb_lineno)
            self.addMessage.emit(MessageType.Error, message)
        finally:
            self.progress_bar.setValue(self.progress_bar.maximum())

    def open_selected_drawing(self, item, column):
        """open selected p&id drawing"""

        app_doc_data = AppDocData.instance()
        drawing = item.data(Qt.UserRole, 0)
        if drawing:
            # uncheck all drawing tree item
            drawing_top = self.treeWidgetDrawingList.topLevelItem(0)
            count = drawing_top.childCount()
            for idx in range(count):
                child = drawing_top.child(idx)
                child.setCheckState(column, Qt.Unchecked)
            # up to here

            drawing.image = None
            self.open_image_drawing(drawing)
            item.setCheckState(column, Qt.Checked)

    def show_detect_symbol_dialog(self):
        from DetectSymbolDialog import QDetectSymbolDialog

        dlg = QDetectSymbolDialog(self)
        dlg.exec_()

    '''
        @brief      OCR Editor
        @author     euisung
        @date       2018.10.05
        @history    2018.10.16 euisung      no more used, Integrated with oCRTrainingClicked
    '''

    def oCRTrainingEdidorClicked(self):
        from TrainingEditorDialog import QTrainingEditorDialog

        try:
            dialog = QTrainingEditorDialog(self)
            dialog.exec_()
        except Exception as ex:
            message = 'error occurred({}) in {}:{}'.format(ex, sys.exc_info()[-1].tb_frame.f_code.co_filename,
                                                           sys.exc_info()[-1].tb_lineno)
            self.addMessage.emit(MessageType.Error, message)

        return

    '''
        @brief      OCR Training
        @author     euisung
        @date       2018.09.27
        @history    euisung 2018.10.16 TrainingListDialog -> TrainingImageListDialog
    '''

    def oCRTrainingClicked(self):
        try:
            dialog = QTrainingImageListDialog(self)
            dialog.exec_()
        except Exception as ex:
            message = 'error occurred({}) in {}:{}'.format(ex, sys.exc_info()[-1].tb_frame.f_code.co_filename,
                                                           sys.exc_info()[-1].tb_lineno)
            self.addMessage.emit(MessageType.Error, message)

    def symbolTrainingClicked(self):
        try:
            dialog = QTrainingSymbolImageListDialog(self)
            dialog.show()
            dialog.exec_()
        except Exception as ex:
            message = 'error occurred({}) in {}:{}'.format(ex, sys.exc_info()[-1].tb_frame.f_code.co_filename,
                                                           sys.exc_info()[-1].tb_lineno)
            self.addMessage.emit(MessageType.Error, message)

    def findReplaceTextClicked(self):
        """pop up find and replace dialog"""
        if not self.graphicsView.hasImage():
            self.showImageSelectionMessageBox()
            return

        from TextItemEditDialog import QTextItemEditDialog

        self.dlgTextItemEdit = QTextItemEditDialog(self)
        self.dlgTextItemEdit.show()
        self.dlgTextItemEdit.exec_()

    def ReplaceInsertSymbolClicked(self):
        """pop up replace and insert dialog"""
        if not self.graphicsView.hasImage():
            self.showImageSelectionMessageBox()
            return

        from ReplaceSymbolDialog import QReplaceSymbolDialog

        self.dlgReplace = QReplaceSymbolDialog(self)
        self.dlgReplace.show()
        self.dlgReplace.exec_()

    def on_recognize_line(self):
        """recognize lines in selected area"""
        from RecognizeLineCommand import RecognizeLineCommand

        if not self.graphicsView.hasImage():
            self.actionOCR.setChecked(False)
            self.showImageSelectionMessageBox()
            return

        cmd = RecognizeLineCommand(self.graphicsView)
        cmd.onSuccess.connect(self.on_success_to_recognize_line)
        cmd.onRejected.connect(self.onCommandRejected)
        self.graphicsView.command = cmd

    '''
            @brief      show text recognition dialog
            @author     humkyung
            @date       2018.08.08
        '''

    def on_success_to_recognize_line(self, x, y, width, height):
        import io
        from LineDetector import LineDetector
        from EngineeringGraphicsLineItem import QEngineeringGraphicsLineItem

        try:
            image = self.graphicsView.image().copy(x, y, width, height)
            buffer = QBuffer()
            buffer.open(QBuffer.ReadWrite)
            image.save(buffer, "PNG")
            pyImage = Image.open(io.BytesIO(buffer.data()))
            img = np.array(pyImage)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            detector = LineDetector(img)
            lines = detector.detect_line_without_symbol()
            for line in lines:
                vertices = [[line[0][0] + x, line[0][1] + y], [line[1][0] + x, line[1][1] + y]]
                line_item = QEngineeringGraphicsLineItem(vertices)
                self.graphicsView.scene().addItem(line_item)

        except Exception as ex:
            message = 'error occurred({}) in {}:{}'.format(repr(ex), sys.exc_info()[-1].tb_frame.f_code.co_filename,
                                                           sys.exc_info()[-1].tb_lineno)
            self.addMessage.emit(MessageType.Error, message)

    def display_number_of_items(self):
        """display count of symbol, line, text"""

        items = [item for item in self.graphicsView.scene().items() if type(item) is QEngineeringUnknownItem]
        if len(items) > 0:
            self.labelStatus.setText(
                "<font color='red'>" + self.tr('Unrecognition') + " : {}</font>".format(len(items)))
        else:
            self.labelStatus.setText(
                "<font color='black'>" + self.tr('Unrecognition') + " : {}</font>".format(len(items)))

        items = [item for item in self.graphicsView.scene().items() if
                 issubclass(type(item), SymbolSvgItem) and type(item) is not QEngineeringErrorItem]
        self.labelSymbolStatus.setText("<font color='blue'>" + self.tr('Symbol') + " : {}</font>".format(len(items)))

        items = [item for item in self.graphicsView.scene().items() if type(item) is QEngineeringLineItem]
        self.labelLineStatus.setText("<font color='blue'>" + self.tr('Line') + " : {}</font>".format(len(items)))

        items = [item for item in self.graphicsView.scene().items() if issubclass(type(item), QEngineeringTextItem)]
        self.labelTextStatus.setText("<font color='blue'>" + self.tr('Text') + " : {}</font>".format(len(items)))

        self.itemTreeWidget.sceneChanged(self.graphicsView.scene().items())

    def dbUpdate(self):
        """ no more used """
        """db update when save or recognition"""

        try:
            appDocData = AppDocData.instance()
            items = appDocData.allItems

            '''
            titleBlockProps = appDocData.getTitleBlockProperties()
            titleBlockItems = []
            for item in items:
                # if type(item) is QEngineeringLineNoTextItem:
                #    item.saveLineData()
                if type(item) is QEngineeringTextItem:
                    for titleBlockProp in titleBlockProps:
                        if item.area == titleBlockProp[0]:
                            titleBlockItems.append(item)
            '''

            # unknown item is not saved now for performance
            db_items = [item for item in items if issubclass(type(item), QEngineeringAbstractItem) and
                        type(item) is not QGraphicsBoundingBoxItem and
                        type(item) is not QEngineeringErrorItem and
                        type(item) is not QEngineeringLineNoTextItem and
                        type(item) is not QEngineeringUnknownItem]
            db_items.extend([item for item in items if type(item) is QEngineeringLineNoTextItem])
            db_items.extend([line for line in appDocData.tracerLineNos if type(line) is QEngineeringTrimLineNoTextItem])
            # db_items.extend(titleBlockItems)
            configs = appDocData.getConfigs('Data Save', 'Unknown Xml Only')
            if configs and int(configs[0].value) == -1:
                db_items.extend([item for item in items if type(item) is QEngineeringUnknownItem])

            '''
            dbItems = [item for item in items if
                       type(item) is QEngineeringInstrumentItem or type(item) is QEngineeringEquipmentItem or type(
                           item) is QEngineeringReducerItem or \
                       type(item) is QEngineeringNoteItem or type(item) is SymbolSvgItem or type(
                           item) is QEngineeringLineNoTextItem or type(
                           item) is QEngineeringVendorItem] + titleBlockItems
            '''
            appDocData.saveToDatabase(db_items)
        except Exception as ex:
            message = 'error occurred({}) in {}:{}'.format(ex, sys.exc_info()[-1].tb_frame.f_code.co_filename,
                                                           sys.exc_info()[-1].tb_lineno)
            self.addMessage.emit(MessageType.Error, message)

    def save_drawing_if_necessary(self):
        """ask to user to save drawing or not when drawing is modified"""

        app_doc_data = AppDocData.instance()
        if app_doc_data.activeDrawing and app_doc_data.activeDrawing.modified:
            #if QMessageBox.Yes == QMessageBox.question(self, self.tr("Question"),
            #                                           self.tr("Do you want to save drawing?"),
            #                                           QMessageBox.Yes | QMessageBox.No):
            #    self.actionSaveCliked()
            #    return True
            if QMessageBox.Ignore == QMessageBox.question(self, self.tr('Continue?'),
                                                       self.tr('Changes may not have been saved.'),
                                                       QMessageBox.Ignore | QMessageBox.Cancel):
                return False
            return True

    '''
        @brief      action save click event
        @author     kyouho
        @date       2018.08.09
        @history    2018.11.02      euisung     add line data list db update
                    humkyung save saved time to database
                    2018.11.05      euisung     add note data list db update
                    2018.11.05      euisung     add db delete process before save
                    2018.11.12      euisung     db part move new method to dbUpdate
    '''

    def actionSaveCliked(self):
        from EngineeringAbstractItem import QEngineeringAbstractItem
        from SaveWorkCommand import SaveWorkCommand

        try:
            if not self.actionSave.isEnabled():
                return
            self.actionSave.setEnabled(False)

            # save alarm
            self.save_alarm_enable(False)

            app_doc_data = AppDocData.instance()
            if app_doc_data.imgName is None:
                self.showImageSelectionMessageBox()
                return

            app_doc_data.clearItemList(False)

            items = self.graphicsView.scene().items()

            '''
            # for check line disappear bug
            disappear_lines = [line for line in app_doc_data.lines if line not in items]
            '''

            '''
            for item in items:
                if issubclass(type(item), QEngineeringAbstractItem):
                    app_doc_data.allItems.append(item)
                    if issubclass(type(item), QEngineeringTextItem):
                        app_doc_data.texts.append(item)
            '''

            '''
            # for check line disappear bug
            if disappear_lines:
                app_doc_data.allItems.extend(disappear_lines)
                for dis_line in disappear_lines:
                    self.addMessage.emit(MessageType.Check, f"disapper line from scene : {str(dis_line)}")
            '''

            '''
            itemTypes = []
            for item in items:
                typeExist = False
                for itemType in itemTypes:
                    if type(item) is itemType:
                        typeExist = True
                        break
                if not typeExist:
                    itemTypes.append(type(item))
            '''

            self._save_work_cmd = SaveWorkCommand(self.graphicsView.scene())
            self._save_work_cmd.show_progress.connect(self.progress_bar.setValue)
            self._save_work_cmd.display_message.connect(self.onAddMessage)
            self._save_work_cmd.finished.connect(self.save_finished)

            self._save_work_cmd.start()
        except Exception as ex:
            message = 'error occurred({}) in {}:{}'.format(repr(ex), sys.exc_info()[-1].tb_frame.f_code.co_filename,
                                                           sys.exc_info()[-1].tb_lineno)
            self.addMessage.emit(MessageType.Error, message)

    def save_finished(self):
        """reload drawing list"""

        self._save_work_cmd.show_progress.emit(100)
        QMessageBox.about(self.graphicsView, self.tr('Information'), self._save_work_cmd.resultStr)
        self.load_drawing_list()

        app_doc_data = AppDocData.instance()
        app_doc_data.activeDrawing.modified = False
        title = self.windowTitle()
        self.setWindowTitle(title[:-1] if title[-1] == '*' else title)

        self.actionSave.setEnabled(True)
        
        # save alarm
        self.save_alarm_enable(True)

    '''
        @brief      refresh resultPropertyTableWidget
        @author     kyouho
        @date       2018.07.19
    '''

    def refreshResultPropertyTableWidget(self):
        items = self.graphicsView.scene().selectedItems()
        if len(items) == 1:
            self.resultPropertyTableWidget.show_item_property(items[0])

    '''
        @brief  add message listwidget
        @author humkyung
        @date   2018.07.31
    '''

    def onAddMessage(self, messageType, message):
        from AppDocData import MessageType

        try:
            current = QDateTime.currentDateTime()

            item = QListWidgetItem('{}: {}'.format(current.toString('hh:mm:ss'), message))
            item.setFlags(item.flags() | Qt.ItemIsEditable)
            if messageType == MessageType.Error:
                item.setBackground(Qt.red)
            elif messageType == 'check':
                item.setBackground(Qt.yellow)

            self.listWidgetLog.insertItem(0, item)
        except Exception as ex:
            print('error occurred({}) in {}:{}'.format(ex, sys.exc_info()[-1].tb_frame.f_code.co_filename,
                                                       sys.exc_info()[-1].tb_lineno))

    '''
        @brief      clear log
        @author     humkyung
        @date       2018.08.01
    '''

    def onClearLog(self):
        self.listWidgetLog.clear()

    '''
        @brief      rotate selected symbol
        @author     humkyung
        @date       2018.08.15
    '''

    def onRotate(self, action):
        selected = [item for item in self.graphicsView.scene().selectedItems() if issubclass(type(item), SymbolSvgItem)]
        if len(selected) == 1:
            from RotateCommand import RotateCommand
            self.graphicsView.scene()._undo_stack.push(RotateCommand(self.graphicsView.scene(), selected))

    '''
        @brief      Area Zoom
        @author     Jeongwoo
        @date       2018.06.27
        @history    connect command's rejected signal
    '''

    def onAreaZoom(self, action):
        if self.actionZoom.isChecked():
            cmd = AreaZoomCommand.AreaZoomCommand(self.graphicsView)
            cmd.onRejected.connect(self.onCommandRejected)
            self.graphicsView.command = cmd

    def onVendor(self, action):
        """make vendor package area"""

        if not self.graphicsView.hasImage():
            self.actionVendor.setChecked(False)
            self.showImageSelectionMessageBox()
            return

        self.actionVendor.setChecked(True)
        if not hasattr(self.actionVendor, 'tag'):
            self.actionVendor.tag = PlacePolygonCommand.PlacePolygonCommand(self.graphicsView)
            self.actionVendor.tag.onSuccess.connect(self.onVendorCreated)
            self.actionVendor.tag.onRejected.connect(self.onCommandRejected)

        self.graphicsView.command = self.actionVendor.tag

    def onVendorCreated(self):
        """add created vendor polygon area to scene"""

        try:
            count = len(self.actionVendor.tag._polyline._vertices)
            if count > 2:
                points = []
                for point in self.actionVendor.tag._polyline._vertices:
                    points.append(QPoint(round(point[0]), round(point[1])))
                polygon = QPolygonF(points)
                item = QEngineeringVendorItem(polygon, pack_type=self.packageComboBox.currentText())
                item.area = 'Drawing'
                item.transfer.onRemoved.connect(self.itemRemoved)
                self.graphicsView.scene().addItem(item)
        finally:
            self.graphicsView.scene().removeItem(self.actionVendor.tag._polyline)
            self.actionVendor.tag.reset()

    '''
        @brief      Fit Window
        @author     Jeongwoo
        @date       2018.06.27
        @history    2018.06.27  Jeongwoo    Chnage method to initialize command [Set None → DefaultCommand]
    '''

    def fitWindow(self, action):
        self.graphicsView.useDefaultCommand()
        self.graphicsView.zoomImageInit()

    def scene_changed(self):
        """update modified flag"""

        self.display_number_of_items()

        app_doc_data = AppDocData.instance()
        app_doc_data.activeDrawing.modified = True
        title = self.windowTitle()
        self.setWindowTitle(title if title[-1] == '*' else title + '*')

    def onConvertPDFToImage(self):
        """convert to selected pdf to image"""
        import os

        try:
            file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'bin64', 'PDF_TO_IMAGE.exe')
            os.startfile(file_path)
        except Exception as ex:
            message = 'error occurred({}) in {}:{}'.format(ex, sys.exc_info()[-1].tb_frame.f_code.co_filename,
                                                           sys.exc_info()[-1].tb_lineno)
            self.addMessage.emit(MessageType.Error, message)

    def onImportTextFromCAD(self):
        """ import text from cad """
        try:
            self.onCommandRejected()
            dialog = QImportTextFromCADDialog(self)
            dialog.show()
            dialog.exec_()
        except Exception as ex:
            message = 'error occurred({}) in {}:{}'.format(ex, sys.exc_info()[-1].tb_frame.f_code.co_filename,
                                                           sys.exc_info()[-1].tb_lineno)
            self.addMessage.emit(MessageType.Error, message)

    def onSymbolThickness(self):
        """ symbol thickness reinforcement by using configuration filter drawing dilate size """
        try:
            self.onCommandRejected()
            dialog = QSymbolThicknessDialog(self)
            dialog.exec_()
        except Exception as ex:
            message = 'error occurred({}) in {}:{}'.format(ex, sys.exc_info()[-1].tb_frame.f_code.co_filename,
                                                           sys.exc_info()[-1].tb_lineno)
            self.addMessage.emit(MessageType.Error, message)

    def on_help(self):
        """ open help file """
        import os

        try:
            help_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ID2 User Manual.pdf')
            os.system('"{}"'.format(help_file_path))
        except Exception as ex:
            message = 'error occurred({}) in {}:{}'.format(ex, sys.exc_info()[-1].tb_frame.f_code.co_filename,
                                                           sys.exc_info()[-1].tb_lineno)
            self.addMessage.emit(MessageType.Error, message)

    def onSelectionChanged(self):
        """selection changed"""
        items = [item for item in self.graphicsView.scene().selectedItems() if issubclass(type(item), SymbolSvgItem) or
                 type(item) is QEngineeringLineItem or issubclass(type(item), QEngineeringTextItem) or
                 type(item) is QEngineeringUnknownItem or type(item) is QEngineeringVendorItem]
        if items:
            lineNos = [item for item in items if type(item) is QEngineeringLineNoTextItem]
            item = items[-1] if not lineNos else lineNos[0]
            self.itemTreeWidget.findItem(item)
            self.resultPropertyTableWidget.show_item_property(item)
            if type(item) is QEngineeringErrorItem:
                for index in range(self.tableWidgetInconsistency.rowCount()):
                    if self.tableWidgetInconsistency.item(index, 1).tag is item:
                        self.tableWidgetInconsistency.selectRow(index)
                        break
            if issubclass(type(item), SymbolSvgItem):
                pass
                #self.symbolTreeWidget.select_symbol(item)
        else:
            self.resultPropertyTableWidget.show_item_property(None)

    '''
        @brief      Initialize scene and itemTreeWidget
        @author     Jeongwoo
        @date       2018.06.14
        @history    humkyung 2018.08.16 ask to delete recognized items before remove
    '''

    def on_initialize_scene(self, action):
        if not self.graphicsView.hasImage():
            self.showImageSelectionMessageBox()

            return

        try:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(self.tr('Do you want to remove all items?\nThis work cannot be recovered.'))
            msg.setWindowTitle(self.tr("Initialize"))
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            if QMessageBox.Ok == msg.exec_():
                app_doc_data = AppDocData.instance()
                app_doc_data.clearItemList(True)

                scene = self.graphicsView.scene()
                pixmap = self.graphicsView.getPixmapHandle()
                scene.removeItem(pixmap)    # disconnect pixmap from scene
                scene.clear()               # remove all items from scene and then delete them
                scene.addItem(pixmap)       # add pixmap

                if self.path is not None:
                    baseName = os.path.basename(self.path)
                    self.itemTreeWidget.setCurrentPID(baseName)

        except Exception as ex:
            message = 'error occurred({}) in {}:{}'.format(ex, sys.exc_info()[-1].tb_frame.f_code.co_filename,
                                                           sys.exc_info()[-1].tb_lineno)
            self.addMessage.emit(MessageType.Error, message)

    '''
        @brief      Manage Checkable Action statement
        @author     Jeongwoo
        @date       2018.05.10
        @history    2018.06.27  Jeongwoo    Chnage method to initialize command [Set None → DefaultCommand]
    '''

    def actionGroupTriggered(self, action):
        if hasattr(self.actionLine, 'tag'):
            self.actionLine.tag.onRejected.emit(None)

        if hasattr(self.actionVendor, 'tag'):
            self.actionVendor.tag.onRejected.emit(None)

        if self.graphicsView.command is not None:
            self.graphicsView.useDefaultCommand()

        for _action in self.actionGroup.actions():
            _action.setChecked(False)

        action.setChecked(True)

    '''
        @brief      Create Equipment
        @author     Jeongwoo
        @date       18.05.03
        @history    2018.05.04  Jeongwoo    Add Parameter on CreateSymbolCommand
    '''

    def createEquipment(self):
        if not self.graphicsView.hasImage():
            self.actionEquipment.setChecked(False)
            self.showImageSelectionMessageBox()
            return
        if self.actionEquipment.isChecked():
            self.graphicsView.command = CreateSymbolCommand.CreateSymbolCommand(self.graphicsView, self.itemTreeWidget,
                                                                                self.symbolTreeWidget)
        else:
            self.graphicsView.useDefaultCommand()

    '''
        @brief      Create Nozzle
        @author     Jeongwoo
        @date       2018.05.03
        @history    2018.05.04  Jeongwoo    Add Parameter on CreateSymbolCommand
    '''

    def createNozzle(self):
        if not self.graphicsView.hasImage():
            self.actionNozzle.setChecked(False)
            self.showImageSelectionMessageBox()
            return
        if self.actionNozzle.isChecked():
            self.graphicsView.command = CreateSymbolCommand.CreateSymbolCommand(self.graphicsView, self.itemTreeWidget,
                                                                                self.symbolTreeWidget)
        else:
            self.graphicsView.useDefaultCommand()

    '''
        @brief      Area OCR
        @author     Jeongwoo
        @date       18.04.18
        @history    2018.05.02  Jeongwoo    Change graphicsView.command by actionOCR checked state
                                            Show MessageBox when imageviewer doesn't have image
    '''

    def onAreaOcr(self):
        if not self.graphicsView.hasImage():
            self.actionOCR.setChecked(False)
            self.showImageSelectionMessageBox()
            return

        if self.actionOCR.isChecked():
            cmd = AreaOcrCommand.AreaOcrCommand(self.graphicsView)
            cmd.onSuccess.connect(self.onRecognizeText)
            cmd.onRejected.connect(self.onCommandRejected)
            self.graphicsView.command = cmd
        else:
            self.graphicsView.useDefaultCommand()

    '''
        @brief      show text recognition dialog
        @author     humkyung
        @date       2018.08.08
    '''

    def onRecognizeText(self, x, y, width, height):
        from OcrResultDialog import QOcrResultDialog
        from Area import Area

        try:
            app_doc_data = AppDocData.instance()

            modifiers = QApplication.keyboardModifiers()
            image = self.graphicsView.image().copy(x, y, width, height)
            dialog = QOcrResultDialog(self, image, QRectF(x, y, width, height),
                                      format=QOcrResultDialog.Format.Table if modifiers == Qt.AltModifier else QOcrResultDialog.Format.Normal)
            if modifiers == Qt.ControlModifier:
                return
            (res, textInfoList) = dialog.showDialog()
            if QDialog.Accepted == res and textInfoList:
                for textInfo in textInfoList:
                    item = QEngineeringTextItem.create_text_with(self.graphicsView.scene(), textInfo)
                    if item:
                        item.setDefaultTextColor(Qt.blue)
                        item.transfer.onRemoved.connect(self.itemRemoved)

                        area_list = app_doc_data.getAreaList()
                        title_area_list = app_doc_data.getTitleBlockProperties()
                        title_list = []
                        if title_area_list:
                            for title_area in title_area_list:
                                area = Area(title_area[0])
                                area.parse(title_area[2])
                                title_list.append(area)
                        for area in area_list + title_list:
                            pt = [item.sceneBoundingRect().center().x(), item.sceneBoundingRect().center().y()]
                            if area.contains(pt):
                                item.area = area.name
                                break
                    else:
                        self.addMessage.emit(MessageType.Normal, self.tr('Fail to create text.'))
            elif QDialog.Accepted == res and not textInfoList:
                QMessageBox.about(self.graphicsView, self.tr("Notice"), self.tr("Fail to recognize text"))
        except Exception as ex:
            message = 'error occurred({}) in {}:{}'.format(ex, sys.exc_info()[-1].tb_frame.f_code.co_filename,
                                                           sys.exc_info()[-1].tb_lineno)
            self.addMessage.emit(MessageType.Error, message)

    '''
        @brief  area configuration
    '''

    def areaConfiguration(self):
        from ConfigurationAreaDialog import QConfigurationAreaDialog
        if not self.graphicsView.hasImage():
            self.showImageSelectionMessageBox()
            return
        self.onCommandRejected()
        self.dlgConfigurationArea = QConfigurationAreaDialog(self)
        self.dlgConfigurationArea.show()
        self.dlgConfigurationArea.exec_()

    '''
        @brief  configuration
    '''

    def configuration(self):
        from ConfigurationDialog import QConfigurationDialog

        self.dlgConfiguration = QConfigurationDialog(self)
        # self.dlgConfiguration.show()
        if QDialog.Accepted == self.dlgConfiguration.exec_():
            QEngineeringLineItem.LINE_TYPE_COLORS.clear()
            QEngineeringInstrumentItem.INST_COLOR = None

    '''
        @brief  show special item types dialog 
        @author humkyung
        @date   2019.08.10
    '''

    def on_show_special_item_types(self):
        from SpecialItemTypesDialog import QSpecialItemTypesDialog

        dlg = QSpecialItemTypesDialog(self)
        dlg.exec_()

    def on_show_data_transfer(self):
        """ show data transfer dialog """
        from DataTransferDialog import QDataTransferDialog

        dlg = QDataTransferDialog(self)
        dlg.exec_()

    def on_show_data_export(self):
        """ show data export dialog """
        from DataExportDialog import QDataExportDialog

        dlg = QDataExportDialog(self)
        dlg.exec_()

    def on_show_eqp_datasheet_export(self):
        """ show eqp datasheet export dialog """
        from EqpDatasheetExportDialog import QEqpDatasheetExportDialog

        dlg = QEqpDatasheetExportDialog(self)
        dlg.exec_()

    def on_show_opc_relation(self):
        """ show opc relation dialog """
        from OPCRelationDialog import QOPCRelationDialog

        dlg = QOPCRelationDialog(self)
        dlg.exec_()

    '''
        @brief  show nominal diameter dialog 
        @author humkyung
        @date   2018.06.28
    '''

    def onShowCodeTable(self):
        from CodeTableDialog import QCodeTableDialog

        dlg = QCodeTableDialog(self)
        dlg.show()
        dlg.exec_()
        if dlg.code_area:
            if dlg.code_area.scene():
                self.graphicsView.scene().removeItem(dlg.code_area)
        if dlg.desc_area:
            if dlg.desc_area.scene():
                self.graphicsView.scene().removeItem(dlg.desc_area)
        self.graphicsView.useDefaultCommand()

    def onShowCustomCodeTable(self):
        from CustomCodeTablesDialog import CustomCodeTablesDialog

        dlg = CustomCodeTablesDialog(self)
        dlg.show()
        dlg.exec_()
        self.graphicsView.useDefaultCommand()

    def onShowReplaceCodeTable(self):
        from CustomCodeTablesDialog import CustomCodeTablesDialog

        dlg = CustomCodeTablesDialog(self, replace=True)
        dlg.show()
        dlg.exec_()
        self.graphicsView.useDefaultCommand()

    '''
        @brief  show HMB data
        @author humkyung
        @date   2018.07.11
    '''

    def onHMBData(self):
        from HMBDialog import QHMBDialog

        dlg = QHMBDialog(self)
        dlg.show()
        dlg.exec_()

    '''
        @brief  show line data list 
        @author humkyung
        @date   2018.05.03
    '''

    def showItemDataList(self):
        from ItemDataExportDialog import QItemDataExportDialog

        dlg = QItemDataExportDialog(self)
        dlg.exec_()

    def showTextDataList(self):
        '''
            @brief      show all text item in scene
            @author     euisung
            @date       2019.04.18
        '''
        try:
            if not self.graphicsView.hasImage():
                self.showImageSelectionMessageBox()
                return

            self.onCommandRejected()
            dialog = QTextDataListDialog(self)
            dialog.show()
        except Exception as ex:
            message = 'error occurred({}) in {}:{}'.format(ex, sys.exc_info()[-1].tb_frame.f_code.co_filename,
                                                           sys.exc_info()[-1].tb_lineno)
            self.addMessage.emit(MessageType.Error, message)

    '''
        @brief  Show Image Selection Guide MessageBox
        @author Jeongwoo
        @date   2018.05.02
    '''

    def showImageSelectionMessageBox(self):
        QMessageBox.about(self.graphicsView, self.tr("Notice"), self.tr("First select image drawing"))

    def on_search_text_changed(self):
        """filter symbol tree view"""
        regexp = QRegExp(self.lineEditFilter.text(), Qt.CaseInsensitive, QRegExp.FixedString)

        proxy_model = self.symbolTreeWidget.model()
        proxy_model.text = self.lineEditFilter.text().lower()
        proxy_model.setFilterRegExp(regexp)

        self.symbolTreeWidget.expandAll()

    '''
        @brief  change selected lines' type by selected line type
        @author humkyung
        @date   2018.06.27
    '''

    def onLineTypeChanged(self, param):
        lineType = self.lineComboBox.itemText(param)
        selected = [item for item in self.graphicsView.scene().selectedItems() if type(item) is QEngineeringLineItem]
        if selected:
            for item in selected:
                item.lineType = lineType

    def display_colors(self, value):
        """ display colors """
        from DisplayColors import DisplayColors
        from DisplayColors import DisplayOptions

        DisplayColors.instance().option = DisplayOptions.DisplayByLineNo if value is True else DisplayOptions.DisplayByLineType
        if hasattr(self, 'graphicsView'):
            self.graphicsView.scene().update(self.graphicsView.sceneRect())
            DisplayColors.instance().save_data()

    def on_new(self):
        pass

    def open_image_drawing(self, drawing, force=False):
        """open and display image drawing file"""
        from Drawing import Drawing
        from App import App
        from LoadCommand import LoadCommand
        import concurrent.futures as futures

        # Yield successive n-sized
        # chunks from l.
        def divide_chunks(l, n):
            # looping till length l
            for i in range(0, len(l), n):
                yield l[i:i + n]

        def update_items(items):
            for item in items:
                # binding items
                item.owner
                for connector in item.connectors:
                    connector.connectedItem

            return items

        try:
            app_doc_data = AppDocData.instance()

            if not self.actionSave.isEnabled():
                return

            if not force and self.save_drawing_if_necessary():
                return

            occupied = app_doc_data.set_occupying_drawing(drawing.UID)
            if occupied:
                QMessageBox.about(self.graphicsView, self.tr("Notice"),
                                  self.tr(f"The drawing is locked for editing by another user({occupied})"))
                return

            # save alarm
            self.save_alarm_enable(False)

            if hasattr(self, '_save_work_cmd'):
                self._save_work_cmd.wait()

            project = app_doc_data.getCurrentProject()

            self.path = self.graphicsView.loadImageFromFile(drawing)
            if os.path.isfile(self.path):
                self.onCommandRejected()
                app_doc_data.clear()

                app_doc_data.setImgFilePath(self.path)
                app_doc_data.activeDrawing = drawing
                
                #app_doc_data.activeDrawing.set_pid_source(Image.open(self.path))
                self.itemTreeWidget.setCurrentPID(app_doc_data.activeDrawing.name)

                drawingList = self.treeWidgetDrawingList.topLevelItem(0)
                for idx in range(drawingList.childCount()):
                    child = drawingList.child(idx)
                    if child.data(Qt.UserRole, 0) is drawing:
                        child.setCheckState(0, Qt.Checked)
                    else:
                        child.setCheckState(0, Qt.Unchecked)

                try:
                    self.show_Progress_bar()

                    # disconnect scene changed if signal is connected
                    if self.graphicsView.scene().receivers(self.graphicsView.scene().contents_changed) > 0:
                        self.graphicsView.scene().contents_changed.disconnect()

                    SymbolSvgItem.DOCUMENTS.clear()

                    # load data
                    cmd = LoadCommand()
                    cmd.display_message.connect(self.onAddMessage)
                    cmd.set_maximum.connect(self.progress.setMaximum)
                    cmd.show_progress.connect(self.progress.setValue)
                    cmd.execute((drawing, self.graphicsView.scene()),
                                symbol=True, text=True, line=True, unknown=True, package=True, update=True)
                    # up to here

                    """"update item tree widget"""
                    line_no_items = [item for item in self.graphicsView.scene().items()
                                     if type(item) is QEngineeringLineNoTextItem]
                    for line_no in line_no_items:
                        line_no_tree_item = self.itemTreeWidget.addTreeItem(self.itemTreeWidget.root, line_no)
                        for run in line_no.runs:
                            for run_item in run.items:
                                if issubclass(type(run_item), SymbolSvgItem):
                                    self.init_add_tree_item(line_no_tree_item, run_item)

                    line_no_items = [item for item in self.graphicsView.scene().items()
                                     if type(item) is QEngineeringTrimLineNoTextItem]
                    for line_no in line_no_items:
                        line_no_tree_item = self.itemTreeWidget.addTreeItem(self.itemTreeWidget.root, line_no)
                        for run in line_no.runs:
                            for run_item in run.items:
                                if issubclass(type(run_item), SymbolSvgItem):
                                    self.init_add_tree_item(line_no_tree_item, run_item)

                    for trim_line_no in app_doc_data.tracerLineNos:
                        line_no_tree_item = self.itemTreeWidget.addTreeItem(self.itemTreeWidget.root, trim_line_no)
                        for run in trim_line_no.runs:
                            for run_item in run.items:
                                if issubclass(type(run_item), SymbolSvgItem):
                                    self.init_add_tree_item(line_no_tree_item, run_item)

                    self.itemTreeWidget.update_item_count()
                    self.itemTreeWidget.expandAll()
                    """up to here"""

                    """update scene"""
                    for item in self._scene.items():
                        item.setVisible(True)

                    self._scene.update(self._scene.sceneRect())

                    """
                    # old open drawing
                    path = os.path.join(app_doc_data.getCurrentProject().getTempPath(), app_doc_data.imgName + '.xml')
                    configs = app_doc_data.getConfigs('Data Load', 'Xml First')
                    if configs and int(configs[0].value) >= 1 and os.path.isfile(path):
                        self.load_recognition_result_from_xml(drawing)
                    elif configs and int(configs[0].value) <= 1:
                        self.load_drawing(app_doc_data.activeDrawing)
                    """

                    self.display_number_of_items()
                    # connect scene changed signal
                    self.graphicsView.scene().contents_changed.connect(self.scene_changed)
                finally:
                    if hasattr(self, 'progress'):
                        self.progress.setValue(self.progress.maximum())

                self.changeViewCheckedState(True)
                self.setWindowTitle(self.title)

                # save alarm
                self.save_alarm_enable(True, True)
        except Exception as ex:
            message = 'error occurred({}) in {}:{}'.format(ex, sys.exc_info()[-1].tb_frame.f_code.co_filename,
                                                           sys.exc_info()[-1].tb_lineno)
            self.addMessage.emit(MessageType.Error, message)

        return self.path

    def on_save(self):
        pass

    def export_as_svg(self):
        """export scene to svg file"""
        from ExportCommand import ExportCommand

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getSaveFileName(self, "Export as svg", os.getcwd(), "svg file(*.svg)",
                                                   options=options)
        if file_path:
            cmd = ExportCommand(self.graphicsView.scene(), 'svg')
            cmd.display_message.connect(self.onAddMessage)
            if cmd.execute(file_path):
                QMessageBox.information(self, self.tr('Information'), self.tr('Successfully export to svg file'))
            else:
                QMessageBox.information(self, self.tr('Error'), self.tr('Fail to export to svg file'))

    def export_as_xml(self):
        pass

    def export_as_image(self):
        """export scene to image file"""
        from ExportCommand import ExportCommand

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getSaveFileName(self, "Export as png", os.getcwd(), "png file(*.png)",
                                                   options=options)
        if file_path:
            try:
                # hide image drawing
                self.onViewImageDrawing(False)

                cmd = ExportCommand(self.graphicsView.scene(), 'image')
                cmd.display_message.connect(self.onAddMessage)

                if cmd.execute(file_path):
                    QMessageBox.information(self, self.tr('Information'), self.tr('Successfully export to image file'))
                else:
                    QMessageBox.information(self, self.tr('Error'), self.tr('Fail to export to image file'))
            finally:
                if self.actionImage_Drawing.isChecked():
                    self.onViewImageDrawing(True)
                    self.actionImage_Drawing.setChecked(True)

    def show_Progress_bar(self):
        """ show progress bar """
        self.progress = QProgressDialog(self.tr("Please wait for a while"), self.tr("Cancel"), 0, 100,
                                        self) if not hasattr(self, 'progress') else self.progress
        self.progress.setWindowModality(Qt.WindowModal)
        self.progress.setAutoReset(True)
        self.progress.setAutoClose(True)
        self.progress.setMinimum(0)
        self.progress.setMaximum(100)
        self.progress.resize(600, 100)
        self.progress.setWindowTitle(self.tr("Reading file..."))
        self.progress.show()

    def changeViewCheckedState(self, checked, clear=True):
        '''
            @brief      change view checked state
            @author     euisung
            @date       2019.03.06
        '''
        # self.actionImage_Drawing.setChecked(checked)
        self.actionViewText.setChecked(checked)
        self.actionViewSymbol.setChecked(checked)
        self.actionViewLine.setChecked(checked)
        self.actionViewUnknown.setChecked(checked)
        self.actionViewInconsistency.setChecked(checked)
        self.actionViewVendor_Area.setChecked(not checked)
        self.actionDrawing_Only.setChecked(not checked)
        if clear:
            self.tableWidgetInconsistency.clearContents()
            self.tableWidgetInconsistency.setRowCount(0)

    def onViewDrawingOnly(self, isChecked):
        '''
            @brief  visible/invisible except image drawing
            @author euisung
            @date   2019.04.22
        '''
        self.changeViewCheckedState(not isChecked, False)
        for item in self.graphicsView.scene().items():
            if type(item) is not QGraphicsPixmapItem:
                item.setVisible(not isChecked)

    '''
        @brief  visible/invisible image drawing
        @author humkyung
        @date   2018.06.25
    '''

    def onViewImageDrawing(self, isChecked):
        for item in self.graphicsView.scene().items():
            if type(item) is QGraphicsPixmapItem:
                item.setVisible(isChecked)
                break

    def onViewText(self, checked):
        """visible/invisible text"""
        selected = [item for item in self.graphicsView.scene().items() if issubclass(type(item), QEngineeringTextItem)
                    and type(item) is not QEngineeringLineNoTextItem]
        for item in selected:
            item.setVisible(checked)

    def onViewSymbol(self, checked):
        """visible/invisible symbol"""
        selected = [item for item in self.graphicsView.scene().items() if
                    (issubclass(type(item), SymbolSvgItem) and type(item) is not QEngineeringErrorItem)]
        for item in selected:
            item.setVisible(checked)

    def onViewLine(self, checked):
        """visible/invisible line"""
        selected = [item for item in self.graphicsView.scene().items() if type(item) is QEngineeringLineItem]
        for item in selected:
            item.setVisible(checked)

    def onViewInconsistency(self, isChecked):
        '''
            @brief  visible/invisible Inconsistency
            @author euisung
            @date   2019.04.03
        '''
        selected = [item for item in self.graphicsView.scene().items() if type(item) is QEngineeringErrorItem]
        for item in selected:
            item.setVisible(isChecked)

    '''
        @brief  visible/invisible Unknown 
        @author humkyung
        @date   2018.06.28
    '''

    def onViewUnknown(self, isChecked):
        selected = [item for item in self.graphicsView.scene().items() if type(item) is QEngineeringUnknownItem]
        for item in selected:
            item.setVisible(isChecked)

    def onViewVendorArea(self, isChecked):
        '''
            @brief  visible/invisible Vendor Area
            @author euisung
            @date   2019.04.29
        '''
        selected = [item for item in self.graphicsView.scene().items() if issubclass(type(item), QEngineeringVendorItem)]
        for item in selected:
            item.setVisible(isChecked)

    '''
        @brief  create a symbol
        @history    2018.05.02  Jeongwoo    Change return value of QSymbolEditorDialog (Single variable → Tuple)
                                            Add SymbolSvgItem
                    2018.05.03  Jeongwoo    Change method to draw Svg Item on Scene (svg.addSvgItemToScene)
                                            Change method to make svg and image path
                    2018.06.08  Jeongwoo    Add Paramter on SymbolSvgItem.buildItem()
    '''
    def onCreateSymbolClicked(self):
        selected = [item for item in self.graphicsView.scene().selectedItems() if issubclass(type(item), QEngineeringVendorItem)]
        if len(selected) == 1:
            symbol_image = AppDocData.instance().activeDrawing.image_origin
            rect = selected[0].sceneBoundingRect()

            points = []
            for conn in selected[0].connectors:
                points.append([round(conn.center()[0] - rect.x()), round(conn.center()[1] - rect.y())])
            poly = np.array(points, np.int32)

            #mask = np.zeros((int(rect.height()), int(rect.width())))
            #cv2.fillPoly(mask, [poly], (255))
            #poly_copied = np.multiply(mask, symbol_image[round(rect.y()):round(rect.y() + rect.height()),
            #                   round(rect.x()):round(rect.x() + rect.width())])
            #cv2.fillPoly(mask,[poly],0)
            #src2 = np.multiply(mask,src2)

            mask = np.ones((int(rect.height()), int(rect.width())), dtype=np.uint8) * 255
            cv2.fillPoly(mask, [poly], (0))
            sym_img = cv2.bitwise_or(mask, symbol_image[int(rect.y()):int(rect.y()) + int(rect.height()), int(rect.x()):int(rect.x()) + int(rect.width())])
            sym_img = cv2.merge((sym_img, sym_img, sym_img))

            h, w, c = sym_img.shape
            qImg = QImage(sym_img.data, w, h, w * c, QImage.Format_RGB888)
            #pixmap = QPixmap.fromImage(qImg)

            self.onAreaSelected(None, None, None, None, package=qImg, position=rect.topLeft(), package_item=selected[0])
        else:
            cmd = FenceCommand.FenceCommand(self.graphicsView)
            cmd.onSuccess.connect(self.onAreaSelected)
            self.graphicsView.command = cmd
            QApplication.setOverrideCursor(Qt.CrossCursor)

    '''
        @brief      show SymbolEditorDialog with image selected by user
        @author     humkyung
        @date       2018.07.20
    '''

    def onAreaSelected(self, x, y, width, height, package=False, position=None, package_item=None):
        try:
            image = self.graphicsView.image()
            if image is not None:
                if not package:
                    symbolEditorDialog = SymbolEditorDialog.QSymbolEditorDialog(self, image.copy(x, y, width, height),
                                                                                AppDocData.instance().getCurrentProject())
                else:
                    symbolEditorDialog = SymbolEditorDialog.QSymbolEditorDialog(self, package,
                                                                                AppDocData.instance().getCurrentProject(), package=True)
                (isAccepted, isImmediateInsert, offsetX, offsetY, newSym) = symbolEditorDialog.showDialog()
                # TODO: not initialize symbol tree view when user reject to create a new symbol
                self.symbolTreeWidget.initSymbolTreeView()
                if isAccepted:
                    if isImmediateInsert:
                        svg = QtImageViewer.createSymbolObject(newSym.getName())
                        offsetX, offsetY = [int(point) for point in newSym.getOriginalPoint().split(',')]
                        QtImageViewer.matchSymbolToLine(self.graphicsView.scene(), svg, QPoint(position.x() + offsetX, position.y() + offsetY))

                        package_item.transfer.onRemoved.emit(selected[0])
        finally:
            self.onCommandRejected()
            QApplication.restoreOverrideCursor()

    def make_label_data(self):
        """ make label data from symbol info """
        from xml.etree.ElementTree import Element, SubElement, dump, ElementTree, parse

        if not self.graphicsView.hasImage():
            self.showImageSelectionMessageBox()
            return

        app_doc_data = AppDocData.instance()
        project = app_doc_data.getCurrentProject()

        smalls = []
        bigs = []

        symbol_list = app_doc_data.getTargetSymbolList(all=True)
        for symbol in symbol_list:
            if symbol.width and symbol.height:
                if symbol.width > 300 or symbol.height > 300:
                    bigs.append(symbol.getName())
                else:
                    smalls.append(symbol.getName())

        symbols = [item for item in self.graphicsView.scene().items() if issubclass(type(item), SymbolSvgItem)]
        names = [smalls, bigs]

        img = app_doc_data.activeDrawing.image_origin

        small_size = 500
        big_size = 850

        save_path = project.getTrainingSymbolFilePath()

        index = 0
        for size in [small_size, big_size]:
            offsets = [0, int(size / 2)]

            width, height = img.shape[1], img.shape[0]
            width_count, height_count = width // size + 2, height // size + 2
            b_width, b_height = width_count * size, height_count * size
            b_img = np.zeros((b_height, b_width), np.uint8) + 255
            b_img[:height, :width] = img[:, :]

            for offset in offsets:
                for row in range(height_count):
                    for col in range(width_count):
                        x, y = col * size + offset, row * size + offset
                        tile_rect = QRectF(x, y, size, size)
                        tile_symbols = []
                        for symbol in [symbol for symbol in symbols if symbol.name in names[index]]:
                            if tile_rect.contains(symbol.sceneBoundingRect()):
                                tile_symbols.append(symbol)
                                symbols.remove(symbol)

                        if tile_symbols:
                            training_uid = str(uuid.uuid4())
                            training_image_path = os.path.join(save_path, training_uid + '.png')
                            training_xml_path = os.path.join(save_path, training_uid + '.xml')

                            # save image
                            #_img = b_img[round(tile_rect.top()):round(tile_rect.bottom()),
                            #       round(tile_rect.left()):round(tile_rect.right())]
                            #cv2.imwrite(training_image_path, _img)
                            _img = self.graphicsView.image().copy(round(tile_rect.left()), round(tile_rect.top()), round(tile_rect.width()), round(tile_rect.height()))
                            _img.save(training_image_path)

                            # save label
                            xml = Element('annotation')
                            SubElement(xml, 'folder').text = 'None'
                            SubElement(xml, 'filename').text = os.path.basename(save_path)

                            pathNode = Element('path')
                            pathNode.text = save_path.replace('/', '\\')
                            xml.append(pathNode)

                            sourceNode = Element('source')
                            databaseNode = Element('database')
                            databaseNode.text = 'Unknown'
                            sourceNode.append(databaseNode)
                            xml.append(sourceNode)

                            sizeNode = Element('size')
                            widthNode = Element('width')
                            widthNode.text = str(int(tile_rect.width()))
                            sizeNode.append(widthNode)
                            heightNode = Element('height')
                            heightNode.text = str(int(tile_rect.height()))
                            sizeNode.append(heightNode)
                            depthNode = Element('depth')
                            depthNode.text = '3'
                            sizeNode.append(depthNode)
                            xml.append(sizeNode)

                            segmentedNode = Element('segmented')
                            segmentedNode.text = '0'
                            xml.append(segmentedNode)

                            labelContent = []
                            counts = {}
                            for item in tile_symbols:
                                rect = item.sceneBoundingRect()
                                label, xMin, yMin, xMax, yMax = item.name, int(rect.x() - 5 - x), int(rect.y() - 5 - y), int(rect.x() + rect.width() + 5 - x), int(rect.y() + rect.height() + 5 - y)
                                xMin = xMin if xMin > 0 else 0
                                yMin = yMin if yMin > 0 else 0
                                xMax = xMax if xMax < size else size
                                yMax = yMax if yMax < size else size

                                if label == 'None' or label == '':
                                    continue
                                if label not in labelContent:
                                    labelContent.append(label)
                                    counts[label] = 1
                                else:
                                    counts[label] = counts[label] + 1

                                objectNode = Element('object')
                                nameNode = Element('name')
                                nameNode.text = label
                                objectNode.append(nameNode)
                                poseNode = Element('pose')
                                poseNode.text = 'Unspecified'
                                objectNode.append(poseNode)
                                truncatedNode = Element('truncated')
                                truncatedNode.text = '0'
                                objectNode.append(truncatedNode)
                                difficultNode = Element('difficult')
                                difficultNode.text = '0'
                                objectNode.append(difficultNode)

                                bndboxNode = Element('bndbox')
                                xminNode = Element('xmin')
                                xminNode.text = str(xMin)
                                bndboxNode.append(xminNode)
                                yminNode = Element('ymin')
                                yminNode.text = str(yMin)
                                bndboxNode.append(yminNode)
                                xmaxNode = Element('xmax')
                                xmaxNode.text = str(xMax)
                                bndboxNode.append(xmaxNode)
                                ymaxNode = Element('ymax')
                                ymaxNode.text = str(yMax)
                                bndboxNode.append(ymaxNode)
                                objectNode.append(bndboxNode)

                                xml.append(objectNode)

                            ElementTree(xml).write(training_xml_path)

            index += 1

        QMessageBox.about(self, self.tr("Notice"), self.tr('Successfully applied. '))

    '''
        @brief      create a line
        @author     humkyung
        @history    Jeongwoo 2018.05.10 Change method for Checkable action
    '''
    def onPlaceLine(self):
        if not self.graphicsView.hasImage():
            self.actionLine.setChecked(False)
            self.showImageSelectionMessageBox()
            return

        self.actionLine.setChecked(True)
        if not hasattr(self.actionLine, 'tag'):
            self.actionLine.tag = PlaceLineCommand.PlaceLineCommand(self.graphicsView)
            self.actionLine.tag.onSuccess.connect(self.onLineCreated)
            self.actionLine.tag.onRejected.connect(self.onCommandRejected)

        self.graphicsView.command = self.actionLine.tag

    '''
        @brief      add created lines to scene
        @author     humkyung
        @date       2018.07.23
    '''

    def onLineCreated(self):
        from EngineeringConnectorItem import QEngineeringConnectorItem
        from LineDetector import LineDetector

        try:
            app_doc_data = AppDocData.instance()

            count = len(self.actionLine.tag._polyline._vertices)
            if count > 1:
                items = []

                detector = LineDetector(None)

                if not self.actionLine.tag.line_type:
                    line_type = self.lineComboBox.currentText()
                else:
                    if not (QEngineeringLineItem.check_piping(self.actionLine.tag.line_type) ^ QEngineeringLineItem.check_piping(self.lineComboBox.currentText())):
                        line_type = self.lineComboBox.currentText()
                    else:
                        line_type = self.actionLine.tag.line_type
                for index in range(count - 1):
                    start = self.actionLine.tag._polyline._vertices[index]
                    end = self.actionLine.tag._polyline._vertices[index + 1]

                    lineItem = QEngineeringLineItem(vertices=[start, end])
                    lineItem.transfer.onRemoved.connect(self.itemRemoved)
                    lineItem.lineType = line_type
                    if items:
                        lineItem.connect_if_possible(items[-1], 5)
                    else:
                        pt = lineItem.start_point()
                        selected = [item for item in self.graphicsView.scene().items(QPointF(pt[0], pt[1])) if
                                    type(item) is QEngineeringConnectorItem or type(item) is QEngineeringLineItem]
                        if selected and selected[0] is not lineItem:
                            if type(selected[0]) is QEngineeringConnectorItem:
                                lineItem.connect_if_possible(selected[0].parent, 5)
                            else:
                                detector.connectLineToLine(selected[0], lineItem, 5)

                    items.append(lineItem)
                    self.graphicsView.scene().addItem(lineItem)
                    #app_doc_data.lines.append(lineItem)

                pt = items[-1].end_point()
                selected = [item for item in self.graphicsView.scene().items(QPointF(pt[0], pt[1])) if
                            (type(item) is QEngineeringConnectorItem and item.parentItem() is not items[-1]) or
                            (type(item) is QEngineeringLineItem and item is not items[-1])]
                if selected and selected[0] is not items[-1]:
                    if type(selected[0]) is QEngineeringConnectorItem:
                        items[-1].connect_if_possible(selected[0].parent, 5)
                    else:
                        detector.connectLineToLine(selected[0], items[-1], 5)

                self._scene.undo_stack.push(CreateCommand(self._scene, items))
        finally:
            self.graphicsView.scene().removeItem(self.actionLine.tag._polyline)
            self.actionLine.tag.reset()

    '''
        @brief      refresh scene
        @author     humkyung
        @date       2018.07.23
    '''

    def onCommandRejected(self, cmd=None):
        try:
            if type(cmd) is PlaceLineCommand.PlaceLineCommand:
                if self.actionLine.tag._polyline:
                    self.graphicsView.scene().removeItem(self.actionLine.tag._polyline)
                self.graphicsView.scene().update()
                self.actionLine.tag.reset()

                self.actionLine.setChecked(False)
            elif type(cmd) is AreaZoomCommand.AreaZoomCommand:
                self.actionZoom.setChecked(False)
            elif type(cmd) is AreaOcrCommand.AreaOcrCommand:
                self.actionOCR.setChecked(False)
            elif type(cmd) is PlacePolygonCommand.PlacePolygonCommand:
                self.actionVendor.setChecked(False)
            else:
                if hasattr(self.actionLine, 'tag') and self.actionLine.tag._polyline:
                    self.graphicsView.scene().removeItem(self.actionLine.tag._polyline)
                    self.graphicsView.scene().update()
                    self.actionLine.tag.reset()
                if hasattr(self.actionVendor, 'tag') and self.actionVendor.tag._polyline:
                    self.graphicsView.scene().removeItem(self.actionVendor.tag._polyline)
                    self.graphicsView.scene().update()
                    self.actionVendor.tag.reset()
                self.actionLine.setChecked(False)
                self.actionZoom.setChecked(False)
                self.actionOCR.setChecked(False)
                self.actionVendor.setChecked(False)
        finally:
            self.graphicsView.useDefaultCommand()

    '''
        @brief      restore to default command when user press Escape key
        @author     humkyung 
        @date       2018.08.09
        
    '''

    def keyPressEvent(self, event):
        try:
            if event.key() == Qt.Key_Escape:
                checked = self.actionGroup.checkedAction()
                if checked:
                    checked.setChecked(False)
                    self.graphicsView.useDefaultCommand()
            elif event.key() == Qt.Key_1:
                if self.actionImage_Drawing.isChecked():
                    self.onViewImageDrawing(False)
                    self.actionImage_Drawing.setChecked(False)
                else:
                    self.onViewImageDrawing(True)
                    self.actionImage_Drawing.setChecked(True)
            elif event.key() == Qt.Key_2:
                if self.actionViewText.isChecked():
                    self.onViewText(False)
                    self.actionViewText.setChecked(False)
                else:
                    self.onViewText(True)
                    self.actionViewText.setChecked(True)
            elif event.key() == Qt.Key_3:
                if self.actionViewSymbol.isChecked():
                    self.onViewSymbol(False)
                    self.actionViewSymbol.setChecked(False)
                else:
                    self.onViewSymbol(True)
                    self.actionViewSymbol.setChecked(True)
            elif event.key() == Qt.Key_4:
                if self.actionViewLine.isChecked():
                    self.onViewLine(False)
                    self.actionViewLine.setChecked(False)
                else:
                    self.onViewLine(True)
                    self.actionViewLine.setChecked(True)
            elif event.key() == Qt.Key_5:
                if self.actionViewUnknown.isChecked():
                    self.onViewUnknown(False)
                    self.actionViewUnknown.setChecked(False)
                else:
                    self.onViewUnknown(True)
                    self.actionViewUnknown.setChecked(True)
            elif event.key() == Qt.Key_6:
                if self.actionViewInconsistency.isChecked():
                    self.onViewInconsistency(False)
                    self.actionViewInconsistency.setChecked(False)
                else:
                    self.onViewInconsistency(True)
                    self.actionViewInconsistency.setChecked(True)
            elif event.key() == Qt.Key_7:
                if self.actionViewVendor_Area.isChecked():
                    self.onViewVendorArea(False)
                    self.actionViewVendor_Area.setChecked(False)
                else:
                    self.onViewVendorArea(True)
                    self.actionViewVendor_Area.setChecked(True)
            elif event.key() == 96:  # '`' key
                if self.actionDrawing_Only.isChecked():
                    self.onViewDrawingOnly(False)
                    self.actionDrawing_Only.setChecked(False)
                else:
                    self.onViewDrawingOnly(True)
                    self.actionDrawing_Only.setChecked(True)
            elif event.key() == Qt.Key_M:  # merge text as vertical
                from TextInfo import TextInfo

                textItems = [text for text in self.graphicsView.scene().selectedItems() if
                             issubclass(type(text), QEngineeringTextItem)]
                if not textItems or len(textItems) == 1:
                    return

                angle = None
                for item in textItems:
                    if angle is None:
                        angle = item.angle
                    else:
                        if angle != item.angle:
                            return

                modifiers = QApplication.keyboardModifiers()
                enter_or_space = ' ' if modifiers == Qt.ControlModifier else '\n'
                x_or_y = 0 if modifiers == Qt.ControlModifier else 1

                textItems = sorted(textItems, key=lambda text: text.loc[x_or_y]) if textItems[0].angle == 0 else ( \
                    sorted(textItems, key=lambda text: text.loc[x_or_y]) if textItems[0].angle == 1.57 else ( \
                        sorted(textItems, key=lambda text: text.loc[x_or_y], reverse=True) if textItems[0].angle == 4.71 else \
                            sorted(textItems, key=lambda text: text.loc[x_or_y], reverse=True)))

                if textItems[0].angle == 1.57 and modifiers == Qt.ControlModifier:
                    textItems.reverse()

                minX = sys.maxsize
                minY = sys.maxsize
                maxX = 0
                maxY = 0
                newText = ''

                for text in textItems:
                    if text.loc[0] < minX: minX = text.loc[0]
                    if text.loc[1] < minY: minY = text.loc[1]
                    if text.loc[0] + text.size[0] > maxX: maxX = text.loc[0] + text.size[0]
                    if text.loc[1] + text.size[1] > maxY: maxY = text.loc[1] + text.size[1]
                    newText = newText + text.text() + enter_or_space
                    text.transfer.onRemoved.emit(text)
                newText = newText[:-1]

                textInfo = TextInfo(newText, minX, minY, maxX - minX, maxY - minY, textItems[0].angle)
                x = textInfo.getX()
                y = textInfo.getY()
                angle = textInfo.getAngle()
                text = textInfo.getText()
                width = textInfo.getW()
                height = textInfo.getH()
                item = TextItemFactory.instance().createTextItem(textInfo)
                if item is not None:
                    item.loc = [x, y]
                    item.size = (width, height)
                    item.angle = angle
                    item.setDefaultTextColor(Qt.blue)
                    item.addTextItemToScene(self.graphicsView.scene())
                    item.transfer.onRemoved.connect(self.itemRemoved)
            elif event.key() == Qt.Key_D:
                # pop up development toolkit dialog
                from DevelopmentToolkitDialog import QDevelopmentToolkitDialog

                modifiers = QApplication.keyboardModifiers()
                if modifiers == Qt.ControlModifier:
                    dlg = QDevelopmentToolkitDialog(self, self.graphicsView)
                    dlg.show()
            elif event.key() == Qt.Key_I:
                # insert symbol item that is selected symbol in tree to main window if symbol already selected on main window, replace
                index = self.symbolTreeWidget.currentIndex()
                proxy_model = self.symbolTreeWidget.model()
                items = [proxy_model.sourceModel().itemFromIndex(proxy_model.mapToSource(index))]
                if items and hasattr(items[0], 'svgFilePath'):
                    symData = items[0].data(self.symbolTreeWidget.TREE_DATA_ROLE)
                    symName = symData.getName()
                else:
                    return

                symbolItems = [symbol for symbol in self.graphicsView.scene().selectedItems() if
                               issubclass(type(symbol), SymbolSvgItem)]
                old_symbol = None
                if symbolItems and len(symbolItems) == 1:
                    old_symbol = symbolItems[0]
                    #scenePos = QPoint(old_symbol.origin[0], old_symbol.origin[1])
                    scenePos = old_symbol.mapToScene(old_symbol.transformOriginPoint())
                    old_symbol.transfer.onRemoved.emit(old_symbol)
                else:
                    scenePos = self.current_pos

                svg = QtImageViewer.createSymbolObject(symName)
                QtImageViewer.matchSymbolToLine(self.graphicsView.scene(), svg, scenePos)

                if old_symbol and svg:
                    from ReplaceCommand import ReplaceCommand

                    cmd = ReplaceCommand(self.graphicsView.scene(), old_symbol, svg)
                    self._scene.undo_stack.push(cmd)
                    return
            elif event.key() == Qt.Key_J:
                # insert and connect symbol item that is selected symbol in tree to selected symbol
                index = self.symbolTreeWidget.currentIndex()
                proxy_model = self.symbolTreeWidget.model()
                items = [proxy_model.sourceModel().itemFromIndex(proxy_model.mapToSource(index))]
                if items and hasattr(items[0], 'svgFilePath'):
                    symData = items[0].data(self.symbolTreeWidget.TREE_DATA_ROLE)
                    symName = symData.getName()
                else:
                    return

                symbolItems = [symbol for symbol in self.graphicsView.scene().selectedItems() if
                               issubclass(type(symbol), SymbolSvgItem)]
                if symbolItems and len(symbolItems) != 1:
                    return
                    
                target_symbol = symbolItems[0]
                index =  [index for index in range(len(target_symbol.conn_type)) \
                            if target_symbol.conn_type[index] == 'Primary' or target_symbol.conn_type[index] == 'Secondary']
                for connector in target_symbol.connectors:
                    svg = QtImageViewer.createSymbolObject(symName)
                    if len(svg.connectors) > 1: 
                        if ((target_symbol.conn_type and target_symbol.connectors.index(connector) in index) or not target_symbol.conn_type) and \
                                    (not connector.connectedItem or (connector.connectedItem and type(connector.connectedItem) is QEngineeringLineItem)):
                            QtImageViewer.matchSymbolToLine(self.graphicsView.scene(), svg, connector.sceneBoundingRect().center())
                    elif len(svg.connectors) == 1:
                        if ((target_symbol.conn_type and target_symbol.connectors.index(connector) in index) or not target_symbol.conn_type) and \
                                    not connector.connectedItem:
                            QtImageViewer.matchSymbolToLine(self.graphicsView.scene(), svg, connector.sceneBoundingRect().center())

                if target_symbol:
                    return
            elif event.key() == Qt.Key_X:
                app_doc_data = AppDocData.instance()
                configs = app_doc_data.getAppConfigs('app', 'mode')
                if configs and 1 == len(configs) and 'advanced' == configs[0].value:
                    advanced = True
                    items = self.graphicsView.scene().selectedItems()
                    if items:
                        item = self.symbolTreeWidget.currentItem()
                        if item:
                            self.symbolTreeWidget.showSymbolEditorDialog(item, 0)
            elif event.key() == Qt.Key_F6:
                from DEXPI import scene_to_dexpi

                app_doc_data = AppDocData.instance()
                scene_to_dexpi('D:\\Temp\\DEXPI.xml', app_doc_data.activeDrawing.name, self.graphicsView.scene())

            QMainWindow.keyPressEvent(self, event)
        except Exception as ex:
            message = f"error occurred({repr(ex)}) in {sys.exc_info()[-1].tb_frame.f_code.co_filename}:" \
                      f"{sys.exc_info()[-1].tb_lineno}"
            self.addMessage.emit(MessageType.Error, message)

    def recognize(self):
        """recognize symbol, text and line for selected drawings"""
        from datetime import datetime
        from RecognitionDialog import QRecognitionDialog

        # save alarm
        self.save_alarm_enable(False)

        app_doc_data = AppDocData.instance()
        current_drawing, currentPid = None, None

        if self.graphicsView.hasImage():
            current_drawing = app_doc_data.activeDrawing
            currentPid = app_doc_data.activeDrawing.name

        # get checked drawings
        drawing_top = self.treeWidgetDrawingList.topLevelItem(0)
        count = drawing_top.childCount()
        checked_drawings = {}
        for idx in range(count):
            child = drawing_top.child(idx)
            if child.checkState(0) == Qt.Checked and child.data(Qt.UserRole, 0):
                checked_drawings[child.data(Qt.UserRole, 0)] = child
        # up to here

        # if there is no checked drawing
        if current_drawing and currentPid and not checked_drawings:
            for idx in range(count):
                child = drawing_top.child(idx)
                if child.data(Qt.UserRole, 0) is current_drawing:
                    checked_drawings[child.data(Qt.UserRole, 0)] = child

        if not checked_drawings:
            self.showImageSelectionMessageBox()
            return

        try:
            self.onClearLog()
            dlg = QRecognitionDialog(self, [drawing for drawing in checked_drawings.keys()])
            dlg.exec_()

            if current_drawing and current_drawing in checked_drawings.keys() and dlg.isTreated:
                self.open_image_drawing(current_drawing, force=True)

            # save working date-time
            _now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            for drawing, tree_item in checked_drawings.items():
                drawing.datetime = _now
                tree_item.setText(1, _now)
            #app_doc_data.saveDrawings(checked_drawings.keys())
            self.changeViewCheckedState(True)
            # up to here
        except Exception as ex:
            message = 'error occurred({}) in {}:{}'.format(repr(ex), sys.exc_info()[-1].tb_frame.f_code.co_filename,
                                                           sys.exc_info()[-1].tb_lineno)
            self.addMessage.emit(MessageType.Error, message)

        # save alarm
            self.save_alarm_enable(True)

    '''
        @brief      remove item from tree widget and then remove from scene
        @date       2018.05.25
        @author     Jeongwoo
    '''

    def itemRemoved(self, item):
        try:
            if type(item) is QEngineeringErrorItem:
                # remove error item from inconsistency list
                for row in range(self.tableWidgetInconsistency.rowCount()):
                    if item is self.tableWidgetInconsistency.item(row, 0).tag:
                        self.tableWidgetInconsistency.removeRow(row)
                        break

                if item.scene() is not None:
                    item.scene().removeItem(item)
                del item
            else:
                remove_scene = item.scene()
                self.itemTreeWidget.itemRemoved(item)

                matches = [_item for _item in remove_scene.items() if
                           hasattr(_item, 'connectors') and [connector for connector in _item.connectors if
                                                             connector.connectedItem is item]]
                for match in matches:
                    for connector in match.connectors:
                        if connector.connectedItem is item:
                            connector.connectedItem = None
                            connector.highlight(False)

                # matches = [_item for _item in self.graphicsView.scene().items() if hasattr(_item, 'remove_assoc_item')]
                # for _item in matches:
                #    _item.remove_assoc_item(item)

                app_doc_data = AppDocData.instance()
                if type(item) is QEngineeringLineNoTextItem and item in app_doc_data.tracerLineNos:
                    app_doc_data.tracerLineNos.pop(app_doc_data.tracerLineNos.index(item))

                if type(item) is QEngineeringLineItem and item in app_doc_data.lines:
                    app_doc_data.lines.remove(item)

                matches = [_item for _item in remove_scene.items() if
                           type(_item) is QEngineeringLineNoTextItem]
                matches.extend([lineNo for lineNo in app_doc_data.tracerLineNos if
                                type(lineNo) is QEngineeringTrimLineNoTextItem])
                for match in matches:
                    if item is match.prop('From'):
                        match.set_property('From', None)
                    if item is match.prop('To'):
                        match.set_property('To', None)

                    for run_index in reversed(range(len(match.runs))):
                        run = match.runs[run_index]
                        if item in run.items:
                            index = run.items.index(item)
                            run.items.pop(index)
                            if not run.items:
                                run.explode()
                                if type(match) is QEngineeringTrimLineNoTextItem and not match.runs:
                                    app_doc_data.tracerLineNos.pop(app_doc_data.tracerLineNos.index(match))
                            # break

                matches = [_item for _item in remove_scene.items() if hasattr(_item, 'owner')]
                for match in matches:
                    if match.owner is item:
                        match.owner = None

                matches = [_item for _item in remove_scene.items() if hasattr(_item, 'attrs')]
                # done = False
                for match in matches:
                    assocs = match.associations()
                    for assoc in assocs:
                        if item is assoc:
                            for attr in match.attrs.keys():
                                if attr.AssocItem and str(item.uid) == str(attr.AssocItem.uid):
                                    attr.AssocItem = None
                                    match.attrs[attr] = ''
                                    # done = True
                            match.remove_assoc_item(item)
                            break
                    # if done: break

                if item.scene() is not None: item.scene().removeItem(item)
        except Exception as ex:
            message = 'error occurred({}) in {}:{}'.format(ex, sys.exc_info()[-1].tb_frame.f_code.co_filename,
                                                           sys.exc_info()[-1].tb_lineno)
            self.addMessage.emit(MessageType.Error, message)
        '''
        finally:
            if hasattr(item, '_cond'):
                item._cond.wakeAll()
        '''


    def connect_attributes(self, MainWindow):
        """connect attributes to symbol"""
        from LineNoTracer import LineNoTracer
        from ConnectAttrDialog import QConnectAttrDialog

        if not self.graphicsView.hasImage():
            self.showImageSelectionMessageBox()
            return

        # save alarm
        self.save_alarm_enable(False)

        try:
            dlg = QConnectAttrDialog(self, self.graphicsView.scene())
            dlg.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint & ~Qt.WindowContextHelpButtonHint)
            dlg.exec_()
            if dlg.isRunned:
                self.refresh_item_list()

                if dlg.validation_checked:
                    self.onValidation()

                self.graphicsView.invalidateScene()
        except Exception as ex:
            message = 'error occurred({}) in {}:{}'.format(ex, sys.exc_info()[-1].tb_frame.f_code.co_filename,
                                                           sys.exc_info()[-1].tb_lineno)
            self.addMessage.emit(MessageType.Error, message)
        finally:
            # save alarm
            self.save_alarm_enable(True)

    def postDetectLineProcess(self):
        '''
            @brief  check allowables among undetected items
            @author euisung
            @date   2018.11.15
            @history    2018.11.15  euisung    no more used, moved to TextItemFactoy isLineNo()
        '''
        from TextItemFactory import TextItemFactory

        appDocData = AppDocData.instance()

        tableNames = ["Fluid Code", "Insulation Purpose", "PnID Number", "Piping Materials Class", "Unit Number"]
        tableDatas = []
        for tableName in tableNames:
            tableNameFormat = tableName.replace(' ', '').replace('&&', 'n')
            tableDatas.append(appDocData.getCodeTable(tableNameFormat))

        items = self.graphicsView.scene().items()
        for item in items:
            if type(item) is not QEngineeringTextItem:
                continue
            text = item.text()
            for tableData in tableDatas:
                for data in tableData:
                    if data[3] == '':
                        continue
                    else:
                        allows = data[3].split(',')
                        for allow in allows:
                            text = text.replace(allow, data[1])

            lineItem = TextItemFactory.instance().createTextItem(text)
            if type(lineItem) is QEngineeringLineNoTextItem:
                lineItem.loc = item.loc
                lineItem.size = item.size
                lineItem.angle = item.angle
                lineItem.area = item.area
                # lineItem.addTextItemToScene(self.graphicsView.scene())
                lineItem.transfer.onRemoved.connect(self.itemRemoved)
                item.transfer.onRemoved.emit(item)
                appDocData.lineNos.append(lineItem)

    def init_add_tree_item(self, line_no_tree_item, run_item):
        """ insert symbol item and find line no as owner """
        # insert
        self.itemTreeWidget.addTreeItem(line_no_tree_item, run_item)
        # find
        self.itemTreeWidget.addTreeItem(line_no_tree_item, run_item)

    def load_drawing(self, drawing):
        """ load drawing """
        from EngineeringRunItem import QEngineeringRunItem
        from QEngineeringTrimLineNoTextItem import QEngineeringTrimLineNoTextItem

        app_doc_data = AppDocData.instance()
        try:
            symbols = []
            lines = []

            components = app_doc_data.get_components(drawing.UID)
            maxValue = len(components) * 2
            self.progress.setMaximum(maxValue) if maxValue > 0 else None

            """ parsing all symbols """
            for symbol in [component for component in components if int(component['SymbolType_UID']) != -1]:
                item = SymbolSvgItem.from_database(symbol)
                if item is not None:
                    item.transfer.onRemoved.connect(self.itemRemoved)
                    symbols.append(item)
                    app_doc_data.symbols.append(item)
                    item.addSvgItemToScene(self.graphicsView.scene())
                else:
                    pt = [float(symbol['X']), float(symbol['Y'])]
                    size = [float(symbol['Width']), float(symbol['Height'])]
                    angle = float(symbol['Rotation'])
                    item = QGraphicsBoundingBoxItem(pt[0], pt[1], size[0], size[1])
                    item.isSymbol = True
                    item.angle = angle
                    item.setPen(QPen(Qt.red, 5, Qt.SolidLine))
                    self.graphicsView.scene().addItem(item)
                    item.transfer.onRemoved.connect(self.itemRemoved)

                self.progress.setValue(self.progress.value() + 1)

            QApplication.processEvents()

            # parse texts
            for text in [component for component in components if
                         component['Name'] == 'Text' and component['SymbolType_UID'] == -1]:
                item = QEngineeringTextItem.from_database(text)
                if item is not None:
                    item.uid = text['UID']
                    item.attribute = text['Value']
                    name = text['Name']
                    item.transfer.onRemoved.connect(self.itemRemoved)
                    item.addTextItemToScene(self.graphicsView.scene())

                self.progress.setValue(self.progress.value() + 1)

            QApplication.processEvents()

            # note
            for note in [component for component in components if
                         component['Name'] == 'Note' and component['SymbolType_UID'] == -1]:
                item = QEngineeringTextItem.from_database(note)
                if item is not None:
                    item.uid = note['UID']
                    attributeValue = note['Value']
                    name = note['Name']
                    item.transfer.onRemoved.connect(self.itemRemoved)
                    item.addTextItemToScene(self.graphicsView.scene())

                self.progress.setValue(self.progress.value() + 1)

            QApplication.processEvents()

            for line in [component for component in components if
                         component['Name'] == 'Line' and component['SymbolType_UID'] == -1]:
                item = QEngineeringLineItem.from_database(line)
                if item:
                    item.transfer.onRemoved.connect(self.itemRemoved)
                    self.graphicsView.scene().addItem(item)
                    lines.append(item)

                self.progress.setValue(self.progress.value() + 1)

            QApplication.processEvents()

            for unknown in [component for component in components if
                            component['Name'] == 'Unknown' and component['SymbolType_UID'] == -1]:
                item = QEngineeringUnknownItem.from_database(unknown)
                item.transfer.onRemoved.connect(self.itemRemoved)
                if item is not None:
                    item.transfer.onRemoved.connect(self.itemRemoved)
                    self.graphicsView.scene().addItem(item)

                self.progress.setValue(self.progress.value() + 1)

            QApplication.processEvents()

            for component in [component for component in components if
                              component['Name'] == 'Line NO' and component['SymbolType_UID'] == -1]:
                line_no = QEngineeringLineNoTextItem.from_database(component)
                if type(line_no) is QEngineeringLineNoTextItem:
                    line_no.transfer.onRemoved.connect(self.itemRemoved)
                    self.addTextItemToScene(line_no)
                    line_no_tree_item = self.itemTreeWidget.addTreeItem(self.itemTreeWidget.root, line_no)

                    runs = app_doc_data.get_pipe_runs(str(line_no.uid))
                    if not runs: continue
                    for run in runs:
                        line_run = QEngineeringRunItem()
                        run_items = app_doc_data.get_pipe_run_items(run['UID'])
                        for record in run_items:
                            uid = record['Components_UID']
                            run_item = self.graphicsView.findItemByUid(uid)
                            if run_item is not None:
                                run_item._owner = line_no
                                line_run.items.append(run_item)
                        line_run.owner = line_no
                        line_no.runs.append(line_run)

                        for run_item in line_run.items:
                            if issubclass(type(run_item), SymbolSvgItem):
                                self.init_add_tree_item(line_no_tree_item, run_item)

                self.progress.setValue(self.progress.value() + 1)
            QApplication.processEvents()

            for component in [component for component in components if
                              component['Name'] == 'Trim Line NO' and component['SymbolType_UID'] == -1]:
                line_no = QEngineeringTrimLineNoTextItem()
                line_no.uid = uuid.UUID(component['UID'])

                runs = app_doc_data.get_pipe_runs(str(line_no.uid))
                if not runs: continue

                line_no_tree_item = self.itemTreeWidget.addTreeItem(self.itemTreeWidget.root, line_no)

                for run in runs:
                    line_run = QEngineeringRunItem()
                    run_items = app_doc_data.get_pipe_run_items(run['UID'])
                    for record in run_items:
                        uid = record['Components_UID']
                        run_item = self.graphicsView.findItemByUid(uid)
                        if run_item is not None:
                            run_item.owner = line_no
                            line_run.items.append(run_item)
                    line_run.owner = line_no
                    line_no.runs.append(line_run)

                    for run_item in line_run.items:
                        if issubclass(type(run_item), SymbolSvgItem):
                            self.init_add_tree_item(line_no_tree_item, run_item)

                app_doc_data.tracerLineNos.append(line_no)

                self.progress.setValue(self.progress.value() + 1)

            for component in [component for component in components if
                              component['Name'] == 'VendorPackage' and component['SymbolType_UID'] == -1]:
                item = QEngineeringVendorItem.from_database(component)
                if item is not None:
                    item.transfer.onRemoved.connect(self.itemRemoved)
                    self.graphicsView.scene().addItem(item)

            # connect flow item to line
            for line in lines:
                line.update_arrow()
                app_doc_data.lines.append(line)
            # for flowMark in [item for item in symbols if type(item) is QEngineeringFlowMarkItem]:
            #    for line in lines:
            #        if flowMark.owner is line:
            #            line._flowMark.append(flowMark)
            #            flowMark.setParentItem(line)
            # up to here

            """ update scene """
            self.graphicsView.scene().update(self.graphicsView.sceneRect())
            for item in self.graphicsView.scene().items():
                up_progress = False
                # binding items
                if hasattr(item, 'owner'):
                    item.owner
                    up_progress = True
                if hasattr(item, 'connectors'):
                    for connector in item.connectors:
                        connector.connectedItem
                    up_progress = True

                if up_progress:
                    self.progress.setValue(self.progress.value() + 1)
            
            for item in self.graphicsView.scene().items():
                item.setVisible(True)

        except Exception as ex:
            message = 'error occurred({}) in {}:{}'.format(ex, sys.exc_info()[-1].tb_frame.f_code.co_filename,
                                                           sys.exc_info()[-1].tb_lineno)
            self.addMessage.emit(MessageType.Error, message)
        finally:
            app_doc_data.clearTempDBData()
            self.itemTreeWidget.update_item_count()
            self.itemTreeWidget.expandAll()
            # self.graphicsView.scene().blockSignals(False)

    '''
        @brief      load recognition result
        @author     humkyung
        @date       2018.04.??
        @history    humkyung 2018.01.12 parse originalpoint and connectionpoint
                    Jeongwoo 2018.04.17 add QGraphicItem with Rotated text
                    Jeongwoo 2018.04.23 Change to Draw texts on QEngineeringTextItem
                    humkyung 2018.04.23 connect item remove slot to result tree
                    Jeongwoo 2018.04.25 Add if state with QEngineeringNoteItem
                    Jeongwoo 2018.04.26 Change method to create TextItem object with TextItemFactory
                    Jeongwoo 2018.05.03 Change method to draw Svg Item on Scene (svg.addSvgItemToScene)
                    Jeongwoo 2018.05.29 Change method name / Change method to add item / Add Line item
                    Jeongwoo 2018.05.30 Add parameters on SymbolSvgItem.__init__() (parentSymbol, childSymbol) / Change method name / Change XML NODE NAMES
                    Jeongwoo 2018.06.12 Add LineNoTextItem from LINE_NO
                    Jeongwoo 2018.06.14 Add UnknownItem from UNKNOWN
                    Jeongwoo 2018.06.18 Update Scene after all item added
                                        Add connect on unknown item
                                        Add [transfer] for using pyqtSignal
                    kyouho  2018.07.12  Add line property logic
                    humkyung 2018.08.22 show progress while loading xml file
                    2018.11.22      euisung     fix note road
    '''

    def load_recognition_result_from_xml(self, drawing):
        # Yield successive n-sized
        # chunks from l.
        def divide_chunks(l, n):
            # looping till length l
            for i in range(0, len(l), n):
                yield l[i:i + n]

        def update_items(items):
            for item in items:
                # binding items
                item.owner
                for connector in item.connectors:
                    connector.connectedItem

            return items

        import concurrent.futures as futures
        from xml.etree.ElementTree import Element, SubElement, dump, ElementTree, parse
        from App import App
        from EngineeringRunItem import QEngineeringRunItem
        from QEngineeringTrimLineNoTextItem import QEngineeringTrimLineNoTextItem
        from EngineeringGraphicsLineItem import QEngineeringGraphicsLineItem

        app_doc_data = AppDocData.instance()

        try:
            file_name = os.path.splitext(os.path.basename(drawing.file_path))[0]
            path = os.path.join(app_doc_data.getCurrentProject().getTempPath(), file_name + '.xml')
            self.graphicsView.scene().blockSignals(True)

            symbols = []
            lines = []

            xml = parse(path)
            root = xml.getroot()

            maxValue = 0
            maxValue = maxValue + len(list(root.iter('SYMBOL'))) - \
                       len(list(root.iterfind('LINENOS/LINE_NO/RUN/SYMBOL'))) - \
                       len(list(root.iterfind('TRIMLINENOS/TRIM_LINE_NO/RUN/SYMBOL')))
            maxValue = maxValue + len(list(root.iterfind('TEXTINFOS/ATTRIBUTE')))
            maxValue = maxValue + len(list(root.iterfind('NOTES/ATTRIBUTE')))
            maxValue = maxValue + len(list(root.iter('LINE_NO')))
            maxValue = maxValue + len(list(root.iter('LINE'))) - \
                       len(list(root.iterfind('LINENOS/LINE_NO/RUN/LINE'))) - \
                       len(list(root.iterfind('TRIMLINENOS/TRIM_LINE_NO/RUN/LINE')))
            maxValue = maxValue + len(list(root.iter('GRAPHICS_LINE')))
            maxValue = maxValue + len(list(root.iter('UNKNOWN')))
            # maxValue = maxValue + len(list(root.iter('SIZETEXT')))
            maxValue = maxValue + len(list(root.iter('TRIM_LINE_NO')))
            maxValue *= 2
            self.progress.setMaximum(maxValue) if maxValue > 0 else None

            """ parsing all symbols """
            """
            with futures.ThreadPoolExecutor(max_workers=App.THREAD_MAX_WORKER) as pool:
                future_symbol = {pool.submit(SymbolSvgItem.fromXml, symbol): symbol for symbol in root.find('SYMBOLS').iter('SYMBOL')}

                for future in futures.as_completed(future_symbol):
                    try:
                        item = future.result()
                        if item:
                            if item is not None:
                                item.transfer.onRemoved.connect(self.itemRemoved)
                                symbols.append(item)
                                docData.symbols.append(item)
                                self.addSvgItemToScene(item)
                            else:
                                pt = [float(x) for x in symbol.find('LOCATION').text.split(',')]
                                size = [float(x) for x in symbol.find('SIZE').text.split(',')]
                                angle = float(symbol.find('ANGLE').text)
                                item = QGraphicsBoundingBoxItem(pt[0], pt[1], size[0], size[1])
                                item.isSymbol = True
                                item.angle = angle
                                item.setPen(QPen(Qt.red, 5, Qt.SolidLine))
                                self.graphicsView.scene().addItem(item)
                                item.transfer.onRemoved.connect(self.itemRemoved)
                    except Exception as ex:
                        message = 'error occurred({}) in {}:{}'.format(repr(ex), sys.exc_info()[-1].tb_frame.f_code.co_filename,
                                                                       sys.exc_info()[-1].tb_lineno)

            """
            for symbol in root.find('SYMBOLS').iter('SYMBOL'):
                item = SymbolSvgItem.fromXml(symbol)
                if item is not None:
                    item.transfer.onRemoved.connect(self.itemRemoved)
                    symbols.append(item)
                    #app_doc_data.symbols.append(item)
                    item.addSvgItemToScene(self.graphicsView.scene())
                else:
                    pt = [float(x) for x in symbol.find('LOCATION').text.split(',')]
                    size = [float(x) for x in symbol.find('SIZE').text.split(',')]
                    angle = float(symbol.find('ANGLE').text)
                    item = QGraphicsBoundingBoxItem(pt[0], pt[1], size[0], size[1])
                    item.isSymbol = True
                    item.angle = angle
                    item.setPen(QPen(Qt.red, 5, Qt.SolidLine))
                    self.graphicsView.scene().addItem(item)
                    item.transfer.onRemoved.connect(self.itemRemoved)

                self.progress.setValue(self.progress.value() + 1)

            QApplication.processEvents()

            # parse texts
            for text in root.find('TEXTINFOS').iter('ATTRIBUTE'):
                item = QEngineeringTextItem.fromXml(text)
                if item is not None:
                    uid = text.find('UID')
                    attributeValue = text.find('ATTRIBUTEVALUE')
                    name = text.find('NAME').text
                    item.transfer.onRemoved.connect(self.itemRemoved)
                    item.addTextItemToScene(self.graphicsView.scene())
                    # docData.texts.append(item)

                    if name == 'TEXT':
                        if uid is not None and attributeValue is not None:
                            item.uid = uid.text
                            item.attribute = attributeValue.text

                self.progress.setValue(self.progress.value() + 1)

            QApplication.processEvents()

            # note
            for text in root.find('NOTES').iter('ATTRIBUTE'):
                item = QEngineeringTextItem.fromXml(text)
                if item is not None:
                    uid = text.find('UID')
                    attributeValue = text.find('ATTRIBUTEVALUE')
                    name = text.find('NAME').text
                    item.transfer.onRemoved.connect(self.itemRemoved)
                    item.addTextItemToScene(self.graphicsView.scene())

                    if name == 'NOTE':
                        if uid is not None:
                            item.uid = uid.text

                self.progress.setValue(self.progress.value() + 1)

            QApplication.processEvents()

            for line in root.find('LINEINFOS').iter('LINE'):
                item = QEngineeringLineItem.fromXml(line)
                if item:
                    item.transfer.onRemoved.connect(self.itemRemoved)
                    self.graphicsView.scene().addItem(item)
                    lines.append(item)

                self.progress.setValue(self.progress.value() + 1)

            for line in root.find('LINEINFOS').iter('GRAPHICS_LINE'):
                item = QEngineeringGraphicsLineItem.fromXml(line)
                if item:
                    item.transfer.onRemoved.connect(self.itemRemoved)
                    self.graphicsView.scene().addItem(item)

                self.progress.setValue(self.progress.value() + 1)

            QApplication.processEvents()

            for unknown in root.iter('UNKNOWN'):
                item = QEngineeringUnknownItem.fromXml(unknown)
                if item is not None:
                    item.transfer.onRemoved.connect(self.itemRemoved)
                    self.graphicsView.scene().addItem(item)

                self.progress.setValue(self.progress.value() + 1)

            QApplication.processEvents()

            # """ add tree widget """
            # for item in symbols:
            #    docData.symbols.append(item)
            #    self.addSvgItemToScene(item)
            #    self.itemTreeWidget.addTreeItem(self.itemTreeWidget.root, item)

            for line_no_node in root.find('LINENOS').iter('LINE_NO'):
                line_no = QEngineeringLineNoTextItem.fromXml(line_no_node)
                if line_no is None: continue
                line_no.transfer.onRemoved.connect(self.itemRemoved)
                line_no.addTextItemToScene(self.graphicsView.scene())
                line_no_tree_item = self.itemTreeWidget.addTreeItem(self.itemTreeWidget.root, line_no)
                if type(line_no) is not QEngineeringLineNoTextItem: continue

                runs_node = line_no_node.findall('RUN')
                if runs_node is None: continue

                for run_node in runs_node:
                    line_run = QEngineeringRunItem()
                    for child_node in run_node:
                        uidElement = child_node.find('UID')
                        if uidElement is not None:
                            uid = uidElement.text
                            run_item = self.graphicsView.findItemByUid(uid)
                            if run_item is not None:
                                run_item._owner = line_no
                                line_run.items.append(run_item)
                    line_run.owner = line_no
                    line_no.runs.append(line_run)

                    for run_item in line_run.items:
                        if issubclass(type(run_item), SymbolSvgItem):
                            self.init_add_tree_item(line_no_tree_item, run_item)

                # docData.tracerLineNos.append(line_no)

                self.progress.setValue(self.progress.value() + 1)
            QApplication.processEvents()

            for trimLineNo in root.iter('TRIM_LINE_NO'):
                line_no = QEngineeringTrimLineNoTextItem()
                line_no.uid = uuid.UUID(trimLineNo.find('UID').text)

                runs_node = trimLineNo.findall('RUN')
                if runs_node is None: continue
                line_no_tree_item = self.itemTreeWidget.addTreeItem(self.itemTreeWidget.root, line_no)

                for run in runs_node:
                    line_run = QEngineeringRunItem()
                    for child in run:
                        uidElement = child.find('UID')
                        if uidElement is not None:
                            uid = uidElement.text
                            run_item = self.graphicsView.findItemByUid(uid)
                            if run_item is not None:
                                run_item.owner = line_no
                                line_run.items.append(run_item)
                    line_run.owner = line_no
                    line_no.runs.append(line_run)

                    for run_item in line_run.items:
                        if issubclass(type(run_item), SymbolSvgItem):
                            self.init_add_tree_item(line_no_tree_item, run_item)

                app_doc_data.tracerLineNos.append(line_no)

                self.progress.setValue(self.progress.value() + 1)
            QApplication.processEvents()

            if root.find('VENDORS') is not None:
                for vendor in root.find('VENDORS').iter('VENDOR'):
                    item = QEngineeringVendorItem.fromXml(vendor)
                    item.transfer.onRemoved.connect(self.itemRemoved)
                    self.graphicsView.scene().addItem(item)

            # connect flow item to line
            for line in lines:
                line.update_arrow()
                app_doc_data.lines.append(line)
            # for flowMark in [item for item in symbols if type(item) is QEngineeringFlowMarkItem]:
            #    for line in lines:
            #        if flowMark.owner is line:
            #            line._flowMark.append(flowMark)
            #            flowMark.setParentItem(line)
            # up to here

            """
            group_box = QGroupBox("Contact Details")
            number_label = QLabel("Telephone number");
            number_edit = QTextEdit('hello\nthis is ....')
            layout = QFormLayout()
            layout.addRow(number_label, number_edit)
            group_box.setLayout(layout)

            proxy =  ㅐ()
            proxy.setWidget(group_box)
            self.graphicsView.scene().addItem(proxy)  # (group_box, QGraphicsItem.ItemIgnoresTransformations)
            """

            """ update scene """
            _items = [_item for _item in self.graphicsView.scene().items() if hasattr(_item, 'owner') or hasattr(_item, 'connectors')]
            if _items:
                items = divide_chunks(_items, App.THREAD_MAX_WORKER if len(_items) > App.THREAD_MAX_WORKER else len(_items))
                with futures.ThreadPoolExecutor(max_workers=App.THREAD_MAX_WORKER) as pool:
                    future_items = {pool.submit(update_items, _items): _items for _items in items}
                    for future in futures.as_completed(future_items):
                        _items = future.result()
                        self.progress.setValue(self.progress.value() + len(_items))

            """
            for item in [_item for _item in self.graphicsView.scene().items() if hasattr(_item, 'owner') or hasattr(_item, 'connectors')]:
                up_progress = False
                # binding items
                item.owner
                for connector in item.connectors:
                    connector.connectedItem

                self.progress.setValue(self.progress.value() + 1)
            """

            for item in self.graphicsView.scene().items():
                item.setVisible(True)

            self.graphicsView.scene().update(self.graphicsView.sceneRect())
        except Exception as ex:
            message = 'error occurred({}) in {}:{}'.format(ex, sys.exc_info()[-1].tb_frame.f_code.co_filename,
                                                           sys.exc_info()[-1].tb_lineno)
            self.addMessage.emit(MessageType.Error, message)
        finally:
            self.itemTreeWidget.update_item_count()
            self.itemTreeWidget.expandAll()
            self.graphicsView.scene().blockSignals(False)

    '''
        @brief      Remove added item on same place and Add GraphicsItem
        @author     Jeongwoo
        @date       2018.05.29
        @history    2018.06.18  Jeongwoo    Set Z-index
    '''

    def addLineItemToScene(self, lineItem):
        self.graphicsView.scene().addItem(lineItem)

    '''
        @brief      generate output xml file
        @author     humkyung
        @date       2018.04.23
        @history    2018.05.02  Jeongwoo    Show MessageBox when imageviewer doesn't have image
    '''

    def generateOutput(self):
        import XmlGenerator as xg

        if not self.graphicsView.hasImage():
            self.showImageSelectionMessageBox()
            return

        try:
            appDocData = AppDocData.instance()

            # collect items
            appDocData.lines.clear()
            appDocData.lines = [item for item in self.graphicsView.scene().items() if
                                type(item) is QEngineeringLineItem and item.owner is None]

            appDocData.symbols.clear()
            appDocData.symbols = [item for item in self.graphicsView.scene().items() if
                                  issubclass(type(item), SymbolSvgItem) and item.owner is None]

            appDocData.equipments.clear()
            for item in self.graphicsView.scene().items():
                if type(item) is QEngineeringEquipmentItem:
                    appDocData.equipments.append(item)

            appDocData.texts.clear()
            appDocData.texts = [item for item in self.graphicsView.scene().items() if
                                issubclass(type(item), QEngineeringTextItem) and type(
                                    item) is not QEngineeringLineNoTextItem]
            # up to here

            appDocData.imgOutput = np.ones((appDocData.activeDrawing.height, appDocData.activeDrawing.width),
                                           np.uint8) * 255
            xg.writeOutputXml(appDocData.imgName, appDocData.activeDrawing.width,
                              appDocData.activeDrawing.height)  # TODO: check
            project = appDocData.getCurrentProject()
            cv2.imwrite(os.path.join(project.getTempPath(), 'OUTPUT.png'), appDocData.imgOutput)
        except Exception as ex:
            message = 'error occurred({}) in {}:{}'.format(ex, sys.exc_info()[-1].tb_frame.f_code.co_filename,
                                                           sys.exc_info()[-1].tb_lineno)
            self.addMessage.emit(MessageType.Error, message)

    '''
        @brief      resetting attribute at secne
        @author     kyoyho
        @date       2018.08.21
    '''
    """
    def checkAttribute(self):
        try:

            docData = AppDocData.instance()
            if not self.graphicsView.hasImage():
                return

            # symbol 경우
            items = [item for item in self.graphicsView.scene().items() if issubclass(type(item), SymbolSvgItem) and type(item) is not QEngineeringSpecBreakItem and type(item) is not QEngineeringEndBreakItem]
            for item in items:
                attrs = item.attrs
                
                removeAttrList = []
                for attr in attrs:
                    if type(attr) is tuple:
                        continue

                    if attr is None:
                        removeAttrList.append(attr)
                        continue

                    attrInfo = docData.getSymbolAttributeByUID(attr.UID)
                    if attrInfo is None:
                        removeAttrList.append(attr)
                    # 해당 attribute가 맞는지 확인
                    else:
                        attrType = attrInfo.AttributeType
                        _type = type(attr)
                        if attrType == 'Symbol Item':
                            if not issubclass(_type, SymbolSvgItem):
                                removeAttrList.append(attr)
                        elif attrType == 'Text Item':
                            if _type is not QEngineeringTextItem:
                                removeAttrList.append(attr)
                        elif attrType == 'Int':
                            if _type is not UserInputAttribute and self.isNumber(attr.text):
                                removeAttrList.append(attr)
                        elif attrType == 'String':
                            if _type is not UserInputAttribute:
                                removeAttrList.append(attr)

                for attr in removeAttrList:
                    del attrs[attr]

            # Line No Text Item의 경우
            items = [item for item in self.graphicsView.scene().items() if issubclass(type(item), QEngineeringLineNoTextItem)]
            for item in items:
                attrs = item.attrs
                
                removeAttrList = []
                for attr in attrs:
                    if type(attr) is UserInputAttribute:
                        attrInfo = docData.getLinePropertiesByUID(attr.attribute)
                        if attrInfo is None:
                            removeAttrList.append(attr)

                for attr in removeAttrList:
                    del attrs[attr]

        except Exception as ex:
                message = 'error occurred({}) in {}:{}'.format(ex, sys.exc_info()[-1].tb_frame.f_code.co_filename, sys.exc_info()[-1].tb_lineno)
                self.addMessage.emit(MessageType.Error, message)
    """
    '''
        @brief      Check Number
        @author     kyouho
        @date       2018.08.20
    '''

    def isNumber(self, num):
        p = re.compile('(^[0-9]+$)')
        result = p.match(num)

        if result:
            return True
        else:
            return False

    '''
        @brief      find overlap Connector
        @author     kyouho
        @date       2018.08.28
    '''

    def findOverlapConnector(self, connectorItem):
        from shapely.geometry import Point
        from EngineeringConnectorItem import QEngineeringConnectorItem
        itemList = []

        x = connectorItem.center()[0]
        y = connectorItem.center()[1]

        connectors = [item for item in self.graphicsView.scene().items() if
                      type(item) is QEngineeringConnectorItem and item != connectorItem]
        for connector in connectors:
            if Point(x, y).distance(Point(connector.center()[0], connector.center()[1])) < 5:
                itemList.append(connector.parent)

        return itemList

