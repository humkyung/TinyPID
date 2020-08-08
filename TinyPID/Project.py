# coding: utf-8
""" This is project module """

import os
from shutil import copyfile
from AppDatabase import AppDatabase


class Project:
    DATABASE = 'TinyPID.db'

    def __init__(self, project):
        self.id = project['Id']
        self._name = project['Name']
        self._desc = project['Desc']
        self._prj_unit = project['Unit']
        self._path = project['Path']
        self.createDate = project['CreatedDate']
        self.updateDate = project['UpdatedDate']
        self._database = None

    def setId(self, id):
        self.id = id

    def getId(self):
        return self.id

    def setName(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    @property
    def desc(self):
        return self._desc

    @desc.setter
    def desc(self, value):
        """ setter of desc """
        self._desc = value

    @property
    def prj_unit(self):
        return self._prj_unit

    @prj_unit.setter
    def prj_unit(self, value):
        """ setter of prj_unit """
        self._prj_unit = value

    @property
    def database(self):
        """ return database instance """
        return self._database

    @database.setter
    def database(self, value):
        self._database = value

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        self._path = value

    '''
        @brief  return drawing file path
        @author humkyung
        @date   2018.07.09
    '''

    def getDrawingFilePath(self):
        return os.path.join(self.getPath(), 'drawings')

    '''
        @brief  return output path
        @author humkyung
        @date   2018.04.10
    '''

    def getOutputPath(self):
        return os.path.join(self.getPath(), 'output')

    '''
        @brief  return image file path
        @author Jeongwoo
        @date   2018.04.10
    '''

    def getImageFilePath(self):
        return os.path.join(self.getPath(), 'image')

    def get_database_file_path(self):
        """return database file path"""
        return os.path.join(self.path, 'db')

    '''
        @brief  return svg file path
        @author humkyung
        @date   2018.04.08
    '''

    def getSvgFilePath(self):
        return os.path.join(self.getPath(), 'svg')

    '''
        @brief  return temporary path
        @author humkyung
        @date   2018.04.10
    '''

    def getTempPath(self):
        return os.path.join(self.getPath(), 'Temp')

    '''
        @brief  return training path
        @author euisung
        @date   2018.09.28
    '''

    def getTrainingFilePath(self):
        return os.path.join(self.getPath(), 'Training')

    def getTrainingSymbolFilePath(self):
        """ return symbol training path """
        return os.path.join(self.getPath(), 'Training_Symbol')

    def get_data_sheet_path(self):
        """ return data sheet path """

        return os.path.join(self.getPath(), 'Datasheets')

    def setCreateDate(self, createDate):
        self.createDate = createDate

    def getCreateDate(self):
        return self.createDate

    def setUpdateDate(self, updateDate):
        self.updateDate = updateDate

    def getUpdateDate(self):
        return self.updateDate

    '''
        @brief  return project unit
        @author humkyung
        @date   2018.04.25
    '''

    def unit(self):
        from AppDocData import AppDocData
        res = 'Metric'  # default value

        docData = AppDocData.instance()
        configs = docData.getConfigs('Line No', 'Size Unit')
        if 1 == len(configs): res = configs[0].value

        return res

    def make_sub_directories(self):
        """ make directories for project """

        dbDir = self.getDbFilePath()
        if not os.path.exists(dbDir):
            os.makedirs(dbDir)
        imgDir = self.getImageFilePath()
        if not os.path.exists(imgDir):
            os.makedirs(imgDir)
        svgDir = self.getSvgFilePath()
        if not os.path.exists(svgDir):
            os.makedirs(svgDir)
        outputDir = self.getOutputPath()
        if not os.path.exists(outputDir):
            os.makedirs(outputDir)
        tempDir = self.getTempPath()
        if not os.path.exists(tempDir):
            os.makedirs(tempDir)
        drawingPath = self.getDrawingFilePath()
        if not os.path.exists(drawingPath):
            os.makedirs(drawingPath)
        trainingPath = self.getTrainingFilePath()
        if not os.path.exists(trainingPath):
            os.makedirs(trainingPath)
        trainingSymbolPath = self.getTrainingSymbolFilePath()
        if not os.path.exists(trainingSymbolPath):
            os.makedirs(trainingSymbolPath)

        path = os.path.join(tempDir, 'Tile')
        if not os.path.exists(path):
            os.makedirs(path)
        path = os.path.join(drawingPath, 'Native')
        if not os.path.exists(path):
            os.makedirs(path)

        # create folder and copy data sheet files
        path = self.get_data_sheet_path()
        if not os.path.exists(path):
            os.makedirs(path)

            source_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Datasheets')
            data_sheet_files = [f for f in os.listdir(source_path) if os.path.isfile(os.path.join(source_path, f))
                                and (os.path.splitext(f)[1].upper() == '.XLSX')]
            for data_sheet in data_sheet_files:
                copyfile(os.path.join(source_path, data_sheet), os.path.join(path, data_sheet))
