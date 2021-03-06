# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\UI\MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1089, 903)
        MainWindow.setBaseSize(QtCore.QSize(0, 300))
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setBold(True)
        font.setWeight(75)
        MainWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/newPrefix/TinyPID.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_spinner = QtWidgets.QLabel(self.centralwidget)
        self.label_spinner.setText("")
        self.label_spinner.setAlignment(QtCore.Qt.AlignCenter)
        self.label_spinner.setObjectName("label_spinner")
        self.verticalLayout.addWidget(self.label_spinner)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1089, 21))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menuTheme = QtWidgets.QMenu(self.menu)
        self.menuTheme.setObjectName("menuTheme")
        self.menuLanguage = QtWidgets.QMenu(self.menu)
        self.menuLanguage.setObjectName("menuLanguage")
        self.menuExport = QtWidgets.QMenu(self.menu)
        self.menuExport.setObjectName("menuExport")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setBold(True)
        font.setWeight(75)
        self.toolBar.setFont(font)
        self.toolBar.setIconSize(QtCore.QSize(32, 32))
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.dockWidget = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget.setMinimumSize(QtCore.QSize(284, 311))
        self.dockWidget.setObjectName("dockWidget")
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.dockWidgetContents)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.splitterSymbol = QtWidgets.QSplitter(self.dockWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.splitterSymbol.sizePolicy().hasHeightForWidth())
        self.splitterSymbol.setSizePolicy(sizePolicy)
        self.splitterSymbol.setBaseSize(QtCore.QSize(0, 1000))
        self.splitterSymbol.setOrientation(QtCore.Qt.Vertical)
        self.splitterSymbol.setObjectName("splitterSymbol")
        self.widget = QtWidgets.QWidget(self.splitterSymbol)
        self.widget.setObjectName("widget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tabWidget = QtWidgets.QTabWidget(self.widget)
        self.tabWidget.setObjectName("tabWidget")
        self.Symbol = QtWidgets.QWidget()
        self.Symbol.setObjectName("Symbol")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.Symbol)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.gridLayout_16 = QtWidgets.QGridLayout()
        self.gridLayout_16.setObjectName("gridLayout_16")
        self.lineEditFilter = QtWidgets.QLineEdit(self.Symbol)
        self.lineEditFilter.setObjectName("lineEditFilter")
        self.gridLayout_16.addWidget(self.lineEditFilter, 0, 0, 1, 1)
        self.pushButtonCreateSymbol = QtWidgets.QPushButton(self.Symbol)
        self.pushButtonCreateSymbol.setMaximumSize(QtCore.QSize(32, 16777215))
        self.pushButtonCreateSymbol.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pushButtonCreateSymbol.setObjectName("pushButtonCreateSymbol")
        self.gridLayout_16.addWidget(self.pushButtonCreateSymbol, 0, 1, 1, 1)
        self.pushButtonDetectSymbol = QtWidgets.QPushButton(self.Symbol)
        self.pushButtonDetectSymbol.setMaximumSize(QtCore.QSize(130, 16777215))
        self.pushButtonDetectSymbol.setObjectName("pushButtonDetectSymbol")
        self.gridLayout_16.addWidget(self.pushButtonDetectSymbol, 0, 2, 1, 1)
        self.verticalLayoutSymbolTree = QtWidgets.QVBoxLayout()
        self.verticalLayoutSymbolTree.setObjectName("verticalLayoutSymbolTree")
        self.gridLayout_16.addLayout(self.verticalLayoutSymbolTree, 1, 0, 1, 3)
        self.gridLayout_9.addLayout(self.gridLayout_16, 0, 0, 1, 1)
        self.tabWidget.addTab(self.Symbol, "")
        self.gridLayout_3.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.widgetSymbolProperty = QtWidgets.QWidget(self.splitterSymbol)
        self.widgetSymbolProperty.setMaximumSize(QtCore.QSize(16777215, 500))
        self.widgetSymbolProperty.setObjectName("widgetSymbolProperty")
        self.gridLayout_10 = QtWidgets.QGridLayout(self.widgetSymbolProperty)
        self.gridLayout_10.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.tabWidgetSymbolProperty = QtWidgets.QTabWidget(self.widgetSymbolProperty)
        self.tabWidgetSymbolProperty.setMaximumSize(QtCore.QSize(16777215, 500))
        self.tabWidgetSymbolProperty.setBaseSize(QtCore.QSize(0, 300))
        self.tabWidgetSymbolProperty.setObjectName("tabWidgetSymbolProperty")
        self.tabLibrary = QtWidgets.QWidget()
        self.tabLibrary.setObjectName("tabLibrary")
        self.gridLayout_13 = QtWidgets.QGridLayout(self.tabLibrary)
        self.gridLayout_13.setObjectName("gridLayout_13")
        self.scrollArea = QtWidgets.QScrollArea(self.tabLibrary)
        self.scrollArea.setMaximumSize(QtCore.QSize(16777215, 500))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 284, 195))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_14 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_14.setObjectName("gridLayout_14")
        self.verticalLayoutLibrary = QtWidgets.QVBoxLayout()
        self.verticalLayoutLibrary.setObjectName("verticalLayoutLibrary")
        self.gridLayout_14.addLayout(self.verticalLayoutLibrary, 0, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_13.addWidget(self.scrollArea, 0, 0, 1, 1)
        self.tabWidgetSymbolProperty.addTab(self.tabLibrary, "")
        self.tabSymbolProperty = QtWidgets.QWidget()
        self.tabSymbolProperty.setObjectName("tabSymbolProperty")
        self.gridLayout_15 = QtWidgets.QGridLayout(self.tabSymbolProperty)
        self.gridLayout_15.setObjectName("gridLayout_15")
        self.verticalLayoutSymbolProperty = QtWidgets.QVBoxLayout()
        self.verticalLayoutSymbolProperty.setObjectName("verticalLayoutSymbolProperty")
        self.gridLayout_15.addLayout(self.verticalLayoutSymbolProperty, 0, 0, 1, 1)
        self.tabWidgetSymbolProperty.addTab(self.tabSymbolProperty, "")
        self.gridLayout_10.addWidget(self.tabWidgetSymbolProperty, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.splitterSymbol, 0, 0, 1, 1)
        self.dockWidget.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockWidget)
        self.dockWidgetObjectExplorer = QtWidgets.QDockWidget(MainWindow)
        self.dockWidgetObjectExplorer.setMinimumSize(QtCore.QSize(300, 219))
        self.dockWidgetObjectExplorer.setObjectName("dockWidgetObjectExplorer")
        self.dockWidgetContents_2 = QtWidgets.QWidget()
        self.dockWidgetContents_2.setObjectName("dockWidgetContents_2")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.dockWidgetContents_2)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.tabWidgetItemExplorer = QtWidgets.QTabWidget(self.dockWidgetContents_2)
        self.tabWidgetItemExplorer.setObjectName("tabWidgetItemExplorer")
        self.tabItemProperty = QtWidgets.QWidget()
        self.tabItemProperty.setObjectName("tabItemProperty")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.tabItemProperty)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.gridLayout_11 = QtWidgets.QGridLayout()
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.pushButtonRefreshTree = QtWidgets.QPushButton(self.tabItemProperty)
        self.pushButtonRefreshTree.setObjectName("pushButtonRefreshTree")
        self.gridLayout_11.addWidget(self.pushButtonRefreshTree, 0, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_11.addItem(spacerItem, 0, 0, 1, 1)
        self.symbolExplorerVerticalLayout = QtWidgets.QVBoxLayout()
        self.symbolExplorerVerticalLayout.setObjectName("symbolExplorerVerticalLayout")
        self.gridLayout_11.addLayout(self.symbolExplorerVerticalLayout, 1, 0, 1, 2)
        self.gridLayout_6.addLayout(self.gridLayout_11, 0, 0, 1, 1)
        self.tabWidgetItemExplorer.addTab(self.tabItemProperty, "")
        self.tabDrawingList = QtWidgets.QWidget()
        self.tabDrawingList.setObjectName("tabDrawingList")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.tabDrawingList)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.verticalLayoutDrawingList = QtWidgets.QVBoxLayout()
        self.verticalLayoutDrawingList.setObjectName("verticalLayoutDrawingList")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.pushButtonRefreshDrawings = QtWidgets.QPushButton(self.tabDrawingList)
        self.pushButtonRefreshDrawings.setObjectName("pushButtonRefreshDrawings")
        self.horizontalLayout_4.addWidget(self.pushButtonRefreshDrawings)
        self.verticalLayoutDrawingList.addLayout(self.horizontalLayout_4)
        self.treeWidgetDrawingList = QtWidgets.QTreeWidget(self.tabDrawingList)
        self.treeWidgetDrawingList.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.treeWidgetDrawingList.setColumnCount(2)
        self.treeWidgetDrawingList.setObjectName("treeWidgetDrawingList")
        self.treeWidgetDrawingList.headerItem().setText(0, "1")
        self.treeWidgetDrawingList.headerItem().setText(1, "2")
        self.treeWidgetDrawingList.header().setVisible(False)
        self.verticalLayoutDrawingList.addWidget(self.treeWidgetDrawingList)
        self.gridLayout_7.addLayout(self.verticalLayoutDrawingList, 0, 0, 1, 1)
        self.tabWidgetItemExplorer.addTab(self.tabDrawingList, "")
        self.gridLayout_4.addWidget(self.tabWidgetItemExplorer, 0, 0, 1, 1)
        self.dockWidgetObjectExplorer.setWidget(self.dockWidgetContents_2)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidgetObjectExplorer)
        self.EditToolbar = QtWidgets.QToolBar(MainWindow)
        self.EditToolbar.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.EditToolbar.sizePolicy().hasHeightForWidth())
        self.EditToolbar.setSizePolicy(sizePolicy)
        self.EditToolbar.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.EditToolbar.setIconSize(QtCore.QSize(32, 32))
        self.EditToolbar.setObjectName("EditToolbar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.EditToolbar)
        self.dockWidgetOutputWnd = QtWidgets.QDockWidget(MainWindow)
        self.dockWidgetOutputWnd.setMinimumSize(QtCore.QSize(145, 202))
        self.dockWidgetOutputWnd.setBaseSize(QtCore.QSize(0, 202))
        self.dockWidgetOutputWnd.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable|QtWidgets.QDockWidget.DockWidgetMovable)
        self.dockWidgetOutputWnd.setAllowedAreas(QtCore.Qt.AllDockWidgetAreas)
        self.dockWidgetOutputWnd.setObjectName("dockWidgetOutputWnd")
        self.dockWidgetContents_3 = QtWidgets.QWidget()
        self.dockWidgetContents_3.setObjectName("dockWidgetContents_3")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.dockWidgetContents_3)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.tabWidget_2 = QtWidgets.QTabWidget(self.dockWidgetContents_3)
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.tabTerminal = QtWidgets.QWidget()
        self.tabTerminal.setObjectName("tabTerminal")
        self.gridLayout_12 = QtWidgets.QGridLayout(self.tabTerminal)
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem2)
        self.pushButtonClearLog = QtWidgets.QPushButton(self.tabTerminal)
        self.pushButtonClearLog.setEnabled(True)
        self.pushButtonClearLog.setMaximumSize(QtCore.QSize(32, 16777215))
        self.pushButtonClearLog.setObjectName("pushButtonClearLog")
        self.horizontalLayout_5.addWidget(self.pushButtonClearLog, 0, QtCore.Qt.AlignRight)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.listWidgetLog = QtWidgets.QListWidget(self.tabTerminal)
        self.listWidgetLog.setObjectName("listWidgetLog")
        self.verticalLayout_3.addWidget(self.listWidgetLog)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)
        self.gridLayout_12.addLayout(self.verticalLayout_3, 0, 0, 1, 1)
        self.tabWidget_2.addTab(self.tabTerminal, "")
        self.tabInconsistency = QtWidgets.QWidget()
        self.tabInconsistency.setObjectName("tabInconsistency")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.tabInconsistency)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tableWidgetInconsistency = QtWidgets.QTableWidget(self.tabInconsistency)
        self.tableWidgetInconsistency.setObjectName("tableWidgetInconsistency")
        self.tableWidgetInconsistency.setColumnCount(0)
        self.tableWidgetInconsistency.setRowCount(0)
        self.tableWidgetInconsistency.horizontalHeader().setSortIndicatorShown(True)
        self.tableWidgetInconsistency.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout_2.addWidget(self.tableWidgetInconsistency)
        self.gridLayout_8.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.tabWidget_2.addTab(self.tabInconsistency, "")
        self.gridLayout_5.addWidget(self.tabWidget_2, 0, 0, 1, 1)
        self.dockWidgetOutputWnd.setWidget(self.dockWidgetContents_3)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.dockWidgetOutputWnd)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/newPrefix/File.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpen.setIcon(icon1)
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        self.actionOpen.setFont(font)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/newPrefix/Save.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave.setIcon(icon2)
        self.actionSave.setObjectName("actionSave")
        self.actionUndo = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/newPrefix/undo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionUndo.setIcon(icon3)
        self.actionUndo.setObjectName("actionUndo")
        self.actionRedo = QtWidgets.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/newPrefix/redo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRedo.setIcon(icon4)
        self.actionRedo.setObjectName("actionRedo")
        self.actionNew = QtWidgets.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/newPrefix/New.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNew.setIcon(icon5)
        self.actionNew.setObjectName("actionNew")
        self.menu.addAction(self.actionOpen)
        self.menu.addAction(self.menuExport.menuAction())
        self.menu.addSeparator()
        self.menu.addAction(self.menuTheme.menuAction())
        self.menu.addAction(self.menuLanguage.menuAction())
        self.menu.addSeparator()
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.toolBar.addAction(self.actionNew)
        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addAction(self.actionSave)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionUndo)
        self.toolBar.addAction(self.actionRedo)
        self.toolBar.addSeparator()
        self.toolBar.addSeparator()
        self.EditToolbar.addSeparator()

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidgetSymbolProperty.setCurrentIndex(0)
        self.tabWidgetItemExplorer.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menu.setTitle(_translate("MainWindow", "File"))
        self.menuTheme.setTitle(_translate("MainWindow", "Theme"))
        self.menuLanguage.setTitle(_translate("MainWindow", "Language"))
        self.menuExport.setTitle(_translate("MainWindow", "Export"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "Main Toolbar"))
        self.dockWidget.setWindowTitle(_translate("MainWindow", "Symbol Explorer"))
        self.lineEditFilter.setPlaceholderText(_translate("MainWindow", "Search..."))
        self.pushButtonCreateSymbol.setText(_translate("MainWindow", "Create"))
        self.pushButtonDetectSymbol.setText(_translate("MainWindow", "Symbol Manager"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Symbol), _translate("MainWindow", "Symbol"))
        self.tabWidgetSymbolProperty.setTabText(self.tabWidgetSymbolProperty.indexOf(self.tabLibrary), _translate("MainWindow", "Library"))
        self.tabWidgetSymbolProperty.setTabText(self.tabWidgetSymbolProperty.indexOf(self.tabSymbolProperty), _translate("MainWindow", "Property"))
        self.dockWidgetObjectExplorer.setWindowTitle(_translate("MainWindow", "Object Explorer"))
        self.pushButtonRefreshTree.setText(_translate("MainWindow", "Refresh Item List"))
        self.tabWidgetItemExplorer.setTabText(self.tabWidgetItemExplorer.indexOf(self.tabItemProperty), _translate("MainWindow", "Object Explorer"))
        self.pushButtonRefreshDrawings.setText(_translate("MainWindow", "Refresh Drawing List"))
        self.treeWidgetDrawingList.setSortingEnabled(True)
        self.tabWidgetItemExplorer.setTabText(self.tabWidgetItemExplorer.indexOf(self.tabDrawingList), _translate("MainWindow", "Drawing List"))
        self.EditToolbar.setWindowTitle(_translate("MainWindow", "Edit Toolbar"))
        self.dockWidgetOutputWnd.setWindowTitle(_translate("MainWindow", "Output Window"))
        self.pushButtonClearLog.setToolTip(_translate("MainWindow", "Clear"))
        self.pushButtonClearLog.setText(_translate("MainWindow", "X"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tabTerminal), _translate("MainWindow", "Output"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tabInconsistency), _translate("MainWindow", "Inconsistency"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionOpen.setToolTip(_translate("MainWindow", "Open(Ctrl + O)"))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setToolTip(_translate("MainWindow", "Save(Ctrl + S)"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionUndo.setText(_translate("MainWindow", "Undo"))
        self.actionUndo.setToolTip(_translate("MainWindow", "Undo"))
        self.actionRedo.setText(_translate("MainWindow", "Redo"))
        self.actionRedo.setToolTip(_translate("MainWindow", "Redo"))
        self.actionNew.setText(_translate("MainWindow", "New"))
import Resource_rc
